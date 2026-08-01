"""
Compress raw camera tiff frames into videos and compute global motion energy.

Script version of video_compress_moten.ipynb, meant to be kicked off on a
server via ssh + nohup for long overnight runs, e.g.:

    nohup python video_compress_moten.py > video_compress_moten.log 2>&1 &

Parameters are hardcoded below (same as the notebook) - edit them directly
in this file if needed.
"""

import cv2
import os
import re
import numpy as np

# continue going one folder up as long as folder name is not 'photostim_deve'
while os.path.basename(os.getcwd()) != 'photostim_deve':
    os.chdir('..')

move_deve_path = os.getcwd()

experimenter = 'jm'
data_raw_dir = 'data_raw/'
data_vid_dir = 'data_vid/'
data_proc_dir = 'data_proc/'

subjects_to_run = ['jm064', 'jm065', 'jm067', 'jm073', 'jm074', 'jm075', 'jm083', 'jm084', 'jm089']  # list of subject names to process (empty list = run all)

fps = 30  # Frames per second (nominal, actual rate varies frame to frame)

# filenames look like: img00001_cam0_strftime33686577.tiff
# the 'strftime' number is a monotonic counter; based on the frame-to-frame
# differences (~3.3e7 units at ~30 Hz) it is assumed to be in nanoseconds
frame_ts_pattern = re.compile(r'_strftime(\d+)\.tiff$')
tstamp_unit_to_sec = 1e-9

# get all 'input folders'

all_subject_dirs = sorted(os.listdir(data_raw_dir + experimenter))
# remove if not a directory
all_subject_dirs = [x for x in all_subject_dirs if os.path.isdir(data_raw_dir + experimenter + '/' + x)]

if subjects_to_run:
    all_subject_dirs = [x for x in all_subject_dirs if x in subjects_to_run]

all_camera_dir = []  # this is where the single frame tiffs live
all_vid_path = []  # this is where we will save the videos
all_proc_dir = []  # this is where we will save tstamps / interframe_int / motion_energy_glob

for subject_dir in all_subject_dirs:
    # get all subdirectories that end with _a
    all_session_dirs = sorted(os.listdir(data_raw_dir + experimenter + '/' + subject_dir))
    # now only take ones that end with '_a'
    all_session_dirs = [x for x in all_session_dirs if x[-2:] == '_s']

    # now if a session has a camera folder, add it to the list
    for session_dir in all_session_dirs:
        if os.path.isdir(data_raw_dir + experimenter + '/' + subject_dir + '/' + session_dir + '/camera'):
            all_camera_dir.append(data_raw_dir + experimenter + '/' + subject_dir + '/' + session_dir + '/camera')
            all_vid_path.append(data_vid_dir + experimenter + '/' + subject_dir + '/' + session_dir + '.avi')
            all_proc_dir.append(data_proc_dir + experimenter + '/' + subject_dir + '/' + session_dir + '/move_deve/')

for i in range(len(all_camera_dir)):
    print(all_camera_dir[i], flush=True)
    print(all_vid_path[i], flush=True)
    print(all_proc_dir[i], flush=True)

# now make a new folder structure in data_vid_dir and data_proc_dir
for i in range(len(all_vid_path)):
    # get the directory where the path is
    vid_dir = os.path.dirname(all_vid_path[i])
    os.makedirs(vid_dir, exist_ok=True)
    os.makedirs(all_proc_dir[i], exist_ok=True)

for (i, input_folder) in enumerate(all_camera_dir):

    output_video = all_vid_path[i]
    proc_dir = all_proc_dir[i]

    tstamps_path = os.path.join(proc_dir, 'tstamps.npy')
    interframe_path = os.path.join(proc_dir, 'interframe_int.npy')
    motion_path = os.path.join(proc_dir, 'motion_energy_glob.npy')

    video_exists = os.path.exists(output_video)
    motion_exists = all(os.path.exists(p) for p in [tstamps_path, interframe_path, motion_path])

    if video_exists and motion_exists:
        print(f"Video and motion energy for {input_folder} already exist, skipping...", flush=True)
        continue

    output_size = None  # Set to (width, height) if resizing is needed
    # do avi for now
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Codec for AVI

    # Get list of images
    images = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tiff')])

    print('First 10 images:', flush=True)
    for img in images[:10]:
        print(img, flush=True)
    print('Last 10 images:', flush=True)
    for img in images[-10:]:
        print(img, flush=True)

    print('Number of images:', len(images), flush=True)

    # extract timestamps from filenames (strftime counter -> seconds)
    tstamps = np.array(
        [int(frame_ts_pattern.search(os.path.basename(f)).group(1)) for f in images],
        dtype=np.float64,
    ) * tstamp_unit_to_sec
    interframe_int = np.diff(tstamps)

    # Read the first image to get dimensions
    first_image = cv2.imread(images[0])
    height, width, _ = first_image.shape
    if output_size:
        width, height = output_size

    print("Video size: {}x{}".format(width, height), flush=True)

    if not video_exists:
        # Create VideoWriter
        video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    prev_gray = None
    motion_energy = []  # pixel-wise frame difference, squared and summed (length N-1)

    # Write images to video and/or compute motion energy
    for idx, image_path in enumerate(images):
        image = cv2.imread(image_path)

        if not video_exists:
            frame = cv2.resize(image, output_size) if output_size else image
            video_writer.write(frame)

        if not motion_exists:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float64)
            if prev_gray is not None:
                diff = gray - prev_gray
                motion_energy.append(np.sum(diff ** 2))
            prev_gray = gray

        # print each 2000 frames
        if idx % 2000 == 0:
            print(f"Processed {idx} / {len(images)} frames", flush=True)

    if not video_exists:
        # Release VideoWriter
        video_writer.release()
        print(f"Video saved at {output_video}", flush=True)
    else:
        print(f"Video {output_video} already exists, skipping video creation...", flush=True)

    if not motion_exists:
        motion_energy = np.array(motion_energy)
        np.save(tstamps_path, tstamps)
        np.save(interframe_path, interframe_int)
        np.save(motion_path, motion_energy)
        print(f"Motion energy data saved at {proc_dir}", flush=True)
    else:
        print(f"Motion energy data for {input_folder} already exists, skipping...", flush=True)

print('Done.', flush=True)
