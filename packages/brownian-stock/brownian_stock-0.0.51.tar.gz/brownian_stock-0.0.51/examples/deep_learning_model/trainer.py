import argparse
import datetime
import random

import numpy as np
import torch
from brownian_stock import StockSet, const, evaluation
from torch import nn
from torch.utils.data import DataLoader, Dataset

from .model import NeuralNetwork, test, train


class StockDatasetLoader(Dataset):
    def __init__(self, stock_set, for_test=False):
        self.x, self.y = self.build_dataset(stock_set, for_test=for_test)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        xi = self.x[idx]
        yi = self.y[idx]
        return xi, yi

    def build_dataset(self, stock_set, for_test=False):

        dates = []
        for s in stock_set:
            dates.extend(s.df[const.COL_DATE].tolist())
        dates = set(dates)
        target_set = stock_set

        x_list = []
        y_list = []
        lag_size = 40
        for d in dates:
            for s in target_set:
                try:
                    before_subset = s.subset_by_recent_n_days(d, lag_size)
                    after_subset = s.subset_by_after_n_days(d, 5)
                except:
                    continue

                if for_test:
                    x, y = self.stock_to_record(before_subset, after_subset)
                    if x is None or y is None:
                        continue
                    x /= x[0]
                    x_list.append(x)
                    y_list.append(y)
                else:
                    for i in range(lag_size):
                        x, y = self.stock_to_record(before_subset, after_subset)
                        if x is None or y is None:
                            continue
                        x /= x[i]
                        x_list.append(x)
                        y_list.append(y)

        x_array = np.stack(x_list).astype(np.float32)
        x_array = np.swapaxes(x_array, 1, 2)
        y_array = np.array(y_list).astype(np.float32)
        print(x_array.shape)
        print(y_array.shape)

        x_array = x_array.clip(-3, 3)
        y_array = y_array.clip(-3, 3)
        print(f"[X-Dist], mean: {x_array.mean()}, std: {x_array.std()}")
        print(f"[Y-Dist], mean: {y_array.mean()}, std: {y_array.std()}")
        return x_array, y_array

    def stock_to_record(self, before_subset, after_subset):
        eval_obj = evaluation.DriftStockEval(const.COL_OPEN)
        try:
            df = before_subset.df
            df = df.loc[
                :,
                [
                    const.COL_CLOSE,
                    # const.COL_OPEN,
                    # const.COL_HIGH,
                    # const.COL_LOW,
                    const.COL_TRADING_VOLUME,
                ],
            ]
            for i in range(len(df)):
                x = df / df.iloc[i]
                score = eval_obj(after_subset)
                return x.values, score * 100
        except Exception as e:
            print(e)
            return None, None

    def y_mean(self):
        return self.y.mean()


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--log_dir", type=str)
    parser.add_argument("--fig_dir", type=str)
    return parser


def main(dir_path, limit=None, log_dir=None, fig_dir=None):
    if log_dir is None:
        log_dir = "./log"
    if fig_dir is None:
        fig_dir = "./log"

    def target_stock(s):
        if s.df[const.COL_TRADING_VOLUME].min() == 0:
            return False
        if s.market_type not in ["113"]:
            return False
        if s.stock_code != "60270":
            return False
        return True

    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)
    stock_set = stock_set.filter(target_stock)
    # stock_set = stock_set.filter(lambda s: s.sector_detail == "3050")
    print(len(stock_set))

    # train data
    train_start = datetime.date(2017, 1, 1)
    train_end = datetime.date(2018, 12, 31)
    train_subset = stock_set.subset_by_range(train_start, train_end)
    train_dataset = StockDatasetLoader(train_subset)
    train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # test data
    test_start = datetime.date(2019, 1, 1)
    test_end = datetime.date(2019, 12, 31)
    test_subset = stock_set.subset_by_range(test_start, test_end)
    test_dataset = StockDatasetLoader(test_subset)
    test_dataloader = DataLoader(test_dataset, shuffle=True)

    model = NeuralNetwork()
    loss_fn = nn.MSELoss()

    lr = 1e-3
    iter_times = 1000
    for i in range(10):
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)
        # optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        for j in range(iter_times):
            print(f"[Epoch{i*iter_times+j+1}]")
            train(train_dataloader, model, loss_fn, optimizer, train_dataset.y_mean())
            test(test_dataloader, model, loss_fn, test_dataset.y_mean())
            print("")
        lr *= 0.1


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.dir_path, limit=args.limit, log_dir=args.log_dir, fig_dir=args.fig_dir)
