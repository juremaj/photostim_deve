import pandas as pd
import os
import numpy as np
import xml.etree.ElementTree as ET

# i guess all can be loaded from the mark points? e.g. make a list of stimuli based on the parameters of the mark points file...22
def parse_mark_points(session_path):
    """
    Loads and parses the MarkPoints.xml file in the session path.
    Returns a dictionary with the parameters of the mark points and the stimulation protocol as set in the PrairieView software.
    
    Parameters
    ----------
    session_path : str
        The path to the session directory containing the MarkPoints.xml file.

    Returns
    -------
    mp_dict : dict
        A dictionary with the parameters of the mark points and the stimulation protocol as set in the PrairieView software.

    """

    mark_points_file = [f for f in os.listdir(session_path) if f.endswith('.xml') and f.startswith('TSeries')]
    if len(mark_points_file) == 0:
        raise FileNotFoundError("No MarkPoints.xml file found in session path")
    elif len(mark_points_file) > 1:
        raise FileExistsError("Multiple MarkPoints.xml files found in session path")
    else:
        mark_points_file = mark_points_file[0]
    
    print(f"Found MarkPoints.xml file: {mark_points_file}")

    xml_data = ET.parse(os.path.join(session_path, mark_points_file))
    root = xml_data.getroot()

    mp_dict = {}

    all_point_dict = []

    for elem in root.iter():
        if elem.tag != 'Point':
            for key, value in elem.attrib.items():
                if key not in mp_dict:
                    mp_dict[key] = value
                else:
                    print(f"Key {key} already exists in dictionary with value {mp_dict[key]}. Overwriting with value {value}.")
        
        # if an element is a 'Point' treat it differently (by appending to list), since it is not unique (e. g. there can be multiple stimulation points)
        else:
            point_dict = {}
            for key, value in elem.attrib.items():
                if key not in mp_dict:
                    point_dict[key] = value
                else:
                    print(f"Key {key} already exists in dictionary with value {point_dict[key]}. Overwriting with value {value}.")

            all_point_dict.append(point_dict)


    mp_dict['AllPoint'] = all_point_dict

    return mp_dict


def mp_dict_to_stim_list(mp_dict, frame_period = 0.033602476, fov_shape=(512, 512), csv_save_path=None):
    """
    Convert the mark points dictionary to a list of stimulation times (in seconds), corresponding frame index and point index for each stimulation.

    Parameters:
    ----------
    mp_dict : dict
        The mark points dictionary containing the parameters of the mark points and the stimulation protocol as set in the PrairieView software.
    frame_period : float
        Exact frame period from metadata used to convert from time to frame index. Default is 0.033602476 (for '30Hz' acquisition).
    
    Returns:
    -------
    stim_times : list
        A list of stimulation times, corresponding frame index and point index for each stimulation.
    stim_frames : list
        A list of frame indices for each stimulation.
    stim_points : list
        Index of stimulated point corresponding to each stimulation.
    stim_coords_x : list
        A list of x coordinates of the stimulated points in the FOV (center of spiral / median of ROI).
    stim_coords_y : list
        A list of y coordinates of the stimulated points in the FOV (center of spiral / median of ROI).
    -----------

    """
    initial_delay = float(mp_dict['InitialDelay'])
    inter_point_delay = float(mp_dict['InterPointDelay'])
    duration = float(mp_dict['Duration'])
    repetitions = int(mp_dict['Repetitions'])
    n_points = len(mp_dict['AllPoint'])

    n_stim = n_points * repetitions

    stim_times = np.zeros((n_stim))
    stim_frames = np.zeros((n_stim))
    stim_points = np.zeros((n_stim))
    stim_coords_x = np.zeros((n_stim))
    stim_coords_y = np.zeros((n_stim))

    point_coords = np.zeros((len(mp_dict['AllPoint']), 2))
    for i, point in enumerate(mp_dict['AllPoint']):
        point_coords[i, 0] = float(point['Y']) * fov_shape[0]
        point_coords[i, 1] = float(point['X'])  * fov_shape[1]


    for i in range(n_stim):
        # points go from 0 to n_points - 1 and then reset
        stim_times[i] = (initial_delay + i * (inter_point_delay + duration)) / 1000
        stim_frames[i] = int(stim_times[i] / frame_period)
        stim_points[i] = i % n_points
        stim_coords_x[i] = point_coords[int(stim_points[i]), 0]
        stim_coords_y[i] = point_coords[int(stim_points[i]), 1]

    if csv_save_path is not None:
        stim_df = pd.DataFrame({
            'time': stim_times,
            'frame': stim_frames,
            'point': stim_points,
            'x': stim_coords_x,
            'y': stim_coords_y
        })
        stim_df.to_csv(csv_save_path, index=False)
        print(f"Saved stimulation data to {csv_save_path}")


    return stim_times, stim_frames, stim_points, stim_coords_x, stim_coords_y

def load_photostim_protocol(csv_path):
    """
    Load the stimulation protocol from a CSV file.

    Parameters:
    ----------
    csv_path : str
        The path to the CSV file containing the stimulation protocol.

    Returns:
    -------
    stim_times : list
        A list of stimulation times, corresponding frame index and point index for each stimulation.
    stim_frames : list
        A list of frame indices for each stimulation.
    stim_points : list
        Index of stimulated point corresponding to each stimulation.
    stim_coords_x : list
        A list of x coordinates of the stimulated points in the FOV (center of spiral / median of ROI).
    stim_coords_y : list
        A list of y coordinates of the stimulated points in the FOV (center of spiral / median of ROI).
    """
    
    stim_df = pd.read_csv(csv_path)

    all_time = stim_df['time'].to_numpy()
    all_frame = stim_df['frame'].to_numpy().astype(int)
    all_point = stim_df['point'].to_numpy().astype(int)
    all_coords_x = stim_df['x'].to_numpy()
    all_coords_y = stim_df['y'].to_numpy()

    return all_time, all_frame, all_point, all_coords_x, all_coords_y

def get_all_tiff_paths(tiff_dir):
    """
    Get full tiff paths from the suite2p motion corrected tiff directory.
    It also ensures that the tiff files are sorted correctly despite strange s2p naming conventions.
    
    -------------
    
    Parameters:
        tiff_dir : (str)
            Directory containing the motion corrected tiff files from suite2p.

    Returns:
        all_tiff_paths : (list) 
            List of full paths to the tiff files, sorted by their start frame index.

    """
    
    all_tiff_paths = [os.path.join(tiff_dir, tiff_path) for tiff_path in os.listdir(tiff_dir) if tiff_path.endswith('.tif')]
    all_tiff_paths.sort()

    # get tiff start frame index for each tiff file (string between file00 and _)
    tiff_start_frames = [int(os.path.basename(tiff_path).split('file00')[1].split('_')[0]) for tiff_path in all_tiff_paths]
    tiff_start_frames = np.array(tiff_start_frames)

    # now resort the tiff paths and start frames
    sort_indices = np.argsort(tiff_start_frames)
    all_tiff_paths = [all_tiff_paths[i] for i in sort_indices]

    return all_tiff_paths