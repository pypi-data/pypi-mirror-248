from typing import Any, Dict, List, Tuple

import numpy as np
from scipy.stats import spearmanr


class SimpleFeatureSample:
    def __init__(self, columns, sample_num=15):
        self.columns = columns
        self.count = [1.0] * len(columns)
        self.score = [0.0] * len(columns)
        self.sample_num = sample_num

    def sample(self, n):
        weights = []
        for i in range(len(self.columns)):
            c = self.count[i]
            s = self.score[i] / c

            v = s + np.log(n) / (2 * c)
            weights.append(v)
        weights = np.array(weights) / sum(weights)
        sample = np.random.choice(self.columns, size=self.sample_num, replace=False, p=weights)
        return sample

    def update(self, cols, score):
        for i, col in enumerate(self.columns):
            if col in cols:
                self.count[i] += 1
                self.score[i] += score

    def show(self):
        for col, s, c in zip(self.columns, self.score, self.count):
            print(f"{col:<20} : {s/c:.5f}")


def simple_feature_sample(model, x, y, columns):
    pass


def lgb_permutation_importance(model, x, y, columns=None, iter_times=10, display=True):
    if columns is None:
        columns = x.columns.tolist()

    metric_func = spearman_metric
    # ベースラインの計算
    baseline = metric_func(y, model.predict(x[columns]))

    # 各列をシャフルして精度の悪化度合いを測定
    mean_dict = {}
    std_dict = {}
    for col in columns:
        px = x[columns].copy()
        score_list = []
        for _ in range(iter_times):
            px[col] = np.random.permutation(px[col])
            y_pred = model.predict(px)
            score = metric_func(y_pred, y)
            score_list.append(score)
        mean_dict[col] = baseline - np.mean(score_list)
        std_dict[col] = np.std(score_list)

    # 降順に並び替え
    sort_ls = []
    for col in columns:
        m = mean_dict[col]
        sort_ls.append((m, col))
    sort_ls = sorted(sort_ls, key=lambda x: x[0], reverse=True)

    # スコアを表示
    if display:
        for _, col in sort_ls:
            m = mean_dict[col]
            s = std_dict[col]
            print(f"{col:<20} : {m:.5f} ± {s:.5f}")

    results = [col for _, col in sort_ls]
    return results


def spearman_metric(y_true, y_pred):
    score, _ = spearmanr(y_true, y_pred)
    return score
