#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,environ
#import psycopg2
from sqlalchemy import create_engine
import time

time.sleep(60)

log = open('/var/log/test.log', 'w')

log.write("Restarting...")
try:
    engine = create_engine('postgres://' + environ['DB_USER'] + ':' + environ['DB_PASSWORD'] + '@localhost:5432/postgres')

    '''
    conn = psycopg2.connect(
        database='postgres',
        user=environ['DB_USER'],
        password=environ['DB_PASSWORD'],
        host='localhost',
        port='5432'
    )

    cursor = conn.cursor()
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from requests""")
    rows = cursor.fetchall()
    log.write(rows)
    '''

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
