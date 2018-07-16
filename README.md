![Python logo](/image/python-logo.png)

This is a Python program.




OpenWave-1KB
============
![GetImage](/image/OpenWave256x256.jpg)

This icon is copyright by Good Will Instrument Co., Ltd all rights reserved.




OpenWave-1KB is an open-source project. It's a simple python program that can get image or raw data from digital storage oscilloscope(GDS-1000B/DCS-1000B/IDS-1000B/DSO-1000D series) via USB port or Ethernet.  

Users can execute the same source code on Windows, Linux(Ubuntu) and Raspbian(on Raspberry Pi 2) operating system without changing a word. By using this version, users can also create multiple DSO connections at the same time.


Equipment
------------
You have to get a new digital storage oscilloscope - GDS-1000B, GDS-1000R(GOOD WILL INSTRUMENT)/DCS-1000B(TEXIO)/IDS-1000B(RS PRO)/DSO-1000D(CONRAD) and a PC or NB with MS Windows OS.




Environment
------------
Currently OpenWave-1KB may be executed on Windows XP/7/8 32 or 64 bits OS. We also tested the program on Win 10, the connection is good but can't guarantee to be 100% no problem on different platforms. You have to download and install the USB driver(dso_vpo V1.08) from [www.gwinstek.com](http://www.gwinstek.com) or [here](/dso_vpo_v108.zip) when the first connection with GDS-1000B. 

Please unzip the [OpenWave-1KB V1.01.zip](/OpenWave-1KB_V1.01.zip) and find the OpenWave-1KB.exe in the folder. OpenWave-1KB.exe can be executed directly without installation. Please be noticed that the path name and folder name can't be double-byte characters.

The OpenWave-1KB source code can also be executed on Ubuntu 32 bits Linux OS or Raspbian OS(on Raspberry Pi 2). The USB driver is not required in this environment.



Command Line Execution
------------
- **Windows Example:**

1.  Connected via USB(please find the port number in the Device Manager)
    ```
    D:\OpenWave-1KB V1.01>OpenWave-1KB COM5
    ```

2.  Connected via USB(automatically reading config file or scanning port)
    ```
    D:\OpenWave-1KB V1.01>OpenWave-1KB
    ```

3.  Connected via Ethernet:
    ```
    D:\OpenWave-1KB V1.01>OpenWave-1KB 172.16.5.12:3000
    ```


- **Linux(or Raspbian) Example:**

1.  Connected via USB(please find the device under /dev)
    ```
    user@Ubuntu:~/workspace_python/OpenWave-1KB V1.01$ sudo python OpenWave-1KB.py ttyACM1
    ```
    
2.  Connected via USB(automatically reading config file or scanning port)
    ```
    user@Ubuntu:~/workspace_python/OpenWave-1KB V1.01$ sudo python OpenWave-1KB.py
    ```
    
3.  Connected via Ethernet:
    ```
    user@Ubuntu:~/workspace_python/OpenWave-1KB V1.01$ sudo python OpenWave-1KB.py 172.16.5.12:3000
    ```

***Tips:***

1.  *If you want to connect your DSO via Ethernet. Don't forget to setup your IP address properly or set DHCP on(Utility -> I/O -> Ethernet -> DHCP/BOOTP on).  And enable the socket server on your DSO(Utility -> I/O -> Socket Server -> Server on).*

2.  *If you are using Linux, please add your username to group ```dialout``` to get proper privilege level for device accessing.*
    ```
    user@Ubuntu:~/workspace_python/OpenWave-1KB V1.01$ $ sudo adduser xxxx dialout     #xxxx is your username
    ```

3.  *You can also create a `port.config` file containing `COM5` or `ttyACM1` or `172.16.5.11:3000`(as an example) in the folder for next time quick connection.*

4.  *If you are using Raspbian on a Raspberry Pi2. Please use root account, that will help you to avoid privilege issues.  You might get trouble if you find your DSO is connected as ttyACM0. Your will have to change some system configuration files manually.*


Development Tools
------------
- **Packages:**
   If you want to modify the source code and run the program by yourself. You have to install the development tools and packages as follows:
   * Python 2.7.9
   * PySerial 2.7
   * Matplotlib 1.3.1
   * Numpy 1.8.0
   * PIL 1.1.7
   * PySide 1.2.1
   * dateutil 2.2
   * pyparsing 2.0.1
   * six 1.4.1

 *OpenWave-1KB.exe is developed under Windows 7 32 bits environment, and all the packages are Windows 32bits version.*

- **Ubuntu Linux:**
   OpenWave-1KB is also tested under Ubuntu 14.04.4 (32 bits) with the same version of the packages listed above.  And the following package and libraries are required:
   * nose-1.3.4
   * qt4-qmake
   * libqt4-dev

- **Raspbian Linux:**
   OpenWave-1KB is also tested on Raspberry Pi 2 with the following package and libraries:
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
![MS Windows](/image/Win7_Screenshot.jpg)


**Screenshot -- Win 10:**
![MS Windows](/image/Win10_Screenshot.jpg)


**Screenshot -- Ubuntu Linux:**
![Ubuntu Linux](/image/Ubuntu1404_Screenshot.jpg)


**Screenshot -- Raspbian on Raspberry Pi 2:**
![Raspbian Linux](/image/RPi2_Screenshot.jpg)
