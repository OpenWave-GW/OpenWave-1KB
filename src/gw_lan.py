# -*- coding: utf-8 -*-
"""
Module name: gw_lan

Copyright:
----------------------------------------------------------------------
gw_lan is Copyright (c) 2014 Good Will Instrument Co., Ltd All Rights Reserved.

This program is free software; you can redistribute it and/or modify it under the terms 
of the GNU Lesser General Public License as published by the Free Software Foundation; 
either version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Lesser General Public License for more details.

You can receive a copy of the GNU Lesser General Public License from 
http://www.gnu.org/

Note:
gw_lan uses third party software which is copyrighted by its respective copyright holder. 
For details see the copyright notice of the individual package.

----------------------------------------------------------------------
Description:
gw_lan is a python Ethernet interface module used to connect and read/write data from/to DSO.

Version: 1.00

Created on JUN 28 2018

Author: Kevin Meng
"""
import socket


class lan:
    def __init__(self, str):
        ip_str=str.split(':')
        ip=ip_str[0].split('.')
        if(ip_str[1].isdigit() and ip[0].isdigit() and ip[1].isdigit() and ip[2].isdigit() and ip[3].isdigit()):
            self.IO = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.IO.settimeout(5) #Set timeout
            try:
                self.IO.connect((ip_str[0], int(ip_str[1])))
            except socket.error, e:
                print "__init__(), socket error: %s" % e
        else:
            raise Exception,'Open port error!'
    
    def write(self, str):
        try:
            self.IO.sendall(str)
        except socket.error, e:
            print "write(), socket error: %s" % e
        
    def read(self):
        line_buf=''
        while True:
            try:
                a=self.IO.recv(1)
            except socket.error, e:
                print "read(), socket error: %s" % e
                return line_buf
            line_buf+=a
            if(a=='\n'):
                return line_buf
    
    def readBytes(self, length):
        str=''
        try:
            str=self.IO.recv(length)
        except socket.error, e:
            print "readBytes(), socket error: %s" % e
        return str
    
    def clearBuf(self):
        pass
        
    def closeIO(self):
        self.IO.close()
    
    @classmethod
    def connection_test(self, str):
        ip_str=str.split(':')
        ip=ip_str[0].split('.')
        if(ip_str[1].isdigit() and ip[0].isdigit() and ip[1].isdigit() and ip[2].isdigit() and ip[3].isdigit()):
            __port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __port.settimeout(2) #2 Second Timeout
            try:
                __port.connect((ip_str[0], int(ip_str[1])))
            except socket.error, e:
                print "Socket error: %s" % e
                return ''
            __port.close()
            return str
        else:
            return ''