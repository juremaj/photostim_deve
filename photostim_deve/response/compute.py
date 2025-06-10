import tifffile
import os
import numpy as np

# IMPORTANT: For now excluding the stimulation frame itself
# IMPORTANT: Deal with the edge case where the stimulation frame is at the beginning or end of the tiff file
# IMPORTANT: Figure out what is causing the mean of empty slice error (catch the RuntimeWarning)
# USE THIS TO DEBUG: warnings.filterwarnings('error')
def get_fov_resp(all_tiff_paths, all_frame, bsln_n_frames=10, resp_n_frames=10, fov_shape=(512, 512), uint12_max=4095*2):
    """
    Load the tiff files and extract the mean fluorescence in the baseline and response windows for each stimulation.

    Parameters:
    ----------
    all_tiff_paths : list
        A list of paths to the tiff files containing the fluorescence data.
    all_frame : list
        A list of frame indices of stimulation (each entry is a single trial of a single point).
    bsln_n_frames : int
        The number of frames before the stimulation to use for the baseline window (default is 10).
    resp_n_frames : int
        The number of frames after the stimulation to use for the response window (default is 10).
    fov_shape : tuple
        The shape of the FOV in pixels (default is (512, 512)).
    uint12_max : int
        The maximum value for the uint12 data type, used for conversion to uint8 (default is 4095 * 2).
        
    Returns:
    -------
    fov_bsln : np.ndarray
        A 2D array of the mean fluorescence in the baseline window for each stimulation point (shape: (n_stim, fov_shape[0], fov_shape[1])).
    fov_resp : np.ndarray
        A 2D array of the mean fluorescence in the response window for each stimulation point (shape: (n_stim, fov_shape[0], fov_shape[1])).

    """

    n_stim = len(all_frame)

    fov_bsln = np.zeros((n_stim, fov_shape[0], fov_shape[1]))
    fov_resp = np.zeros((n_stim, fov_shape[0], fov_shape[1]))
    fov_diff = np.zeros((n_stim, fov_shape[0], fov_shape[1])) # difference between response and baseline

    cum_frames = 0 # cumulative frames loaded so far (to get correct offset for each trial)
    
    for i, tiff_path in enumerate(all_tiff_paths):
        print(f"Loading tiff file {i+1}/{len(all_tiff_paths)}: {tiff_path}")
        tiff = tifffile.imread(tiff_path)
        # tiff = tiff / uint12_max * 255
        # tiff = tiff.astype(np.uint8)
        
        n_frames = tiff.shape[0]
        
        for (j, stim_frame) in enumerate(all_frame):
            if stim_frame < cum_frames or stim_frame >= cum_frames + n_frames:
                continue
            
            bsln_on = int(stim_frame - cum_frames - bsln_n_frames)
            bsln_off = int(stim_frame - cum_frames - 1) # excluding the stimulation frame

            resp_on = int(stim_frame - cum_frames + 1) # excluding the stimulation frame
            resp_off = int(stim_frame - cum_frames + resp_n_frames)
            print(f'Processing stim: {j} resp_onset: {resp_on}, resp_offset: {resp_off}, bsln_offset: {bsln_off}, bsln_onset: {bsln_on}')

            fov_bsln[j, :, :] = np.mean(tiff[bsln_on:bsln_off, :, :], axis=0)
            fov_resp[j, :, :] = np.mean(tiff[resp_on:resp_off, :, :], axis=0)
            fov_diff[j, :, :] = fov_resp[j, :, :] - fov_bsln[j, :, :]

        cum_frames += n_frames

    return fov_bsln, fov_resp, fov_diff

def get_fov_resp_mn(fov_cond, all_point):
    """
    Get the mean fluorescence response for each point across all trials.

    Parameters:
    ----------
    fov_cond : np.ndarray
        A 3D array of the mean fluorescence response for each point (shape: (n_stim, fov_shape[0], fov_shape[1])).
        Can be either baseline, response or difference (response - baseline).
    all_point : list
        A list of indices of the stimulated points corresponding to each stimulation.
    Returns:
    -------
    fov_cond_mn : np.ndarray
        A 3D array of the mean across all points for the given condition (shape: (len(unique_point), fov_shape[0], fov_shape[1])).
    
    """
    
    unique_point = np.unique(all_point)
    fov_cond_mn = np.zeros((len(unique_point), fov_cond.shape[1], fov_cond.shape[2]))

    for point in unique_point:
        point = int(point)
        point_mask = all_point == point
        fov_cond_mn[point, :, :] = np.nanmean(fov_cond[point_mask, :, :], axis=0)

    return fov_cond_mn