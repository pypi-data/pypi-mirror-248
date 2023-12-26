import argparse
import datetime
import pathlib

import pandas as pd
from brownian_stock import StockSet, const, evaluation, stock, universe
from scipy.stats import spearmanr
from utils import compute_market_index


def cluster_stats(cluster_num: int, subset: StockSet, dir_path: str):
    start_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2018, 12, 31)
    dates = stock.market_open_dates(dir_path, start_date, end_date)

    eval_return = evaluation.PercentageChangeStockSetEval()
    eval_volatlity = evaluation.VolatilityStockSetEval(const.COL_TRADING_VOLUME)

    def compute_coef(lag_x, lag_y, eval_x, eval_y):
        x_list = []
        y_list = []
        for d in dates:
            try:
                prev_subset = subset.subset_by_recent_n_days(d, lag_x)
                after_subset = subset.subset_by_after_n_days(d, lag_y)
                if len(prev_subset) == 0 or len(after_subset) == 0:
                    continue
                x_list.append(eval_x(prev_subset))
                y_list.append(eval_y(after_subset))
            except Exception as e:
                pass
        coef, _ = spearmanr(x_list, y_list)
        return coef

    print(f"== Cluster {cluster_num}==============")
    # 含まれる銘柄の数
    print(f"[Number In Cluster] {len(subset)}")

    # 10日ボラティリティと5日騰落率の関係
    coef = compute_coef(10, 5, eval_volatlity, eval_return)
    print(f"[10 Days Volatility Coef] {coef:.3f}")

    # 40日ボラティリティと5日騰落率の関係
    coef = compute_coef(40, 5, eval_volatlity, eval_return)
    print(f"[40 Days Volatility Coef] {coef:.3f}")

    # 10日騰落率と5日騰落率の関係
    # 相関係数にはスピアマンの順位相関係数を使用
    coef = compute_coef(10, 5, eval_return, eval_return)
    print(f"[10 Days Momentum Coef] {coef:.3f}")

    # 40日騰落率と5日騰落率の関係
    coef = compute_coef(40, 5, eval_return, eval_return)
    print(f"[40 Days Momentum Coef] {coef:.3f}")

    # 80日騰落率と5日騰落率の関係
    coef = compute_coef(80, 5, eval_return, eval_return)
    print(f"[80 Days Momentum Coef] {coef:.3f}")

    # 200日騰落率と5日騰落率の関係
    coef = compute_coef(200, 5, eval_return, eval_return)
    print(f"[200 Days Momentum Coef] {coef:.3f}")


def main(dir_path, limit=None, fig_path=None, csv_path=None):
    """全期間の情報を使って銘柄をクラスタリングする処理
    クラスタリングした結果はデフォルトで同じフォルダに画像とCSVで吐き出す
    """
    # StockSetを読み込んでフィルター
    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)
    start_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2018, 12, 31)
    stock_set = stock_set.subset_by_range(start_date, end_date)
    univ = universe.Topix1000()
    stock_set = stock_set.filter(univ)

    market_index = compute_market_index(stock_set)
    stock_set = stock_set.neutralize(market_index)

    cluster_csv = pathlib.Path(__file__).parent / "clustering_result.csv"
    cluster_df = pd.read_csv(cluster_csv)

    cluster_list = sorted(cluster_df["Cluster"].unique().tolist())
    # クラスター毎に統計量を算出
    for cluster_idx in cluster_list:
        # クラスターに属する銘柄を列挙してsubsetから抽出
        code_list = cluster_df.loc[cluster_df["Cluster"] == cluster_idx, "Code"].values.tolist()
        code_list = [str(c) for c in code_list]
        cluster_subset = stock_set.filter(lambda s: s.stock_code in code_list)
        cluster_stats(cluster_idx, cluster_subset, dir_path)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--fig_path", type=str)
    parser.add_argument("--csv_path", type=str)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.dir_path, limit=args.limit, fig_path=args.fig_path, csv_path=args.csv_path)
