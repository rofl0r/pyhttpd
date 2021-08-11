#!/usr/bin/env python2

# httpsrv library routines for python.
# Copyright (C) 2018-2021 rofl0r

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

# you can find the full license text at
# https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html

import socket, urllib, os

def _format_addr(addr):
        ip, port = addr
        return "%s:%d"%(ip, port)

def _isnumericipv4(ip):
	try:
		a,b,c,d = ip.split('.')
		if int(a) < 256 and int(b) < 256 and int(c) < 256 and int(d) < 256:
			return True
		return False
	except:
		return False

def _resolve(host, port, want_v4=True):
	if _isnumericipv4(host):
		return socket.AF_INET, (host, port)
	for res in socket.getaddrinfo(host, port, \
			socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
		af, socktype, proto, canonname, sa = res
		if want_v4 and af != socket.AF_INET: continue
		if af != socket.AF_INET and af != socket.AF_INET6: continue
		else: return af, sa
	return None, None

def _parse_req(line):
	r = line.find(' ')
	if r == -1:
		return '', '', ''
	method = line[:r]
	rest = line[r+1:]
	r = rest.find(' ')
	if r == -1:
		return method, '', ''
	else:
		ver = rest[r+1:]
		url = rest[:r]
		return method, url, ver

class HttpClient():
	def __init__(self, addr, conn):
		self.addr = addr
		self.conn = conn
		self.active = True
		self.keep_alive = True
		self.debugreq = False

	def _send_i(self, data):
		self.conn.send(data)
		if self.debugreq and len(data): print ">>>\n", data

	def send_header(self, code, msg, response_len, headers=None):
		r = "HTTP/1.1 %d %s\r\n"%(code, msg)
		if headers:
			for h in headers:
				r += "%s: %s\r\n"%(h, headers[h])
		r += "Content-Length: %d\r\n\r\n" % response_len
		try: self._send_i(r)
		except:
			self.disconnect()
			return False
		return True

	def send(self, code, msg, response, headers=None):
		if not self.send_header(code, msg, len(response), headers):
			return
		try:
			self._send_i(response)
		except:
			self.disconnect()

	def serve_file(self, filename, start=0):
		st = os.stat(filename)
		sz = st.st_size
		sent = 0
		if start == 0:
			self.send_header(200, "OK", sz-start)
		elif start >= sz:
			self.send(416, "Range not satisfiable", "")
			return
		else:
			self.send_header(206, "Partial Content", sz-start, {"Content-Range": "bytes %d-%d/%d"%(start, sz-1, sz)})

		with open(filename, 'r') as h:
			h.seek(start)
			while sent < sz-start:
				chunk = h.read(4096)
				try: self._send_i(chunk)
				except:
					self.disconnect()
					break
				sent += len(chunk)

	def redirect(self, url, headers=None):
		h = dict() if not headers else headers.copy()
		h['Location'] = url
		self.send(301, "Moved Permanently", "", headers=h)

	def _url_decode(self, s): return urllib.unquote_plus(s)

	def read_request(self):
		s = ''
		CHUNKSIZE = 1024
		while 1:
			if len(s):
				rnrn = s.find('\r\n\r\n')
				if rnrn != -1: break
			r = self.conn.recv(CHUNKSIZE)
			if len(r) == 0:
				return self.disconnect()
			s += r

		cl = 0
		range = None
		for line in s.split('\n'):
			if line.lower().startswith('connection:'):
				try: ka = line.lower().split(':', 1)[1].strip()
				except: pass
				if ka != 'keep-alive': c.keep_alive = False
			elif line.lower().startswith('range: bytes='):
				try: range = line.split('=')[1].strip()
				except: pass
			elif line.lower().startswith('content-length:'):
				try: cl = int(line.split(':', 1)[1].strip())
				except: pass
				break

		while len(s) < rnrn + 4 + cl:  # 4 == len('\r\n\r\n')
			r = self.conn.recv(CHUNKSIZE)
			if len(r) == 0: return None
			s += r

		err = False
		if not s: err = True
		if err:
			self.active = False
			self.conn.close()
			return None

		if self.debugreq: print "<<<\n", s

		n = s.find('\r\n')
		if n == -1: err = True
		else:
			line = s[:n]
			a = s[n+2:]
			meth, url, ver = _parse_req(line)
			if not (ver == "HTTP/1.0" or ver == "HTTP/1.1"):
				err = True
			if not (meth == 'GET' or meth == 'POST'):
				err = True
		if err:
			self.send(500, "error", "client sent invalid request")
			return self.disconnect()
		result = dict()
		result['method'] = meth
		result['url'] = self._url_decode(url)
		for x in a.split('\r\n'):
			if ':' in x:
				y,z = x.split(':', 1)
				result[y] = z.strip()
		if meth == 'POST':
			result['postdata'] = dict()
			postdata = s[rnrn:]
			for line in postdata.split('\n'):
				if '=' in line:
					k,v = line.split('=', 1)
					result['postdata'][k] = self._url_decode(v.strip())
		result['range'] = 0
		if range and range[0] != '-' and range.endswith('-'):
			try: result['range'] = int(range[:-1])
			except: pass
		return result

	def disconnect(self):
		if self.active: self.conn.close()
		self.conn = None
		self.active = False
		self.keep_alive = False
		return None

class HttpSrv():
	def __init__(self, listenip, port):
		self.port = port
		self.listenip = listenip
		self.s = None

	def setup(self):
		af, sa = _resolve(self.listenip, self.port)
		s = socket.socket(af, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((sa[0], sa[1]))
		s.listen(128)
		self.s = s

	def wait_client(self):
		conn, addr = self.s.accept()
		c = HttpClient(addr, conn)
		return c

def forbidden_page():
	return (
		'<!DOCTYPE html>\n'
		'  <head>\n'
		'    <style>div.e{position:fixed;top:25%;bottom:25%;left:25%;right:25%;font-size:150px;text-align:center;}</style>\n'
		'    <title>Forbidden</title>\n'
		'  </head>\n'
		'  <body>\n'
		'    <div class="e">&#128405;</div>\n'
		'  </body>\n'
		'</html>')

def http_client_thread(c, evt_done):
	while c.keep_alive and c.active:
		req = c.read_request()
		if req is None or req['method'] != 'GET': pass
		elif os.path.isdir(req['url'][1:]):
			c.send(403,'Forbidden', forbidden_page())
		elif req['url'] == '/':
			c.redirect('/index.html')
		elif not '..' in req['url'] and os.path.exists(os.getcwd() + req['url']):
			c.serve_file(os.getcwd() + req['url'], req['range'])
		elif req['url'] == '/robots.txt':
			c.send(200, "OK", "User-agent: *\nDisallow: /\n")
		else:
			c.send(404, "not exist", "the reqested file not exist!!!1\n")
	c.disconnect()
	evt_done.set()

if __name__ == "__main__":
	import threading, sys
	port = 8000 if len(sys.argv) < 2 else int(sys.argv[1])
	hs = HttpSrv('0.0.0.0', port)
	hs.setup()
	client_threads = []
	while True:
		c = hs.wait_client()
		sys.stdout.write("[%d] %s\n"%(c.conn.fileno(), _format_addr(c.addr)))
		evt_done = threading.Event()
		cthread = threading.Thread(target=http_client_thread, args=(c,evt_done))
		cthread.daemon = True
		cthread.start()

		ctrm = []
		for ct, ct_done in client_threads:
			if ct_done.is_set():
				ctrm.append((ct,ct_done))
				ct.join()

		if len(ctrm):
			client_threads = [ x for x in client_threads if not x in ctrm ]

		client_threads.append((cthread, evt_done))

