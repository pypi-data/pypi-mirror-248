import argparse
import datetime
import json
import os
import pathlib
import warnings
from functools import partial

import brownian_stock
import lightgbm as lgb
import numpy as np
import optuna
import optuna.integration.lightgbm as lgbo
import pandas as pd
import xfeat
from brownian_stock import ReturnMap, StockSet, const, evaluation, stock
from brownian_stock.services import universe
from choose_feature import SimpleFeatureSample, lgb_permutation_importance
from scipy.stats import spearmanr
from sklearn.metrics import mean_squared_error

warnings.simplefilter(action="ignore")

CATEGORICAL_FEATURES = ["CLUSTER"]


class LightGBMScorer:
    def __init__(self, subset: StockSet, dir_path):
        # セクター毎のモデルと変換器
        self.sector_model = {}
        self.sector_label_encoder = {}
        self.init_cluster_dict = False
        self.dir_path = dir_path

        # キャッシュ
        self.x_cache = {}
        self.y_cache = {}

        # 不要な銘柄をフィルター
        subset = subset.filter(lambda s: self.code_to_cluster(s.stock_code) != -1)
        # self.market_index_rate = compute_market_index(subset, change=True)
        self.market_index = brownian_stock.average_index(subset)

        # 市場全体の影響を控除したサブセットを構成
        self.stock_set = subset
        # self.stock_set = subset.neutralize(self.market_index)
        self.pct_set = subset.pct_change()
        # self.pct_set = subset.pct_change().neutralize(self.market_index_rate)

        self.evaluator = evaluation.PercentageChangeStockEval()
        self.eval_volatility = evaluation.VolatilityStockEval(const.COL_CLOSE)

        current_path = pathlib.Path(__file__).parent
        self.train_columns = None
        self.train_parameters = None

        # with open(current_path / "column.json") as fp:
        #    self.train_columns = json.load(fp)

        with open(current_path / "parameter.json") as fp:
            self.train_parameters = json.load(fp)

    def daily_scoring(self, trade_date):
        # すべての銘柄に対して予測を実施
        rmap = ReturnMap()
        records = []
        codes = []
        for s in self.stock_set:
            try:
                record = self.subset_to_feature(s.stock_code, trade_date)
                records.append(record)
                codes.append(s.stock_code)
                # df = pd.DataFrame([record])
                # df = self.feature_engineering(df)[self.train_columns]
                # pred = self.model.predict(df)
                # score = pred[0]
            except Exception as e:
                score = None
            # rmap[s.stock_code] = score

        # 予測してReturnMapを生成
        df = pd.DataFrame(records)
        # df = self.feature_engineering(df)[self.train_columns]
        cols = [c for c in list(df.columns) if not c.startswith("__")]
        df = df[cols]
        pred = self.model.predict(df).tolist()
        for c, v in zip(codes, pred):
            rmap[c] = v
        return rmap

    def optimize(self, start, end, test_date_num=100):
        """ """
        print("[*] Building datasets")

        train_end = end - datetime.timedelta(test_date_num + 1)
        test_start = end - datetime.timedelta(test_date_num)

        train_d, train_x, train_y = self.to_dataset(self.stock_set, start, train_end)
        test_d, test_x, test_y = self.to_dataset(self.stock_set, test_start, end)
        train_x = self.feature_engineering(train_x)
        test_x = self.feature_engineering(test_x)
        train_dataset = (train_d, train_x, train_y)
        test_dataset = (test_d, test_x, test_y)

        print("[*] Training model")
        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "boosting_type": "gbdt",
            "first_metric_only": True,
            "label_gain": [i for i in range(1000)],
        }
        columns = train_dataset[1].columns.tolist()

        columns = self.optimize_features(train_dataset, test_dataset, params, columns)
        params = self.optimize_paramater(train_dataset, test_dataset, columns)

        dir_path = pathlib.Path(__file__).parent
        with open(dir_path / "column.json", "w") as fp:
            json.dump(columns, fp)
        with open(dir_path / "parameter.json", "w") as fp:
            json.dump(params, fp)
        print(params)
        print(columns)

    def optimize_paramater(self, train_dataset, test_dataset, columns):
        """パラメータの最適化を行う"""
        train_d, train_x, train_y = train_dataset
        test_d, test_x, test_y = test_dataset

        # クエリを抽出
        columns = [c for c in columns if not c.startswith("__")]
        train_query = to_query(train_x["__QUERY"])
        train_x = train_x[columns]
        test_query = to_query(test_x["__QUERY"])
        test_x = test_x[columns]

        lgb_train = lgbo.Dataset(train_x, train_y, group=train_query)
        lgb_eval = lgbo.Dataset(test_x, test_y, group=test_query)

        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "boosting_type": "gbdt",
            "first_metric_only": True,
            "label_gain": [i for i in range(1000)],
        }

        categorical_feature = [c for c in columns if c in CATEGORICAL_FEATURES]

        # 最適化を実行
        model = lgbo.train(
            params,
            lgb_train,
            num_boost_round=1000,
            valid_names=["train", "valid"],
            valid_sets=[lgb_train, lgb_eval],
            early_stopping_rounds=20,
            verbose_eval=False,
            categorical_feature=categorical_feature,
        )
        best_params = model.params
        print(best_params)

        # 学習結果を表示
        train_pred = model.predict(train_x)
        test_pred = model.predict(test_x)
        train_mse = mean_squared_error(train_y, train_pred)
        test_mse = mean_squared_error(test_y, test_pred)
        print(f"MSE - Train: {train_mse}, Test: {test_mse}")
        train_coef, train_std = self.spearman_coef(model, train_d, train_x, train_y)
        test_coef, test_std = self.spearman_coef(model, test_d, test_x, test_y)
        print(f"Spearman Coef - Train: {train_coef:.5f} ± {train_std:.5f}, Test: {test_coef:.5f} ± {test_std:.5f}")
        return best_params

    def optimize_features(self, train_dataset, test_dataset, params, input_cols=None):
        """特徴量の探索を行う"""
        _, train_x, train_y = train_dataset
        _, test_x, test_y = test_dataset

        # 特徴量の探索
        # __で始まる特徴量は前処理用なので探索の対象にしない
        if input_cols is None:
            input_cols = train_x.columns.tolist()
            input_cols = [c for c in input_cols if not c.startswith("__")]

        # クエリを抽出
        train_query = to_query(train_x["__QUERY"])
        test_query = to_query(test_x["__QUERY"])

        ignore = ["num_iterations", "early_stopping_round", "categorical_column"]
        params = {name: value for name, value in params.items() if name not in ignore}

        best_columns = []
        best_score = -1000
        sampler = SimpleFeatureSample(input_cols)
        for i in range(2, 2000):
            print("")
            print(i)
            sampled = sampler.sample(i)
            print(sampled)
            categorical_feature = [c for c in sampled if c in CATEGORICAL_FEATURES]
            lgb_train = lgb.Dataset(train_x[sampled], train_y.astype(int), group=train_query)
            lgb_eval = lgbo.Dataset(test_x[sampled], test_y.astype(int), group=test_query)
            model = lgb.train(
                params,
                lgb_train,
                num_boost_round=1000,
                valid_names=["train", "valid"],
                valid_sets=[lgb_train, lgb_eval],
                early_stopping_rounds=20,
                verbose_eval=False,
                feval=spearman_metric,
                categorical_feature=categorical_feature,
            )
            test_pred = model.predict(test_x[sampled])
            m, _ = spearmanr(test_pred, test_y)
            print(m)
            sampler.update(sampled, m)

            if best_score < m:
                best_columns = sampled
                best_score = m

            if i % 50 == 0:
                sampler.show()
        print(best_columns)
        print(best_score)
        return best_columns

    def train(self, start, end, test_date_num=50, verbose=1, no_feng=False):
        print("[*] Building datasets")
        train_end = end - datetime.timedelta(test_date_num + 1)
        test_start = end - datetime.timedelta(test_date_num)

        train_d, train_x, train_y = self.to_dataset(self.stock_set, start, train_end)
        test_d, test_x, test_y = self.to_dataset(self.stock_set, test_start, end)

        # 特徴量の変換を行う
        if not no_feng:
            train_x = self.feature_engineering(train_x)
            test_x = self.feature_engineering(test_x)
            # remove_cols = [c for c in train_x.columns if c not in self.train_columns]
            # remove_cols = [c for c in remove_cols if not c.startswith("__")]
            # train_x.drop(columns=remove_cols, inplace=True)
            # test_x.drop(columns=remove_cols, inplace=True)

        # データを保存
        train_x["TARGET"] = train_y
        train_x.to_csv("tmp/train.csv", index=False)
        train_x.drop(columns=["TARGET"], inplace=True)

        # クエリを抽出
        train_query = to_query(train_x["__QUERY"])
        train_x.drop(columns=["__QUERY"], inplace=True)
        test_query = to_query(test_x["__QUERY"])
        test_x.drop(columns=["__QUERY"], inplace=True)

        print("[*] Training model")
        lgb_train = lgb.Dataset(train_x, train_y.astype(int), group=train_query)
        lgb_eval = lgbo.Dataset(test_x, test_y.astype(int), group=test_query)

        # 最適化を実行
        params = {
            "objective": "lambdarank",
            "metric": "ndcg",
            "ndcg_at_eval": [10, 50, 100],
            "boosting_type": "gbdt",
            "label_gain": [i * 2 for i in range(1000)],
        }

        categorical_feature = [c for c in train_x.columns if c in CATEGORICAL_FEATURES]
        model = lgb.train(
            params,
            lgb_train,
            num_boost_round=1000,
            valid_names=["train", "valid"],
            valid_sets=[lgb_train, lgb_eval],
            early_stopping_rounds=20,
            verbose_eval=False,
            # feval=spearman_metric,
            categorical_feature=categorical_feature,
        )
        best_params = model.params
        print(best_params)

        # 学習結果を表示
        train_pred = model.predict(train_x)
        test_pred = model.predict(test_x)
        train_mse = mean_squared_error(train_y, train_pred)
        test_mse = mean_squared_error(test_y, test_pred)
        print(f"MSE - Train: {train_mse}, Test: {test_mse}")
        m = spearman_metric(test_pred, lgb_eval)
        print(m)

        train_coef, train_std = self.spearman_coef(model, train_d, train_x, train_y)
        test_coef, test_std = self.spearman_coef(model, test_d, test_x, test_y)
        print(f"Spearman Coef - Train: {train_coef:.5f} ± {train_std:.5f}, Test: {test_coef:.5f} ± {test_std:.5f}")
        self.model = model
        lgb_permutation_importance(model, test_x, test_y)
        # self.optimize_feature()

    def to_dataset(self, subset, start_date, end_date):
        """指定した日付の範囲のデータセットを作成する

        Returns:
            tuple: tuple like (d_series, x_df, y_array)
        """
        dates = stock.market_open_dates(self.dir_path, start_date, end_date)
        x_list = []
        y_list = []
        d_list = []

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
                    d_list.append(d)
                except ValueError as e:
                    continue
            x_df = pd.DataFrame(x_tmp)
            x_list.append(x_df)
            order = np.argsort(np.argsort(np.array(y_tmp)))
            y_list.extend(order.tolist())
        x_df = pd.concat(x_list)
        x_df["__TARGET"] = y_list
        x_df["__DATE"] = d_list

        # __QUERYで並び替えて分割
        x_df.sort_values(by="__QUERY", inplace=True)
        x_df.reset_index(drop=True, inplace=True)
        y_series = x_df["__TARGET"].astype(int)
        d_series = x_df["__DATE"]
        x_df.drop(columns=["__TARGET", "__DATE"], inplace=True)
        return d_series, x_df, y_series

    def subset_to_feature(self, code, trade_date: datetime.date):
        key = (code, trade_date)
        if key in self.x_cache:
            return self.x_cache[key]

        stock_series = self.stock_set.get_stock(code)
        market_series = self.market_index.subset_by_recent_n_days(trade_date, 40)
        market_values = market_series.to_array() + 1
        turnover_values = stock_series.to_array(const.COL_TURNOVER_VALUE)

        # 直近40日の変化率の取得
        pct_series = self.pct_set.get_stock(code)
        pct_series = pct_series.subset_by_recent_n_days(trade_date, 40)
        pct_close = pct_series.to_array(const.COL_CLOSE) + 1
        pct_volume = pct_series.to_array(const.COL_TRADING_VOLUME) + 1
        pct_turnover = pct_series.to_array(const.COL_TURNOVER_VALUE) + 1

        high = stock_series.to_array(const.COL_HIGH)
        low = stock_series.to_array(const.COL_LOW)
        close = stock_series.to_array(const.COL_CLOSE)
        daily_range = (high - low) / close

        search = True
        if search:
            record = {
                "__QUERY": (trade_date - datetime.date(2017, 1, 1)).days,
                "VOLUME": turnover_values[-20:].mean(),
                "CLUSTER": self.code_to_cluster(code),
                "WEEKYDAY": trade_date.weekday(),
                "MARKET_3": market_values[-3:].prod(),
                "MARKET_5": market_values[-5:].prod(),
                "MARKET_10": market_values[-10:].prod(),
                "MARKET_20": market_values[-20:].prod(),
                "MARKET_40": market_values[-40:].prod(),
                "PERCENT_3": pct_close[-3:].prod(),
                "PERCENT_5": pct_close[-5:].prod(),
                "PERCENT_10": pct_close[-10:].prod(),
                "PERCENT_20": pct_close[-20:].prod(),
                "PERCENT_40": pct_close[-40:].prod(),
                "TURNOVER_MEAN_3": pct_turnover[-3:].prod(),
                "TURNOVER_MEAN_5": pct_turnover[-5:].prod(),
                "TURNOVER_MEAN_10": pct_turnover[-10:].prod(),
                "TURNOVER_MEAN_20": pct_turnover[-20:].prod(),
                "TURNOVER_MEAN_40": pct_turnover[-40:].prod(),
                "TURNOVER_STD_3": pct_turnover[-3:].std(),
                "TURNOVER_STD_5": pct_turnover[-5:].std(),
                "TURNOVER_STD_10": pct_turnover[-10:].std(),
                "TURNOVER_STD_20": pct_turnover[-20:].std(),
                "TURNOVER_STD_40": pct_turnover[-40:].std(),
                "VOLUME_LAG_3": pct_volume[-3:].prod(),
                "VOLUME_LAG_5": pct_volume[-5:].prod(),
                "VOLUME_LAG_10": pct_volume[-10:].prod(),
                "VOLUME_LAG_20": pct_volume[-20:].prod(),
                "VOLUME_LAG_40": pct_volume[-40:].prod(),
                "ATR_3": daily_range[-3:].mean(),
                "ATR_5": daily_range[-5:].mean(),
                "ATR_10": daily_range[-10:].mean(),
                "ATR_20": daily_range[-20:].mean(),
                "ATR_40": daily_range[-40:].mean(),
                # "VOLA_3": pct_close[-3:].std(),
                # "VOLA_5": pct_close[-5:].std(),
                # "VOLA_10": pct_close[-10:].std(),
                # "VOLA_20": pct_close[-20:].std(),
                # "VOLA_40": pct_close[-40:].std(),
            }
        else:
            record = {
                "__QUERY": (trade_date - datetime.date(2017, 1, 1)).days,
                "CLUSTER": self.code_to_cluster(code),
                "PERCENT_3": pct_close[-3:].prod() / pct_close[-40:].prod(),
                "PERCENT_5": pct_close[-5:].prod() / pct_close[-40:].prod(),
                "PERCENT_10": pct_close[-10:].prod() / pct_close[-40:].prod(),
                "PERCENT_20": pct_close[-20:].prod() / pct_close[-40:].prod(),
            }

        self.x_cache[key] = record
        return record

    def subset_to_target(self, code, trade_date):
        key = (code, trade_date)
        if key in self.y_cache:
            return self.y_cache[key]
        pct_series = self.pct_set.get_stock(code)
        pct_series = pct_series.subset_by_after_n_days(trade_date, 1)
        mean = np.prod(pct_series.to_array(const.COL_CLOSE) + 1)
        std = np.std(pct_series.to_array(const.COL_CLOSE))
        score = mean
        # score = (mean - 1) / std
        self.y_cache[key] = score
        return score

    def spearman_coef(self, model, d_series, x_df, y_series):
        """スピアマンの相関係数を日毎に計算する"""
        coef_list = []
        for d in d_series.unique():
            index = (d_series == d).values
            tmp_x = x_df[index]
            tmp_p = model.predict(tmp_x)
            tmp_y = y_series[index].values
            coef, _ = spearmanr(tmp_p, tmp_y)
            coef_list.append(coef)
        avg = np.mean(coef_list)
        std = np.std(coef_list)
        return avg, std

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

    def feature_engineering(self, df):
        ignore = ["CLUSTER", "WEEKDAY"]
        cols = df.columns.tolist()
        cols = [c for c in cols if c not in ignore]
        cols = [c for c in cols if not c.startswith("__")]

        encoder = xfeat.Pipeline(
            [
                xfeat.ArithmeticCombinations(
                    input_cols=cols, drop_origin=False, operator="*", r=2, output_suffix="_mul"
                ),
                xfeat.ArithmeticCombinations(
                    input_cols=cols, drop_origin=False, operator="/", r=2, output_suffix="_div"
                ),
                xfeat.ArithmeticCombinations(
                    input_cols=cols, drop_origin=False, operator="+", r=2, output_suffix="_plus"
                ),
            ]
        )
        return encoder.fit_transform(df)


