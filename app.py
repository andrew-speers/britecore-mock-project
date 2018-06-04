#!/usr/bin/python
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,environ
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

time.sleep(60)

log = open('/var/log/test.log', 'w')

log.write("Restarting...\n")
engine = create_engine('postgres://' + environ['DB_USER'] + \
                       ':' + environ['DB_PASSWORD'] + '@localhost:5432/postgres')
base = declarative_base()

class Request(base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    Title = Column(String)
    Description  = Column(String)
    Client = Column(String)
    Priority = Column(Integer)
    Target_Date = Column(Date)
    Product_Area = column(String)

Session = sessionmaker(engine)
session = Session()

reqs = session.query(Request)
for req in reqs:
    log.write(req.Title + '\n')

log.write('Backend OK.\n')
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
