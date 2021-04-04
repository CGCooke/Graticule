# Graticule
Pose Network initialisation using ArUco tags.


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

## Bundle Adjustment


Notes: Need to use pip list --format=freeze > requirements.txt for requirements.