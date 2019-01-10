#!/usr/bin/env python
from conanos.build import Main
import os

if __name__ == "__main__":
    os.system("conan remove --force --locks")
    Main('gst-sdk',pure_c=True)