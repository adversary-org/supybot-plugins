#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# Copyright (C) Ben McGinnes, 2013-2014
# ben@adversary.org
# OpenPGP/GPG key:  0x321E4E2373590E5D
#
# Version:  0.0.8
#
# BTC:  1KvKMVnyYgLxU1HnLQmbWaMpDx3Dz15DVU
# License:  BSD
#
# Requirements:
#
# * Python 3.2 or later (developed with Python 3.4.x).
# * Converted from scripts initially developed with Python 2.7.x.
# * Tor service with SOCKS support (optional)
#
# Options and notes:
#
# The config.py file must be customised prior to running either
# gen-auth.py or authinfo.py in order to set the correct path for the
# GPG configuration and adjust other settings.
#
# Usage:  
#
##

__author__ = "Ben McGinnes <ben@adversary.org>"
__copyright__ = "Copyright © Benjamin D. McGinnes, 2013-2014"
__copyrighta__ = "Copyright (C) Benjamin D. McGinnes, 2013-2014"
__copyrightu__ = "Copyright \u00a9 Benjamin D. McGinnes, 2013-2014"
__license__ = "BSD"
__version__ = "0.0.8"
__bitcoin__ = "1KvKMVnyYgLxU1HnLQmbWaMpDx3Dz15DVU"

import socket


class permanent:
    def checktor1():
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", 9050))
            return True
        except socket.error:
            return False

    def checktor2():
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", 9150))
            return True
        except socket.error:
            return False

    if checktor1() is True:
        client_args = {
            "verify": True,
            "headers": {
                "User-Agent": "Mozilla gecko compliant python script",
                "Cache-Control": "no-cache",
                },
            "proxies": {
                "http": "socks5://127.0.0.1:9050",
                "https": "socks5://127.0.0.1:9050",
                }
            }
        msg = "Tor configuration set on localhost and port 9050."
    elif checktor2() is True:
        client_args = {
            "verify": True,
            "headers": {
                "User-Agent": "Mozilla gecko compliant python script",
                "Cache-Control": "no-cache",
                },
            "proxies": {
                "http": "socks5://127.0.0.1:9150",
                "https": "socks5://127.0.0.1:9150",
                }
            }
        msg = "Tor configuration set on localhost and port 9150."
    else:
        client_args = {
            "verify": True,
            "headers": {
                "User-Agent": "Mozilla gecko compliant python script",
                "Cache-Control": "no-cache",
                },
            "proxies": False
            }
        print("No Tor configuration set, direct connection enabled.")


