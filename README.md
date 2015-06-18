![Python logo](/image/python-logo.png)

This is a Python program.




OpenWave-1KB
============
![GetImage](/image/OpenWave256x256.jpg)

This icon is copyright 2015 (c) Good Will Instrument Co., Ltd all rights reserved.




OpenWave-1KB is an open-source project. It's a simple python program that can get image or raw data from digital storage oscilloscope(GDS-1000B) via the USB port.  

Now we can execute the same source code on Windows, Linux(Ubuntu) and Raspbian(on Raspberry Pi 2) operating system without changing a word.


Equipment
------------
You have to get a new digital storage oscilloscope - GDS-1000B(GOOD WILL INSTRUMENT) and a PC or NB with MS Windows or Ubuntu Linux OS or a Raspberry Pi 2 single board computer.




Environment
------------
Currently OpenWave-1KB may be executed on Windows XP/7/8 32 or 64 bits OS. You have to download and install the USB driver(dso_vpo V1.08) from [www.gwinstek.com](http://www.gwinstek.com) or [here](/dso_vpo_v108.zip) when the first connection with GDS-1000B. 

Please unzip the [OpenWave-1KB V1.00.zip](/OpenWave-1KB V1.00.zip) and find the OpenWave-1KB.exe in the folder. OpenWave-1KB.exe can be executed directly without installation.

The OpenWave-1KB source code can also be executed on Ubuntu 32 bits Linux OS or Raspbian OS(on Raspberry Pi 2). The USB driver is not required in this environment.


Development Tools
------------
- **Packages:**
   If you want to modify the source code and run the program by yourself. You have to install the development tools and packages as following:
   * Python 2.7.6
   * PySerial 2.7
   * Matplotlib 1.3.1
   * Numpy 1.8.0
   * PIL 1.1.7
   * PySide 1.2.1
   * dateutil 2.2
   * pyparsing 2.0.1
   * six 1.4.1

 *OpenWave-1KB is developed under Windows 32 bits environment, and all the packages are Windows 32bits version.*
 
- **Ubuntu Linux:**
   OpenWave-1KB is also tested under Ubuntu 10.04 (32 bits) with the same version of the packages listed above.  And the following package and libraries are required:*
   * nose-1.3.4
   * qt4-qmake
   * libqt4-dev

- **Raspbian Linux:**
   OpenWave-1KB is also tested on Raspberry Pi 2 with following package and libraries:
   * python-matplotlib
   * python-numpy
   * python-scipy
   * libatlas-base-dev
   * gfortran
   * python-pip
   * scipy
   * Pillow
   * python-pyside
   * python-serial
   * pyserial


- **Python IDE:**
   If you need a Python IDE tool, Eric4 4.5.19  is recommended:


- **Executable File:**
   If you want to convert python program into stand-alone executables under Windows. The following packages are required:
   * PyInstaller 2.1
   * pywin32 218.4



   
Screenshot
------------
**Get image:**
![GetImage](/image/pic1.png)


**Get raw data:**
![GetRawData](/image/pic2.png)


**Screenshot -- Win 7:**
![MS Windows](/image/Win7_Screenshot.png)


**Screenshot -- Ubuntu Linux:**
![Ubuntu Linux](/image/Ubuntu1004_Screenshot.png)


**Screenshot -- Raspbian on Raspberry Pi 2:**
![Raspbian Linux](/image/Raspbian_Screenshot.png)
