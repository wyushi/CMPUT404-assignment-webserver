import urllib
import urlparse


def routing(route):
    print 'route:'
    print route
    if route[-1:] == '/':
        route += 'index.html'
    return '/www' + urllib.url2pathname(route)