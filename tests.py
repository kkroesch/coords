# -*- coding: utf-8 -*-

import unittest

import convert

class TestConverter(unittest.TestCase):

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
        lat = "N47°40'46.900\""
        lng = "E183°54'53.000\""
        #self.assertRaises(AssertionError, convert.parse(lat, lng))

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


if __name__ == '__main__':
    unittest.main()
