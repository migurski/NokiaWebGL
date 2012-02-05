Nokia 3D WebGL Maps
===================

This is me experimenting with extraction of 3D data from the Nokia tiles.

``tiles.py`` requires Modest Maps (``pip install ModestMaps``), otherwise it
uses only the Python 2.6 standard library. To choose a different tile, scroll
all the way to the bottom and edit the latitude, longitude, and zoom. At the
moment, I'm stuck with the height lookup tables, getting correct height values
for Oakland but too-small values for San Francisco.

Sample usage:

    python tiles.py

Output:

    out-0.obj
    out-0.jpg
    out-1.obj
    out-1.jpg

![Sample blender image](https://raw.github.com/migurski/NokiaWebGL/master/sf-ovi-blender.gif)
