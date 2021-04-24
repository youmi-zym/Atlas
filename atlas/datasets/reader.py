import argparse
import os, sys

from SensorData import SensorData

import re

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """
    Turn a string into a list of string and number chunks.
    'z23a' -> ['z', 23, a]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]

def sort_nicely(l):
    l.sort(key=alphanum_key)

# params
parser = argparse.ArgumentParser()
# data paths
parser.add_argument('--root', required=True, help='path to DIR, e.g., /path/to/scans, scans_test and so on')
parser.add_argument('--index', required=True, type=int,  help='ID from $index sense will be read, e.g., setting 2 means all senses(order in alphabet) from 2 will be read ')
parser.add_argument('--log', type=str, default="./log.txt", help="data exporting log file path")
parser.add_argument('--export_depth_images', dest='export_depth_images', action='store_true')
parser.add_argument('--export_color_images', dest='export_color_images', action='store_true')
parser.add_argument('--export_poses', dest='export_poses', action='store_true')
parser.add_argument('--export_intrinsics', dest='export_intrinsics', action='store_true')
parser.set_defaults(export_depth_images=False, export_color_images=False, export_poses=False, export_intrinsics=False)

opt = parser.parse_args()

with open(opt.log, 'w') as fp:
    fp.write("Begin recording!\n")

def stdout(s):
    with open(opt.log, 'a') as fp:
        fp.write(s)
    print(s)

stdout("{}\n".format(opt))



def main():
    if not os.path.exists(opt.root):
        stdout("{} not exist, exit\n".format(opt.root))
        return
    root = opt.root
    fileNames = os.listdir(root)
    fileNames = [name for name in fileNames if name.find('scene') > -1]
    stdout("Found {} scenes in {}\n".format(len(fileNames), root))
    sort_nicely(fileNames)

    for i, filename in enumerate(fileNames):
        if i < opt.index:
            continue
        stdout("process {}th sense\n".format(i))
        # set output path
        output_path = os.path.join(root, filename)
        stdout("output path is {}\n".format(output_path))

        # filename renamed, load the data
        filename = os.path.join(root, filename, filename+'.sens')
        stdout("loading {} ... \n".format(filename))

        sd = SensorData(filename)
        stdout('loaded!\n')

        if opt.export_depth_images:
            sd.export_depth_images(os.path.join(output_path, 'depth'))
            stdout("depth read\t")
        if opt.export_color_images:
            sd.export_color_images(os.path.join(output_path, 'color'))
            stdout("color readed\t")
        if opt.export_poses:
            sd.export_poses(os.path.join(output_path, 'pose'))
            stdout("pose readed\t")
        if opt.export_intrinsics:
            sd.export_intrinsics(os.path.join(output_path, 'intrinsic'))
            stdout("intrinsic readed\t")

        stdout('\n')


if __name__ == '__main__':
    main()
    stdout("Done!")
