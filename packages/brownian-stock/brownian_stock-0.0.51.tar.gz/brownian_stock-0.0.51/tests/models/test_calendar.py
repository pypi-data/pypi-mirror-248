import datetime

import brownian_stock


def test_is_busienss_day():
    cal = brownian_stock.Calendar.get_instance()

    # 営業日が正しく判定できること(平日すべて)
    assert cal.is_business_day(datetime.date(2023, 3, 13))
    assert cal.is_business_day(datetime.date(2023, 3, 14))
    assert cal.is_business_day(datetime.date(2023, 3, 15))
    assert cal.is_business_day(datetime.date(2023, 3, 16))
    assert cal.is_business_day(datetime.date(2023, 3, 17))

    # 土日が営業日判定で無いこと
    assert not cal.is_business_day(datetime.date(2023, 3, 11))
    assert not cal.is_business_day(datetime.date(2023, 3, 12))

    # 祝日の判定が正しくできること
    assert not cal.is_business_day(datetime.date(2023, 1, 1))
    assert not cal.is_business_day(datetime.date(2023, 12, 31))
    assert not cal.is_business_day(datetime.date(2023, 3, 21))


def test_days_from_last_business_day():
    cal = brownian_stock.Calendar.get_instance()

    # 平日の判定
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 13)) == 2
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 14)) == 0
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 15)) == 0
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 16)) == 0
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 17)) == 0

    # 使われることは無いだろうが休日
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 11)) == 0
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 12)) == 1

    # 祝日も正しく動作するかどうか
    assert cal.days_from_last_business_day(datetime.date(2023, 3, 22)) == 1


def test_record_date():
    cal = brownian_stock.Calendar.get_instance()
    assert cal.record_date_of_month(datetime.date(2023, 2, 1)) == datetime.date(2023, 2, 24)
    assert cal.record_date_of_month(datetime.date(2023, 3, 1)) == datetime.date(2023, 3, 29)
    assert cal.record_date_of_month(datetime.date(2023, 7, 1)) == datetime.date(2023, 7, 27)
