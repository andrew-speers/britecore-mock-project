#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,environ
import psycopg2
import time

time.sleep(60)

log = open('/var/log/test.log', 'w')

log.write("Restarting...")
try:
    conn = psycopg2.connect(
        database='postgres',
        user=environ['DB_USER'],
        password=environ['DB_PASSWORD'],
        host='localhost',
        port='5432'
    )
    #connect_str = "dbname='postgres' user='" + environ['DB_USER'] + \
        #                       "' host='127.0.0.1' port='5432' password='" + \
        #                       environ['DB_PASSWORD'] + "'"
    # use our connection values to establish a connection
    #conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from requests""")
    rows = cursor.fetchall()
    log.write(rows)
except Exception as e:
    log.write(str(e))

log.close()

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
