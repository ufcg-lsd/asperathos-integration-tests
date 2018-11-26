import os
import subprocess
import sys


def pytest_runtest_setup(item):
    print("setting up for ", item)
    script = subprocess.Popen("scripts/monitor/run.sh", shell=True)
    script.wait()
