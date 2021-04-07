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
from scipy.spatial.transform import Rotation as Rot

class Pose(object):
	"""docstring for Pose"""
	def __init__(self):
		self.rotation = None
		self.t = None
		self.coordinate_system = None

class Scene(object):
	"""docstring for Scene"""
	def __init__(self, img_dir):
		self.img_dir = img_dir
		self.Observed_Tag_IDs = set()
		self.Observations = []

	def load_tags(self):
		for camera_id, f_str in enumerate(sorted(glob.glob('Test_data/*.jpg'))):
			observation = Observation(f_str, camera_id = camera_id)
			observation.extract_tags()
			self.Observations.append(observation)			
			for tag in observation.TagObservations:
				self.Observed_Tag_IDs.add(tag.tag_id)

class Tag(Pose):
	"""docstring for Tag"""
	def __init__(self):
		Pose.__init__(self)
		self.tag_id = None

class Observation(object):
	"""docstring for Observation"""
	def __init__(self, img_path, camera_id):
		self.img_path = img_path
		self.camera_id = camera_id
		self.Camera = Camera(camera_id)
		self.TagObservations = []

	def extract_tags(self):
		marker_size = 1.2 #units
		points_3d = np.array([[0.0,marker_size,0.0],
		                      [marker_size,marker_size,0.0],
		                      [marker_size,0.0,0.0],
		                      [0.0,0.0,0.0]])

		points_3d[:,0:2] -= marker_size/2.0

		arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
		arucoParams = cv2.aruco.DetectorParameters_create()

		img = cv2.imread(self.img_path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # change img to grayscale
		
		(corners, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters = arucoParams)
		
		for tag_corners, tag_id in zip(corners, ids):
			points_2d = tag_corners.squeeze()
			R, t = self.find_tag_pose(points_3d, points_2d)

			tag_observation = TagObservation(f'Tag_{int(tag_id)}')
			tag_observation.rotation = R
			tag_observation.t = t
			tag_observation.coordinate_system = f'Camera_{self.camera_id}'
			self.TagObservations.append(tag_observation)

	def find_tag_pose(self, points_3d, points_2d):
		K = self.Camera.K
		dist = self.Camera.dist

		ret, rvec, tvec = cv2.solvePnP(objectPoints = points_3d, imagePoints = points_2d, cameraMatrix = K, distCoeffs = dist, flags = cv2.SOLVEPNP_IPPE_SQUARE)

		#Find tag R & t wrt camera.
		R = Rot.from_rotvec(rvec[:,0])
		t = np.array(tvec)
		return(R,t)
		
		#Find Camera C & R wrt tag.
		#C = -np.dot(R.T,tvec)
		#R = Rot.from_matrix(R.T).as_matrix()

class CameraIntrinsics(object):
	"""docstring for CameraIntrinsics"""
	def __init__(self):
		focal_length_mm = 50 #mm
		width_pixels = 800.0
		height_pixels = 600.0
		width_mm = 36.0
		pixels_per_mm = width_pixels/width_mm
		focal_length_pixels = pixels_per_mm * focal_length_mm

		self.K = np.array([[focal_length_pixels, 0.0 , width_pixels/2],
					  [0.0   , focal_length_pixels, height_pixels/2],
					  [0.0   , 0.0   ,    1.0]])

		self.dist = np.array([[0],[0],[0],[0],[0]])

class Camera(Pose, CameraIntrinsics):
	"""docstring for Camera"""
	def __init__(self, camera_id):
		Pose.__init__(self)
		CameraIntrinsics.__init__(self)
		self.camera_id = camera_id

class TagObservation(Pose):
	"""docstring for TagObservation"""
	def __init__(self, tag_id):
		Pose.__init__(self)
		self.tag_id = tag_id



		

		
		