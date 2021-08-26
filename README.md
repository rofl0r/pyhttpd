pyhttd
======

a tiny, multithreaded http server in pure python2 without external
dependencies.

about
-----

it's basically a replacement for `python -m SimpleHTTPServer` allowing
one to quickly serve contents of the current directory for file transfers
across machines, however unlike SimpleHTTPServer allows to continue file
downloads where you left off using HTTP/1.1 Ranges.

just drop the pyhttp.py somewhere in your `$PATH`, cd to the directory
you want to server and run `pyhttpd.py` and launch your browser on the other
end.

also unlike SimpleHTTPServer/BaseHTTPServer which were written in a horrible
OOP-style requiring mind-bending class inheritance by some java fanboi,
pyhttpd uses a simple and tiny procedural codebase, which can be easily
extended/modified and serve as an application server and as a replacement for
flask (which requires lots of dependencies) and other similar projects.

there's an optional script called `pyexpander.py` included in the directory
which is not required for basic functionality, but when made available
to pyhttpd, turns .html files into server pages with full python and macro
scripting facilities. see [pyexpander.rst](pyexpander.rst) for docs and
to learn what you can do with it.
pyexpander has been modified by me to use `~` instead of `$` for its
expansion facilities in order to work smoothly with embedded javascript,
and "amalgamated" into a single file.

usage
-----
just run `python2 pyhttpd.py` to serve contents of current directory
on `0.0.0.0` interface and port `8000`. if you pass a command line
argument, it's treated as a port number to use instead.

**NEW!!!!1**
pyhttpd now has an extended mode, which allows to override port, ip,
root directory, and even the main client loop of the app.
help output:

```
pyhttpd (c) 2021 rofl0r.
simple mode (zero or one argument):
pyhttpd [PORT]
        serves current directory on 0.0.0.0 port 8000, or on PORT

extended mode:
pyhttpd [OPTIONS]
        available OPTIONS:
        -i LISTENIP - specify ip to listen on
        -p PORT     - specify port to listen on
        -r ROOT     - specify root directory of webservice
        -a APP      - specify python module name for client_main()
        -A FILE     - read basic auth user:pass from FILE (use - for stdin)
```

see `helloworld.py` for how a custom app may look like, and run

    pyhttpd -a helloworld

this allows you to run your own web app without having to mess
with the code inside `pyhttpd.py`.

basic auth
----------
in order to use basic authentication to access the "built-in app",
which serves files and directory listings (if no index.html is found),
use argument `-A FILE` with a filename containing a user:pass pair
separated with a colon character. `-A -` reads the pair from stdin.
