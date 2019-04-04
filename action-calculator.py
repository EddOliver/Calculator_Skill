#!/usr/bin/env python3
# -*- coding: utf-8 -*-

### **************************************************************************** ###
#
# Project: Calculator Skill for Snips
# Created Date: Wednesday, January 30th 2019, 6:41:12 pm
# Author: Greg
# -----
# Last Modified: Thu Apr 04 2019
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



import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
from Utilities import Utilities
import io
import sys
import os


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


util = Utilities()


class SnipsConfigParser(configparser.ConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            #conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()


def strip_float_point_zero(f):
        """removes '.0' from the end of a float

        Arguments:
            text {float} -- float to remove '.0' from

        Returns:
            str -- striped string
        """
        f = repr(f)
        if not f.endswith(".0"):
            return f
        return f[:len(f)-len(".0")]

def convert_lengths(amount, input_length_type, output_length_type):
    """Convert input length type to mm's then mm's to output length type

    Arguments:
        amount {int} -- length amount
        input_length_type {str} -- millimeter, centimeter etc
        output_length_type {str} -- meter, kilometer etc

    Returns:
        list -- returns answer and word for units from and units to
    """
    answer = 0
    length = amount
    unitsfrom = "millimeters"
    unitsto = "millimeters"

    # convert the length to lowest number (millimeters)
    if not input_length_type == "millimeter":
        # we dont have to change the amount if it is already in millimeters
        if input_length_type == "centimeter":
            length = amount / 0.10000
            unitsfrom = input_length_type if amount == 1 else "centimeters"
        elif input_length_type == "meter":
            length = amount / 0.0010000
            unitsfrom = input_length_type if amount == 1 else "meters"
        elif input_length_type == "kilometer":
            length = amount / 0.0000010000
            unitsfrom = input_length_type if amount == 1 else "kilometers"
        elif input_length_type == "inch":
            length = amount / 0.039370
            unitsfrom = input_length_type if amount == 1 else "inches"
        elif input_length_type == "yard":
            length = amount / 0.0010936
            unitsfrom = input_length_type if amount == 1 else "yards"
        elif input_length_type == "feet":
            length = amount / 0.0032808
            unitsfrom = "foot" if amount == 1 else "feet"
        elif input_length_type == "furlong":
            length = amount / 0.0000049710
            unitsfrom = input_length_type if amount == 1 else "furlongs"
        elif input_length_type == "mile":
            length = amount / 0.00000062137
            unitsfrom = input_length_type if amount == 1 else "miles"
        elif input_length_type == "nautical mile":
            if conf['global']['us_or_uk_metric'].lower() == "uk":
                length = amount / 0.00000053961
            else:
                length = amount / 0.00000053996
            unitsfrom = input_length_type if amount == 1 else "nautical miles"
    else:
        unitsfrom = input_length_type if amount == 1 else "millimeters"

    # now convert millimeters to the length type
    if output_length_type == "millimeter":
        answer = length
        unitsto = "millimeters"
    elif output_length_type == "centimeter":
        answer = length / 10.000
        unitsto = "centimeters"
    elif output_length_type == "meter":
        answer = length / 1000.0
        unitsto = "meters"
    elif output_length_type == "kilometer":
        answer = length / 1000000.0
        unitsto = "kilometers"
    elif output_length_type == "inch":
        answer = length * 0.039370
        unitsto = "inches"
    elif output_length_type == "yard":
        answer = length * 0.0010936
        unitsto = "yards"
    elif output_length_type == "feet":
        answer = length * 0.0032808
        unitsto = "feet"
    elif output_length_type == "furlong":
        answer = length * 0.0000049710
        unitsto = "furlongs"
    elif output_length_type == "mile":
        answer = length * 0.00000062137
        unitsto = "miles"
    elif output_length_type == "nautical mile":
        unitsto = "nautical miles"
        if conf['global']['us_or_uk_metric'].lower() == "uk":
            answer = length * 0.00000053961
        else:
            answer = length * 0.00000053996

    return answer, unitsfrom, unitsto


def subscribe_intent_weightConverter(hermes, intentMessage):
    sayMessage = "Something has gone wrong, and I can not convert that weight for you"

    try:
        weightFunction1 = intentMessage.slots.weightFunction1.first().value.lower()
        weightFunction2 = intentMessage.slots.weightFunction2.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if weightFunction1 and weightFunction2 and isinstance(amount, (int, float)):
            answer = 0
            weight = amount

            # convert the amount to lowest number (milligrams)
            if not weightFunction1 == "milligram":
                # we dont have to change the amount if it is already in milligrams
                if weightFunction1 == "kilogram":
                    weight = amount * 1000000.0
                elif weightFunction1 == "ounce":
                    weight = amount * 28349.5
                elif weightFunction1 == "gram":
                    weight = amount * 1000.0
                elif weightFunction1 == "pound":
                    weight = amount * 453592.0
                elif weightFunction1 == "stone":
                    weight = amount * 6350290.0

            # now convert milligrams to the mass type
            if weightFunction2 == "kilogram":
                answer = weight / 1000000.0
            elif weightFunction2 == "ounce":
                answer = weight * 0.000035274
            elif weightFunction2 == "gram":
                answer = weight / 1000.0
            elif weightFunction2 == "pound":
                answer = weight * 0.0000022046
            elif weightFunction2 == "stone":
                answer = weight * 0.00000015747
            else:
                answer = weight

            if "{:.3g}".format(answer) == "1" and not units == "stone":
                sayMessage = "That would be one {}".format(weightFunction2)
            elif "{:.3g}".format(answer) == "1" and units == "stone":
                sayMessage = "That would be one stone"
            else:
                amount = util.number_to_words(amount)
                answer = util.number_to_words(answer)
                #amount = strip_end(p.number_to_words(float_to_str(amount))).strip()
                #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                sayMessage = "{} {}s would be {} {}s".format(
                    amount, weightFunction1, answer, weightFunction2)
                #sayMessage = "That would be {} {}".format(p.number_to_words(float_to_str(answer)),units)

    except Exception as e:
        print("Error in weightConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


def subscribe_intent_lengthConverter(hermes, intentMessage):
    sayMessage = "Something has gone wrong, and I can not convert that length for you"

    try:
        lengthFunction1 = intentMessage.slots.lengthFunction1.first().value.lower()
        lengthFunction2 = intentMessage.slots.lengthFunction2.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if lengthFunction1 and lengthFunction2 and isinstance(amount, (int, float)):
            answer, unitsfrom, unitsto = convert_lengths(
                amount, lengthFunction1, lengthFunction2)

            amount = util.number_to_words(amount)
            #amount = strip_end(p.number_to_words(float_to_str(amount))).strip()
            if "{:.2g}".format(answer) == "1":
                if unitsto == "feet":
                    sayMessage = "{} {}, that would be one foot".format(
                        amount, unitsfrom)
                else:
                    sayMessage = "{} {}, that would be one {}".format(
                        amount, unitsfrom, unitsto[:-1])
            else:
                answer = util.number_to_words(answer, 2)
                #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                sayMessage = "{} {}, would be {} {}".format(
                    amount, unitsfrom, answer, unitsto)

    except Exception as e:
        print("Error in lengthConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


def subscribe_intent_currencyConverter(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    sayMessage = "Something has gone wrong, and I can not convert that currency for you"

    try:
        currencyFrom = None
        if intentMessage.slots.currencyFrom:
            currencyFrom = intentMessage.slots.currencyFrom.first().value
        currencyTo = None
        if intentMessage.slots.currencyTo:
            currencyTo = intentMessage.slots.currencyTo.first().value
        amount = None
        unit = None
        if intentMessage.slots.amount:
            amount = intentMessage.slots.amount.first().value
            unit = intentMessage.slots.amount.first().unit
            if len(unit) == 3:
                currencyFrom = unit
        

        if currencyTo == None:
            currencyTo = conf['global']['default_currency']

        if currencyFrom == None:
            currencyFrom = conf['global']['default_currency']

        if currencyFrom == currencyTo:
            sayMessage = "Converting {} to {} would be the same. {}".format(
                currencyFrom, currencyTo, amount)
        elif currencyFrom and currencyTo and isinstance(amount, (int, float)):
            import urllib.request
            import json
            import ssl
            context = ssl._create_unverified_context()

            api = conf['secret']['exchange_rate_api']
            url = "https://www.amdoren.com/api/currency.php?"
            response = urllib.request.urlopen("{}api_key={}&from={}&to={}&amount={}".format(
                url, api, currencyFrom, currencyTo, amount), context=context)
            r = json.loads(response)
            if r['error'] == 0:
                sayMessage = "In {}, that would be {:.2f}".format(
                    currencyTo, r['amount'])
            elif r['error'] == 100:
                sayMessage = "You have not provided an API key in the config"
            elif r['error'] == 110:
                sayMessage = "Invalid currency converter API key"
            elif r['error'] == 210:
                sayMessage = "Invalid from currency value"
            elif r['error'] == 260:
                sayMessage = "Invalid to currency value"
            elif r['error'] == 300:
                sayMessage = "The amount must be numeric value"
            elif r['error'] == 310:
                sayMessage = "The amount value is invalid"
            elif r['error'] == 320:
                sayMessage = "The amount cannot be zero"
            else:
                sayMessage = "Sorry, your API limit has been reached for the month"

            current_session_id = intentMessage.session_id
            hermes.publish_end_session(current_session_id, sayMessage)


    except Exception as e:
        print("Error in currencyConverter Snippet: {}".format(e))
        current_session_id = intentMessage.session_id
        hermes.publish_end_session(
            current_session_id, "Currency converter error. the API limit may have been reached for the month")


def subscribe_intent_mathsQuestion(hermes, intentMessage):
    sayMessage = "Something went wrong, I can not do that maths calculation for you"

    try:
        # uses BODMAS.. so in order do division and multiplication, then addition and subtraction..from left to right
        #slot_dict = intentMessage.slots.toDict()
        function_array = []
        number_array = []
        function_array = intentMessage.slots['function'].all()
        number_array = intentMessage.slots['number'].all()
            
        is_error = False

        mynumbers = []
        for num in number_array:
            mynumbers.append(num.value)

        myfunctions = []
        for fun in function_array:
            myfunctions.append(fun.value)

        

        funloopindex = 0
        evalString = ""
        for index,num in enumerate(mynumbers):
            mathsstr = "{}".format(num)
            functionstr = ""
            insertString = ""

            if len(myfunctions) > funloopindex:
                functionstr = "{}".format(myfunctions[funloopindex])

            if functionstr == "squared":
                insertString = "**2"
            elif functionstr == "cubed":
                insertString = "**3"
            elif functionstr == "square root":
                insertString = "**0.5"
            elif functionstr == "cubed root":
                insertString = "**0.3333333333"
                
            if len(insertString) > 0:
                funloopindex +=1
                functionstr = ""
                if len(myfunctions) > funloopindex:
                    functionstr = "{}".format(myfunctions[funloopindex])
            
            if functionstr == "plus":
                functionstr = "+"
            elif functionstr == "minus":
                functionstr = "-"
            elif functionstr == "times":
                functionstr = "*"
            elif functionstr == "to the power of":
                functionstr = "**"
            elif functionstr == "divide":
                # has to be "divide"
                # is the next number a ZERO.. cant divide by ZERO
                next_number = mynumbers[index+1]
                if next_number == 0:
                    sayMessage = "Sorry, I can not divide by zero"
                    is_error = True
                    break
                else:
                    functionstr = "/"

            evalString = "{}{}{}{}".format(evalString,mathsstr,insertString,functionstr)
        
            funloopindex +=1
           
        
        if not is_error:
           
           
            answer = eval(evalString)
           
            answer = util.number_to_words(answer, 5)
            #answer = strip_end(p.number_to_words(float_to_str(answer,5))).strip()
            sayMessage = "That would be {}".format(answer)
        
    except Exception as e:
        print("Error in mathsQuestion Snippet: {}".format(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)
    

def subscribe_intent_areaFunction(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    sayMessage = "Something might have gone wrong or I do not know how to convert that area"

    try:
        areaFunction1 = intentMessage.slots.areaFunction1.first().value.lower()
        areaFunction2 = intentMessage.slots.areaFunction2.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if isinstance(amount, (int, float)):
            answer = 0
            area = amount
            unitsfrom = "square millimeters"
            unitsto = "square millimeters"

            # convert the area to lowest area unit (square millimeters)
            if not areaFunction1 == "square millimeters":
                # we dont have to change the amount if it is already in square millimeters
                if areaFunction1 == "square meter":
                    area = amount / 0.0000010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "square metres"
                    else:
                        unitsfrom = "square meters"
                elif areaFunction1 == "square centimeter":
                    area = amount / 0.010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "square centimetres"
                    else:
                        unitsfrom = "square centimeters"
                elif areaFunction1 == "square inch":
                    area = amount / 0.0015500
                    unitsfrom = "square inches"
                elif areaFunction1 == "square feet":
                    area = amount / 0.000010764
                    unitsfrom = "square feet"
                elif areaFunction1 == "square yard":
                    area = amount / 0.0000011960
                    unitsfrom = "square yards"
                elif areaFunction1 == "square kilometer":
                    area = amount / 0.0000000000010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "square kilometres"
                    else:
                        unitsfrom = "square kilometers"
                elif areaFunction1 == "square mile":
                    area = amount / 0.00000000000038610
                    unitsfrom = "square miles"
                elif areaFunction1 == "acre":
                    area = amount / 0.00000000024711
                    unitsfrom = "acres"
                elif areaFunction1 == "hectare":
                    area = amount / 0.00000000010000
                    unitsfrom = "hectares"

            # now convert square millimeters to the area unit type
            if areaFunction2 == "square millimeters":
                answer = area
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "square millimetres"
                else:
                    unitsto = "square millimeters"
            elif areaFunction2 == "square meter":
                answer = area * 0.0000010000
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "square metres"
                else:
                    unitsto = "square meters"
            elif areaFunction2 == "square centimeter":
                answer = area * 0.010000
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "square centimetres"
                else:
                    unitsto = "square centimeters"
            elif areaFunction2 == "square inch":
                answer = area * 0.0015500
                unitsto = "square inches"
            elif areaFunction2 == "square feet":
                answer = area * 0.000010764
                unitsto = "square feet"
            elif areaFunction2 == "square yard":
                answer = area * 0.0000011960
                unitsto = "square yards"
            elif areaFunction2 == "square kilometer":
                answer = area * 0.0000000000010000
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "square kilometres"
                else:
                    unitsto = "square kilometers"
            elif areaFunction2 == "square mile":
                answer = area * 0.00000000000038610
                unitsto = "square miles"
            elif areaFunction2 == "acre":
                answer = area * 0.00000000024711
                unitsto = "acres"
            elif areaFunction2 == "hectare":
                answer = area * 0.00000000010000
                unitsto = "hectares"

            amount = util.number_to_words(amount)
            #amount = strip_end(p.number_to_words(float_to_str(amount))).strip()

            if "{:.3g}".format(answer) == "1":
                if unitsto == "square feet":
                    sayMessage = "{} {}, is one square foot".format(
                        amount, unitsfrom)
                elif unitsto == "cubic inches":
                    sayMessage = "{} {}, is one cubic inch".format(
                        amount, unitsfrom)
                else:
                    answer = util.number_to_words(answer)
                    #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                    sayMessage = "{} {}, is {} {}".format(
                        amount, unitsfrom, answer, unitsto[:-1])
            else:
                answer = util.number_to_words(answer)
                #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                sayMessage = "{} {}, is {} {}".format(
                    amount, unitsfrom, answer, unitsto)

    except Exception as e:
        print("Error in areaConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


def subscribe_intent_temperatureConverter(hermes, intentMessage):
    sayMessage = "Something has gone wrong, and I can not convert that temperature for you"

    try:
        tempFunction1 = intentMessage.slots.tempFunction1.first().value.lower()
        tempFunction2 = intentMessage.slots.tempFunction2.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if tempFunction1 and tempFunction2 and isinstance(amount, (int, float)):
            answer = 0
            unitsfrom = "celsius"
            unitsto = "celsius"

            if tempFunction1 == "c":
                # convert celsius to other temp value
                unitsfrom = "celsius"
                if tempFunction2 == "f":
                    answer = (amount * 1.8) + 32.00
                    unitsto = "fahrenheit"
                elif tempFunction2 == "kelvin":
                    answer = amount + 273.15
                    unitsto = "kelvin"
            elif tempFunction1 == "f":
                # convert Fahrenheit to other temp value
                unitsfrom = "fahrenheit"
                if tempFunction2 == "c":
                    answer = (amount - 32) / 1.8
                    unitsto = "celsius"
                elif tempFunction2 == "kelvin":
                    answer = ((amount-32)/1.8) + 273.15
                    unitsto = "kelvin"
            elif tempFunction1 == "kelvin":
                # convert Fahrenheit to other temp value
                unitsfrom = "kelvin"
                if tempFunction2 == "c":
                    answer = amount - 273.15
                    unitsto = "celsius"
                elif tempFunction2 == "f":
                    answer = ((amount - 273.15)*1.8) + 32.00
                    unitsto = "fahrenheit"
            amount = util.number_to_words(amount)
            answer = util.number_to_words(answer)
            #amount = strip_end(p.number_to_words(float_to_str(amount))).strip()
            #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
            sayMessage = "{} {} would be {} {}".format(
                amount, unitsfrom, answer, unitsto)

    except Exception as e:
        print("Error in temperatureConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


def subscribe_intent_volumeConverter(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    sayMessage = "Something might have gone wrong or I do not know how to convert that volume"

    try:
        volumeFunction1 = intentMessage.slots.volumeFunction1.first().value.lower()
        volumeFunction2 = intentMessage.slots.volumeFunction2.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if isinstance(amount, (int, float)):
            answer = 0
            volume = amount
            unitsfrom = "milliliter"
            unitsto = "milliliter"

            # convert the weight to lowest number (milliliter)
            if not volumeFunction1 == "milliliter":
                # we dont have to change the amount if it is already in milliliters
                if volumeFunction1 == "ounce":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.035195
                    else:
                        volume = amount / 0.033814
                    unitsfrom = "fluid onces"
                elif volumeFunction1 == "teaspoon":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.28156
                    else:
                        volume = amount / 0.20288
                    unitsfrom = "teaspoons"
                elif volumeFunction1 == "pint":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.00175986
                    else:
                        volume = amount / 0.0021134
                    unitsfrom = "pints"
                elif volumeFunction1 == "liter":
                    volume = amount / 0.0010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "litres"
                    else:
                        unitsfrom = "liters"
                elif volumeFunction1 == "centiliter":
                    volume = amount / 0.10000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "centilitres"
                    else:
                        unitsfrom = "centiliters"
                elif volumeFunction1 == "tablespoon":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.070390
                    else:
                        volume = amount / 0.067628
                    unitsfrom = "tablespoons"
                elif volumeFunction1 == "kiloliter":
                    volume = amount / 0.0000010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "kilolitres"
                    else:
                        unitsfrom = "kiloliters"
                elif volumeFunction1 == "cubic inch":
                    volume = amount / 0.061024
                    unitsfrom = "cubic inches"
                elif volumeFunction1 == "cup":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.0035211
                    else:
                        volume = amount / 0.0042268
                    unitsfrom = "cups"
                elif volumeFunction1 == "cubic meter":
                    volume = amount / 0.0000010000
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        unitsfrom = "cubic metres"
                    else:
                        unitsfrom = "cubic meters"
                elif volumeFunction1 == "cubic feet":
                    volume = amount / 0.000000035314662
                    unitsfrom = "cubic feet"
                elif volumeFunction1 == "quart":
                    if conf['global']['us_or_uk_metric'].lower() == "uk":
                        volume = amount / 0.00087988
                    else:
                        volume = amount / 0.0010567
                    unitsfrom = "quarts"

            # now convert milliliters to the volume type
            if volumeFunction2 == "milliliter":
                answer = volume
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "millilitres"
                else:
                    unitsto = "milliliters"
            elif volumeFunction2 == "teaspoon":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.28156
                else:
                    answer = volume * 0.20288
                unitsto = "teaspoons"
            elif volumeFunction2 == "pint":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.0017598
                else:
                    answer = volume * 0.0021134
                unitsto = "pints"
            elif volumeFunction2 == "liter":
                answer = volume / 1000.0
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "litres"
                else:
                    unitsto = "liters"
            elif volumeFunction2 == "centiliter":
                answer = volume / 10.000
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "centilitres"
                else:
                    unitsto = "cemtiliters"
            elif volumeFunction2 == "tablespoon":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.070390
                else:
                    answer = volume * 0.067628
                unitsto = "tablespoons"
            elif volumeFunction2 == "ounce":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.035195
                else:
                    answer = volume * 0.033814
                unitsto = "fluid ounces"
            elif volumeFunction2 == "kiloliter":
                answer = volume * 0.000000001
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "kilolitres"
                else:
                    unitsto = "kiloliters"
            elif volumeFunction2 == "cubic inch":
                answer = volume * 0.061024
                unitsto = "cubic inches"
            elif volumeFunction2 == "cup":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.0035211
                else:
                    answer = volume * 0.0042268
                unitsto = "cups"
            elif volumeFunction2 == "cubic meter":
                answer = volume * 0.000000001
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    unitsto = "cubic metres"
                else:
                    unitsto = "cubic meters"
            elif volumeFunction2 == "cubic feet":
                answer = volume * 0.000035315
                unitsto = "cubic feet"
            elif volumeFunction2 == "quart":
                if conf['global']['us_or_uk_metric'].lower() == "uk":
                    answer = volume * 0.00087988
                else:
                    answer = volume * 0.0010567
                unitsto = "quarts"

            amountStr = util.scientificnumber_to_str(amount)
            answerStr = util.scientificnumber_to_str(answer)

            if "{:.3g}".format(amount) == "1":
                unitsfrom = unitsfrom[:-1] if unitsfrom.endswith("s") else unitsfrom

            amount = util.number_to_words(amount)

            if "{:.3g}".format(answer) == "1":
                if unitsto == "cubic feet":
                    sayMessage = "{} {}, is one cubic foot".format(
                        amount, unitsfrom)
                elif unitsto == "cubic inches":
                    sayMessage = "{} {}, is one cubic inch".format(
                        amount, unitsfrom)
                else:
                    answer = util.number_to_words(answer)
                    #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                    sayMessage = "{} {}, is {} {}".format(
                        amount, unitsfrom, answer, unitsto[:-1])
                    unitsto = unitsto[:-1]
            else:
                answer = util.number_to_words(answer)
                #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                sayMessage = "{} {}, is {} {}".format(
                    amount, unitsfrom, answer, unitsto)

            
    except Exception as e:
        print("Error in volumeConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


def subscribe_intent_speedConverter(hermes, intentMessage):
    sayMessage = "I might not have heard that properly or I do not know how to convert that speed"

    try:
        speedFunction1 = intentMessage.slots.speedFunction1.first().value.lower()
        speedFunction2 = intentMessage.slots.speedFunction2.first().value.lower()
        speedUnitFrom = intentMessage.slots.speedUnitFrom.first().value.lower()
        speedUnitTo = intentMessage.slots.speedUnitTo.first().value.lower()
        amount = intentMessage.slots.amount.first().value

        if isinstance(amount, (int, float)):
            answer = 0
            length = amount
            unitsfrom = "meter"
            unitsto = "meter"

            answer, unitsfrom, unitsto = convert_lengths(
                amount, speedFunction1, speedFunction2)

            # covert per X to per Y
            if not speedUnitFrom == speedUnitTo:
                if speedUnitFrom == "per second":
                    if speedUnitTo == "per minute":
                        answer = answer * 60
                    elif speedUnitTo == "per hour":
                        answer = answer * 60 * 60
                    elif speedUnitTo == "per day":
                        answer = answer * 60 * 60 * 24
                elif speedUnitFrom == "per minute":
                    if speedUnitTo == "per second":
                        answer = answer / 60
                    elif speedUnitTo == "per hour":
                        answer = answer * 60
                    elif speedUnitTo == "per day":
                        answer = answer * 60 * 24
                elif speedUnitFrom == "per hour":
                    if speedUnitTo == "per second":
                        answer = answer / 3600
                    elif speedUnitTo == "per minute":
                        answer = answer / 60
                    elif speedUnitTo == "per day":
                        answer = answer * 24
                elif speedUnitFrom == "per day":
                    if speedUnitTo == "per second":
                        answer = answer / 86400
                    elif speedUnitTo == "per minute":
                        answer = answer / 1440
                    elif speedUnitTo == "per hour":
                        answer = answer / 24

            amountStr = util.scientificnumber_to_str(amount)
            answerStr = util.scientificnumber_to_str(answer)

            if "{:.1g}".format(answer) == "1" and not unitsto == "feet":
                if unitsto == "feet":
                    unitsto = "feet"
                    sayMessage = "{} {} {}, is one foot {}".format(
                        amount, unitsfrom, speedUnitFrom, speedUnitTo)
                else:
                    sayMessage = "{} {} {}, is one {} {}".format(
                        amount, unitsfrom, speedUnitFrom, unitsto[:-1], speedUnitTo)
                    unitsto == unitsto[:-1]
            else:
                amount = util.number_to_words(amount)
                answer = util.number_to_words(answer, 1)
                #amount = strip_end(p.number_to_words(float_to_str(amount))).strip()
                #answer = strip_end(p.number_to_words(float_to_str(answer))).strip()
                sayMessage = "{} {} {}, is {} {} {}".format(
                    amount, unitsfrom, speedUnitFrom, answer, unitsto, speedUnitTo)

            
    except Exception as e:
        print("Error in speedConverter Snippet: {}".format(e))

    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, sayMessage)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("ozie:weightConverter",       subscribe_intent_weightConverter) \
            .subscribe_intent("ozie:lengthConverter",       subscribe_intent_lengthConverter) \
            .subscribe_intent("ozie:currencyConverter",     subscribe_intent_currencyConverter) \
            .subscribe_intent("ozie:mathsQuestion",         subscribe_intent_mathsQuestion) \
            .subscribe_intent("ozie:areaFunction",          subscribe_intent_areaFunction) \
            .subscribe_intent("ozie:temperatureConverter",  subscribe_intent_temperatureConverter) \
            .subscribe_intent("ozie:volumeConverter",       subscribe_intent_volumeConverter) \
            .subscribe_intent("ozie:speedConverter",        subscribe_intent_speedConverter) \
            .loop_forever()

