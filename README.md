GLCD Bitmap Converter
---------------------

A tool for converting bitmaps to C arrays for monochrome GLCDs.

Usage
-----

Use ```python converter.py -h``` to see a list of arguments.

Example
-------

The original image was converted with ```python converter.py -f sakuya.png -i --height 64 -o "sakura.h" --threshold 244``` and is shown on a TiLDA MKe.

![Original](https://github.com/DanNixon/GLCD-BitmapCOnverter/raw/master/sakuya.png "Original")
![On TiLDA MKe](https://github.com/DanNixon/GLCD-BitmapConverter/raw/master/sakuya_glcd.jpg "On TiLDA MKe")

[Image source](http://en.touhouwiki.net/wiki/File:Touhoudex_2_HSakuya.png)

Another example ```python converter.py -f soba.bmp -i --height 32 -o "soba.h"```

Changelog:
----------

* Now export to C file with format based on output name.
* *TODO* get height from image.
* *TODO* use assets folder and output folder.
