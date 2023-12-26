import argparse
import datetime
import json
import os
import pathlib
import warnings
from functools import partial

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
from utils import compute_market_index

warnings.simplefilter(action="ignore")

CATEGORICAL_FEATURES = ["CLUSTER"]


class ClusterScorer:
    def __init__(self, stock_set):
        pass

    def daily_scoring(self):
        pass

    def train(self, start, end, test_date_num):
        print("[*] Building datasets")
        train_end = end - datetime.timedelta(test_date_num + 1)
        test_start = end - datetime.timedelta(test_date_num)

        train_d, train_x, train_y = self.to_dataset(self.stock_set, start, train_end)
        test_d, test_x, test_y = self.to_dataset(self.stock_set, test_start, end)


def command_train(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Lightgbm Scorer")
    subparsers = parser.add_subparsers()

    dir_path = "~/Document/jquants/stock"
    parser_train = subparsers.add_parser("train")
    parser_train.add_argument("--dir_path", type=str, default=dir_path)
    parser_train.add_argument("--no-feng", action="store_true")
    parser_train.add_argument("--limit", type=int, default=None)
    parser_train.set_defaults(handler=command_train)

    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
