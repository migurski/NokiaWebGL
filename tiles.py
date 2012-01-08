from sys import argv, stderr
from math import log, pow, pi, ceil

from ModestMaps.Geo import Location, MercatorProjection, deriveTransformation
from ModestMaps.Providers import IMapProvider
from ModestMaps.Core import Coordinate

def fromNokia(x, y, zoom):
    """ Return column, row, zoom for Nokia x, y, z.
    """
    row = int(pow(2, zoom) - y - 1)
    col = x
    return col, row, zoom

def toNokia(col, row, zoom):
    """ Return x, y, z for Nokia tile column, row, zoom.
    """
    x = col
    y = int(pow(2, zoom) - row - 1)
    return x, y, zoom

class BadZoom (Exception): pass

class Provider (IMapProvider):
    
    def __init__(self):
        # the spherical mercator world tile covers (-π, -π) to (π, π)
        t = deriveTransformation(-pi, pi, 0, 0, pi, pi, 1, 0, -pi, -pi, 0, 1)
        self.projection = MercatorProjection(0, t)

    def getTilePath(self, coord):
        x, y, z = toNokia(int(coord.column), int(coord.row), int(coord.zoom))
        
        #
        # maximum number of digits in row or column at this zoom
        # and a zero-padded string format for integers.
        #
        len = ceil(log(2 ** z) / log(10))
        fmt = '%%0%dd' % len
        
        row, col = fmt % y, fmt % x
        
        if len == 4:
            dir = '%s%s/%s%s' % (row[0:2], col[0:2], row[2:3], col[2:3])
        elif len == 5:
            dir = '%s%s/%s%s' % (row[0:2], col[0:2], row[2:4], col[2:4])
        elif len == 6:
            dir = '%s%s/%s%s/%s%s' % (row[0:2], col[0:2], row[2:4], col[2:4], row[4:5], col[4:5])
        else:
            raise BadZoom('len = %d unsupported' % len)
        
        return '%(z)d/%(dir)s/map_%(z)d_%(y)d_%(x)d' % locals()
    
    def getTileServer(self, coord):
        return 'bcde'[int(coord.row + coord.column + coord.zoom) % 4]
    
    def getTileUrls(self, coord):
        server, path = self.getTileServer(coord), self.getTilePath(coord)
        
        return 'http://%(server)s.maps3d.svc.nokia.com/data4/%(path)s_0.jpg' % locals()

if __name__ == '__main__':

    p = Provider()
    l = Location(37.804310, -122.271164)
    z = 18
    
    print p.getTileUrls(p.locationCoordinate(l).zoomTo(z))
    