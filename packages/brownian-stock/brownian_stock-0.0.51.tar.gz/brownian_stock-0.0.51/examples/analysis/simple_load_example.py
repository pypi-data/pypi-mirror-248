import argparse
import os

import brownian_stock


def main(dir_path: str):
    dir_path = os.path.expanduser(dir_path)
    repo_path = brownian_stock.repository.RepositoryPath(dir_path)
    repository = brownian_stock.repository.StockSQLRepository(repo_path)

    stock_set = repository.load()
    print(len(stock_set))


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", type=str)
    parser.add_argument("--limit", type=int)
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(args.dir_path)
