Flask-Twip
===========

A twitter API proxy extension for [Flask](http://flask.pocoo.org) microframework.


## Know bugs

1. Only supports Override mode (well, at least for now. Will add Transparent mode if I have the time)
2. Only supports FileBackend as storage backend for OAuth access tokens (pull-requests are welcome!)


## Using Flask-Twip

Configuration file example can be found at [here](https://github.com/yegle/flask_twip/blob/master/examples/settings-example.py).

### Run test server locally

For developers.

 1. `pip install -e git+git://github.com/yegle/flask_twip.git#egg=Flask-Twip`
 2. Refer to <https://github.com/yegle/flask_twip/tree/master/examples/dev>.

### Run in CGI mode

CGI is supported on most web hosting servers.

 1. Create a virtual environment using `virtualenv`
 2. Install `Flask-Twip` using `pip install Flask-Twip`
 3. Refer to <https://github.com/yegle/flask_twip/tree/master/examples/cgi>.

### Run on Heroku

Heroku is a widely used PaaS platform.

 1. Create a heroku project. Refer to Heroku's docs if you don't know how to.
 2. Add dev DB server to this project. Run `heroku addons:add heroku-postgresql:dev` in the root directory of your project
 3. Copy files in <https://github.com/yegle/flask_twip/tree/master/examples/heroku> to your project directory
 4. Push your project to heroku.
