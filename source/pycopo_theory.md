(top_page-target)=
# The theory behind Pycopo

## the composite

Before going any further, let's define what we will need to have in order to use pycopo:

  + The whole process is based on the monocular vision, so obviously we will start with a camera.
  + A set of Aruco markers big enough to be detected. The marker size depends on the average distance of work (sides of 15mm for a work distance of 75 cm seems to be a good starting point).
  + Finally, our object we'll define as our composite. 
  
>**&#9432;**
>The geometry of the object needs to have plane faces on which we'll stick our Aruco markers. This requirement is essential to the good detection of the markers! 


## pinhole_camera_model

<br>

**The pinhole_camera_model** models a camera by perspective projection. It establish the link between the 3D point expressed in its own referential into a 2D point expressed in the image plan.

The transformation is characterised according to 2 types of parameters:
+ The internal camera parameters, which are
    * the principal point offset.
    * the distortion coefficient from the lens.
+ The external parameters which correspond to the rotation matrix and translation vector that rely the two referentials. These external parameters are the key to the pose estimation function.

<p align="center">
    <img src="_images/modèle_sténopé.jpg"  width="80%" height="80%">
</p>

<p align="right">
  <a href="https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html" style="font-size: 15px;">opencv_pinhole_model_camera</a>
</p>


<p align="center">
    <img src="https://i.stack.imgur.com/Wqp5X.jpg"  width="50%" height="60%">
</p>

<p align="center">
    <font size="2">A : internal camera parameters | [R,t] : Transformation matrix | M : 3D coord | m : 2D coord | &lambda; : scale factor </font>
</p>

<p align="right">
  <a href="https://math.stackexchange.com/questions/96357/coordinate-transformation-formula-for-a-pinhole-camera-model" style="font-size: 15px;">pinhole_model_camera_formula</a>
</p>

<br>

________________ 

## aruco_marker_detection

<br>

Now that we are aware of the relation between the 2D and the 3D corresponding point, the first step of the pycopo process relies on retrieving the 2D coordinates of the object we want to track in the image plan. The strategy employed in our case is to detect every marker visible on an image and store the 2D corner's coordinates associated as its id.

This step is executed using the `aruco.detect_marker()` function avaible in the opencv module.

<br>

<p align="center">
    <img src="_images/Aruco_marker_detection.JPG"  width="50%" height="60%">
</p>

<br>

Behind the function are hidding a succession of thresholding, contour detection and binary transcription which allow us to locate on the image and identify every aruco marker present in the frame.   

<p align="right">
  <a href="https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html" style="font-size: 15px;">to know more about aruco detection system</a>
</p>

________________ 

(pose_estimation-target)=
## pose_estimation

<br>

Once the marker corner's 2D coordinate stored, we will define a new virtual square with the same dimension of the marker that we are simply going to translate on (Z) axis first. The corners of this virtual square is now expressed in 3D.


<p align="center">
  <img src="_images/3d_coord_corners.jpg" width="70%" height="70%">
</p>

<br>

<p align="center">
  <img src="_images/3d_coord_corners_3d_views.JPG" width="70%" height="70%">
</p>

As the pose is characterised by its transformation matrix [R|t], the goal here is to find the matching matrix which allows us to go from the 4 virtual corners in 3D to the 4 reals corners in 2D from our marker obtained with the `aruco.detect_marker()` function.

The strategy developped in pycopo's module, initialize a first transformation matrix which allows us to project our 3D points towards their 2D expression.

