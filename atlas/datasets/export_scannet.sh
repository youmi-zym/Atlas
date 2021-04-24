# Python2.7
# imageio==2.6.0
# opencv-python==4.2.0.32
# numpy

INDEX=$1 # 0
LOGFILE=$2  # ./log.txt

# For the 1st time for data exporting:
python reader.py --root ~/data/ScanNet/scans/ --index $INDEX --log $LOGFILE --export_color_images --export_poses --export_intrinsics

# Otherwise, select depth, color, pose, intrinsic by yourself
# python reader.py --root ~/data/ScanNet/scans/ --index $INDEX --log $LOGFILE
