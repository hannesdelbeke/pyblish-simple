# pyblish-simple
A Pyblish GUI trying to be more 'intuitive' than [pyblish lite](https://github.com/pyblish/pyblish-lite) & [pyblish-qml](https://github.com/pyblish/pyblish-qml)

## Limitations
⚠️ It was designed for validating instances, and currently doesn't show context, export or publish plugins.

![](/docs/screen1.jpg)
_left pyblish_lite, right pyblish_simple_

## How to use
### Users
- Collected instances show on the left 
- Select an instance to show relevant validations in the bottom right
- Select a validation to show it's description in the top right
- right click an instance or plugin to show it's actions in the menu.

colors:
- 🟢 <span style="color: green;">green</span>: the validation passed 
- 🟠 <span style="color: orange;">orange</span>: a warning, soft fail, publishing is allowed to continue
- 🔴 <span style="color: red;">red</span>: an error, hard fail, publishing is not allowed to continue
- ⚪ <span style="color: white;">white</span>: validation did not run
- ⚫ <span style="color: grey;">grey</span>: validation is disabled but registered (NOT YET IMPLEMENTED) 

### Devs
- to hook up the `fix all` button: Give your plugins the attribute `fix`.  
Pyblish simple assumes this is a pyblish action & runs it
```python
# code in pyblish simple
if hasattr(plugin, 'fix'):
    pyblish_action = plugin.fix
    pyblish_action.process(self=pyblish_action, context=self.context, plugin=plugin)
```
- avoid context plugins, and use instance plugins instead.

## install
- copy paste the pyblish_simple module
- install the dependencies `Qt.py` & optionally `PyQt5_stylesheets`

to launch the UI, run:
```python
import pyblish_simple
pyblish_simple.show()
```


## What's pyblish simple & why was it developed? 
The standard UI for Pyblish confused artists:
- it shows which validation failed, but not which instance failed.   
e.g. Pyblish flags that a vertex is incorrect, but not which one. The artist is frustrated, because they don't know which vertex to fix.
- it shows a lot of info, overwhelming non-technical users. Artists don't find it intuitive.  

To solve this, pyblish-simple shows a list of instances.  
When you select an instance, it only shows the valiations that affected that instance.  
This UI is much more intuitive for 3D artists.
- it shows only relevant info for each instance, hiding all other validations. Making the UI less overwhelming
- It's more relatable, because a list of instances is something the 3d artist is used to.  
e.g. a list of meshes in the scene, a list of materials in the scene, the outliner in 3ds Max, Maya, Unreal, Unity, ...


## development
- [ ] improve the stylesheet. current dark mode doesn't look as nice as pyblish lite
- [ ] selected color overwrites the color, which is bad UX, fix this
- [ ] clean up the code. It's in need of some love, since it was quickly put together.
- [ ] it was designed for validating instances, and currently assumes a standard collect, validate, export, publish workflow.
  - [ ] research how to show context plugins
  - [ ] research how to show export and publish plugins

PR-s are welcome.

## community
- [Pyblish forum thread](https://forums.pyblish.com/t/pyblish-simple-a-new-ui-aimed-at-artists/701)


