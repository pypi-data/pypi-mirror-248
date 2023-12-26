import argparse
import datetime

import numpy as np
from brownian_stock import StockSet, const, evaluation


def sector_momentum_relation(stock_set, sector_code, lag=5):
    dates = stock_set.get_stock("86970").df[const.COL_DATE]
    target_set = stock_set.filter(lambda s: s.sector_detail == sector_code)

    coef_ls = []
    for s in target_set:
        x_list = []
        y_list = []
        for d in dates:
            try:
                drift_obj = evaluation.DriftStockEval()
                change_obj = evaluation.PercentageChangeStockEval()
                prev_n = s.subset_by_recent_n_days(d, lag)
                after_n = s.subset_by_after_n_days(d, 5)
                prev_rate = drift_obj(prev_n)
                after_rate = drift_obj(after_n)
                x_list.append(prev_rate)
                y_list.append(after_rate)
            except Exception as e:
                continue
        coef_matrix = np.corrcoef(x_list, y_list)
        coef = coef_matrix[0, 1]
        coef_ls.append(coef)
        print(f"Coef for {s.company_name} {sector_code}: {coef}")


def main(dir_path, limit=None, log_dir=None, fig_dir=None):
    # StockSetを読み込んでフィルター
    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)

    def target_stock(s):
        if s.stock_code == "86970":
            return True
        if s.df[const.COL_TRADING_VOLUME].mean() < 100000:
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
    sector_momentum_relation(stock_set, "3050")
    sector_momentum_relation(stock_set, "3050", lag=40)


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
