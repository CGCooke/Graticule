from Scene import Scene, Observation
import numpy as np
from scipy.spatial.transform import Rotation as Rot


def test_Scene():
    scene = Scene('Test_data/*.jpg')
    assert scene.img_dir == 'Test_data/*.jpg'


def test_Observation():
    observation = Observation('Test_data/0.jpg', camera_id=0)
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
    assert scene.Observed_Tag_IDs == {'Tag_0', 'Tag_1', 'Tag_2', 'Tag_3'}
    assert sorted(list(scene.Tags.keys())) == ['Tag_0', 'Tag_1', 'Tag_2', 'Tag_3']


def test_set_global_origin():
    scene = Scene('Test_data/*.jpg')

    scene.load_tags()

    assert scene.origin_coordinate_system is None
    assert scene.Tags['Tag_0'].is_origin is False
    scene.set_global_origin('Tag_0')

    assert scene.origin_coordinate_system == 'Tag_0'
    assert scene.Tags['Tag_0'].is_origin is True

    assert np.allclose(scene.Tags['Tag_0'].t, np.array([[0.0], [0.0], [0.0]]))
    assert np.allclose(scene.Tags['Tag_0'].rotation.as_matrix(), np.eye(3))


def test_update_camera_coordinate_systems():
    scene = Scene('Test_data/*.jpg')
    scene.load_tags()
    scene.set_global_origin('Tag_0')

    for observation in scene.Observations:
        assert observation.Camera.t is None
        assert observation.Camera.rotation is None

    scene.update_camera_coordinate_systems()

    for observation in scene.Observations:
        if scene.origin_coordinate_system not in observation.TagObservations.keys():
            assert observation.Camera.t is None
            assert observation.Camera.rotation is None

    ground_truth = np.genfromtxt('Test_data/Camera_Locations.csv', delimiter=',', skip_header=1)

    # Check camera positions
    for observation in scene.Observations:
        if scene.origin_coordinate_system in observation.TagObservations.keys():
            image_index = int(observation.img_path.split('/')[1].split('.jpg')[0])

            [_, X, Y, Z] = ground_truth[image_index]
            t = observation.Camera.t.ravel()
            error_units = np.sqrt((X - t[0]) ** 2 + (Y - t[1]) ** 2)
            assert error_units < 1.0

    # Check camera orientations
    for observation in scene.Observations:
        if scene.origin_coordinate_system in observation.TagObservations.keys():
            image_index = int(observation.img_path.split('/')[1].split('.jpg')[0])

            R1 = observation.Camera.rotation.as_quat()

            theta_x_radians = np.radians(-130)
            theta_z_radians = np.radians(10 * image_index + 90)

            R_x = np.array([[1, 0, 0],
                            [0, np.cos(theta_x_radians), -np.sin(theta_x_radians)],
                            [0, np.sin(theta_x_radians), np.cos(theta_x_radians)]])

            R_z = np.array([[np.cos(theta_z_radians), -np.sin(theta_z_radians), 0],
                            [np.sin(theta_z_radians), np.cos(theta_z_radians), 0],
                            [0, 0, 1]])

            R_composed = np.dot(R_z, R_x)
            R2 = Rot.from_matrix(R_composed).as_quat()

            assert np.dot(R1, R2) > 0.99


def test_update_tag_coordinate_systems():
    scene = Scene('Test_data/*.jpg')
    scene.load_tags()
    scene.set_global_origin('Tag_0')
    scene.update_camera_coordinate_systems()
    scene.update_tag_coordinate_systems()

    ground_truth = np.genfromtxt('Test_data/Tag_Locations.csv', delimiter=',', skip_header=1)

    # Check tag positions
    for tag_id in scene.Tags.keys():
        Tag = scene.Tags[tag_id]
        [_, X, Y, Z] = ground_truth[int(tag_id[4:])]

        t = Tag.t.ravel()
        error_units = np.sqrt((X - t[0]) ** 2 + (Y - t[1]) ** 2)
        assert error_units < 1.0

    # Check tag orientations
    for tag_id in scene.Tags.keys():
        Tag = scene.Tags[tag_id]

        R1 = Tag.rotation.as_quat()
        R2 = Rot.from_matrix(np.eye(3)).as_quat()
        assert np.dot(R1, R2) > 0.99


test_update_tag_coordinate_systems()
