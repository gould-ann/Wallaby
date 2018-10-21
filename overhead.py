import cgi
form = cgi.FieldStorage()
# send to server instead 
print form["username"]