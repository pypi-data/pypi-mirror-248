import datetime
import tempfile

from brownian_stock.models.index_series import IndexSeries
from brownian_stock.repository.index_csv_repository import IndexCsvRepository
from brownian_stock.repository.repository_path import RepositoryPath


def test_index_csv_repository():
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = IndexCsvRepository(repo_path)

        # テスト用のIndexSeriesオブジェクト
        base_date = datetime.date(2022, 4, 1)
        dates = [base_date + datetime.timedelta(days=i) for i in range(5)]
        values = list(range(5))
        index_series = IndexSeries(dates, values)

        # 元と同じデータが読み込めることを確認する
        repository.save("test", index_series)
        loaded = repository.load("test")
        assert index_series.to_list() == loaded.to_list()
