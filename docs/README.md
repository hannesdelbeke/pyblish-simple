# pyblish-simple
A more artist friendly Pyblish GUI (a bold claim)

![](/docs/screen1.jpg)
_left pyblish_lite, right pyblish_simple_

[pyblish lite](https://github.com/pyblish/pyblish-lite) & [pyblish-qml](https://github.com/pyblish/pyblish-qml) can feel confusing to artists.  
- It shows which validation failed, but not which instance. So you know a vertex is incorrect, but not which one. Good luck finding it.  
- It shows a lot of info. , overwhelming the user. It's not intuitive.  

To solve this, pyblish-simple shows a list of instances.  
When you select an instance, it only shows the valiations that affected that instance.  
This UI is much more intuitive for 3D artists.
- it shows only relevant info for each instance, hiding all other validations. Making the UI less overwhelming
- It's more relatable, because a list of instances is something the 3d artist is used to. It's similar to the outliner in 3ds Max, Maya, Unreal, Unity.


# install
copy paste the pyblish_simple module, and the dependencies Qt.py & PyQt5_stylesheets in your python environment and run:
```python
import pyblish_simple
pyblish_simple.show()
```

### development
Unlike the artist's experience, the Pyblish-Simple code does not claim to be intuitive.  
It's in need of some love, since it was quickly put together.
PR-s are welcome.
