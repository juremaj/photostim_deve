import tifffile
import os
import numpy as np

from scipy.interpolate import interp1d


# IMPORTANT: For now excluding the stimulation frame itself
# IMPORTANT: Deal with the edge case where the stimulation frame is at the beginning or end of the tiff file
# IMPORTANT: Figure out what is causing the mean of empty slice error (catch the RuntimeWarning)
# USE THIS TO DEBUG: warnings.filterwarnings('error')
def get_fov_resp(all_tiff_paths, all_frame, bsln_n_frames=10, resp_n_frames=10, fov_shape=(512, 512)):
    """
    IMPORTANT!!! THIS FUNCTION IS DEPRECATED (replace with the function in photostim_deve.image_analysis.compute)!!!
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
    comp_fov_dyn: tuple
        If to compute the 'dynamics' of the average response (e. g. each frame of the stim window not just before and after)
        
    Returns:
    -------
    fov_bsln : np.ndarray
        A 2D array of the mean fluorescence in the baseline window for each stimulation point (shape: (n_stim, fov_shape[0], fov_shape[1])).
    fov_resp : np.ndarray
        A 2D array of the mean fluorescence in the response window for each stimulation point (shape: (n_stim, fov_shape[0], fov_shape[1])).
    fov_diff : np.ndarray
        A 2D array of the difference between the two (response - baseline)
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

def get_fov_resp_mn_md(fov_cond, all_point):
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
    fov_cond_md = np.zeros((len(unique_point), fov_cond.shape[1], fov_cond.shape[2]))

    for point in unique_point:
        point = int(point)
        point_mask = all_point == point
        fov_cond_mn[point, :, :] = np.nanmean(fov_cond[point_mask, :, :], axis=0)
        fov_cond_md[point, :, :] = np.nanmedian(fov_cond[point_mask, :, :], axis=0)

    return fov_cond_mn, fov_cond_md

def get_dist_dff(fov_map, all_point, all_coords_x, all_coords_y, fov_shape=(512, 512), n_dist_bins=724):
    """
    Calculate the df/f of a pixel in the response map as a function of distance from the stimulus point.
    This function computes the mean and standard deviation across pixels within specified distance bins from each stimulus point.
    
    ------------------
    
    Parameters:
        fov_map : (np.ndarray)
            The response map with shape (n_stim_points, height, width) where each slice corresponds to a mean pixel response to a stimulus point (averaged across all repetitions of that stimulus).
        all_point : (np.ndarray)
            Array of stimulus point indices corresponding to each stimulation.
        all_coords_x : (np.ndarray)
            X coordinates of the stimulus point corresponding to each stimulation
        all_coords_y : (np.ndarray)
            Y coordinates of the stimulus point corresponding to each stimulation
        fov_shape : (tuple)
            Shape of the field of view (height, width).
        n_dist_bins : (int)
            Number of distance bins to compute statistics for.

    Returns:
        dist_diff_mn : (np.ndarray)
            Each row corresponds to the mean of the pixel values for all pixels within a distance bin from a stimulus point. Rows correspond to different stimulus points.
        dist_diff_std : (np.ndarray)
            Each row corresponds to the standard deviation of the pixel values for all pixels within a distance bin from a stimulus point. Rows correspond to different stimulus points.

    """

    dist_max = np.sqrt(fov_shape[0]**2 + fov_shape[1]**2)  # Maximum distance in pixels (diagonal of the FOV)
    dist_bins = np.linspace(0, dist_max, n_dist_bins)  # Create bins for distances

    dist_diff_mn = np.zeros((len(np.unique(all_point)), n_dist_bins))
    dist_diff_std = np.zeros((len(np.unique(all_point)), n_dist_bins))

    for i in np.unique(all_point):
        coords_x = all_coords_x[i]
        coords_y = all_coords_y[i]

        print(f"Stimulus Point {i}: Coordinates: ({coords_x}, {coords_y})")
        
        # Create a distance map
        y_indices, x_indices = np.indices(fov_shape)
        distance_map = np.sqrt((x_indices - coords_x) ** 2 + (y_indices - coords_y) ** 2).T

        for j in range(1, n_dist_bins):
            dist_mask = np.zeros(fov_shape, dtype=bool)
            dist_mask = (distance_map >= dist_bins[j-1]) & (distance_map < dist_bins[j])

            mn = np.mean(fov_map[i][dist_mask])
            std = np.std(fov_map[i][dist_mask])

            dist_diff_mn[i, j-1] = mn
            dist_diff_std[i, j-1] = std

    return dist_diff_mn, dist_diff_std


def compute_dist_kernel(dist_diff_mn, n_dist_bins=724):
    """
    Compute the distance kernel from the mean df/f as a function of distance from the stimulus point.
    
    Parameters:
        dist_diff_mn : (np.ndarray)
            Each row corresponds to the mean of the pixel values for all pixels within a distance bin from a stimulus point. Rows correspond to different stimulus points.
        n_dist_bins : (int)
            Number of distance bins to compute statistics for. This should match the number of distance bins used in get_dist_dff.
    
    Returns:
        k1d : (np.ndarray)
            The distance kernel computed as the mean of the mean df/f across all stimulus points.
        k2d : (np.ndarray)
            The distance kernel rotated around the center of FOV.

    """
    k1d = np.nanmean(dist_diff_mn, axis=0)

    # now generate a 2D kernel from the 1D kernel
    kernel_size = n_dist_bins  # Size of the 2D kernel (e.g., 512x512)
    x = np.linspace(-kernel_size//2, kernel_size//2, kernel_size)
    y = np.linspace(-kernel_size//2, kernel_size//2, kernel_size)
    # Create a meshgrid for 2D coordinates
    X, Y = np.meshgrid(x, y)

    # Calculate the distance from the center for each point in the 2D grid
    distance = np.sqrt(X**2 + Y**2)
    # Interpolate the 1D kernel to create a 2D kernel
    interp_func = interp1d(np.linspace(0, kernel_size//2, len(k1d)), k1d, bounds_error=False, fill_value="extrapolate")
    # Create the 2D kernel by applying the interpolation function to the distance map
    k2d = interp_func(distance)

    return k1d, k2d