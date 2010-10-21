# SkypeChatStats

A Python script to talk with Skype API to show top chatters in a chat for a given period.

Jaanus Kase, <http://www.jaanuskase.com>

## How to get started

1. Get the skypeChatStats.py script.
1. Install the dependencies: [Jinja2](http://jinja.pocoo.org/) for templates and [dateutil.parser](http://labix.org/python-dateutil) for date parsing. Both are also available through [pip.](http://pip.openplans.org/)
1. It also needs Skype4Py, bundled here.
1. Run the script with the right parameters.
1. Look at the results. :)

The right way to run the script is something like this:

    skypeChatStats.py -s "start-date" -e "end-date" -c "chat-name"

For example:

    skypeChatStats.py -s "2010-01-01" -e "2010-04-01" -c "#example/$8947847abcd"

You can get the chat name in any Skype chat if you enter the message "/chatname" (without quotes) and you get a magic response with the name.

## Example output

	Chat statistics for 1.1.2007–31.12.2008

	By message count:
	  8235   Al Bino
	  4925   Al Fresco
	  4111   Amanda Lynn
	  2947   Barb Dwyer
	  2904   Barry Cade
	  2881   Bea Minor
	  2852   Bill Board

	By text length:
	404819   Bill Loney
	328649   Billy Rubin
	216267   Bud Light
	175678   Dan D. Lyons
	165080   Dick Bush
	155606   Dick Tator
	154309   Dilbert Pickles
	134121   Don Key

	By posted links:
	  1063   Doug Graves
	  1038   Dr. Butcher
	   525   Dr. Kauff
	   403   Earl E. Bird
	   385   Fanny O'Rear
	   365   Gene Poole
	   341   Helen Back
	   316   Herb Rice

	Total traffic: 210 KB

## Misc notes

The latest Skype4Py version is hard to find. [The files are here](http://sourceforge.net/projects/skype4py/files/) but there’s no "homepage" to speak of. So I bundled it just in case.

The script crashes on Mac. It looks like latest Skype4Py, Python and Skype do not get along and Python crashes spectacularly (I haven’t seen Python crash before, yay.) It works OK on Windows, but to make things more fun, Windows terminals may not render Unicode correctly, so if you use UTF-8 in your templates, be prepared for fun.

## Change log

### October 18, 2010

* Initial public release. Only works with Windows for me.

## License (MIT)

Copyright (c) 2010 Jaanus Kase

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.