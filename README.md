Flask-Twip
===========

A twitter API proxy extension for [Flask](http://flask.pocoo.org) microframework.


## Know bugs

1. Only supports Override mode (well, at least for now. Will add Transparent mode if I have the time)

## TODO

1. Test transparent mode with [Hotot](http://www.hotot.org)
2. Convert this README into reStructuredText and display it on PyPI
3. Documentation about customized deployment

## Features

 1. Support multiple platforms
    1. CGI on virtual hosts
    2. Heroku
    3. Run as a `WSGI` server
 2. Support multiple mode
    1. Override Mode: override OAuth signatures from clients
    2. Transparent Mode: passing all HTTP paramters onto Twitter (still experimenting)
 3. Support multiple storage backend
    1. `FileBackend`
    2. `SQLBackend` (using `SQLAlchemy`)

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

In order for the dev DB server to work, you need an extra step to init the database

 1. Run `herku run python`
 2. Type the following Python code

```python
from app import be
be.init_db()
```

You only need to init your database the first time you setup `Flask-Twip`

## Contributors

* [yegle](https://github.com/yegle)

## Tips

Gratuity greatly appreciated but not necessary. <https://www.gittip.com/yegle/>

---

Project is a member of the [OSS Manifesto](http://ossmanifesto.org/)
