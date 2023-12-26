import argparse
import datetime
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import umap
from brownian_stock import StockSet, const, universe, utils
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from utils import compute_market_index


def to_dataframe(stock_set, market_trend=None):
    brand_dict = {}
    for s in stock_set:
        brand_dict[s.stock_code] = s.df[const.COL_CLOSE] / s.df[const.COL_OPEN]
    df = pd.DataFrame(brand_dict)
    df.dropna(axis=1, inplace=True, how="any")

    if market_trend is not None:
        # 各列から市場全体の値動きに関する情報を削除
        for code in df.columns:
            df[code] = utils.neutralize_series(df[code], market_trend.df[const.COL_INDEX_VALUE])
    return df


def main(dir_path, limit=None, fig_path=None, csv_path=None, method="UMAP"):
    """全期間の情報を使って銘柄をクラスタリングする処理
    クラスタリングした結果はデフォルトで同じフォルダに画像とCSVで吐き出す
    """
    # StockSetを読み込んでフィルター
    stock_set = StockSet.init_by_path(dir_path=dir_path, limit=limit)
    start_date = datetime.date(2017, 4, 1)
    end_date = datetime.date(2021, 12, 31)
    stock_set = stock_set.subset_by_range(start_date, end_date)
    univ = universe.TopixSmall1()
    stock_set = stock_set.filter(univ)

    # 使用する定数の定義
    col_factor1 = "Factor1"
    col_factor2 = "Factor2"
    col_cluster = "Cluster"

    # 市場全体の値動きを計算
    market_trend = compute_market_index(stock_set, change=True)

    # 2次元まで圧縮した結果をcompressedという変数に格納
    df = to_dataframe(stock_set, market_trend).T
    print(f"Total Brand Num: {df.shape[0]}")

    if method == "PCA":
        pca = PCA(n_components=2, random_state=42)
        compressed = pca.fit_transform(df.values)
        residual_ratio = sum(pca.explained_variance_ratio_)
        print(f">> Explainable variance ratio: {residual_ratio:.3f}")
    elif method == "TSNE":
        tsne = TSNE(n_components=2, random_state=42)
        compressed = tsne.fit_transform(df.values)
    elif method == "UMAP":
        mapper = umap.UMAP(random_state=0)
        compressed = mapper.fit_transform(df.values)
    else:
        raise ValueError(f"Unknown method `{method}`")
    index = df.index
    columns = [col_factor1, col_factor2]
    compressed = pd.DataFrame(compressed, index=index, columns=columns)
    compressed.index.name = "Code"

    # クラスタリングした結果をcompressedに格納
    kmeans = KMeans(n_clusters=20, init="random", algorithm="lloyd", random_state=123, n_init=1)
    compressed[col_cluster] = kmeans.fit_predict(compressed)

    # compressed_csvの保存
    if not csv_path:
        filename = "clustering_result.csv"
        csv_path = pathlib.Path(__file__).parent / filename

    # 会社名を補完
    company_name_list = []
    for code in compressed.index:
        s = stock_set.get_stock(code)
        company_name_list.append(s.company_name)
    compressed["Name"] = company_name_list
    compressed.to_csv(csv_path)
    print(f">> Save clustring csv to {csv_path}")

    # 描画領域の調整
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1)

    for cluster in compressed[col_cluster].unique():
        x = compressed.loc[compressed[col_cluster] == cluster, col_factor1]
        y = compressed.loc[compressed[col_cluster] == cluster, col_factor2]
        ax.scatter(x, y, alpha=0.6)

    # ファイルを保存
    if fig_path is None:
        filename = f"clustering_result.png"
        fig_path = pathlib.Path(__file__).parent / filename
    fig.show()
    fig.savefig(fig_path)
    print(f">> Save clustring image to {fig_path}")


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--method", type=str, default="TSNE")
    parser.add_argument("--fig_path", type=str)
    parser.add_argument("--csv_path", type=str)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.dir_path, limit=args.limit, fig_path=args.fig_path, csv_path=args.csv_path)
