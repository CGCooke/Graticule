from Scene import Scene, Observation, Camera, TagObservation
import glob
import cv2
import numpy as np

def test_Scene():
	scene = Scene('Test_data/*.jpg')
	assert scene.img_dir == 'Test_data/*.jpg'

def test_Observation():
	observation = Observation('Test_data/0.jpg', camera_id = 0)
	observation.extract_tags()

	for observation in observation.TagObservations:
		if observation.tag_id == 'Tag_0':
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