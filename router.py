import urllib
import urlparse
import os


def routing(route):
    # print 'route: ' + route
    # if is_beyound_root(route):
    #     return None
    if route[-1:] == '/':
        route += 'index.html'
    return os.curdir + '/www' + route

# def is_beyound_root(route):
#     parts = route.split('/')
#     print parts
#     map(str.strip, parts)
#     parts = filter(None, parts)
#     print parts
#     return True



