'''
## Scene management

A captured scene can be described using a hierarchy of objects.

### Scene
A collection of photos and tags.

#### Tag
A tag, with a position, orientation, and ID.
* Coordinate System

#### Observation
An observation/image taken by a camera, which observed (0) or more tags.

##### Camera
A camera, with associated intrinsic and extrinsic parameters.

###### Camera Intrinsics
Parameters internal to the camera. 

###### Camera Extrinsics
The position and orientation of the camera.
* Coordinate System

##### Tag Observation
The position, orientation, and ID of a tag, as observed by the camera.
* Coordinate System
'''


class Scene(object):
	"""docstring for Scene"""
	def __init__(self, arg):
		self.arg = arg


class Observation(object):
	"""docstring for Observation"""
	def __init__(self, arg):
		self.arg = arg


class Camera(object):
	"""docstring for Camera"""
	def __init__(self, arg):
		self.arg = arg


class Tag(object):
	"""docstring for Tag"""
	def __init__(self, arg):
		self.arg = arg


class CoordinateSystem(object):
	"""docstring for CoordinateSystem"""
	def __init__(self, arg):
		self.arg = arg
		
		