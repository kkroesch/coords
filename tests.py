# -*- coding: utf-8 -*-

import itertools
from unittest import TestCase

import convert
from coords import WgsLocation, SwissLocation, MaidenheadLocation, furthest_away

class TestConverter(TestCase):

    def test_parse(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEquals('N', lat['hemisphere'])
        self.assertEquals('E', lng['hemisphere'])
        self.assertEquals(47, lat['deg'])
        self.assertEquals(7, lng['deg'])
        self.assertEquals(40, lat['min'])
        self.assertEquals(54, lng['min'])
        self.assertEquals(46.9, lat['sec'])
        self.assertEquals(53, lng['sec'])

    def test_malformed(self):
        lat = "N91°40'46.900\""
        lng = "E183°54'53.000\""
        self.assertRaises(AssertionError, convert.parse, lat, lng)

    def test_decimal(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEquals('N47.67969 E7.91472', convert.decimal(lat, lng))

    def test_decimal_minutes(self):
        lat = "N47°40'46.900\""
        lng = "E007°54'53.000\""
        lat, lng = convert.parse(lat, lng)
        self.assertEquals('N 47° 40.782" E 7° 54.883"', convert.decimal_minutes(lat, lng))


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

    def test_load_data(self):
        import yaml
        import json
        with open("fixtures.yml") as stream:
            fix = yaml.load(stream, Loader=yaml.Loader)
            locations = fix['locations']
            jl = list()
            for key, value in locations.items():
                m = MaidenheadLocation(value)
                jl.append({
                    'name': key, 
                    'lat': m.latitude, 
                    'lon': m.longitude}
                )
            print(json.dumps(jl, indent=4))
