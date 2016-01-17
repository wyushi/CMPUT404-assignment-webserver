import urllib
import urlparse
import os


def routing(route):
    if route[-1:] == '/':
        route += 'index.html'
    return os.curdir + '/www' + route


