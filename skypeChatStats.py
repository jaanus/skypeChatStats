#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Skype4Py, sys, optparse, re, copy
from datetime import datetime

# from http://labix.org/python-dateutil
import dateutil.parser

# from http://jinja.pocoo.org/
from jinja2 import Environment, FileSystemLoader

optParser = optparse.OptionParser()

# got useful tips from http://blog.doughellmann.com/2007/08/pymotw-optparse.html
optParser.add_option('-s', '--start'
    , dest="periodStart"
    , help="Start date/time of the period you're analyzing"
    , default="bogus")
        
optParser.add_option('-e', '--end'
    , dest="periodEnd"
    , help="End date/time of the period you're analyzing"
    , default="bogus")
        
optParser.add_option('-c', '--chatname'
    , dest="chatName"
    , help="Chat identifier of the chat you are analyzing. Type /CHATNAME in a Skype chat to get the name for that chat."
    , default="")
        
optParser.add_option('-q', '--quiet'
    , dest="quiet"
    , action="store_true"
    , help="Don't show message processing progress on the console. Use this if running automatically e.g as a cronjob"
    , default=False)
        
optParser.add_option('-d', '--debug'
    , dest="debug"
    , action="store_true"
    , help="Whether to dump debugging info like message author, timestamp and body as the processing is happening"
    , default=False)

options, remainder = optParser.parse_args()

meta = {'totalTraffic': 0}

# make sure we have start and end time and chat name
try:
    meta['start'] = dateutil.parser.parse(options.periodStart)
except ValueError:
    optParser.error("Invalid or missing start date/time. Run with the -h option to see instructions.")
try:
    meta['end'] = dateutil.parser.parse(options.periodEnd)
except ValueError:
    optParser.error("Invalid or missing end date/time. Run with the -h option to see instructions.")
if options.chatName=='':
    optParser.error("Missing chat name. Run with the -h option to see instructions.")

skype = Skype4Py.Skype()
skype.FriendlyName = 'Skype chat stats collector'

# This crashes on Mac with Skype 2.8.0.851, Python 2.6.1, Skype4Py 1.0.32.0.
# Works OK in Windows XP, Python 2.7, Skype 5.0.0.152.
skype.Attach()

# list of dictionaries holding data about each person
topChatters = []

# {skypename -> index} hash table to the above list 
topChatterIndexes = {}

for c in skype.Chats:
    if c.Name == options.chatName:
        chat = c

try:
    chat
except NameError:
    print "Could not find a chat with the name '{0}'. Check your input.".format(options.chatName)
    sys.exit(0)

if not options.quiet:
    currMsg = 0
    sys.stdout.write("Total messages: " + str(len(chat.Messages)) + ", now processing: ")

# to capture how many urls everybody has posted in a chat
urlPattern = re.compile('http://')

for m in chat.Messages:
    
    # report progress
    if not options.quiet:
        currMsg += 1
        if (currMsg % 100 == 0):
            sys.stdout.write(str(currMsg))
            sys.stdout.flush()
            
    # if a given message falls in our date period range and is of the right type (actual text and not some
    # "meta-message"), then process it
    if (meta['start'] <= m.Datetime <= meta['end']) and (m.Type in ['SETTOPIC', 'SAID', 'EMOTED']):
        
        # see if we already know something about this skypename.. if not, create their record
        try:
            topChatterIndexes[m.FromHandle]
        except KeyError:
            topChatterIndexes[m.FromHandle] = len(topChatters)
            topChatters.append({'skypeName': m.FromHandle, 'msgCount': 0, 'charCount': 0,
                'urlCount': 0, 'latestTimestamp': datetime(1900, 1, 1)})
                
        topChatters[topChatterIndexes[m.FromHandle]]['msgCount'] += 1
        topChatters[topChatterIndexes[m.FromHandle]]['charCount'] += len(m.Body)
        
        # count the urls in this message. we don't need a comprehensive pattern, a simple
        # http:// is enough because we just want to capture the fact that a url was posted.
        # findall returns a list of match objects, so this works also when there was >1 url
        # in this message.
        topChatters[topChatterIndexes[m.FromHandle]]['urlCount'] += len(urlPattern.findall(m.Body))

        # overwrite display name from the latest msg from this handle. we assume that the person
        # always wants to be known by their latest displayname.
        if m.Datetime > topChatters[topChatterIndexes[m.FromHandle]]['latestTimestamp']: 
            topChatters[topChatterIndexes[m.FromHandle]]['latestTimestamp'] = m.Datetime
            topChatters[topChatterIndexes[m.FromHandle]]['fromDisplayName'] = m.FromDisplayName
        meta['totalTraffic'] += len(m.Body)

    # if we are echoing progress (which happens every 100th message), remove current progress
    # so next one can be nicely printed. apparently the backspaces won't be printed before we do
    # a flush above, this is why the number is always visible even though we only print something
    # every 100th message and backspace it here.
    if not options.quiet:
        if (currMsg % 100 == 0):
            for i in range(len(str(currMsg))):
                sys.stdout.write('\b')
    if options.debug:
        print m.Datetime, m.FromHandle, m.FromDisplayName, m.Body

if not options.quiet:
    sys.stdout.write(str(currMsg)) # to make it look nice in the end
    print " ... done."

meta['startFormatted'] = meta['start'].strftime('%d.%m.%Y')
meta['endFormatted'] = meta['end'].strftime('%d.%m.%Y')

# Denormalize the data into separate lists. The more complex topChatters data structure could be
# passed to Django template engine where we could use complex "dictsortreversed" filters.
# Since Jinja2 templating is more simplistic, we'll pre-cook the data this way.
topCounts = sorted(topChatters, key=lambda count: count['msgCount'], reverse=True)
topUrls = sorted(topChatters, key=lambda count: count['urlCount'], reverse=True)
topChars = sorted(topChatters, key=lambda count: count['charCount'], reverse=True)

# render the output with Jinja2's templating system from the data.
jinjaEnv = Environment(loader=FileSystemLoader('.', encoding='utf-8'))
template = jinjaEnv.get_template("skypeChatStatsTemplateEn.txt")
print template.render(topCounts=topCounts, topUrls=topUrls, topChars=topChars, meta=meta)
