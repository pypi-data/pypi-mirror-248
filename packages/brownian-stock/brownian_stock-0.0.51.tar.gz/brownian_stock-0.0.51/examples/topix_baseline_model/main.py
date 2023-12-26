""" TOPIXを持ち続けた場合の収支評価モデル
"""
import argparse
import datetime

from brownian_stock import AbstractModel, Simulator, StockSet, const

INITIAL_FUNDS = 3000000


class TopixBaselineModel(AbstractModel):
    def __init__(self, stock_set, log_dir):
        super().__init__(stock_set, log_dir)
        self.initialized = False

    def name(self):
        return "TopixBaselineModel"

    def trade(self, trade_date, is_first_date, is_last_date):
        if not self.initialized and self.stock_set.get_stock("13080").has_record(trade_date):
            num = self.available_buy_volume(trade_date, "13080")
            self.buy(trade_date, "13080", num)
            self.initialized = True


def main(dir_path, limit=None, log_dir=None, fig_dir=None):
    if log_dir is None:
        log_dir = "./log"
    if fig_dir is None:
        fig_dir = "./log"

    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)
    model = TopixBaselineModel(stock_set, log_dir)

    start_date = datetime.date(2022, 4, 1)
    end_date = datetime.date(2022, 12, 20)
    simulator = Simulator(model, save_figure=fig_dir)
    simulator.init_state(INITIAL_FUNDS)
    simulator.walk(start_date, end_date)


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
