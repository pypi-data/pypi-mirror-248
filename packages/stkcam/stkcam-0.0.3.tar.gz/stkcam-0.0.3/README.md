# Python module for simple ASUS tinkerboard camera

## Overview
This repository documentation for simple asus tinkerboard camera control. Test create python module and upload python pypi. May with a lots of bug :)

## Test Environment

* [ASUS Tinkerboard](https://www.asus.com/networking-iot-servers/aiot-industrial-solutions/tinker-series/tinker-board/)
  * image: v2.2.2
  * camera:
    * OV5647 (Raspiberry Camera V1, 5MP)
    * IMX219 (Raspiberry Camera V2, 8MP)
  * python version: 3.5
* [ASUS Tinkerboard 2](https://www.asus.com/networking-iot-servers/aiot-industrial-solutions/tinker-series/tinker-system-2/)
  * image: v3.0.6
  * camera:
    * OV5647 (Raspiberry Camera V1, 5MP)
    * IMX219 (Raspiberry Camera V2, 8MP)
  * python version: 3.9.2

## Usage
* preview
```console
$ from stkcam import TKCam, CamType
$ cam = TKCam(CamType.OV5647)
$ cam.preview()
```
* take a picture
```console
$ from stkcam import TKCam, CamType
$ cam = TKCam(CamType.OV5647)
$ cam.take_image('/home/linaro/Desktop\image.jpg') # image path
```