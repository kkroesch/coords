# -*- coding: utf-8 -*-

import re
import sys

COMPASS = ['N','W','S','E']
MIN_SEC_PATTERN = r"(?P<minutes>\d+)'(?P<seconds>\d+\.?\d*)\""
DEG_PATTERN = r"(?P<compass>[NSEW])?\s?(?P<degrees>\d+)°"
coord_pattern = re.compile(DEG_PATTERN + MIN_SEC_PATTERN)


def parse(lat, lng):
    m = re.match(coord_pattern, lat)
    assert m is not None
    coord_dict = m.groupdict()
    lat = {
        "hemisphere": coord_dict['compass'],
        "deg": int(coord_dict['degrees']),
        "min": int(coord_dict['minutes']),
        "sec": float(coord_dict['seconds'])
    }
    assert 0 <= lat['deg'] <= 90
    assert lat['hemisphere'] == 'N' or lat['hemisphere'] == 'S'

    m = re.match(coord_pattern, lng)
    assert m is not None
    coord_dict = m.groupdict()
    lng = {
        "hemisphere": coord_dict['compass'],
        "deg": int(coord_dict['degrees']),
        "min": int(coord_dict['minutes']),
        "sec": float(coord_dict['seconds'])
    }
    assert 0 <= lng['deg'] <= 180
    assert lng['hemisphere'] == 'E' or lng['hemisphere'] == 'W'

    return lat, lng


def decimal(lat, lng):
    latitude = ((lat['sec'] / 60 + lat['min']) / 60.0) + lat['deg']
    longitude = ((lng['sec'] / 60 + lng['min']) / 60.0) + lng['deg']

    return '{}{:.{prec}f} {}{:.{prec}f}'.format(lat['hemisphere'], latitude, lng['hemisphere'], longitude, prec=5)


def decimal_minutes(lat, lng):
    latitude = lat['sec'] / 60 + lat['min']
    longitude = lng['sec'] / 60 + lng['min']
    return "{} {}° {:.{prec}f}\" {} {}° {:.{prec}f}\"".format(
        lat['hemisphere'], lat['deg'], latitude,
        lng['hemisphere'], lng['deg'], longitude,
        prec=3
    )


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2]:
        lat = sys.argv[1]
        lng = sys.argv[2]
    else:
        lat = raw_input("Enter coordinates (lat): ")
        lng = raw_input("Enter coordinates (lng): ")

    lat,lng = parse(lat, lng)

    print decimal(lat, lng)
    print decimal_minutes(lat, lng)
