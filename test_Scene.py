from Scene import Scene, Observation, Camera, TagObservation
import glob
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as Rot

import matplotlib.pyplot as plt

def test_Scene():
	scene = Scene('Test_data/*.jpg')
	assert scene.img_dir == 'Test_data/*.jpg'

def test_Observation():
	observation = Observation('Test_data/0.jpg', camera_id = 0)
	observation.extract_tags()

	observation = observation.TagObservations['Tag_0']
	assert observation.coordinate_system == 'Camera_0'			
	assert np.allclose(observation.t, np.array([[-3.3121481], [-3.51199432], [20.23151067]]))
	assert np.allclose(observation.rotation.as_rotvec(), np.array([1.69683488, 1.6904307, -0.79607287]))
	assert observation.tag_id == 'Tag_0'

def test_Multiple_Observations():
	scene = Scene('Test_data/*.jpg')
	scene.load_tags()
	assert len(scene.Observations) == 36
	assert scene.Observed_Tag_IDs == set({'Tag_0', 'Tag_1', 'Tag_2', 'Tag_3'})

def test_Multiple_Observations():
	scene = Scene('Test_data/*.jpg')
	scene.load_tags()
	assert len(scene.Observations) == 36
	assert scene.Observed_Tag_IDs == set({'Tag_0', 'Tag_1', 'Tag_2', 'Tag_3'})
	assert sorted(list(scene.Tags.keys())) == ['Tag_0', 'Tag_1', 'Tag_2', 'Tag_3']
	
def test_set_global_origin():
	scene = Scene('Test_data/*.jpg')
	
	scene.load_tags()
	
	assert scene.origin_coordinate_system == None
	assert scene.Tags['Tag_0'].is_origin == False
	scene.set_global_origin('Tag_0')

	assert scene.origin_coordinate_system == 'Tag_0'
	assert scene.Tags['Tag_0'].is_origin == True

	assert np.allclose(scene.Tags['Tag_0'].t,np.array([[0.0], [0.0], [0.0]]))
	assert np.allclose(scene.Tags['Tag_0'].rotation.as_matrix(), np.eye(3))

def test_update_camera_coordinate_systems():
	scene = Scene('Test_data/*.jpg')
	scene.load_tags()
	scene.set_global_origin('Tag_0')

	for observation in scene.Observations:
		assert observation.Camera.t == None
		assert observation.Camera.rotation == None
	
	scene.update_camera_coordinate_systems()

	for observation in scene.Observations:
		if scene.origin_coordinate_system not in observation.TagObservations.keys():
			assert observation.Camera.t == None
			assert observation.Camera.rotation == None

	
	ground_truth = np.genfromtxt('Test_data/Camera_Locations.csv',delimiter=',',skip_header=1)

	for observation in scene.Observations:
		if scene.origin_coordinate_system in observation.TagObservations.keys():			
			image_index = int(observation.img_path.split('/')[1].split('.jpg')[0])
			
			[i, X, Y, Z] = ground_truth[image_index ]
			t = observation.Camera.t.ravel()

			error_units = np.sqrt((X-t[0])**2+(Y-t[1])**2)
			assert error_units < 1.0

	



