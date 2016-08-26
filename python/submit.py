#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is free and unencumbered software released into the public domain.
# 
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
# 
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# 
# For more information, please refer to <http://unlicense.org>
# 

import numpy
from gnuradio import gr
import pmt
import array
import binascii
import datetime
import urllib

class submit(gr.basic_block):
    """
    docstring for block submit
    """
    def __init__(self, url, noradID, source, longitude, latitude, initialTimestamp):
        gr.basic_block.__init__(self,
            name="submit",
            in_sig=[],
            out_sig=[])

        self.url = url
        self.request = { 'noradID': noradID,\
                         'source': source,\
                         'locator': 'longLat',\
                         'longitude': str(abs(longitude)) + ('E' if longitude >= 0 else 'W'),\
                         'latitude': str(abs(latitude)) + ('N' if latitude >= 0 else 'S'),\
                         'version': '1.6.6' }
        dtformat = '%Y-%m-%d %H:%M:%S'
        self.initialTimestamp = datetime.datetime.strptime(initialTimestamp, dtformat) \
            if initialTimestamp != '' else None
        self.startTimestamp = datetime.datetime.utcnow()
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        

    def handle_msg(self, msg_pmt):
        # check that callsign and QTH have been entered
        if self.request['source'] == '':
            return
        if self.request['longitude'] == 0.0 and self.request['latitude'] == 0.0:
            return

        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return

        self.request['frame'] = \
          binascii.b2a_hex(str(bytearray(pmt.u8vector_elements(msg)))).upper()
        
        now = datetime.datetime.utcnow()
        timestamp = now - self.startTimestamp + self.initialTimestamp \
          if self.initialTimestamp else now
        self.request['timestamp'] = timestamp.isoformat()[:-3] + 'Z'

        params = urllib.urlencode(self.request)
        f = urllib.urlopen('{}?{}'.format(self.url, params), data=params)
        reply = f.read()
        if f.getcode() != 200:
            print "Server error while submitting telemetry:"
            print reply
        f.close()
        
