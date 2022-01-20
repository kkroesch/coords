# -*- coding: utf-8 -*-

import itertools
from unittest import TestCase, main as unittest_main

import convert
from coords import WgsLocation, SwissLocation, MaidenheadLocation, furthest_away

class TestConverter(TestCase):

    def test_parse(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEqual('N', lat['hemisphere'])
        self.assertEqual('E', lng['hemisphere'])
        self.assertEqual(47, lat['deg'])
        self.assertEqual(7, lng['deg'])
        self.assertEqual(40, lat['min'])
        self.assertEqual(54, lng['min'])
        self.assertEqual(46.9, lat['sec'])
        self.assertEqual(53, lng['sec'])

    def test_malformed(self):
        lat = "N91°40'46.900\""
        lng = "E183°54'53.000\""
        self.assertRaises(AssertionError, convert.parse, lat, lng)

    def test_decimal(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEqual('N47.67969 E7.91472', convert.decimal(lat, lng))

    def test_decimal_minutes(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEqual('N 47° 40.782" E 7° 54.883"', convert.decimal_minutes(lat, lng))


class CoordTest(TestCase):

    def test_wgs_distance(self):
        bonn = WgsLocation(50.738, 7.1)
        dulliken = WgsLocation(47.35, 7.9)
        assert 370 < (bonn - dulliken) < 390
    
    def test_ch_distance(self):
        dulliken = SwissLocation(638323, 244782)
        zürich = SwissLocation(683354, 247353)
        assert 40 < (zürich - dulliken) < 50

    def test_maidenhead_distance(self):
        dulliken = MaidenheadLocation("JN37xi")
        zürich = MaidenheadLocation("JN47gi")
        assert 40 < (zürich - dulliken) < 50

    def test_maidenhead_bearing(self):
        dulliken = MaidenheadLocation("JN37xi")
        stein = MaidenheadLocation("JN37xn")
        bearing = dulliken.bearing_to(stein)
        assert bearing == 0.0
        zürich = MaidenheadLocation("JN47gi")
        assert dulliken.bearing_to(zürich) > 273.0

    def test_furthest_city(self):
        dulliken = MaidenheadLocation("JN37xi")
        zürich = MaidenheadLocation("JN47gi")
        san_francisco = MaidenheadLocation("CM87ts")
        furthest = furthest_away(*[dulliken, zürich, san_francisco])
        assert furthest[1] == san_francisco
        assert furthest[0] > 9000


if __name__ == '__main__':
    unittest_main()