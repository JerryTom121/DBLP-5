# -*- coding: utf-8 -*-
#
#
# Define the tool that will be used for other program.
#
import os
import time
import json
from logger import Logger

log = Logger.get_logger("utils")


def name_without_extension(path):
    """get the file name without extension."""
    return os.path.splitext(path)[0]


def read_txt(path):
    """read text file from path."""
    with open(path, "r") as f:
        return f.readlines()


def read_json(path):
    """read json file from path."""
    with open(path, 'r') as f:
        return json.load(f)


def build_result_folder(timestamp=str(int(time.time()))):
    """build folder for the running result."""
    out_path = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
    log.info("Writing to {}\n".format(out_path))

    data_path = os.path.abspath(os.path.join(out_path, "data"))
    evaluation_path = os.path.abspath(os.path.join(out_path, "evaluation"))

    if not os.path.exists(out_path):
        os.makedirs(data_path)
        os.makedirs(evaluation_path)
    return out_path
