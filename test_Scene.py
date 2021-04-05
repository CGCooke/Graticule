from Scene import Scene
import cv2

def test_Scene():
	scene = Scene('Test_data/*.jpg', aruco_tag_type = cv2.aruco.DICT_4X4_50)