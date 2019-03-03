#!/usr/bin/env python3
# -*- coding:utf-8 -*-

### **************************************************************************** ###
# 
# Project: Snips Screen Project
# Created Date: Sunday, February 10th 2019, 10:06:44 pm
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




import json
import paho.mqtt.publish as publish



TOPIC = "snipsscreen/display" #MQTT topic to publish to which the screen is subscribed to

class SnipsScreenPublisher:
    """Published information to display on the Snips Screen Application"""

    def __init__(self, mqttHost="localhost", mqttPort=1883, username=None, password=None):
        """Class INIT
        
        Keyword Arguments:
            mqttHost {str} -- MQTT Host (default: {"localhost"})
            mqttPort {int} -- MQTT Port (default: {1883})
            username {str} -- MQTT Connection Username (default: {None})
            password {str} -- MQTT COnnection Password (default: {None})
        """
        self.mqttHost = mqttHost
        self.mqttPort = mqttPort
        self.Auth = None
        if username:
            self.Auth = {'username':username, 'password':password}


    def publish(self, htmlString=''):
        """Publish MQTT - HTML code for the screen to display
        
        Keyword Arguments:
            htmlString {str} -- HTML code that the screen displays (default: {''})
        """
        publish.single(TOPIC, payload=htmlString.encode('base64', 'strict'), 
                                qos=0, 
                                retain=False, 
                                hostname=self.mqttHost,
                                port=int(self.mqttPort), 
                                client_id="", 
                                keepalive=60, 
                                will=None, 
                                auth=self.Auth,
                                tls=None, 
                                protocol=publish.paho.MQTTv31)
