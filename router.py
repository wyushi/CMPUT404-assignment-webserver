import urllib
import urlparse
import os


def routing(route):
    route = urllib.unquote(route)
    if is_beyound_root(route):
        return None
    if route[-1:] == '/':
        route += 'index.html'
    return os.curdir + '/www' + route

def is_beyound_root(route):
    parts = route.split('/')
    map(str.strip, parts)
    parts = filter(None, parts)
    path = root = os.path.join(os.curdir, 'www')
    for part in parts:
        if part == '.':
            continue
        elif part == '..':
            if path == root:
                return True
            else:
                path = os.path.dirname(path)
        else:
            path = os.path.join(path, part)
            if os.path.exists(path):
                continue
            else:
                return True
    return False



