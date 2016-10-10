#BuzzPy
#####Created and developed by Adriana Galvez.

###### [Back-end](https://github.com/Attacktic/capstoneBackend)

###### [iOS](https://github.com/Attacktic/iosCapstone)

###### [Android](https://github.com/Attacktic/androidCapstone)
## How does it work?
###After setting up the Raspberry Pi and installing BuzzPy you can use the following commands run the camera:
```
  $ workon cv
  $ python pi_surveillance.py --conf conf.json
```
##### Images will show up in the app and you will get text message updates when the camera detects motion.

##### To stop the stream and updates:
```
  CTRL + C
```

## Set Up Instructions:

### 1. Download and Install latest version of Raspbian on your Raspberry Pi.

### 2. Update your RPi with the following commands:
```
  $ sudo apt-get update
  $ sudo apt-get upgrade
  $ sudo rpi-update
```

### 3. Install all dependencies:
```
  $ sudo apt-get install build-essential cmake pkg-config
  $ sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
  $ sudo apt-get install libgtk2.0-dev
  $ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  $ sudo apt-get install libatlas-base-dev gfortran
  $ wget https://bootstrap.pypa.io/get-pip.py
  $ sudo python get-pip.py
  $ sudo pip install virtualenv virtualenvwrapper
  $ sudo rm -rf ~/.cache/pip
  $ nano ~/.profile
```
### 4. add the following lines to ~/.profile:
```
  export WORKON_HOME=$HOME/.virtualenvs
  source /usr/local/bin/virtualenvwrapper.sh
```
### 5. Create virtual environment and install more dependencies:
```
  $ mkvirtualenv cv
  $ sudo apt-get install python2.7-dev
  $ pip install numpy
  $ wget -O opencv-2.4.10.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download
  $ unzip opencv-2.4.10.zip
  $ cd opencv-2.4.10
  $ mkdir build
  $ cd build
  $ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON .
  $ make
  $ sudo make install
  $ sudo ldconfig
  $ cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
  $ ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so
  $ ln -s /usr/local/lib/python2.7/site-packages/cv.py cv.py
```
### 6. Enable Camera in rasps-config menu:
```
  $ sudo raspi-config
```
##### 6.5. Install Camera:
```
  $ pip install "picamera[array]"
```
### 7. Download BuzzPy Set Up File and Install:
```
  $ git clone git@github.com:Attacktic/BuzzPy.git
  $ cd BuzzPy/main
  $ workon cv
  $ python setup.py
```
##### Enter Required Data When Prompted
```
  $ python pi_surveillance.py --conf conf.json
```
