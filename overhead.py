import cgi
form = cgi.FieldStorage()
print form["username"]