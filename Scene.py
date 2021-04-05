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

import glob
import numpy as np
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from scipy.spatial.transform import Rotation as Rot
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix


class Scene(object):
	"""docstring for Scene"""
	def __init__(self, img_dir, aruco_tag_type):
		self.img_dir = img_dir
		self.aruco_tag_type = aruco_tag_type
		self.Tags = []
		self.Observations = []


class Tag(object):
	"""docstring for Tag"""
	def __init__(self):
		pass

class Observation(object):
	"""docstring for Observation"""
	def __init__(self, img_path):
		self.img_path = []
		self.Camera = Camera()
		self.TagObservations = []

	def extract_tags(self):
		pass
		
class Camera(object):
	"""docstring for Camera"""
	def __init__(self):
		pass

class TagObservation(object):
	"""docstring for TagObservation"""
	def __init__(self):
		pass

class Pose(object):
	"""docstring for Pose"""
	def __init__(self):
		pass
		
		