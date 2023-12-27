# oreiller

The package for easy image manipulation. 

The package for clean Pillow codebases.

```python
from oreiller import Oreiller as orey

w, h = 220, 190
shape = [(40, 40), (w - 10, h - 10)] 

img = orey.new("RGB", (w, h)) 
orey.fill(None)
orey.oline(40, 40, w-10, h-10, width=0) # use .line for normal
img.show() 

orey.cleanup()
```

## Docs

### .new

Returns Image.new 


### .fill

Modifies fill value

### .line

Draws line without the need of ImageDraw

### .oline

Processing api of line(x1, y1, x2, y2)

## Changelog

[Emojilog 1.0](https://github.com/Abdur-rahmaanJ/emojilog)

```
0.1.0
🎉 Package skeleton
🎉 Oreiller class
🎉 .line
🎉 .oline
🔧 Fix cleanup: inform when closing closed images
```