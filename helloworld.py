def client_main(c, evt_done):
	root = c.root
	while c.keep_alive and c.active:
		req = c.read_request()
		if req is None: break
		if req['url'] == '/':
			c.redirect('/index.html')
		elif req['url'] == '/index.html':
			c.send(200, "OK", "Hello world!")
		else:
			c.send(404, "not exist", "the reqested file not exist!!!1\n")
	c.disconnect()
	evt_done.set()

