Flask-Twip
===========

A twitter API proxy extension for [Flask](http://flask.pocoo.org) microframework.


**Warning: still in a very early stage. Pull requests are welcome!**

## Know bugs

1. Only supports Override mode (well, at least for now. Will add Transparent mode if I have the time)
2. Only supports FileBackend as storage backend for OAuth access tokens (pull-requests are welcome!)


## Using Flask-Twip

Configuration file example can be found at [here](https://github.com/yegle/flask_twip/blob/master/examples/settings-example.py).

### Run test server locally

 1. `pip install -e git+git://github.com/yegle/flask_twip.git#egg=Flask-Twip`
 2. Refer to <https://github.com/yegle/flask_twip/tree/master/examples/dev>.

### Run in CGI mode

 1. Create a virtual environment using `virtualenv`
 2. Refer to <https://github.com/yegle/flask_twip/tree/master/examples/cgi>.
