#!/usr/bin/env python3

################################################################################
# Copyright (c) 2024,D-Robotics.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################


#右轮2
import sys
import signal
import Hobot.GPIO as GPIO
import time

def signal_handler(signal, frame):
    sys.exit(0)

# 支持PWM的管脚: 32 and 33, 在使用PWM时，必须确保该管脚没有被其他功能占用

AIN1_PIN = 29#左
AIN2_PIN = 31
PWMA_PIN = 33

BIN1_PIN = 16#右
BIN2_PIN = 18
PWMB_PIN = 32

GPIO.setwarnings(False)

def set_motor_directions(forward=True):
    if forward:
        GPIO.output(AIN1_PIN, GPIO.HIGH)
        GPIO.output(AIN2_PIN, GPIO.LOW)
        GPIO.output(BIN1_PIN, GPIO.LOW)
        GPIO.output(BIN2_PIN, GPIO.HIGH)
    else:
        GPIO.output(AIN1_PIN, GPIO.LOW)
        GPIO.output(AIN2_PIN, GPIO.HIGH)
        GPIO.output(BIN1_PIN, GPIO.HIGH)
        GPIO.output(BIN2_PIN, GPIO.LOW)


def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(AIN1_PIN, GPIO.OUT)
    GPIO.setup(AIN2_PIN, GPIO.OUT)
    GPIO.setup(BIN1_PIN, GPIO.OUT)
    GPIO.setup(BIN2_PIN, GPIO.OUT)
    
    
    # 支持的频率范围： 48KHz ~ 192MHz
    p_a = GPIO.PWM(PWMA_PIN, 48000)
    p_b = GPIO.PWM(PWMB_PIN, 48000)
    # 初始占空比 25%
    initial_val = 25
    p_a.ChangeDutyCycle(initial_val)
    p_a.start(initial_val)
    p_b.ChangeDutyCycle(initial_val)
    p_b.start(initial_val)

    print("PWM running. Press CTRL+C to exit.")
    try:
        while True:
            # 正转
            set_motor_directions(forward=False)  
            for duty_cycle in range(1, 100, 10):
                p_a.ChangeDutyCycle(duty_cycle)
                p_b.ChangeDutyCycle(duty_cycle)
                #time.sleep(0.25)
            
          
    finally:
        p_a.stop()
        p_b.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()
