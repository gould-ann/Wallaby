#!/usr/bin/python
import cgi
import cgitb

cgitb.enable()

print "Content-type: text/html\r\n\r\n"

form = cgi.FieldStorage()
if "file" in form.keys():
	files = form["file"]
	print files.filename, files.name, files.value
	open('/tmp/' + files.filename, 'wb').write(files.value.read())