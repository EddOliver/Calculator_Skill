#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
#
# Project: Snips Screen Project
# Created Date: Sunday, February 10th 2019, 11:13:46 pm
# Author: Greg
# -----
# Last Modified: Sun Mar 03 2019
# Modified By: Greg
# -----
# Copyright (c) 2019 Greg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
### **************************************************************************** ###


import inflect


class Utilities:
    """ Helpers Functions to convert objects """

    def __init__(self):
        self.inflectObj = inflect.engine()

    @staticmethod
    def strip_end(text):
        """removes 'point zero' from the end of a string

        Arguments:
            text {str} -- string text to remove 'point zero' from

        Returns:
            str -- striped string
        """
        if not text.endswith("point zero"):
            return text
        return text[:len(text)-len("point zero")]

    @staticmethod
    def strip_float_point_zero(f):
        """removes '.0' from the end of a float

        Arguments:
            text {float} -- float to remove '.0' from

        Returns:
            str -- striped string
        """
        float_string = repr(f)
        if not float_string.endswith(".0"):
            return text
        return float_string[:len(float_string)-len(".0")]

    @staticmethod
    def scientificnumber_to_str(f, decimalplaces=3):
        """converts scientific number to full number as a string
           1.0E-02 returns a string of '0.001'

        Arguments:
            f {number} -- number

        Keyword Arguments:
            decimalplaces {int} -- number of digits to limit after the decimal point (default: {3})

        Returns:
            str -- passing in 1.0E-02 returns a string of '0.001'
        """
        float_string = repr(f)
        if 'e' in float_string:  # detect scientific notation
            digits, exp = float_string.split('e')
            digits = digits.replace('.', '').replace('-', '')
            exp = int(exp)
            # minus 1 for decimal point in the sci notation
            zero_padding = '0' * (abs(int(exp)) - 1)
            sign = '-' if f < 0 else ''
            if exp > 0:
                float_string = '{}{}{}'.format(sign, digits, zero_padding)
            else:
                float_string = '{}0.{}{}'.format(
                    sign, zero_padding, digits[:decimalplaces])
        else:
            digits, exp = float_string.split('.')
            sign = '-' if f < 0 else ''
            float_string = '{}{}.{}'.format(sign, digits, exp[:decimalplaces])
        return float_string

    def number_to_words(self, number=0, decimalplaces=3):
        """ Converts a number to a readable string 

         Keyword arguments:
            number {number} -- int float to convert
            decimalplaces -- number of numbers after the decimal place (default: {3})

        Returns:
            string -- number in string : 100 > one hundred
        """

        return self.strip_end(self.inflectObj.number_to_words(self.scientificnumber_to_str(number, decimalplaces))).strip()
