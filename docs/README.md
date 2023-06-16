# pyblish-simple
A Pyblish GUI with a more artist friendly UX

![](/docs/screen1.jpg)
_left pyblish_lite, right pyblish_simple_

## What's pyblish simple & why was it developed? 
The standard UI for Pyblish ([pyblish lite](https://github.com/pyblish/pyblish-lite) & [pyblish-qml](https://github.com/pyblish/pyblish-qml)) confused artists:
- The standard UI shows which validation failed, but not which instance failed.   
e.g. Pyblish flags that a vertex is incorrect, but not which one. The artist is frustrated, because they don't know which vertex to fix.
- The standard UI shows a lot of info, overwhelming non-technical users. Artists don't find it intuitive.  

To solve this, pyblish-simple shows a list of instances.  
When you select an instance, it only shows the valiations that affected that instance.  
This UI is much more intuitive for 3D artists.
- it shows only relevant info for each instance, hiding all other validations. Making the UI less overwhelming
- It's more relatable, because a list of instances is something the 3d artist is used to. It's similar to the outliner in 3ds Max, Maya, Unreal, Unity.

## How to use
- A list of collected instances shows on the left 
- When you select an instance, the validations that ran on this instance show on the right.
- When you select a validation, the validation's description load's on the top right
- color guide for validations & instances
  - 🟢 <span style="color: green;">green</span>: the validation passed 
  - 🟠 <span style="color: orange;">orange</span>: a warning, soft fail, publishing is allowed to continue
  - 🔴 <span style="color: red;">red</span>: an error, hard fail, publishing is not allowed to continue
  - ⚪ <span style="color: white;">white</span>: validation did not run
  - ⚫ <span style="color: grey;">grey</span>: validation is disabled but registered (NOT YET IMPLEMENTED) 

## install
- copy paste the pyblish_simple module
- install the dependencies `Qt.py` & `PyQt5_stylesheets`

to launch the UI, run:
```python
import pyblish_simple
pyblish_simple.show()
```

## development
- [ ] improve the stylesheet. current dark mode doesn't look as nice as pyblish lite
- [ ] selected color overwrites the color, which is bad UX, fix this
- [ ] clean up the code. It's in need of some love, since it was quickly put together.

PR-s are welcome.

## community
- [Pyblish forum thread](https://forums.pyblish.com/t/pyblish-simple-a-new-ui-aimed-at-artists/701)


