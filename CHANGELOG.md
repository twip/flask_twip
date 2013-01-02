CHANGELOG
=========

## 0.0.6 (in development)

Feature update

* Mod: add log handler in CGI example code

## 0.0.5

Bugfix update

* Fix: a bug in `SQLBackend` introduced in version 0.0.4, which doesn't
  handle token re-generating properly
* Add: database initializing instruction when using under Heroku in README

## 0.0.4

Feature update

* Add: `HerokuEnvironment` and corresponding example code
* Add: HOWTO for heroku environment in README
* Add: transparent mode (experimental)
* Add: `SQLBackend` using `SQLAlchemy`
* Mod: heroku example code to use `SQLBackend`


## 0.0.3

Feature update

* Mod: CGI mode example code
* Mod: develop mode example code
* Ref: `Environment` class is now standard WSGI middleware
* Fix: several errors in the jinja template

## 0.0.2

Feature update

* Add: introduce the `Environment` class for platform-specific
  environment information extraction
* Fix: wrong link in jinja templates
* Add: `CGIEnvironment` for working with CGI mode

## 0.0.1

First working version

* Add: `FileBackend` to store OAuth tokens as files
* Add: develop server example code
