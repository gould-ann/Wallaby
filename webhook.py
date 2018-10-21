#!/usr/bin/python
import cgi
import cgitb
import json

cgitb.enable()

print "Content-type: text/html\r\n\r\n"

form = cgi.FieldStorage()

print open("/var/www/html/data.json").read()
data = json.loads(open("/var/www/html/data.json").read())


for i in range(len(data)):
	x = data[i]["patient"]
	if x["name"] == form["name"].value:
		data[i]["patient"]["data"]["exercises"] += {"exercise": form["exercise"].value, "reps": form["reps"].value, "date": form["date"].value}

f =  opem("/var/www/html/data.json", "w")
f.write(json.dumps(data))
f.close()

print "record added successfully"
