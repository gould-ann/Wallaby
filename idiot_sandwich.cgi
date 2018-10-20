# remembered its a cgi file...
import cgi
import cgitb
import json
import os

cgitb.enable()

form = cgi.FieldStorage()

print "Content-Type: text/html"     # HTML is following
print ""                            # blank line, end of headers

user = form["user"].value
print form["words"]

server_names = []