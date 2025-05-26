import sys
import os

sys.path.insert(1, os.getcwd())
from src.udp.plane_obj import Plane

plane = Plane()

import time

while True:
    print(plane)
    time.sleep(1)