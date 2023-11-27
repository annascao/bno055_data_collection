# bno055 data collection for UBC Aerodesign

## Overview

Abstract quaternion, euler angles, linear acceleration and angular velocity from the bno055 using the STM32F103C8T6.
<br>
Includes calibrating the sensor and re-centering the origin to the current position of the plane once upon startup and also upon the press of a button. Data logging via SD card is also available.

## STM32CubeIDE Settings

<img src="/Images/Pin Configurations.png" width="200"/>

## Acknowledgements

BNO055 STM32 Library used found in this repo: https://github.com/ivyknob/bno055_stm32