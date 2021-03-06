#!/usr/bin/python
from http.server import SimpleHTTPRequestHandler,HTTPServer
from os import curdir,sep,environ
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import parse_qs
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
    Product_Area = Column(String)

Session = sessionmaker(engine)
session = Session()

reqs = session.query(Request)
for req in reqs:
    log.write(req.Title + '\n')

log.write('Backend OK.\n')

PORT_NUMBER = 8080

class myHandler(SimpleHTTPRequestHandler):

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        write_log('OPTIONS\n')
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()


    def do_GET(self):
        write_log('GET\n')
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        #f = open(curdir + sep + 'logo.png')
        self.wfile.write(bytes("<strong>Geoffrey</strong>", "utf-8"))
        return

    def do_POST(self):
        log = open('/var/log/test.log', 'a')
        log.write('POST\n')
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        try:
            length = int(self.headers['Content-Length'])
            post_data = parse_qs(self.rfile.read(length).decode('utf-8'))
            log.write(post_data['title'] + '\n')
        except Exception as e:
            log.write(str(e))
        log.close()
        # You now have a dictionary of the post data
        self.wfile.write(bytes("<strong>Post Geoffrey</strong>", "utf-8"))
        return

def write_log(arg):
    log = open('/var/log/test.log', 'a')
    log.write(arg)
    log.close()

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    log.write('Started server on port 8080\n')
    log.close()
    server.serve_forever()
except:
    write_log('Error\n')
