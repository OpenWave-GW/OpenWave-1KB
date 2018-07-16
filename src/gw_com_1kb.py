# -*- coding: utf-8 -*-
"""
Module name: gw_com_1kb

Copyright:
----------------------------------------------------------------------
gw_com_1kb is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.

This program is free software; you can redistribute it and/or modify it under the terms 
of the GNU Lesser General Public License as published by the Free Software Foundation; 
either version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Lesser General Public License for more details.

You can receive a copy of the GNU Lesser General Public License from 
http://www.gnu.org/

Note:
gw_com_1kb uses third party software which is copyrighted by its respective copyright holder. 
For details see the copyright notice of the individual package.

----------------------------------------------------------------------
Description:
gw_com_1kb is a python USB interface module used to connect and read/write data from/to DSO.

Module imported:
  1. PySerial 2.7

Version: 1.00

Created on JUL 16 2018

Author: Kevin Meng
"""
import time
import serial
from serial.tools import list_ports

#usb_id={'2184' : ['003f', '0040', '0041', '0042'], '098f' : ['2204']}  #USB VID/PID for GDS-2000E/MSO-2000E/MDO-2000E/DCS-2000E/IDS-2000E
usb_id={'2184' : ['0043', '0044', '0045', '0046'], '098f' : ['2205']}  #USB VID/PID for GDS-1000B/DCS-1000B/IDS-1000B/DSO-1000D

class com:
    def __init__(self, port):
        try:
            self.IO = serial.Serial(port, baudrate=38400, bytesize=8, parity ='N', stopbits=1, xonxoff=False, dsrdtr=False, timeout=5)
        except serial.SerialException, e:
            print e.message
            raise Exception,'__init__(), open port failed!'

    def write(self, str):
        try:
            self.IO.write(str)
        except serial.SerialException, e:
            print "write(), %s" % e
        
    def read(self):
        try:
            return self.IO.readline()
        except serial.SerialException, e:
            print "read(), %s" % e
            return ''
        
    def readBytes(self, length):
        try:
            str=self.IO.read(length)
            return str
        except serial.SerialException, e:
            print "readBytes(), %s" % e
            return ''
    
    def clearBuf(self):
        time.sleep(0.5)
        while(True):
            num=self.IO.inWaiting()
            if(num==0):
                break
            else:
                print '-',
            self.IO.flushInput()    #Clear input buffer.
            time.sleep(0.1)
    
    def closeIO(self):
        self.IO.close()
    
    @classmethod
    def connection_test(self, port):
        try:
            __port = serial.Serial(port, baudrate=38400, bytesize=8, parity ='N', stopbits=1, xonxoff=False, dsrdtr=False, timeout=5)
            __port.close()
            return port
        except serial.SerialException, e:
            print e.message
            return ''

    @classmethod
    def scanComPort(self):
        port_list=list(list_ports.comports())
        num=len(port_list)
        #print 'num=', num
        for i in xrange(num):
            str=port_list[i][2].split('=')
            #print str
            if(str[0]=='USB VID:PID'):
                str=str[1].split(' ')[0] #Extract VID and PID from string.
                str=str.split(':')
                print str
                if(str[0] in usb_id):
                    if(str[1].lower() in usb_id[str[0]]):
                        port=port_list[i][0]
                        try:
                            __port = serial.Serial(port, baudrate=38400, bytesize=8, parity ='N', stopbits=1, xonxoff=False, dsrdtr=False, timeout=5)
                        except serial.SerialException, e:
                            print e.message
                            continue
                        time.sleep(0.5)
                        while(True):
                            num=__port.inWaiting()
                            if(num==0):
                                break
                            else:
                                print '-',
                            __port.flushInput()  #Clear input buffer.
                            time.sleep(0.1)
                        __port.close()
                        return port
        print('Device not found!')
        return ''
