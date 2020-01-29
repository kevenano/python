# mapIt.py
# Launch a map in the browser using an address from the
# command line or clipboard

import webbrowser
import sys
import pyperclip

if len(sys.argv) > 1:
    # Get address from the command line
    address = ' '.join(sys.argv[1:])
else:
    # Get address from the clipboard
    address = pyperclip.paste()

# Open the address in webbrowser
webbrowser.open('www.google.com/maps/place/'+address)
