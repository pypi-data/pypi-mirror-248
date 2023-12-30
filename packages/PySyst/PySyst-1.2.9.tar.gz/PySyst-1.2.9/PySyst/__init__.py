# PySyst - Init

''' This is the __init__.py file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import sys
import pickle
import platform
import webbrowser
import os as python_os
from colorama import Fore, Style
from .Packages import package_versions
from datetime import datetime, timedelta

# Variables - Package Information
__name__ = "PySyst"
__version__ = "1.2.9"
__description__ = "This Python package alters your computer's settings and files and comes with various system-related functions."
__license__ = "Apache License 2.0"
__author__ = "Aniketh Chavare"
__author_email__ = "anikethchavare@outlook.com"
__github_url__ = "https://github.com/anikethchavare/PySyst"
__pypi_url__ = "https://pypi.org/project/PySyst"
__docs_url__ = "https://anikethchavare.gitbook.io/pysyst"

# Variables
os = platform.system()
os_release = platform.release()
os_version = platform.version()
pc_name = platform.node()
machine = platform.machine()
processor = platform.processor()

# Try/Except - Importing "wmi" and Assigning Variables
try:
    # Imports
    import wmi

    # Variables
    manufacturer = wmi.WMI().Win32_ComputerSystem()[0].Manufacturer
    model = wmi.WMI().Win32_ComputerSystem()[0].Model
except:
    pass

# Function 1 - Version Check
def version_check():
    # Variables
    directory = python_os.path.dirname(python_os.path.realpath(__file__)).replace(python_os.sep, "/")

    # Nested Function 1 - Version Check 2
    def version_check_2(make_directory):
        # Try/Except - Checking the Version
        try:
            # Variables
            versions = package_versions("python", "PySyst")

            # Checking the Version
            if (versions["Upgrade Needed"]):
                # Checking the Environment
                if ("idlelib.run" in sys.modules):
                    print("You are using PySyst version " + versions["Installed"] + ", however version " + versions["Latest"] + " is available.")
                    print("Upgrade to the latest version for new features and improvements using this command: pip install --upgrade PySyst" + "\n")
                else:
                    print(Fore.YELLOW + "You are using PySyst version " + versions["Installed"] + ", however version " + versions["Latest"] + " is available.")
                    print(Fore.YELLOW + "Upgrade to the latest version for new features and improvements using this command: " + Fore.CYAN + "pip install --upgrade PySyst" + Style.RESET_ALL + "\n")

            # Making the Cache Directory
            if (make_directory):
                # Try/Except - Making the Cache Directory
                try:
                    python_os.mkdir(directory + "/cache")
                except FileExistsError:
                    pass

            # Opening and Writing to the Cache File
            with open(directory + "/cache/version.cache", "wb") as cache_file:
                pickle.dump({"Future Time": datetime.now() + timedelta(hours=24)}, cache_file)
        except:
            pass

    # Checking if Cache File Exists
    if (python_os.path.exists(directory + "/cache/version.cache")):
        # Opening and Reading the Cache File
        with open(directory + "/cache/version.cache", "rb") as cache_file:
            # Comparing the Time
            if (pickle.load(cache_file)["Future Time"] < datetime.now()):
                # Running the "version_check_2()" Function
                version_check_2(False)
    else:
        # Running the "version_check_2()" Function
        version_check_2(True)

# Function 2 - GitHub
def github():
    # Opening PySyst's GitHub Repository
    try:
        webbrowser.open(__github_url__)
    except:
        # Raising an Exception
        raise Exception("An error occurred while opening the GitHub repository. Please try again.")

# Function 3 - PyPI
def pypi():
    # Opening PySyst's PyPI Page
    try:
        webbrowser.open(__pypi_url__)
    except:
        # Raising an Exception
        raise Exception("An error occurred while opening the PyPI page. Please try again.")

# Function 4 - Docs
def docs():
    # Opening PySyst's Docs
    try:
        webbrowser.open(__docs_url__)
    except:
        # Raising an Exception
        raise Exception("An error occurred while opening the docs. Please try again.")

# Running the "version_check()" Function
version_check()