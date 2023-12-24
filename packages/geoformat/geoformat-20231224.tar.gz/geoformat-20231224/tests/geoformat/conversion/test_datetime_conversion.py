import datetime

from tests.utils.tests_utils import test_function

from geoformat.conversion.datetime_conversion import (
    format_datetime_object_to_str_value,
    date_to_int,
    time_to_int,
    int_to_date,
    int_to_time,
)

from tests.data.features import date_time_value


format_datetime_object_to_str_value_parameters = {
    0: {
        "datetime_value": datetime.datetime(year=2022, month=12, day=12),
        "format": ["year", "month", "day"],
        "return_value": "20221212",
    },
    1: {
        "datetime_value": datetime.datetime(year=2022, month=12, day=12),
        "format": ["year", "month"],
        "return_value": "202212",
    },
    2: {
        "datetime_value": datetime.datetime(year=2022, month=12, day=12, hour=11),
        "format": ["year", "month", "hour"],
        "return_value": "20221211",
    },
}

date_to_int_parameters = {
    0: {
        "date_value": datetime.date(1970, 1, 1),
        "epoch": datetime.date(1970, 1, 1),
        "return_value": 0,
    },
    1: {
        "date_value": datetime.date(1, 1, 1),
        "epoch": datetime.date(1970, 1, 1),
        "return_value": -719162,
    },
    2: {
        "date_value": datetime.date(1970, 1, 1),
        "epoch": datetime.date(1, 1, 1),
        "return_value": 719162,
    },
    3: {
        "date_value": datetime.date(2023, 12, 1),
        "epoch": datetime.date(1970, 1, 1),
        "return_value": 19692,
    },
    4: {
        "date_value": datetime.date(2023, 12, 31),
        "epoch": datetime.date(1970, 1, 1),
        "return_value": 19692+30,
    },
    5: {
        "date_value": datetime.date(2011, 2, 10),
        "epoch": datetime.date(1970, 1, 1),
        "return_value": 15015,
    },
}


time_to_int_parameters = {
    0: {
        "time_value": date_time_value.time(),
        "return_value": 40930000999
    },
    1: {
        "time_value": datetime.time(hour=0, minute=0, second=0, microsecond=0),
        "return_value": 0
    },
    2: {
        "time_value": datetime.time(hour=0, minute=0, second=0, microsecond=1),
        "return_value": 1
    },
    3: {
        "time_value": datetime.time(hour=23, minute=59, second=59, microsecond=999999),
        "return_value": 86399999999
    },
}


int_to_date_parameters = {
    0: {
        "int_value": 0,
        "epoch": datetime.date(1970, 1, 1),
        "return_value": datetime.date(1970, 1, 1),
    },
    1: {
        "int_value": -719162,
        "epoch": datetime.date(1970, 1, 1),
        "return_value": datetime.date(1, 1, 1),
    },
    2: {
        "int_value": 719162,
        "epoch": datetime.date(1, 1, 1),
        "return_value": datetime.date(1970, 1, 1),
    },
    3: {
        "int_value": 19692,
        "epoch": datetime.date(1970, 1, 1),
        "return_value": datetime.date(2023, 12, 1),
    },
    4: {
        "int_value": 19692+30,
        "epoch": datetime.date(1970, 1, 1),
        "return_value": datetime.date(2023, 12, 31),
    },
    5: {
        "int_value": 15015,
        "epoch": datetime.date(1970, 1, 1),
        "return_value": datetime.date(2011, 2, 10),
    },
}

int_to_time_parameters = {
    0: {
        "int_value": 40930000999,
        "return_value": date_time_value.time()
    },
    1: {
        "int_value": 0,
        "return_value": datetime.time(hour=0, minute=0, second=0, microsecond=0)
    },
    2: {
        "int_value": 1,
        "return_value": datetime.time(hour=0, minute=0, second=0, microsecond=1)
    },
    3: {
        "int_value": 86399999999,
        "return_value": datetime.time(hour=23, minute=59, second=59, microsecond=999999)
    },
}


def test_all():
    # format_datetime_object_to_str_value
    print(
        test_function(
            format_datetime_object_to_str_value,
            format_datetime_object_to_str_value_parameters,
        )
    )

    print(test_function(date_to_int, date_to_int_parameters))

    print(test_function(time_to_int, time_to_int_parameters))

    print(test_function(int_to_date, int_to_date_parameters))

    print(test_function(int_to_time, int_to_time_parameters))


if __name__ == "__main__":
    test_all()
