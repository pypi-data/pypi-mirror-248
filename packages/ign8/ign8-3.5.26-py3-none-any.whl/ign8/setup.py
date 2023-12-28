import os
import requests
import datetime
from .common import prettyllog
from .netbox.netbox import checknetbox


def main():
    prettyllog("main", "check", "main", "all", "200", "Success")
    return True

def getenvironmentvalue(myenv):
    myenv = os.getenv(myenv, "false")
    return myenv

def getenvironment():
    environment = {}
    environment["IGN8_NETBOX_URL"] = getenvironmentvalue("IGN8_NETBOX_URL")
    environment["IGN8_NETBOX_TOKEN"] = getenvironmentvalue("IGN8_NETBOX_TOKEN")
    environment["IGN8_NETBOX_VERIFY_SSL"] = getenvironmentvalue("IGN8_NETBOX_VERIFY_SSL")
    if checknetbox():
        prettyllog("getenvironment", "check", "getenvironment", "all", "200", "Success")
        return environment
    else:
        prettyllog("getenvironment", "check", "getenvironment", "all", "500", "Failed", "ERROR")
        return False


def setupign8():
    prettyllog("setupign8", "check", "setupign8", "all", "200", "Success")
    myenv = getenvironment()
    if myenv:
        prettyllog("setupign8", "check", "setupign8", "all", "200", "Success")
        return True
    else:
        prettyllog("setupign8", "check", "setupign8", "all", "500", "Failed", "ERROR")
        return False    

