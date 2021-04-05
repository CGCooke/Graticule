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
* Detect tags
* Find orientation of tags w.r.t camera
* Set a tag as the origin image coordinate system
* Orientate the other tags in the image to the origin tag
* Set one tag as a global origin 
* Add an image which shares one or more tags
* Perform bundle adjustment
* Repeat


***

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

***


## Bundle Adjustment

Fundamentally, the bundle adjustment is performed by scipy.optimize.least_squares.

`scipy.optimize.least_squares(fun = bundle_adjustment_function, x0 = x0, jac_sparsity = jac_sparsity_matrix, args = bundle_adjustment_function_args)`

Fundamentally, we need to provide it with 4 things.

1. A function which computes the vector of residuals (bundle_adjustment_function).
2. An initial estimate of the independent variables (x0).
3. An array defining the sparsity structure of the jacobian matrix (jac_sparsity_matrix). 
4. Arguments passed to our function bundle_adjustment_function (bundle_adjustment_function_args).


***

Notes: Need to use pip list --format=freeze > requirements.txt for requirements.