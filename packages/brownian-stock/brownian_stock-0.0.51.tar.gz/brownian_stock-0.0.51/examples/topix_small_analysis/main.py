""" 直近の騰落率の高い銘柄を持ち続けた場合の収支評価モデル
"""
import argparse
import datetime

import brownian_stock
from brownian_stock import AbstractModel, Simulator, const, trading
from ligthgbm_scorer import LightGBMScorer
from utils import stockset_universe

INITIAL_FUNDS = 3000000


class Topix1000Model(AbstractModel):
    def __init__(self, dir_path, log_dir, limit=None):
        self.dir_path = dir_path
        stock_set = brownian_stock.load_stock_set(dir_path=dir_path, limit=limit)
        super().__init__(stock_set, log_dir)

    def name(self):
        return "Topix100Model"

    def initialize(self):
        """取引開始前の初期化処理"""
        # 取引のない銘柄は除去
        def target_stock(s):
            if min(s.to_list(const.COL_TRADING_VOLUME)) == 0:
                return False
            return True

        self.stock_set = self.stock_set.filter(target_stock)

        # Universeの選択
        # univ = universe.TopixSmall1()
        # self.stock_set = self.stock_set.filter(univ)
        self.stock_set = stockset_universe(self.stock_set)

        # 各ロジックを初期化
        self.lgbm_scorer = LightGBMScorer(self.stock_set, self.dir_path)

    def trade(self, trade_date, is_first_date, is_last_date):
        if trade_date.month == 1 and trade_date.day == 1:
            year = trade_date.year - 1
            start_date = datetime.date(2017, 1, 1)
            end_date = datetime.date(year, 12, 31)
            self.lgbm_scorer.train(start_date, end_date, no_feng=True)

        # 平日のみ取引を実施する
        if trade_date.weekday() not in [0, 1, 2, 3, 4]:
            return

        subset = self.stock_set.subset_by_available_at(trade_date)
        if len(subset) == 0:
            return

        # 各ファクターのスコアを計算して加重平均
        lgbm_return_map = self.lgbm_scorer.daily_scoring(trade_date)
        return_map = lgbm_return_map.remove_none()
        drop_count = len(lgbm_return_map) - len(return_map)
        print(f"Drop {drop_count} brands.")
        return_map = lgbm_return_map.ranked()

        # 所有している株をすべて精算
        self.sell_all_if_possible(trade_date)
        self.buy_all_if_possible(trade_date)
        capacity = self.margin(trade_date)
        order = trading.long_short_trading(capacity, trade_date, subset, return_map, reverse_order=False, top_n=10)
        order.show()
        trading.execute_order(self, trade_date, order)


def main(dir_path, limit=None, log_dir=None, fig_dir=None):
    if log_dir is None:
        log_dir = "./log"
    if fig_dir is None:
        fig_dir = "./log"

    model = Topix1000Model(dir_path, log_dir, limit=limit)
    model.initialize()

    start_date = datetime.date(2018, 1, 1)
    end_date = datetime.date(2022, 12, 31)
    simulator = Simulator(model, save_figure=fig_dir)
    simulator.init_state(INITIAL_FUNDS)
    simulator.walk(start_date, end_date, display_progress=True)


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
