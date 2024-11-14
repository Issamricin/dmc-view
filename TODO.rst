TODO LIST
=========

Device Simulator(|done|)
------------------------
| 
| We need to build a simulator which sends a constant value for the declination(the difference between real north and magnetic north). The azimuth, inclination and bank should be repeated across a small range as below:
| Azimuth: [45.5, 46.5,47.0, 47.5, 48.0, 48.5] with delay timer of 100 Millisecond
| Inclination Angle: [60,60.5,61.0,61.5,62.0] with  delay time of 200 Millisecond
| Bank Angle: [30.0,30.5, 31.0, 31.5,32.0.32.5] with delay time of 150 Millisecond


Adding X, Y and Z acceleration:
-------------------------------
We need to add and view the 3 axis-es acceleration data to be viewed and displayed

Device Manufactures Common Interface(API):
------------------------------------------
The application should work in a plug and play manner. Any device manufacturer should be able to 
plug the device via USB (RS-232 or RS-485) serial communication. The application should be able to have different 
parser implementation for difference device manufacturers. It helps the autonomous car to test the device before 
embedding it into their products. Different parsing implementation upon reading from serial port. Common interface to extract the data from different device manufacturers  

Device Manufactures Details DMC Product Information:
----------------------------------------------------
1. A  hyberlink list of DMC product in the market for 2D and 3D.
2. Detail price and features 
3. User manual
4. Reference implementation in Python  if exist 
5. Direct sales contact information

.. |done| image::  https://img.shields.io/badge/DONE-green
            :alt: DONE
