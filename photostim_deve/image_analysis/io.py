import numpy as np
import os
import tifffile as tiff
import pandas as pd


from suite2p.registration import register

def get_all_fov_image(subject_path, session_type='_a', session_reg_idx=0,run_motcorr=True, fov_imsize=(1024, 1024), nimg_init=128, force_recompute=False):

    """
    For a given subject, load all FOV images from the first session of the specified type.
    If motion correction is requested, perform Suite2p motion correction on each FOV and save the mean image.

    Parameters:
    ----------
    subject_path: str
        Path to the subject directory.
    session_type: str
        Suffix to identify the session type (default is '_a').
    session_reg_idx: int
        Index of the session to process (default is 0, i.e., the first session).
    run_motcorr: bool
        Boolean indicating whether to perform motion correction (default is True).
    fov_imsize: tuple
        Tuple indicating the size of the FOV images (default is (1024, 1024)).
    nimg_init: int
        Number of initial images to use for registration (default is 128).
    force_recompute: bool
        Boolean indicating whether to force recomputation even if files exist (default is False).

    Returns:
    all_fov_image: dict
        Dictionary with FOV directory names as keys and corresponding mean images as values. (motion corrected if requested - in that case the original mean image is also included with '_mn' suffix)
    """
    
    # find first sessio of the subject 
    all_session_dir = [d for d in os.listdir(subject_path) if d.endswith(session_type)]
    all_session_dir.sort()

    session_dir = all_session_dir[session_reg_idx]
    all_session_fov_dir = [d for d in os.listdir(os.path.join(subject_path, session_dir, 'fov')) if os.path.isdir(os.path.join(subject_path, session_dir, 'fov', d))]
    all_session_fov_dir.sort()

    # initialise a dictionary where all_session_fov_dir are the keys and values are the images
    all_fov_image = {}

    for session_fov_dir in all_session_fov_dir:

        # 0) if corresponding images area already computed, skip and just load to dictionary
        if run_motcorr and not force_recompute:
            if os.path.exists(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_motcorr_mn.npy')) and not force_recompute:
                print(f"Motion corrected image for {session_fov_dir} already exists, skipping...")
                all_fov_image[session_fov_dir + '_mn'] = np.load(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy'))
                all_fov_image[session_fov_dir] = np.load(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_motcorr_mn.npy'))
                continue
            
        else:
            if os.path.exists(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy')) and not force_recompute:
                print(f"Mean image for {session_fov_dir} already exists, skipping...")
                all_fov_image[session_fov_dir] = np.load(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy'))
                all_fov_image[session_fov_dir + '_mn'] = np.load(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy'))
                continue

        # 1) find and load tiff file from TSeries folder
        tseries_folders = [f.path for f in os.scandir(os.path.join(subject_path, session_dir, 'fov', session_fov_dir)) if f.is_dir() and f.name.startswith('TSeries')]
        tseries_folder = tseries_folders[0] 

        tif_files = [f.path for f in os.scandir(tseries_folder) if f.is_file() and f.name.endswith('.tif')]
        tif_file = tif_files[0]

        tiff_data = tiff.imread(tif_file)
        fov_image_mn = np.mean(tiff_data, axis=0)

        # 2) perform Suite2p motion correction and save mean image (if run_motcorr == True otherwise just save mean image)
        if run_motcorr:

            ops = [
                {
                    'reg_file': tiff_data,
                    'Ly': fov_imsize[0],
                    'Lx': fov_imsize[1],
                    'nimg_init': nimg_init
                }
            ]

            tiff_data_float = tiff_data.astype(np.float32)
            _, _, _, fov_image_motcorr_mn, _, _, _ = register.compute_reference_and_register_frames(tiff_data_float, ops)

            all_fov_image[session_fov_dir] = fov_image_motcorr_mn
            all_fov_image[session_fov_dir + '_mn'] = fov_image_mn

            np.save(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_motcorr_mn.npy'), fov_image_motcorr_mn)
            np.save(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy'), fov_image_mn)

        else:
            
            all_fov_image[session_fov_dir] = fov_image_mn
            np.save(os.path.join(subject_path, session_dir, 'fov', f'{session_fov_dir}_mn.npy'), fov_image_mn)

    return all_fov_image

def get_s2p_image(session_path):
    """
    Get the Suite2p mean image from the session path.

    Parameters
    ----------
    session_path : str
        Path to the session directory.

    Returns
    -------
    s2p_image : np.ndarray
        Suite2p mean image.
    """
    ops = np.load(os.path.join(session_path, 'suite2p', 'plane0', 'ops.npy'), allow_pickle=True).item()
    s2p_image = ops['meanImg']
    return s2p_image

def get_xy_stim(session_path, session_type='_a'):
    """
    Get the XY coordinates of stimulation points from a photostimulation
    protocol file.

    This function assumes that the ``photostim_protocol.csv`` file has already
    been generated from the Bruker MarkPoints metadata.

    Parameters
    ----------
    session_path : str
        Path to the session directory.
    session_type : str
        Suffix to identify the session type (default is '_a').

    Returns
    -------
    x_stim : np.ndarray
        X coordinates of the stimulation points.
    y_stim : np.ndarray
        Y coordinates of the stimulation points.
    """

    try:
        stim_protocol_path = os.path.join(session_path.replace(session_type, '_b'), 'photostim_protocol.csv')
        stim_protocol = np.loadtxt(stim_protocol_path, delimiter=',', skiprows=1)
    except:
        print(f'Warning: Could not find corresponding _b session or stimulation protocol file...')
        return None, None

    unique_point_ids = np.unique(stim_protocol[:, 2]).astype(int)
    print(type(unique_point_ids[0]))
    # now get the values in colums 3 and 4 for each unique point id
    x_stim = stim_protocol[unique_point_ids, 3] 
    y_stim = stim_protocol[unique_point_ids, 4]

    return x_stim, y_stim

def save_keypoints(viewer, keypoints_save_path):
    """
    Save manually defined keypoints from napari viewer to a CSV file.

    Parameters:
    ----------
    viewer: napari.Viewer
        The napari viewer containing the keypoints layers.
    keypoints_save_path: str
        Path to save the CSV file containing the keypoints.
        
    Returns:
    -------
    None
    """

    s2p_keypoints = viewer.layers['s2p_keypoints'].data
    fov_1100nm_keypoints = viewer.layers['fov_1100nm_keypoints'].data

    keypoints_df = pd.DataFrame({
        'y_s2p': s2p_keypoints[:, 0],
        'x_s2p': s2p_keypoints[:, 1],
        'y_fov_1100nm': fov_1100nm_keypoints[:, 0],
        'x_fov_1100nm': fov_1100nm_keypoints[:, 1],
    })
    keypoints_df.to_csv(keypoints_save_path, index=False)
    print(f'Saved keypoints to {keypoints_save_path}')

def load_keypoints(keypoints_save_path):
    """
    Load keypoints from a CSV file.

    Parameters:
    ----------
    keypoints_save_path: str
        Path to the CSV file containing the keypoints.
    
    Returns:
    -------
    x_s2p: np.ndarray
        x coordinates of keypoints in s2p image.
    y_s2p: np.ndarray
        y coordinates of keypoints in s2p image.
    x_fov: np.ndarray
        x coordinates of keypoints in fov 1100nm image.
    y_fov: np.ndarray
        y coordinates of keypoints in fov 1100nm image.
    """
    
    keypoints_df = pd.read_csv(keypoints_save_path)
    x_s2p = keypoints_df['x_s2p'].values
    y_s2p = keypoints_df['y_s2p'].values
    x_fov = keypoints_df['x_fov_1100nm'].values
    y_fov = keypoints_df['y_fov_1100nm'].values
    return x_s2p, y_s2p, x_fov, y_fov

def get_t2p_s2p_indices_session(subject_path, track2p_dirname='track2p', session_reg_idx=0):
    """
    Get the suite2p indices for this session corresponding only to the cells that were tracked on all days.

    Parameters:
    ----------
    subject_path : str
        Path to the subject directory.
    track2p_dirname : str   
        Name of the track2p directory (for example if track2p is run separately for spontaneous and evoked sessions, it could be 'track2p_a' or 'track2p_s').
    session_reg_idx : int
        Index of the session used as reference for FOV registration across sessions.
        
    Returns
    -------
    t2p_idxs_session : list of int
        List of suite2p indices for this session corresponding only to the cells that were tracked on all days.
    """

    t2p_idxs_alldays = np.load(os.path.join(subject_path, track2p_dirname, 'plane0_suite2p_indices_nan.npy'), allow_pickle=True)

    t2p_idxs_alldays_nonan = t2p_idxs_alldays[~np.isnan(t2p_idxs_alldays).any(axis=1)]
    
    t2p_idxs_session = t2p_idxs_alldays_nonan[:, session_reg_idx].astype(int)

    return t2p_idxs_session

def get_s2p_rois_filt(session_path, filt_by='t2p', t2p_idxs_session=None, cell_prob_thr=None):
    """
    Returns Suite2p ROIs and their medians for the given session.

    Parameters
    ----------
    session_path : str
        Path to the session directory.
    filt_by : str
        How to choose which s2p ROIs consider for matching. Options are:
        't2p' : only consider ROIs that were tracked by track2p across all days (requires t2p_idxs_session to be provided)
        'iscell_cell_prob' : consider all ROIs classified as cells by Suite2p classifier-assigned probability (based on second column of iscell.npy and cell_prob_thr)
        'iscell_manual_cur' : consider all ROIs classified as cells by manual curation (based on first column of iscell.npy)
    t2p_idxs_session : list or np.ndarray
        List of suite2p ROI indices in this session corresponding only to the cells that were tracked by track2p across all days (required if filt_by is 't2p')
    cell_prob_thr : float or None
        Cell probability threshold for filtering ROIs when filt_by is 'iscell_cell_prob'.

    Returns
    -------
    roi_s2p: list of np.ndarray
        Each element in list is one ROI, np.ndarray of shape (N, 2) with x,y coordinates of pixels in ROI.
    x_s2p_med: np.ndarray
        x coordinates of ROI medians.
    y_s2p_med: np.ndarray
        y coordinates of ROI medians.
    roi_s2p_idxs: np.ndarray
        List of suite2p ROI indices. (used for cross-referencing with other suite2p and track2p data)
    """

    stat = np.load(os.path.join(session_path, 'suite2p', 'plane0', 'stat.npy'), allow_pickle=True)
    iscell = np.load(os.path.join(session_path, 'suite2p', 'plane0', 'iscell.npy'), allow_pickle=True)
    idxs = np.arange(len(stat))

    # Get s2p indices based on filtering criteria
    if filt_by == 't2p':
        if t2p_idxs_session is None:
            raise ValueError("t2p_idxs_session must be provided when filt_by is 't2p'")
        idxs_filt = np.array([i for i in idxs if i in t2p_idxs_session])
    elif filt_by == 'iscell_cell_prob':
        if cell_prob_thr is None:
            raise ValueError("cell_prob_thr must be provided when filt_by is 'iscell_cell_prob'")
        idxs_filt = np.array([i for i in idxs if iscell[i, 1] >= cell_prob_thr])
    elif filt_by == 'iscell_manual_cur':    
        idxs_filt = np.array([i for i in idxs if iscell[i, 0] == 1])
    else:
        raise ValueError("Invalid filt_by option. Choose from 't2p', 'iscell_cell_prob', 'iscell_manual_cur'.")
    
    print(f"Number of ROIs after filtering: {len(idxs_filt)} out of {len(stat)}")

    # Now index the stat to only include filtered ROIs
    stat_filt = [stat[i] for i in idxs_filt]

    # flip the convention to match photostim coordinates (x,y)
    roi_s2p = [np.stack([s['ypix'], s['xpix']], axis=1) for s in stat_filt]

    # flip the convention to match photostim coordinates (x,y)
    x_s2p_med = np.array([np.median(s['ypix']) for s in stat_filt])
    y_s2p_med = np.array([np.median(s['xpix']) for s in stat_filt])
    
    roi_s2p_idxs = idxs_filt

    return roi_s2p, x_s2p_med, y_s2p_med, roi_s2p_idxs