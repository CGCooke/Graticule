# Graticule
Pose Network initialisation using ArUco tags.


***

## Introduction

Given a set of images, which contain observations of ArUCo tags, how can we determine the relative position of both the cameras and the tags?


Essentially we have two phases.

1. Collecting a set of observations.
2. Combining these observations into a coherent, global view.

***

## Algorithm Overview
* Detect tags :white_check_mark:
* Find orientation of tags w.r.t camera :white_check_mark:
* Set one tag as a global origin :white_check_mark:
* Add an image which shares one or more tags  :white_check_mark:
* Position/Orientate the new camera to w.r.t origin  :white_check_mark:
* Position/Orientate new, previously unseen tags w.r.t origin  :white_check_mark:
* Perform bundle adjustment
* Re-orient origin tag back to origin
* Repeat


***

## Scene management
A captured scene can be described using a hierarchy of objects.

### Scene
A collection of photos and tags.

#### Tag
A tag, with a position, orientation, and ID.
* Pose

#### Observation
An observation/image taken by a camera, which observed (0) or more tags.

##### Camera
A camera, with associated intrinsic and extrinsic parameters.

###### Camera Intrinsics
Parameters internal to the camera. 

###### Camera Extrinsics
The position and orientation of the camera.
* Pose

##### Tag Observation
The position, orientation, and ID of a tag, as observed by the camera.
* Pose

***

## Global Orientation

* Set one tag as a global origin :white_check_mark:
* Find cameras which can observe this tag :white_check_mark:
* Update camera locations :white_check_mark:
* Update associated tags :white_check_mark:

***


## Bundle Adjustment

Fundamentally, the bundle adjustment is performed by scipy.optimize.least_squares.

`scipy.optimize.least_squares(fun = bundle_adjustment_function, x0 = x0, jac_sparsity = jac_sparsity_matrix, args = bundle_adjustment_function_args)`

We need to create:

1. A function which computes the vector of residuals (bundle_adjustment_function).
2. An initial estimate of the independent variables (x0).
3. An array defining the sparsity structure of the jacobian matrix (jac_sparsity_matrix). 
4. Arguments passed to our function bundle_adjustment_function (bundle_adjustment_function_args).


State Vector Format:
:camera::camera::triangular_flag_on_post::triangular_flag_on_post::triangular_flag_on_post:




***

Notes: Need to use pip list --format=freeze > requirements.txt for requirements.