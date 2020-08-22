# This file is executed on every boot (including wake-boot from deepsleep)

import os
import esp
import machine
from machine import Timer, Pin
import dht

import gc
import utime as time

gc.collect()
