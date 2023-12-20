# Metody biometryczne
# Przemyslaw Pastuszka

from PIL import Image, ImageDraw
import utils
import argparse
import math
import os
import numpy as np
from tqdm import tqdm

signum = lambda x: -1 if x < 0 else 1

cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

def find_rectangle_coordinates(x_coordinates, y_coordinates):
    n = len(x_coordinates)
    if len(x_coordinates) == 2 and len(y_coordinates) == 2:
        return (sum(x_coordinates)/2, sum(y_coordinates)/2)

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = x_coordinates[i], y_coordinates[i]
            x2, y2 = x_coordinates[j], y_coordinates[j]

            # Calculate the other two points to form a rectangle
            x3, y3 = x2 + (y2 - y1), y2 - (x2 - x1)
            x4, y4 = x1 + (y2 - y1), y1 - (x2 - x1)

            # Check if the other two points are present in the given coordinates
            if (x3 in x_coordinates) and (y3 in y_coordinates) and (x4 in x_coordinates) and (y4 in y_coordinates):
                # return [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                return ((x1 + x3)/2, (y2 + y4)/2)
    return (0, 0)
    

def get_angle(left, right):
    angle = left - right
    if abs(angle) > 180:
        angle = -1 * signum(angle) * (360 - abs(angle))
    return angle

def poincare_index_at(i, j, angles, tolerance):
    deg_angles = [math.degrees(angles[i - k][j - l]) % 180 for k, l in cells]
    index = 0
    for k in range(0, 8):
        if abs(get_angle(deg_angles[k], deg_angles[k + 1])) > 90:
            deg_angles[k + 1] += 180
        index += get_angle(deg_angles[k], deg_angles[k + 1])

    if 180 - tolerance <= index and index <= 180 + tolerance:
        return "loop"
    if -180 - tolerance <= index and index <= -180 + tolerance:
        return "delta"
    if 360 - tolerance <= index and index <= 360 + tolerance:
        return "whorl"
    return "none"

def calculate_singularities(im, angles, tolerance, W):
    (x, y) = im.size
    # result = im.convert("RGB")

    # draw = ImageDraw.Draw(result)

    colors = {"loop" : (150, 0, 0), "delta" : (0, 150, 0), "whorl": (0, 0, 150)}
    center_x = []
    center_y = []
    for i in range(1, len(angles) - 1):
        for j in range(1, len(angles[i]) - 1):
            singularity = poincare_index_at(i, j, angles, tolerance)
            if singularity != "none":
                # draw.ellipse([(i * W, j * W), ((i + 1) * W, (j + 1) * W)], outline = colors[singularity])
                if singularity == "loop":
                    center_x.append((i * W + (i+1)*W)/2)
                    center_y.append((j * W + (j+1)*W)/2)

    return find_rectangle_coordinates(center_x, center_y)

# parser = argparse.ArgumentParser(description="Singularities with Poincare index")
# parser.add_argument("image", nargs=1, help = "Path to image")
# parser.add_argument("block_size", nargs=1, help = "Block size")
# parser.add_argument("tolerance", nargs=1, help = "Tolerance for Poincare index")
# parser.add_argument('--smooth', "-s", action='store_true', help = "Use Gauss for smoothing")
# parser.add_argument("--save", action='store_true', help = "Save result image as src_poincare.gif")
# args = parser.parse_args()

image_names4 = os.listdir('D:/Academics_4th_year/7th_sem/CS663/DB3_B_one_to_four')
image_names4.sort()

singularPoint_4 = (-1) * np.ones((80, 2))
i = 0
for images in tqdm(image_names4):
    if int(images[4:5]) > 4:
        continue
    im = Image.open('D:/Academics_4th_year/7th_sem/CS663/DB3_B_one_to_four/' + images)
    im = im.convert("L")  # covert to grayscale
    W = 16

    f = lambda x, y: 2 * x * y
    g = lambda x, y: x ** 2 - y ** 2

    angles = utils.calculate_angles(im, W, f, g)
    angles = utils.smooth_angles(angles)

    (a, b) = calculate_singularities(im, angles, 1, W)
    singularPoint_4[i,0] = a
    singularPoint_4[i, 1] = b
    print(images)
    print(a,b)
    i = i+1
np.save('cores_3_1234.npy', singularPoint_4)





# if args.save:
#     base_image_name = os.path.splitext(os.path.basename(args.image[0]))[0]
#     result.save(base_image_name + "_poincare.gif", "GIF")
