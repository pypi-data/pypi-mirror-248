import argparse
import datetime

import numpy as np
from brownian_stock import StockSet, const, evaluation
from scipy.stats import spearmanr


def sector_relation(stock_set, sector1, sector2, lag=40):
    dates = stock_set.get_stock("86970").df[const.COL_DATE]
    set1 = stock_set.filter(lambda s: s.sector == sector1)
    set2 = stock_set.filter(lambda s: s.sector == sector2)

    x_list = []
    y_list = []
    for d in dates:
        try:
            price_drift = evaluation.DriftStockSetEval(const.COL_CLOSE)
            prev = set1.subset_by_recent_n_days(d, lag, ignore_error=True)
            after = set2.subset_by_after_n_days(d, 5, ignore_error=True)
            prev_rate = price_drift(prev)
            after_rate = price_drift(after)
            x_list.append(prev_rate)
            y_list.append(after_rate)
        except Exception as e:
            continue
    coef_matrix = np.corrcoef(x_list, y_list)
    rho, p = spearmanr(x_list, y_list)
    coef = coef_matrix[0, 1]
    print(f"Pearson Coef of {sector1} => {sector2}: {coef}")
    print(f"Spearman Coef of {sector1} => {sector2}: {rho}")


def main(dir_path, limit=None, log_dir=None, fig_dir=None):
    # StockSetを読み込んでフィルター
    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)

    def target_stock(s):
        if s.stock_code == "86970":
            return True
        if s.df[const.COL_TRADING_VOLUME].min() == 0:
            return False
        if s.market_type not in ["111"]:
            return False
        return True

    stock_set = stock_set.filter(target_stock)

    start_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2017, 12, 31)
    stock_set = stock_set.subset_by_range(start_date, end_date)

    code_ls = [
        "0050",
        "1050",
        "2050",
        "3050",
        "3100",
        "3150",
        "3200",
        "3250",
        "3300",
        "3350",
        "3400",
        "3450",
        "3500",
        "3550",
        "3600",
        "3650",
        "3700",
        "3750",
        "3800",
        "4050",
        "5050",
        "5100",
        "5150",
        "5200",
        "5250",
        "6050",
        "6100",
        "7050",
        "7100",
        "7150",
        "7200",
        "8050",
        "9050",
        "9999",
    ]

    lag = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    for l in lag:
        print(f"Lag {l}")
        for code1 in range(1, 18):
            # for code2 in range(1, 18):
            sector_relation(stock_set, str(code1), str(code1), lag=l)
        print("")


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--log_dir", type=str)
    parser.add_argument("--fig_dir", type=str)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.dir_path, limit=args.limit, log_dir=args.log_dir, fig_dir=args.fig_dir)