Then by comparison in regard to the 2D coordinates obtained with Aruco.detectmarker() function, we can decide whether yes or no the transformation matrix is correct. The transformation matrix optimization is applied using the [least square](https://fr.wikipedia.org/wiki/M%C3%A9thode_des_moindres_carr%C3%A9s).

Here the results: 

<p align="center">
  <img src="_images/repere_marker.JPG" width="50%">
</p>

________________ 

(pose_ambiguity-target)=
## pose_ambiguity

<br>

A problem still resides in our pose estimation method. As we are working with **monocular vision**, we encouter geometrical perspective problem for long distance object detection.

<p align="center">
  <img src="_images/ambiguité_de_pose.JPG" width="100%" height="100%">
</p>

As illustrated in the figure above, two rotations are valid when it comes to determine the transformation matrix.

In order to solve the problematic, we are going to introduce **composite marker**.

________________ 

## composite_marker

<br>

What we define as composite marker is every object in which we can detect a minimum of two markers for any angle vision in which it can be observed.

Here a set of example of what can a composite marker:

<br>

<p align="center">
  <img src="_images/totem.png" width="33%" height="33%">
  <img src="_images/rock_composite.JPG" width="19%" height="19%">
</p>

<p align="center">
  <img src="_images/composite_im.jpg" width="20%" height="20%">
  <img src="_images/pendulum_im2.png" width="32%" height="32%">
</p>

<br>

Composite marker confer the benefit to present multiples aruco markers in a same frame, which will help us to create relations between their pose using [graph theory](https://en.wikipedia.org/wiki/Graph_theory#:~:text=In%20mathematics%2C%20graph%20theory%20is,also%20called%20links%20or%20lines).

________________ 

(graph_theory-target)=
## graph_theory

<br>

In pycopo module, we use graph theory in order to establish the whole possible relationship between a set of image of a composite and the markers detected in each frame. 

<p align="center">
  <img src="_images/graph_M_I.JPG" width="45%" height="45%">
</p>

In the figure above, the markers are represented by the blue points and the red ones correspond to the images. The key specifity of our image dataset is **that an image detects multiples markers and a marker can be detected in several images**.  
It allows us to build cycles in our graph as illustrated here:

<p align="center">
  <img src="_images/graph_cycle.JPG" width="40%" height="40%">
</p>

Let's focus on the &xi;0 cycle drew in green. It is composed of the following path: **{[M1;I0]->[I0;M2]->[M2;I1]->[I1;M1]}** 

***(Note that [M1,I0] refers to the matrix transformation for the marker M1 detected in the image I0 of our dataset. Additionally, remember that every marker detected in an image is associated to two transformation matrix due to pose ambiguity).***

The cycle property we use to decide weather a transformation refers to a good or bad pose is the following formulation:

> ***"If we multiply every transformation matrix associated to a good pose from a cycle following its path order until we get back to the starting point, we end up with a total transformation matrix equivalent to the Identity matrix"***

Once we know this, we submit every combination from each cycle in our graph to this condition in order to only keep the transformation that leads us to the ID matrix. *(2 poses possibility in a cycle composed of 4 transformations means: 2^4=16 combinations to test)* 

As final step to this calibration process, we rebuild our cycles using exclusively good poses transformation.

________________ 

## composite_pose_estimation

<br>

Our ultimate goal is to locate our composite regardless its orientation. The process here starts from where we ended in the [previous section](#graph_theory-target).

From the valid graph determined during the calibration phase, we define the marker the most detected in our image dataset as the reference marker **(Mref)**.

<br>

According to the different cycles in our graph we can now obtain every transformation matrix which project a point coordinate expressed in **any marker referential to the Mref referential**. The marker composite structure is now completely defined according to the reference marker referential Mref.

Finally, the pose estimation of our composite depends on:
  + Firstly, the transformation matrix that rely the **camera coordinate system to the marker detected referential.**
  + Secondly, the transformation matrix that goes from the **marker detected to the Mref referential.**

It follows the same optimization process described in the [pose_estimation section](#pose_estimation-target)taking now as argument those two transformations matrix.


  It's called the  
  <a href="https://en.wikipedia.org/wiki/Bundle_adjustment" style="font-size: 15px;">Bundle adjustment</a>
  process.
</p>

Here the results: 

<p align="center">
  <img src="_images/repere_composite.JPG" width="110%">
</p>

We invite you to familiarize yourself with the ***pycopo module*** by following the tutorial available in the Tutorial chapter of the doc.