def spearman_metric(y_pred, data):
    y_true = data.get_label()
    groups = data.get_group()

    coef_ls = []
    start = 0
    for g in groups:
        t = y_true[start : start + g]
        p = y_pred[start : start + g]
        coef, _ = spearmanr(t, p)
        coef_ls.append(coef)
        start += g
    coef = np.mean(coef_ls)
    std = np.std(coef_ls)
    return "spearman", coef, False


def to_query(series):
    series = series.values.tolist()
    series.append(None)  # 番兵
    prev_idx = 0
    prev_v = series[0]
    results = []
    for idx, v in enumerate(series):
        if v != prev_v:
            results.append(idx - prev_idx)
            prev_v = v
            prev_idx = idx
    assert sum(results) == len(series) - 1
    return results


def command_train(args):
    """学習処理を実行する"""
    no_feng = args.no_feng
    limit = args.limit
    dir_path = args.dir_path
    dir_path = os.path.expanduser(dir_path)

    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)

    univ = universe.TopixSmall1()
    stock_set = stock_set.filter(univ)

    scorer = LightGBMScorer(stock_set, dir_path)
    scorer.train(datetime.date(2017, 1, 1), datetime.date(2019, 12, 31), test_date_num=200, no_feng=no_feng)


def command_optimize(args):
    """最適化処理を実行する"""
    limit = args.limit
    dir_path = args.dir_path
    dir_path = os.path.expanduser(dir_path)
    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)

    univ = universe.TopixSmall1()
    stock_set = stock_set.filter(univ)

    scorer = LightGBMScorer(stock_set, dir_path)
    scorer.optimize(datetime.date(2017, 1, 1), datetime.date(2019, 12, 31), test_date_num=200)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Lightgbm Scorer")
    subparsers = parser.add_subparsers()

    dir_path = "~/Document/jquants/stock"
    parser_train = subparsers.add_parser("train")
    parser_train.add_argument("--dir_path", type=str, default=dir_path)
    parser_train.add_argument("--no-feng", action="store_true")
    parser_train.add_argument("--limit", type=int, default=None)
    parser_train.set_defaults(handler=command_train)

    dir_path = "~/Document/jquants/stock"
    parser_optimize = subparsers.add_parser("optimize")
    parser_optimize.add_argument("--dir_path", type=str, default=dir_path)
    parser_optimize.add_argument("--limit", type=int, default=None)
    parser_optimize.set_defaults(handler=command_optimize)

    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
