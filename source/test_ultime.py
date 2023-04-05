import os
from PIL import Image
import json
import time
import tarfile

from skimage import io
import numpy as np
from cv2 import aruco
import pycopo as pcp
import matplotlib.pyplot as plt
import networkx as nx

# SETUP
image_directory = "./_dataset/"

metadata = json.load(open(image_directory + "metadata.json"))
camera_matrix = np.array(metadata["camera_matrix"])
distortion_coefficients = np.array(metadata["distortion_coefficients"])
md = float(metadata["aruco_marker_size"].split()[0])
marker_dimension = {i: md for i in range(1, 250)}
marker_size = 12.4079e-3
marker_dimension = {i: marker_size for i in range(1, 250)}

# Aruco settings
parameters = aruco.DetectorParameters()
parameters.cornerRefinementMethod = 1
parameters.cornerRefinementWinSize = 2
parameters.cornerRefinementMaxIterations = 10

target_dir = "../build/html/_images/"
files = os.listdir(target_dir)
no_gif = True
for file in files:
    if file == "imdataset.gif":  # Change the file extensions to match your image format
        no_gif = False
if no_gif:
    dir = "./_dataset"
    files = sorted([file for file in os.listdir(dir) if file.endswith(".tif")], key=lambda x: int(os.path.splitext(x)[0].split("_")[1]))
    images = []
    for file in files:
        if file.endswith(".tif"):  # Change the file extensions to match your image format
            file_path = os.path.join(dir, file)
            im = Image.open(file_path)
            width, height = im.size
            im = im.resize((int(width/2),int(height/2)))
            images.append(im)
    images[0].save(
        "../build/html/_images/imdataset.gif", save_all=True, append_images=images[1:], duration=100, loop=0
    )

print("# BATCH INTITIALIZATION")
batch = pcp.calibration.ImageBatchCalibration(
    aruco_dict=aruco.DICT_6X6_250,
    parameters=parameters,
    marker_dimension=marker_dimension,
    output_directory="./_outputs_calibration/",
    camera_matrix=camera_matrix,
    distortion_coefficients=distortion_coefficients,
)

batch.load_image_batch(directory=image_directory)

batch.detect_markers(
    plot_markers=False,
    enforce=False,
)
_ = batch.estimate_pose()

dir = "./_outputs_calibration"
contents = os.listdir(dir)
if len(contents) == 0:
    batch.draw_markers()

im = io.imread("./_outputs_calibration/img_0099_markers.jpg")
zoomed = im[950:1600, 2400:2800]

io.imshow(zoomed)

data = batch.merge_all()
MG = pcp.utils.get_multigraph(data=data)
G = pcp.utils.get_graph(data=data)

batch.get_graph_data(plot_markers=False, criterion=0.15, atomic_cycle=True, deph_max=1)

batch.graph_calibration()

batch.optimize_calibration()

batch.plot_reprojection_errors()

compo = batch.composites[-1]
compo.set_marker_reference(mk_ref=190, inplace=True)
compo.save(path="composite.json")

batch_compo = pcp.calibration.ImageBatchCompositePose(
    aruco_dict=aruco.DICT_6X6_250,
    parameters=parameters,
    output_directory="./_outputs_composite_pose/",
    camera_matrix=camera_matrix,
    distortion_coefficients=distortion_coefficients,
    # directory ="./_dataset_composite_pose/",
    directory = image_directory,
    composites={"my_compo":compo}
)

batch_compo.load_image_batch(directory=batch_compo.directory)
batch_compo.detect_markers(plot_markers=False, enforce=False)
batch_compo.estimate_composite_pose(method="pycopo", planar=True)


batch_compo.draw_markers().draw_xyz_composite(key="my_compo", dimension=0.1, thickness=5)

dir = "./_outputs_composite_pose/"
files = sorted([file for file in os.listdir(dir) if file.endswith(".jpg")], key=lambda x: int(x.split("_")[1]))
img = []
for file in files:
    if file.endswith(".jpg"):  # Change the file extensions to match your image format
        file_path = os.path.join(dir, file)
        im = Image.open(file_path)
        width, height = im.size
        im = im.resize((int(width/2),int(height/2)))
        img.append(im)
img[0].save(
    "../build/html/_images/axis_on image.gif", save_all=True, append_images=img[1:], duration=100, loop=0
)