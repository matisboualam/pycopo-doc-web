import os
from PIL import Image

files = sorted(os.listdir("../"))
images = []
for file in files:
    if file.endswith(".tif"):  # Change the file extensions to match your image format
        file_path = os.path.join("../", file)
        images.append(Image.open(file_path))
images[0].save(
    "imdataset.gif", save_all=True, append_images=images[1:], duration=10, loop=0
)
