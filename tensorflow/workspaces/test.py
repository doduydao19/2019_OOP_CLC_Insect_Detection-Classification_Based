from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

label_map_path = "annotations/label_map.pbtxt"

def read_label_map():
    item_id = None
    item_name = None
    items = {}

    with open(label_map_path, "r") as file:
        for line in file:
            line.replace(" ", "")
            if line == "item{":
                pass
            elif line == "}":
                pass
            elif "id:" in line:
                item_id = int(line.split(":", 1)[1].strip())
            elif "name" in line:
                item_name = line.split(":", 1)[1].replace("'", "").strip()

            if item_id is not None and item_name is not None:
                items[item_name] = item_id
                item_id = None
                item_name = None

    return items  
def main(_):
    read_label_map()
    print("done")
    #generate_tfrecord('images/train_labels.csv', 'images/train', 'annotations/train.record')
    #generate_tfrecord('images/test_labels.csv', 'images/test', 'annotations/test.record')

if __name__ == '__main__':
    tf.app.run()