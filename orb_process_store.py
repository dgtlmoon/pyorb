from skimage import data
from skimage import transform as tf
from skimage import io
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
from skimage import filters
from StringIO import StringIO
import Image
import tempfile
import struct
import numpy as np
import cv2
import pickle
import os

keypoints = 200



# Given an image, process it with ORB extraction and save the descriptors
def processDescriptorsFromImage(img_str, id_tag):

    # @todo load img_str directly into data.imread somehow
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(img_str)
    f.close()

    # Read and convert to greyscale, apply gaussian blur
    img1 = filters.gaussian(data.imread(f.name, True), sigma=1)
    descriptor_extractor = ORB(n_keypoints=keypoints, fast_n=122)
    descriptor_extractor.detect_and_extract(img1)

    p = []

    if os.path.isfile("data.bin"):
        p = pickle.load(open("data.bin", "rb"))

    p.append({"id": id_tag, "descriptors": descriptor_extractor.descriptors})

    with open('data.bin', 'wb') as handle:
        pickle.dump(p, handle)

# @todo
# experimental, each pickle is about 200kb :( use our own file format? 51kb per entry? keypoints*256, still not good
#    with open("test.bnr", "a") as f:
#        for descriptor in descriptors:
#            # Pack 8 bits to a int8 and append
#            f.write( np.packbits(np.uint8(descriptor)) )
#    f.close()


# Given a image string, find the best match in our stored data
def search(img_str):

    # @todo load img_str directly into data.imread somehow
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(img_str)
    f.close()


    # Read and convert to greyscale, apply gaussian blur
    img1 = filters.gaussian(data.imread(f.name, True), sigma=1)
    descriptor_extractor = ORB(n_keypoints=keypoints, fast_n=122)
    descriptor_extractor.detect_and_extract(img1)


    p = pickle.load(open("data.bin", "rb"))
    matches = []

    # Build a list dict based on the number of matches
    # @todo having to scan the whole stored dataset doesnt feel right?
    for entry in p:
        x = match_descriptors(descriptor_extractor.descriptors, entry['descriptors'], cross_check=True)
        if(len(x)> 65):
            print entry['id']
            print len(x);

