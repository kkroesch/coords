# -*- coding: utf-8 -*-

from dataclasses import dataclass
from tokenize import Double
from math import pi as π, cos, sin, asin, atan2, sqrt
from itertools import combinations

R_EARTH = 6371 


@dataclass
class SwissLocation:
    north: float
    west: float

    def __sub__(self, other):
        assert type(other) == SwissLocation, "Must be Swiss (CH1903) locatiom"
        x = abs(self.west - other.west)
        y = abs(self.north - other.north)
        return sqrt(x**2 + y**2) / 1000


@dataclass
class WgsLocation:
    latitude: float
    longitude: float

    def __sub__(self, other):
        """ Gets the distance in kilometers between two locations (Haversine formula). """
        assert issubclass(other.__class__, WgsLocation), "Must be WGS location"
        a = 0.5 - cos((self.latitude - other.latitude) * π / 180) / 2 + \
              cos(self.latitude * π / 180) * cos(other.latitude * π / 180) * \
            (1 - cos((other.longitude - self.longitude) * π / 180)) / 2
        return 2 * R_EARTH * asin(sqrt(a))

    def course_to(self, other):
        """ Gets the compass direction to other coordinate. """
        assert issubclass(other.__class__, WgsLocation), "Must be WGS location"
        dist_long = (other.longitude - self.longitude)
        y = sin(dist_long) * cos(other.latitude)
        x = cos(self.latitude) * sin(other.latitude) - \
            sin(self.latitude) * cos(other.latitude) * cos(dist_long)
        bearing = atan2(y, x)
        return (bearing * 180 / π + 360) % 360

    
@dataclass
class MaidenheadLocation(WgsLocation):
    locator: str

    def __init__(self, locator):
        self.locator = locator
        c1 = int(locator[0:1], 36)-10
        c2 = int(locator[1:2], 36)-10
        c3 = int(locator[2:3], 10)
        c4 = int(locator[3:4], 10)
        if (len(locator) > 4):
            c5 = int(locator[4:5], 36)-10
            c6 = int(locator[5:6], 36)-10
            self.latitude = (((c2 * 10) + c4 + ((c6 + 0.5)/24)) - 90)
            self.longitude = (((c1 * 20) + (c3 * 2) + ((c5 + 0.5) / 12)) - 180)
        else:
            self.latitude = (((c2 * 10) + c4 ) - 90)
            self.longitude = (((c1 * 20) + (c3 * 2)) - 180)

    def bearing_to(self, other):
        return self.course_to(other)


def furthest_away(*locations):
    # Returns the location that is furthest away from all others
    assert len(locations) > 1, "Must have at least 2 locations"
    pairs = combinations(locations, 2)
    distances = [a - b for (a, b) in pairs]
    return max(distances), locations[distances.index(max(distances))]
