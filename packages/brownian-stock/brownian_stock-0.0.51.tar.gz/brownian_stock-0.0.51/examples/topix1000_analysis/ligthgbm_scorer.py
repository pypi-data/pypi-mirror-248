import datetime
import os
import pathlib
import warnings

import brownian_stock
import lightgbm as lgb
import numpy as np
import optuna.integration.lightgbm as lgbo
import pandas as pd
from brownian_stock import ReturnMap, StockSet, const, evaluation, stock
from brownian_stock.services import universe
from scipy.stats import spearmanr
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from utils import compute_market_index

warnings.simplefilter(action="ignore")


class LightGBMScorer:
    def __init__(self, subset: StockSet, dir_path):
        # self.market_index = compute_market_index(subset)
        # self.market_index_rate = compute_market_index(subset, change=True)
        self.market_index = brownian_stock.average_index(subset)

        # 市場全体の影響を控除したサブセットを構成
        self.stock_set = subset
        # self.stock_set = subset.neutralize(self.market_index)
        self.pct_set = subset.pct_change()
        # self.pct_set = subset.pct_change().neutralize(self.market_index_rate)
        self.dir_path = dir_path

        self.evaluator = evaluation.PercentageChangeStockEval()
        self.eval_volatility = evaluation.VolatilityStockEval(const.COL_CLOSE)

        # セクター毎のモデルと変換器
        self.sector_model = {}
        self.sector_label_encoder = {}
        self.init_cluster_dict = False

        # キャッシュ
        self.x_cache = {}
        self.y_cache = {}

    def daily_scoring(self, trade_date):
        # すべての銘柄に対して予測を実施
        rmap = ReturnMap()
        for s in self.stock_set:
            try:
                # encoder = self.sector_label_encoder[cluster_idx]
                record = self.subset_to_feature(s.stock_code, trade_date)
                df = pd.DataFrame([record])
                # df["STOCK_CODE"] = encoder.transform(df["STOCK_CODE"])
                pred = self.model.predict(df)
                score = pred[0]
            except Exception as e:
                score = None
            rmap[s.stock_code] = score
        return rmap

    def optimize(self, start, end, test_date_num=100):
        """ """
        print("[*] Building datasets")
        train_end = end - datetime.timedelta(test_date_num + 1)
        test_start = end - datetime.timedelta(test_date_num)

        train_x, train_y = self.to_dataset(self.stock_set, start, train_end)
        test_x, test_y = self.to_dataset(self.stock_set, test_start, end)

        print("[*] Training model")
        lgb_train = lgbo.Dataset(train_x, train_y)
        lgb_eval = lgbo.Dataset(test_x, test_y)

        params = {
            "objective": "mean_squared_error",
            "metric": "mae",
            "verbosity": 1,
            "boosting_type": "gbdt",
        }

        # 最適化を実行
        model = lgbo.train(
            params,
            lgb_train,
            num_boost_round=1000,
            valid_names=["train", "valid"],
            valid_sets=[lgb_train, lgb_eval],
            early_stopping_rounds=20,
            categorical_feature=["CLUSTER"],
        )
        best_params = model.params
        print(best_params)

        # 学習結果を表示
        train_pred = model.predict(train_x)
        test_pred = model.predict(test_x)
        train_mse = mean_squared_error(train_y, train_pred)
        test_mse = mean_squared_error(test_y, test_pred)
        print(f"MSE - Train: {train_mse}, Test: {test_mse}")
        train_coef, _ = spearmanr(train_pred, train_y)
        test_coef, _ = spearmanr(test_pred, test_y)
        print(f"Spearman Coef - Train: {train_coef}, Test: {test_coef}")
        self.model = model

    def train(self, start, end, test_date_num=50, verbose=1):
        print("[*] Building datasets")
        train_end = end - datetime.timedelta(test_date_num + 1)
        test_start = end - datetime.timedelta(test_date_num)

        train_x, train_y = self.to_dataset(self.stock_set, start, train_end)
        test_x, test_y = self.to_dataset(self.stock_set, test_start, end)
        train_x.to_csv("train.csv")

        # encoder = LabelEncoder()
        # train_x["STOCK_CODE"] = encoder.fit_transform(train_x["STOCK_CODE"])
        # test_x["STOCK_CODE"] = encoder.transform(test_x["STOCK_CODE"])

        print("[*] Training model")
        model = lgb.LGBMRegressor(
            reg_alpha=1e-8,
            reg_lambda=0.84,
            num_leaves=29,
            colsample_bytree=0.7,
            subsample=1,
            subsample_freq=0,
            min_child_samples=5,
            objective="mean_squared_error",
        )
        model.fit(
            train_x,
            train_y,
            eval_set=[(train_x, train_y), (test_x, test_y)],
            eval_metric="l1",
            callbacks=[lgb.early_stopping(stopping_rounds=20, verbose=False), lgb.log_evaluation(verbose)],
            categorical_feature=["CLUSTER"],
        )

        # 学習結果を表示
        train_pred = model.predict(train_x)
        test_pred = model.predict(test_x)
        train_mse = mean_squared_error(train_y, train_pred)
        test_mse = mean_squared_error(test_y, test_pred)
        print(f"MSE - Train: {train_mse}, Test: {test_mse}")
        train_coef, _ = spearmanr(train_pred, train_y)
        test_coef, _ = spearmanr(test_pred, test_y)
        print(f"Spearman Coef - Train: {train_coef}, Test: {test_coef}")
        self.model = model

        # feature importanceの測定
        r = permutation_importance(model, test_x, test_y, n_repeats=30, random_state=0)
        for i in r.importances_mean.argsort()[::-1]:
            if r.importances_mean[i] - 2 * r.importances_std[i] > 0:
                print(f"{test_x.columns[i]:<12} " f"{r.importances_mean[i]:.5f}" f" +/- {r.importances_std[i]:.5f}")

    def to_dataset(self, subset, start_date, end_date):
        dates = stock.market_open_dates(self.dir_path, start_date, end_date)
        x_pd_list = []
        y_list = []
        for d in dates:
            x_tmp = []
            y_tmp = []
            # 生の収益率を使うのではなくランク化する
            for s in subset:
                try:
                    code = s.stock_code
                    x = self.subset_to_feature(code, d)
                    y = self.subset_to_target(code, d)
                    x_tmp.append(x)
                    y_tmp.append(y)
                except Exception as e:
                    continue
            x_df = pd.DataFrame(x_tmp)
            x_pd_list.append(x_df)
            order = np.argsort(np.argsort(np.array(y_tmp))) / len(y_tmp)
            y_list.extend(order.tolist())

        x_df = pd.concat(x_pd_list)
        y_array = np.array(y_list)
        return x_df, y_array

    def subset_to_feature(self, code, trade_date):
        key = (code, trade_date)
        if key in self.x_cache:
            return self.x_cache[key]

        stock_series = self.stock_set.get_stock(code)
        market_series = self.market_index_rate.subset_by_recent_n_days(trade_date, 40)
        market_values = market_series.to_array() + 1
        # market_values = market_series.df[const.COL_INDEX_VALUE].values + 1

        # 直近40日の変化率の取得
        pct_series = self.pct_set.get_stock(code)
        pct_series = pct_series.subset_by_recent_n_days(trade_date, 40)
        pct_close = pct_series.df[const.COL_CLOSE].values + 1
        pct_volume = pct_series.df[const.COL_TRADING_VOLUME].values + 1
        stock_volume = stock_series.df[const.COL_TRADING_VOLUME].values

        record = {
            # "CLOSE_PERCENT": close_price / open_price,
            # "HIGH_PERCENT": high_price / open_price,
            # "LOW_PERCENT": low_price / open_price,
            "MARKET_05": market_values[-5:].prod() * 100,
            "MARKET_10": market_values[-10:].prod() * 100,
            "MARKET_20": market_values[-20:].prod() * 100,
            "PERCENT_3": pct_close[-3:].prod() * 100,
            "PERCENT_5": pct_close[-5:].prod() * 100,
            "PERCENT_10": pct_close[-10:].prod() * 100,
            "PERCENT_20": pct_close[-20:].prod() * 100,
            "PERCENT_40": pct_close[-40:].prod() * 100,
            "CLUSTER": self.code_to_cluster(code),
            "VOLA_5": pct_close[-5:].std(),
            "VOLA_10": pct_close[-10:].std(),
            "VOLA_20": pct_close[-20:].std(),
            "VOLA_40": pct_close[-40:].std(),
            "VOLUME": stock_volume[-10:].sum(),
            "VOLUME_LAG5": pct_volume[-5:].prod(),
            "VOLUME_STD5": pct_volume[-5:].std(),
            "VOLUME_LAG10": pct_volume[-10:].prod(),
            "VOLUME_STD10": pct_volume[-10:].std(),
            "VOLUME_LAG20": pct_volume[-20:].prod(),
            "VOLUME_STD20": pct_volume[-20:].std(),
            # "STOCK_CODE": stock_series.stock_code,
        }
        self.x_cache[key] = record
        return record

    def subset_to_target(self, code, trade_date):
        key = (code, trade_date)
        if key in self.y_cache:
            return self.y_cache[key]
        pct_series = self.pct_set.get_stock(code)
        pct_series = pct_series.subset_by_after_n_days(trade_date, 5)
        score = (pct_series.df[const.COL_CLOSE] + 1).product() * 100
        self.y_cache[key] = score
        return score

    def code_to_cluster(self, code):
        if not self.init_cluster_dict:
            self.cluster_dict_idx = {}
            cluster_csv = pathlib.Path(__file__).parent / "clustering_result.csv"
            cluster_df = pd.read_csv(cluster_csv)

            for _, row in cluster_df.iterrows():
                code = str(row["Code"])
                cluster = row["Cluster"]
                self.cluster_dict_idx[code] = cluster

        self.init_cluster_dict = True
        v = self.cluster_dict_idx.get(code, None)
        if v is not None:
            return v
        return -1
        # raise ValueError(f"Cant detect cluster of {code}")


if __name__ == "__main__":
    dir_path = "~/Document/jquants/stock"
    dir_path = os.path.expanduser(dir_path)
    stock_set = StockSet.init_by_path(dir_path=dir_path)

    univ = universe.Topix1000()
    stock_set = stock_set.filter(univ)

    scorer = LightGBMScorer(stock_set, dir_path)
    # scorer.optimize(datetime.date(2017, 1, 1), datetime.date(2019, 12, 31), test_date_num=200)
    scorer.train(datetime.date(2017, 1, 1), datetime.date(2019, 12, 31), test_date_num=200)
