# -*- coding: utf-8 -*-
"""
Program name: OpenWave-1KB

Copyright:
----------------------------------------------------------------------
OpenWave-1KB is Copyright (c) 2015 Good Will Instrument Co., Ltd All Rights Reserved.

This program is free software; you can redistribute it and/or modify it under the terms 
of the GNU Lesser General Public License as published by the Free Software Foundation; 
either version 2.1 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You can receive a copy of the GNU Lesser General Public License from http://www.gnu.org/

Note:
OpenWave-1KB uses third party software which is copyrighted by its respective copyright 
holder. For details see the copyright notice of the individual package.

The Qt GUI Toolkit is Copyright (c) 2014 Digia Plc and/or its subsidiary(-ies).
OpenWave-1KB use Qt version 4.8 library under the terms of the LGPL version 2.1.
----------------------------------------------------------------------
Description:
OpenWave-1KB is a python example program used to get waveform and image from DSO.

Environment:
  1. Python 2.7.9
  2. dso1kb 1.01
  3. gw_com_1kb 1.00
  4. gw_lan 1.00
  5. PySerial 2.7
  6. Matplotlib 1.3.1
  7. Numpy 1.8.0
  8. PySide 1.2.1
  9. PIL 1.1.7

Version: 1.03

Modified on APR 01 2020

Author: Kevin Meng
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['backend.qt4'] = 'PySide'  #Used for PySide.
mpl.rcParams['agg.path.chunksize'] = 100000 #For big data.
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
from PySide import QtCore, QtGui
import numpy as np
from PIL import Image
import os, sys, time
from gw_com_1kb import com
from gw_lan import lan
import dso1kb

__version__ = "1.03" #OpenWave-1KB software version.

def checkInterface(str):
    if str!= '':
        print str
    #Load config file if it exists
    elif os.path.exists('port.config'):
        f = open('port.config', 'r')
        while(1):
            str = f.readline()
            if(str == ''):
                f.close()
                return ''
            if(str[0] != '#'):
                break
        f.close()
       
    #Check ethernet connection(model name not checked)
    sInterface=str.split('\n')[0]
    #print 'sInterface=',sInterface
    if(sInterface.count('.') == 3 and sInterface.count(':') == 1): #Got ip address.
        ip_str=sInterface.split(':')
        ip=ip_str[0].split('.')
        if(ip_str[1].isdigit() and ip[0].isdigit() and ip[1].isdigit() and ip[2].isdigit() and ip[3].isdigit()):
            #print('ip addr=%s.%s.%s.%s:%s'%(ip[0],ip[1],ip[2],ip[3],ip_str[1]))
            str=lan.connection_test(sInterface)
            if(str != ''):
                return str
    #Check COM port connection(model name not checked)
    elif('COM' in sInterface):
        if(com.connection_test(sInterface) != ''):
            return sInterface
    elif('ttyACM' in sInterface):
        if 'ttyACM' == sInterface[0:6]:
            sInterface='/dev/'+sInterface
        if(com.connection_test(sInterface) != ''):
            return sInterface
    
    return com.scanComPort()  #Scan all the USB port.

class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setWindowTitle('OpenWave-1KB V%s'%__version__)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("openwave.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        #Waveform area.
        self.figure = plt.figure()
        self.figure.set_facecolor('white')

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumSize(800,  400)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()

        #Zoom In/out and Capture Buttons
        self.zoomBtn = QtGui.QPushButton('Zoom')
        self.zoomBtn.setFixedSize(100, 30)
        self.zoomBtn.clicked.connect(self.toolbar.zoom)

        self.panBtn = QtGui.QPushButton('Pan')
        self.panBtn.setFixedSize(100, 30)
        self.panBtn.clicked.connect(self.toolbar.pan)

        self.homeBtn = QtGui.QPushButton('Home')
        self.homeBtn.setFixedSize(100, 30)
        self.homeBtn.clicked.connect(self.toolbar.home)

        self.captureBtn = QtGui.QPushButton('Capture')
        self.captureBtn.setFixedSize(100, 50)
        self.captureBtn.clicked.connect(self.manualCapture)
        if(dso.connection_status==0):
            self.captureBtn.setEnabled(False)
            
        self.continuousBtn = QtGui.QRadioButton('Continuous')
        self.continuousBtn.setEnabled(True)
        self.continuousBtn.clicked.connect(self.setContinuous)

        #Continuous capture selection
        self.captureLayout = QtGui.QHBoxLayout()
        self.captureLayout.addWidget(self.captureBtn)
        self.captureLayout.addWidget(self.continuousBtn)

        #Type: Raw Data/Image
        self.typeBtn = QtGui.QPushButton('Raw Data')
        self.typeBtn.setToolTip("Switch to get raw data or image from DSO.")
        self.typeBtn.setFixedSize(120, 50)
        self.typeFlag=True #Initial state -> Get raw data
        self.typeBtn.setCheckable(True)
        self.typeBtn.setChecked(True)
        self.typeBtn.clicked.connect(self.typeAction)
        
        #Channel Selection.
        self.ch1checkBox = QtGui.QCheckBox('CH1')
        self.ch1checkBox.setFixedSize(60, 30)
        self.ch1checkBox.setChecked(True)
        self.ch2checkBox = QtGui.QCheckBox('CH2')
        self.ch2checkBox.setFixedSize(60, 30)
        if(dso.chnum==4):
            self.ch3checkBox = QtGui.QCheckBox('CH3')
            self.ch3checkBox.setFixedSize(60, 30)
            self.ch4checkBox = QtGui.QCheckBox('CH4')
            self.ch4checkBox.setFixedSize(60, 30)
        
        #Set channel selection layout.
        self.selectLayout = QtGui.QHBoxLayout()
        self.selectLayout.addWidget(self.ch1checkBox)
        self.selectLayout.addWidget(self.ch2checkBox)
        if(dso.chnum==4):
            self.selectLayout2 = QtGui.QHBoxLayout()
            self.selectLayout2.addWidget(self.ch3checkBox)
            self.selectLayout2.addWidget(self.ch4checkBox)

        self.typeLayout = QtGui.QHBoxLayout()
        self.typeLayout.addWidget(self.typeBtn)
        self.typeLayout.addLayout(self.selectLayout)
        if(dso.chnum==4):
            self.typeLayout.addLayout(self.selectLayout2)

        self.zoominoutLayout = QtGui.QHBoxLayout()
        self.zoominoutLayout.addWidget(self.zoomBtn)
        self.zoominoutLayout.addWidget(self.panBtn)
        self.zoominoutLayout.addWidget(self.homeBtn)

        #Save/Load/Quit button
        self.saveBtn = QtGui.QPushButton('Save')
        self.saveBtn.setFixedSize(100, 50)
        self.saveMenu = QtGui.QMenu(self)
        self.csvAction = self.saveMenu.addAction("&As CSV File")
        self.pictAction = self.saveMenu.addAction("&As PNG File")
        self.saveBtn.setMenu(self.saveMenu)
        self.saveBtn.setToolTip("Save waveform to CSV file or PNG file.")
        self.connect(self.csvAction, QtCore.SIGNAL("triggered()"), self.saveCsvAction)
        self.connect(self.pictAction, QtCore.SIGNAL("triggered()"), self.savePngAction)

        self.loadBtn = QtGui.QPushButton('Load')
        self.loadBtn.setToolTip("Load CHx's raw data from file(*.csv, *.lsf).")
        self.loadBtn.setFixedSize(100, 50)
        self.loadBtn.clicked.connect(self.loadAction)

        self.quitBtn = QtGui.QPushButton('Quit')
        self.quitBtn.setFixedSize(100, 50)
        self.quitBtn.clicked.connect(self.quitAction)

        # set the layout
        self.waveLayout = QtGui.QHBoxLayout()
        self.waveLayout.addWidget(self.canvas)
        
        self.wave_box=QtGui.QVBoxLayout()
        self.wave_box.addLayout(self.waveLayout)
        
        self.wavectrlLayout = QtGui.QHBoxLayout()
        self.wavectrlLayout.addStretch(1)
        self.wavectrlLayout.addLayout(self.zoominoutLayout)
        self.wavectrlLayout.addStretch(1)
        self.wavectrlLayout.addLayout(self.captureLayout)
        self.wavectrlLayout.addStretch(1)
        
        self.saveloadLayout = QtGui.QHBoxLayout()
        self.saveloadLayout.addWidget(self.saveBtn)
        self.saveloadLayout.addWidget(self.loadBtn)
        self.saveloadLayout.addWidget(self.quitBtn)
        
        self.ctrl_box=QtGui.QHBoxLayout()
        self.ctrl_box.addLayout(self.typeLayout)
        self.ctrl_box.addLayout(self.saveloadLayout)
        
        main_box=QtGui.QVBoxLayout()
        main_box.addLayout(self.wave_box)         #Waveform area.
        main_box.addLayout(self.wavectrlLayout)   #Zoom In/Out...
        main_box.addLayout(self.ctrl_box)         #Save/Load/Quit
        self.setLayout(main_box)
        
        self.captured_flag=0
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.timerCapture)

    def typeAction(self):
        if(self.typeFlag==True):
            self.typeFlag=False
            self.typeBtn.setText("Image")
            self.csvAction.setEnabled(False)
        else:
            self.typeFlag=True
            self.typeBtn.setText("Raw Data")
            self.csvAction.setEnabled(True)
        self.typeBtn.setChecked(self.typeFlag)
        self.ch1checkBox.setEnabled(self.typeFlag)
        self.ch2checkBox.setEnabled(self.typeFlag)
        if(dso.chnum==4):
            self.ch3checkBox.setEnabled(self.typeFlag)
            self.ch4checkBox.setEnabled(self.typeFlag)

    def saveCsvAction(self):
        if(self.typeFlag==True): #Save raw data to csv file.
            file_name=QtGui.QFileDialog.getSaveFileName(self, "Save as", 'DS0001', "Fast CSV File(*.csv)")[0]
            num=len(dso.ch_list)
            #print num
            for ch in xrange(num):
                if(dso.info[ch]==[]):
                    print('Failed to save data, raw data information is required!')
                    return
            f = open(file_name, 'wb')
            item=len(dso.info[0])
            #Write file header.
            f.write('%s,\r\n' % dso.info[0][0])
            for x in xrange(1,  23):
                str=''
                for ch in xrange(num):
                    str+=('%s,' % dso.info[ch][x])
                str+='\r\n'
                f.write(str)
            #Write Fast CSV mode only.
            str=''
            for ch in xrange(num):
                str+='Mode,Fast,'
            str+='\r\n'
            f.write(str)

            str=''
            if(num==1):
                str+=('%s,' % dso.info[0][24])
            else:
                for ch in xrange(num):
                    str+=('%s,,' % dso.info[ch][24])
            str+='\r\n'
            f.write(str)
            #Write raw data.
            item=len(dso.iWave[0])
            #print item
            tenth=int(item/10)
            n_tenth=tenth-1
            percent=10
            for x in xrange(item):
                str=''
                if(num==1):
                    str+=('%s,' % dso.iWave[0][x])
                else:
                    for ch in xrange(num):
                        str+=('%s, ,' % dso.iWave[ch][x])
                str+='\r\n'
                f.write(str)
                if(x==n_tenth):
                    n_tenth+=tenth
                    print('%3d %% Saved\r'%percent),
                    percent+=10
            f.close()

    def savePngAction(self):
        #Save figure to png file.
        file_name=QtGui.QFileDialog.getSaveFileName(self, "Save as", 'DS0001', "PNG File(*.png)")[0]
        if(file_name==''):
            return
        if(self.typeFlag==True): #Save raw data waveform as png file.
            main.figure.savefig(file_name)
        else:  #Save figure to png file.
            if(dso.osname=='pi'): #For raspberry pi only.
                img=dso.im.transpose(Image.FLIP_TOP_BOTTOM)
                img.save(file_name)
            else:
                dso.im.save(file_name)
        print('Saved image to %s.'%file_name)

    def loadAction(self):
        dso.ch_list=[]
        full_path_name=QtGui.QFileDialog.getOpenFileName(self,self.tr("Open File"),".","CSV/LSF files (*.csv *.lsf);;All files (*.*)")  
        sFileName=unicode(full_path_name).split(',')[0][3:-1] #For PySide
        print sFileName
        if(len(sFileName)<=0):
            return
        if os.path.exists(sFileName):
            print 'Reading file...'
            count=dso.readRawDataFile(sFileName)
            #Draw waveform.
            if(count>0):
                total_chnum=len(dso.ch_list)
                if(total_chnum==0):
                    return
                self.drawWaveform(0)
        else:
            print('File not found!')

    def quitAction(self):
        if(dso.connection_status==1):
            dso.closeIO()
        self.close()
    
    def timerCapture(self):
        self.captureAction()
        if(self.continuousBtn.isChecked()==True):
            self.timer.start(10)  #Automatic capturing. 
        
    def manualCapture(self):
        if(self.continuousBtn.isChecked()==True):
            if(self.captured_flag ==0):
                self.captured_flag = 1   #Continuous capture started.
                self.captureBtn.setText("Click to Stop")
                self.loadBtn.setEnabled(False)
                self.timer.start()
            else:
                self.captured_flag = 0   #Continuous capture stopped.
                self.captureBtn.setText("Capture")
                self.loadBtn.setEnabled(True)
                self.timer.stop()
        self.captureAction()
    
    def captureAction(self):
        dso.iWave=[[], [], [], []]
        dso.ch_list=[]
        if(self.typeFlag==True): #Get raw data.
            draw_flag=False
            #Turn on the selected channels.
            if((self.ch1checkBox.isChecked()==True) and (dso.isChannelOn(1)==False)):
                dso.write(":CHAN1:DISP ON\n")           #Set CH1 on.
            if((self.ch2checkBox.isChecked()==True) and (dso.isChannelOn(2)==False)):
                dso.write(":CHAN2:DISP ON\n")           #Set CH2 on.
            if(dso.chnum==4):
                if((self.ch3checkBox.isChecked()==True) and (dso.isChannelOn(3)==False)):
                    dso.write(":CHAN3:DISP ON\n")       #Set CH3 on.
                if((self.ch4checkBox.isChecked()==True) and (dso.isChannelOn(4)==False)):
                    dso.write(":CHAN4:DISP ON\n")       #Set CH4 on.
            #Get all the selected channel's raw datas.
            if(self.ch1checkBox.isChecked()==True):
                dso.getRawData(True, 1)              #Read CH1's raw data from DSO (including header).
            if(self.ch2checkBox.isChecked()==True):
                dso.getRawData(True, 2)              #Read CH2's raw data from DSO (including header).
            if(dso.chnum==4):
                if(self.ch3checkBox.isChecked()==True):
                    dso.getRawData(True, 3)          #Read CH3's raw data from DSO (including header).
                if(self.ch4checkBox.isChecked()==True):
                    dso.getRawData(True, 4)          #Read CH4's raw data from DSO (including header).
            #Draw waveform.
            total_chnum=len(dso.ch_list)
            if(total_chnum==0):
                return
            if(self.drawWaveform(1)==-1):
                time.sleep(5)
                self.drawWaveform(0)
        else: #Get image.
            img_type=1   #1 for RLE format, 0 for PNG format.
            if(img_type):
                dso.write(':DISP:OUTP?\n')                 #Send command to get image from DSO.
            else:
                dso.write(':DISP:PNGOutput?\n')            #Send command to get image from DSO.
            dso.getBlockData()
            dso.ImageDecode(img_type)
            self.showImage()
            plt.tight_layout(True)
            self.canvas.draw()
            print('Image is ready!')

    def setContinuous(self):
        if(self.continuousBtn.isChecked()==False):
            self.captured_flag = 0   #Continuous capture stopped.
            self.timer.stop()
            self.loadBtn.setEnabled(True)
            self.captureBtn.setText("Capture")

    def showImage(self):
        #Turn the ticks off and show image.
        plt.clf()
        ax = plt.gca()
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        plt.imshow(dso.im)

    def drawWaveform(self, mode):
        total_chnum=len(dso.ch_list)
        num=dso.points_num
        ch_colortable=['#C0B020',  '#0060FF',  '#FF0080',  '#00FF60']
        ch=int(dso.ch_list[0][2])-1 #Get the channel of first waveform.
        plt.cla()
        plt.clf()
        #Due to the memory limitation of matplotlib, we must reduce the sample points.
        if(num==10000000):
            if(total_chnum>2):
                down_sample_factor=4
            elif(total_chnum==2):
                down_sample_factor=4
            else:
                down_sample_factor=1
            num=num/down_sample_factor
        else:
            down_sample_factor=1
        dt=dso.dt[0] #Get dt from the first opened channel.
        t_start=dso.hpos[0]-num*dt/2
        t_end  =dso.hpos[0]+num*dt/2
        t = np.arange(t_start, t_end, dt)
        #print t_start, t_end, dt, len(t)
        if((len(t)-num)==1): #Avoid floating point rounding error.
            t=t[:-1]
        wave_type='-' #Set waveform type to vector.
        #Draw waveforms.
        ax=[[], [], [], []]
        p=[]
        for ch in xrange(total_chnum):
            if(ch==0):
                ax[ch]=host_subplot(111, axes_class=AA.Axes)
                ax[ch].set_xlabel("Time (sec)")
            else:
                ax[ch]=ax[0].twinx()
            ax[ch].set_ylabel("%s Units: %s" %(dso.ch_list[ch],  dso.vunit[ch]))
            ch_color=ch_colortable[int(dso.ch_list[ch][2])-1]
            if(ch>1):
                new_fixed_axis = ax[ch].get_grid_helper().new_fixed_axis
                ax[ch].axis["right"] = new_fixed_axis(loc="right", axes=ax[ch], offset=(60*(ch-1), 0))
            ax[ch].set_xlim(t_start, t_end)
            ax[ch].set_ylim(-4*dso.vdiv[ch]-dso.vpos[ch], 4*dso.vdiv[ch]-dso.vpos[ch]) #Setup vertical display range.
            fwave=dso.convertWaveform(ch, down_sample_factor)
            #print('Length=%d'%(len(fwave)))
            if(ch==0):
                try:
                    p=ax[ch].plot(t, fwave, color=ch_color, ls=wave_type, label = dso.ch_list[ch])
                except:
                    if(mode==1):
                        #print sys.exc_info()[0]
                        time.sleep(5)
                        print 'Trying to plot again!',
                    return -1
            else:
                try:
                    p+=ax[ch].plot(t, fwave, color=ch_color, ls=wave_type, label = dso.ch_list[ch])
                except:
                    if(mode==1):
                        #print sys.exc_info()[0]
                        time.sleep(5)
                        print 'Trying to plot again!',
                    return -1
        if(total_chnum>1):
            labs = [l.get_label() for l in p]
            plt.legend(p, labs,   loc='upper right')
        plt.tight_layout() 
        self.canvas.draw()
        del ax, t, p
        return 0

if __name__ == '__main__':

    f = open('license.txt', 'r')
    print('-----------------------------------------------------------------------------');
    print f.read()
    f.close()
    print('-----------------------------------------------------------------------------');
    print('OpenWave-1KB V%s\n'% __version__)

    #Get command line arguments.
    cmd=sys.argv[-1]
    if('OpenWave' in cmd):
        cmd=''
    
    #Check interface according to config file or command line argument.
    port=checkInterface(cmd)
    
    #Connecting to a DSO.
    dso=dso1kb.Dso(port)

    app = QtGui.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())
