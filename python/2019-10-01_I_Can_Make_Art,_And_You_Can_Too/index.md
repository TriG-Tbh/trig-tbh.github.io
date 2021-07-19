[Main Page](/) / [Python Projects](/python) / [I Can Make Art, And You Can Too](/python/2019-10-01_I_Can_Make_Art,_And_You_Can_Too)

# I Can Make Art, And You Can Too

## Date: 2019-10-01

I've always wanted to make art, but I've never been particularly *good* at art.

While playing around with PIL, I was wondering what it would look like for an image to be built pixel-by-pixel.

I wanted to make a program that would start at the top left of an image with a set color, then slightly modify the surrounding pixels.

The pixels surrounding *those* pixels would average and slightly modify the colors of all non-blank surrounding pixels.

This process would repeat over and over until the entire image was procedurally created.

The result is a left-to-right, top-to-bottom gradient with streaks that make it look as if the image was hand-drawn with a crayon.

It should be noted - "seed" in the program is the exact opposite of what a seed does to randomness.

Included with this is a 1920x1080 picture (demo.png) that shows what this program is capable of.

-----

## Files

[demo.png](demo.png)

[formats.py](formats.py)

[functions.py](functions.py)

[greyscale.py](greyscale.py)

[main.py](main.py)