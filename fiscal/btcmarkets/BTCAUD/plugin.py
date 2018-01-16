###
# Copyright (c) 2018, Ben McGinnes
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import datetime
import requests
import time

from .cargs import permanent
ca = permanent.client_args
domain = "https://api.btcmarkets.net"
uri = "/market/BTC/AUD/tick"
url = "{0}{1}".format(domain, uri)
try:
    r = requests.get(url, verify=True, headers=ca["headers"],
                     proxies=ca["proxies"])
    # r = requests.get(url, verify=True)
except:
    r = None
    pass

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization, internationalizeDocstring
    _ = PluginInternationalization('BTCAUD')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class BTCAUD(callbacks.Plugin):
    """BTC to AUD prices from btcmarkets.net."""
    threaded = True
    @internationalizeDocstring
    def ticker(self, irc, msg, args):
        """Displays a ticker of the BTC to AUD prices."""
        
        if r is not None and r.status_code == 200:
            ask = str(r.json()["bestAsk"])
            bid = str(r.json()["bestBid"])
            last = str(r.json()["lastPrice"])
            spread = str(round(r.json()["bestAsk"] - r.json()["bestBid"], 2))
            tstamp = r.json()["timestamp"]
            ltime = time.ctime(tstamp)
            utime = time.asctime(time.gmtime(tstamp))
            # Note, offset only works for positive TZ offsets, use +
            # or - to indicate which it is.  The utcdiff value is used
            # to determine the + or - later in the script.  Specific
            # TZ names must still be specified.
            offset = str(abs((datetime.datetime.now() - datetime.datetime.utcnow()) / 3600 * 3600))
            utcdiff = round((datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds())
            age = str(datetime.timedelta(seconds=abs(time.time() - tstamp))).split(':')

            if int(age[0]) == 0 and int(age[1]) == 0:
                secs = str(float(age[2]))
                since = "{0} seconds ago.".format(secs)
            elif int(age[0]) == 0 and int(age[1]) > 0:
                mins = str(int(age[1]))
                secs = str(float(age[2]))
                since = "{0} minutes and {1} seconds ago.".format(mins, secs)
            elif int(age[0]) > 0 and int(age[1]) > 0:
                hours = str(int(age[0]))
                mins = str(int(age[1]))
                secs = str(float(age[2]))
                since = "{0} hours, {1} minutes and {2} seconds ago.".format(hours, mins, secs)
            else:
                hours = str(int(age[0]))
                mins = str(int(age[1]))
                secs = str(float(age[2]))
                since = "{0} hours, {1} minutes and {2} seconds ago.".format(hours, mins, secs)

            # This must be changed if TZ is at +1000, +1100, -1100 or
            # -1000 UTC and not in Australia (in the first two cases):
            if offset == "10:00:00":
                localtz = "AEST"
            elif offset == "11:00:00":
                localtz = "AEDT"
            else:
                localtz = "local time"

            if len(offset) == 8:
                # oset = "".join(offset[0:5].split(":")) # standard
                # format without colon
                oset = offset[0:5]  # standard format with colon
            elif len(offset) == 7:
                # oset = "".join(offset[0:4].split(":")) # standard
                # format without colon
                oset = "0{0}".format(offset[0:4])  # standard format with colon
            else:
                oset = offset

            utcdiff = round((datetime.datetime.now() - datetime.datetime.utcnow()).total_seconds())

            if utcdiff > 0:
                p = "BTCMarkets BTCAUD | Best bid: {0}, Best ask: {1}, Bid-Ask spread: {2}, last trade: {3} | valid at: {4} UTC | {5} {6} (UTC+{7}) | {8}".format(bid, ask, spread, last, utime, ltime, localtz, oset, since)
            elif utcdiff < 0:
                p = "BTCMarkets BTCAUD | Best bid: {0}, Best ask: {1}, Bid-Ask spread: {2}, last trade: {3} | valid at: {4} UTC | {5} {6} (UTC-{7}) | {8}".format(bid, ask, spread, last, utime, ltime, localtz, oset, since)
            elif utcdiff == 0:
                p = "BTCMarkets BTCAUD | Best bid: {0}, Best ask: {1}, Bid-Ask spread: {2}, last trade: {3} | valid at: {4} UTC | {8}".format(bid, ask, spread, last, utime, since)
            else:
                p = "BTCMarkets BTCAUD | Best bid: {0}, Best ask: {1}, Bid-Ask spread: {2}, last trade: {3} | valid at: {4} UTC | {8}".format(bid, ask, spread, last, utime, since)
        elif r is not None and r.ok is False and r.status_code is None:
            p = "Error code: {0}".format("unknown1")
        elif r is not None and r.ok is False:
            p = "Error code: {0}".format(str(r.status_code))
        elif r is None:
            p = "Error code: {0}".format("unknown2")
        else:
            p = "Error code: {0}".format("unknown0")
        irc.reply(format(_('%s'), (p)), prefixNick=False)
    ticker = wrap(ticker)
        
        

Class = BTCAUD


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
