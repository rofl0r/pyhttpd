import os

# this is a minimalistic pyhttpd app to run on a sabotage host to serve
# the installed packages to other hosts.
# the packages are created with butch pack on demand, if they're not
# already in CACHE_DIR, else served from there.
# for those created on demand they're only served if the installed pkgver
# matches the one requested.
# no great effort was spent to make this secure, so use it only in trusted
# environments.

# you should probably edit this, else your RAM might run out quickly...
CACHE_DIR="/dev/shm"

# only supporting .tar should be good enough for a LAN. if you want to
# support other extensions, you als need to mod the code to run butch pack
# with the right arguments. xz is the best option for permanent storage,
# .zstd or .gz to keep cpu usage low and provide reasonable compression.
EXT_ALLOW = { 'tar': 1, }

# this should match your A variable in /src/config.
SUPPORTED_ARCHS = { 'x86_64': 1, }

def butchdb_got_version(pkg, ver):
	fs = "%s %d"%(pkg, ver)
	with open("/var/lib/butch.db", "r") as db:
		while 1:
			s = db.readline()
			if s == '': break
			s = s.strip()
			if s == fs: return True
	return False

def process_req(c, req):
	fn = req['url'].lstrip('/')
	if '/' in fn or not '.' in fn: return False
	full_path = "%s/%s" % (CACHE_DIR, fn)
	print("request: " + fn)
	if os.path.exists(full_path):
		c.serve_file(full_path)
		return True
	fp, ext = fn.split('.', 1)
	parts = fp.split('_')
	veridx = 2
	if len(parts) == 4:
		arch = "%s_%s"%(parts[1], parts[2])
		veridx = 3
	elif len(parts) == 3:
		arch = parts[1]
	else: return False
	pkg = parts[0]
	try: ver = int(parts[veridx])
	except: return False

	if ext not in EXT_ALLOW: return False
	if arch not in SUPPORTED_ARCHS: return False
	if not butchdb_got_version(pkg, ver): return False
	# here we could e.g. create a .tar.zstd on demand
	ret = os.system("cd %s && butch pack %s"%(CACHE_DIR, pkg))
	if ret != 0: return False
	if os.path.exists(full_path):
		c.serve_file(full_path)
		return True
	return False

def sec_check(fs, root):
	rp = os.path.normpath(fs)
	return rp == root or rp.startswith(root + os.path.sep)

def client_main(c, evt_done):
	root = c.root
	while c.keep_alive and c.active:
		req = c.read_request()
		if req is None: break
		if req['method'] != 'GET':
			c.send_error(405)
			break

		# check that url stays within the confines of the current dir
		if not sec_check(root + req['url'], root):
			c.send_error(403, "nope")
			break

		if not process_req(c, req):
			c.send_error(404)

	c.disconnect()
	evt_done.set()

