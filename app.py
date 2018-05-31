#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,environ
import psycopg2

try:
    connect_str = "dbname='earnest-vent-205713:northamerica-northeast1:d6539' user='" + environ['DB_USER'] + \
                "' host='127.0.0.1' port='5432' password='" + \
                environ['DB_PASSWORD'] + "'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from requests""")
    rows = cursor.fetchall()
    print(rows)
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)

PORT_NUMBER = 8080

class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','image/png')
		self.end_headers()
		f = open(curdir + sep + 'logo.png')
		self.wfile.write(f.read())
		return

try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print('Started httpserver on port ' , PORT_NUMBER)
	server.serve_forever()

except KeyboardInterrupt:
	server.socket.close()
