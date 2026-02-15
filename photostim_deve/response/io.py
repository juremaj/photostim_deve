import pandas as pd
import os
import numpy as np
import xml.etree.ElementTree as ET

from scipy.ndimage import maximum_filter1d, minimum_filter1d, gaussian_filter

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

def parse_evoked_protocol_csv(session_path, csv_save_path=None, frame_period=0.033602476):
    """
    Convert the evoked stim protcol data (.npy files) to a list of stimulation times (in seconds), corresponding frame index and evoked stim type index (currently all the same, due to a single stim time) for each stimulation.
    Also saves the stimulation protocol as a .csv file for easier loading in the future.

    Parameters:
    ----------
    session_path : str 
        Path to the session directory containing the .npy files with stimulation protocol data. 
    csv_save_path : str 
        Path to save (or load from) the converted stimulation protocol as a .csv file.
    frame_period : float
        Exact frame period from metadata used to convert from time to frame index. Default is 0.033602476 (for '30Hz' acquisition).
    
    Returns:
    -------
    stim_times : list
        A list of stimulation times, corresponding frame index and evoked stim type index for each stimulation.
    stim_frames : list
        A list of frame indices for each stimulation.
    stim_type : list
        Evoked stim type index corresponding to each stimulation (currently all the same, due to a single stim time). (Equivalent of 'stim_points' in the 'resp_photostim' protocol).

    """
    
    stim_frames = np.load(os.path.join(session_path, 'stim_times.npy')) # NOTE: here the 'stim_times.npy' file actually contains the frame indices of the stim times, not the stim times in seconds. 
    stim_times = stim_frames * frame_period # convert from frame index to time in seconds
    stim_type = np.load(os.path.join(session_path, 'stim_protocol.npy'))

    print(f"Loaded stim_times.npy with shape {stim_times.shape} and stim_protocol.npy with shape {stim_type.shape}")
    print(f'stim_protocol unique values: {np.unique(stim_type)}')
    print(f'stim_times values: {stim_times}')

    if csv_save_path is not None:
        stim_df = pd.DataFrame({
            'time': stim_times,
            'frame': stim_frames,
            'type': stim_type
        })
        stim_df.to_csv(csv_save_path, index=False)
        print(f"Saved stimulation data to {csv_save_path}")

    return stim_times, stim_frames, stim_type

# preprocess function to get dff (from Suite2p)
def preprocess(F: np.ndarray, baseline: str, win_baseline: float, sig_baseline: float,
               fs: float, prctile_baseline: float = 8) -> np.ndarray:
    """ preprocesses fluorescence traces for spike deconvolution

    baseline-subtraction with window "win_baseline"
    
    Parameters
    ----------------

    F : float, 2D array
        size [neurons x time], in pipeline uses neuropil-subtracted fluorescence

    baseline : str
        setting that describes how to compute the baseline of each trace

    win_baseline : float
        window (in seconds) for max filter

    sig_baseline : float
        width of Gaussian filter in frames

    fs : float
        sampling rate per plane

    prctile_baseline : float
        percentile of trace to use as baseline if using `constant_prctile` for baseline
    
    Returns
    ----------------

    F : float, 2D array
        size [neurons x time], baseline-corrected fluorescence

    """
    win = int(win_baseline * fs)
    if baseline == "maximin":
        Flow = gaussian_filter(F, [0., sig_baseline])
        Flow = minimum_filter1d(Flow, win)
        Flow = maximum_filter1d(Flow, win)
    elif baseline == "constant":
        Flow = gaussian_filter(F, [0., sig_baseline])
        Flow = np.amin(Flow)
    elif baseline == "constant_prctile":
        Flow = np.percentile(F, prctile_baseline, axis=1)
        Flow = np.expand_dims(Flow, axis=1)
    else:
        Flow = 0.

    F = F - Flow

    return F

def baseline_neu_sub(F, Fneu, tau=1.0, neucoeff=0.7, fs=30.0, baseline='maximin', sig_baseline=10.0, win_baseline=60.0, run_dcnv=False):
    """ 
    
    Baseline and neuropil subtraction for fluorescence traces

    Inputs
    ----------------
    F : float, 2D array
        size [neurons x time], fluorescence trace
    
    Fneu : float, 2D array
        size [neurons x time], neuropil trace

    for others see preprocess()

    Returns
    ----------------
    Fc : float, 2D array
        size [neurons x time], baseline and neuropil-corrected fluorescence

    """

    ops = {'tau': tau, 'fs': fs, 'neucoeff': neucoeff,
        'baseline': baseline, 'sig_baseline': sig_baseline, 'win_baseline': win_baseline}

    print(f"dff with neuropil subtraction (neucoeff={neucoeff}) and baseline subtraction (baseline={baseline}, win_baseline={win_baseline}s, sig_baseline={sig_baseline} frames)")

    Fc = F - ops['neucoeff'] * Fneu

    # baseline operation
    Fc = preprocess(
        F=Fc,
        baseline=ops['baseline'],
        win_baseline=ops['win_baseline'],
        sig_baseline=ops['sig_baseline'],
        fs=ops['fs']
        )

    # get spike
    
    return Fc

# Suite2p loader class (taken from 'longipy')
class Suite2pLoader: 

    def __init__(self, ds_path, fs=30, act_type='dff', n_planes=1):
        """
        Loader for suite2p data.

        Parameters:
            ds_path: str
                path to the dataset
            fs: int
                sampling rate of the data
            act_type: str
                type of activity to extract. Can be 'dff' or 'spks'
            n_planes: int
                number of planes in the session
        """

        self.ds_path = ds_path
        self.fs = fs
        self.act_type = act_type
        self.n_planes = n_planes

        self.get_ops_session() # to get the number of channels


    def get_n_rois(self, c_idxs=None):
        """
        Returns the number of ROIs in the session.
        
        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
        Returns:
            n_rois: int
                number of ROIs in the session
        """

        stat = self.get_stat_session(c_idxs=c_idxs)
        n_rois = len(stat) if self.n_planes == 1 else np.sum([len(stat[i]) for i in range(self.n_planes)])

        return n_rois
    
    def get_iscell_redcell(self, mode='iscell', c_idxs=None):
        """
        Returns the iscell (or redcell) boolean and cell probability for each ROI.

        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
            mode: str
                mode to extract. Can be 'iscell' or 'redcell'
        Returns:
            iscell_bool: array
                iscell boolean for each ROI
            iscell_prob: array
                cell probability for each ROI
        """

        if self.n_planes == 1:
            cell = np.load(os.path.join(self.ds_path, 'suite2p', 'plane0', f'{mode}.npy'), allow_pickle=True)
            cell_bool = cell[c_idxs, 0]
            cell_prob = cell[c_idxs, 1]

        elif self.n_planes > 1:
            cell_bool = []
            cell_prob = []
            for i in range(self.n_planes):
                cell = np.load(os.path.join(self.ds_path, 'suite2p', f'plane{i}', f'{mode}.npy'), allow_pickle=True)
                cell_bool.append(cell[c_idxs[i], 0])
                cell_prob.append(cell[c_idxs[i], 1])

            cell_bool = np.concatenate(cell_bool, axis=0)
            cell_prob = np.concatenate(cell_prob, axis=0)
        return cell_bool, cell_prob

    def get_cell_plane(self, c_idxs=None):
        """
        For each cell, returns the plane in which it is located.

        Parameters:
            c_idxs: int
                index of the cell to extract
        
        Returns:
            plane: int
                index of the plane in which the cell is located
        """

        n_cells = self.get_n_rois(c_idxs=c_idxs)

        print(f'Number of cells: {n_cells}')
        
        cell_plane = np.zeros(n_cells)

        if self.n_planes == 1:
            pass

        elif self.n_planes > 1:

            stat = self.get_stat_session(c_idxs=c_idxs)

            for i in range(1, self.n_planes):
                cell_plane[len(stat[i-1]):len(stat[i-1]) + len(stat[i])] = i

        cell_plane = cell_plane.astype(int)   
        return cell_plane

    def get_s2p_idxs(self, c_idxs=None):
        """
        Returns the suite2p indices for the neurons.

        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
        
        Returns:
            s2p_idxs: array
                Original suite2p indices of the neurons
        """

        n_rois = self.get_n_rois()
        s2p_idxs = np.arange(n_rois)
        if self.n_planes == 1:
            s2p_idxs = s2p_idxs[c_idxs] if c_idxs is not None else s2p_idxs
        else:
            s2p_idxs = [s2p_idxs[c_idxs[i]] for i in range(self.n_planes)] if c_idxs is not None else s2p_idxs
            s2p_idxs = np.concatenate(s2p_idxs)

        return s2p_idxs


    def get_act_plane(self, c_idxs_plane=None, t_idxs_plane=None, plane='plane0'):
        """
        Extracts activity of all selected neurons in a plane.

        Parameters:
            c_idxs_plane: array
                list of indices of the neurons to extract. None to extract all neurons
            t_idxs_plane: array
                indices of the frames to extract. None to extract all frames.
            plane: str
                name of the plane to extract the activity from

        Returns:
            act_pl: array
                activity of all selected neurons in the plane
        """

        if self.act_type == 'dff':
            F = np.load(os.path.join(self.ds_path, 'suite2p', plane, 'F.npy'))
            Fneu = np.load(os.path.join(self.ds_path, 'suite2p', plane, 'Fneu.npy'))

            act_pl = baseline_neu_sub(F, Fneu, fs=self.fs)

            print(f'Indexing activity data by t_idxs ({(len(t_idxs_plane)/act_pl.shape[1])*100:.0f}% of frames)') if t_idxs_plane is not None else None

            act_pl = act_pl[c_idxs_plane, :] if c_idxs_plane is not None else act_pl[:,:]
            act_pl = act_pl[:, t_idxs_plane] if t_idxs_plane is not None else act_pl[:,:]


        elif self.act_type == 'spks':
            act_pl = np.load(os.path.join(self.ds_path, 'suite2p', plane, 'spks.npy'))

            print(f'Indexing activity data by t_idxs ({(len(t_idxs_plane)/act_pl.shape[1])*100:.0f}% of frames)') if t_idxs_plane is not None else None

            act_pl = act_pl[c_idxs_plane, :] if c_idxs_plane is not None else act_pl[:,:]
            act_pl = act_pl[:, t_idxs_plane] if t_idxs_plane is not None else act_pl[:,:]


        else:
            raise ValueError(f"Activity type {self.act_type} not recognized")

        return act_pl
    
    def get_act_session(self, c_idxs=None, t_idxs=None):
        """
        Extracts activity of all selected neurons in the session.

        Parameters:
            c_idxs: list
                list of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
            t_idxs: array
                indices of the frames to extract. None to extract all frames.

        Returns:
            act: array
                activity of all selected neurons in the session
        """
        if self.n_planes == 1:
            print('Loading activity for plane0')

            self.act = self.get_act_plane(c_idxs_plane=c_idxs, t_idxs_plane=t_idxs, plane='plane0').squeeze()

        elif self.n_planes > 1:
            act = []
            for i in range(self.n_planes):
                print(f'Loading activity for plane{i}')

                c_idxs_plane = c_idxs[i] if c_idxs is not None else None
                t_idxs_plane = t_idxs if t_idxs is not None else None

                act_pl = self.get_act_plane(c_idxs_plane=c_idxs_plane, t_idxs_plane=t_idxs_plane, plane=f'plane{i}')
                act.append(act_pl)

            self.act = np.concatenate(act, axis=0)

        return self.act

    def get_stat_session(self, c_idxs=None):
        """
        Extracts the ROI properties saved in stat from suite2p sessions.

        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
        
        Returns:
            stat: list or list of lists
                list of dictionaries containing the ROI properties (one dictinoary per ROI) for each plane.
        """

        if self.n_planes == 1:
            stat = np.load(os.path.join(self.ds_path, 'suite2p', 'plane0', 'stat.npy'), allow_pickle=True)
            stat = stat[c_idxs] if c_idxs is not None else stat

        elif self.n_planes > 1:
            stat = []
            for i in range(self.n_planes):
                stat_pl = np.load(os.path.join(self.ds_path, 'suite2p', f'plane{i}', 'stat.npy'), allow_pickle=True)
                stat_pl = stat_pl[c_idxs[i]] if c_idxs is not None else stat_pl
                stat.append(stat_pl)

        return stat

    def get_ops_session(self):
        """
        Extracts the ops dictionary saved in ops from suite2p sessions.

        Returns:
            ops: dictionary
                dictionary containing the ops properties.
        """
        
        if self.n_planes == 1:
            ops = np.load(os.path.join(self.ds_path, 'suite2p', 'plane0', 'ops.npy'), allow_pickle=True).item()
            self.n_channels = ops['nchannels']
        
        elif self.n_planes > 1:
            ops = []
            print('Number of planes:', self.n_planes)
            for i in range(self.n_planes):
                ops_pl = np.load(os.path.join(self.ds_path, 'suite2p', f'plane{i}', 'ops.npy'), allow_pickle=True).item()
                ops.append(ops_pl)
                self.n_channels = ops_pl['nchannels']

        return ops
    
    def pad_max_proj(self, ops, max_proj):
        """
        Pads the max projection to the size of the mean image.

        Parameters:
            max_proj: array
                max projection to pad
        
        Returns:
            max_proj_padded: array
                padded max projection
        """

        meanImg = ops['meanImg']
        xrange = ops['xrange']
        yrange = ops['yrange']

        max_proj_padded = np.zeros_like(meanImg)
        max_proj_padded[yrange[0]:yrange[1], xrange[0]:xrange[1]] = max_proj

        return max_proj_padded

    def get_img_session(self, img_type='mean'):
        """
        Extracts the mean for each channel or max projection (of functional channel) of the imaging data.

        Parameters:
            img_type: str
                type of image to extract. Can be 'meanImg', 'meanImg_chan2' or 'max_proj'

        Returns:
            img: array or list of arrays
                image data for each plane
        """

        if self.n_planes == 1:
            ops = self.get_ops_session()
            img = ops[img_type]
            img = self.pad_max_proj(ops, img) if img_type == 'max_proj' else img

        elif self.n_planes > 1:
            
            ops = self.get_ops_session()
            img = []

            for i in range(self.n_planes):                
                img_pl = ops[i][img_type]
                img_pl = self.pad_max_proj(ops[i], img_pl) if img_type == 'max_proj' else img_pl
                img.append(img_pl)
        
        return img
    
    def get_meds_session(self, c_idxs=None):
        """
        Extracts the median of the ROI pixels from stat.

        Parameters:
            c_idxs: array or list
                Array or list of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons

        Returns:
            meds: array (n_cells x 2) or list of arrays
                (n_cells x 2) array of the median pixel coordinates (y and x) for each ROI in each plane.
        """

        stat = self.get_stat_session(c_idxs=c_idxs)

        if self.n_planes == 1:
            meds = np.array([stat[i]['med'] for i in range(len(stat))])

        elif self.n_planes > 1: 
            meds = []
            for i in range(self.n_planes):
                meds_pl = np.array([stat[i][j]['med'] for j in range(len(stat[i]))])
                meds.append(meds_pl)
        
        return meds
    
    def get_med_xy(self, xy_mode=None, c_idxs=None):
        """
        Helper to get just the y or x coordinates when adding entries to tables
        """
        meds = self.get_meds_session(c_idxs=c_idxs)
        
        if xy_mode == 'x':
            xy_idx = 1
        elif xy_mode == 'y':
            xy_idx = 0
        else:
            raise ValueError('xy_mode must be either x or y')

        if self.n_planes == 1:
            med_xy = meds[:, xy_idx]

        elif self.n_planes > 1: 
            med_xy = []
            for i in range(self.n_planes):
                med_xy_pl = meds[i][:, xy_idx]
                med_xy.append(med_xy_pl)

            med_xy = np.concatenate(med_xy, axis=0)
        return med_xy


    
    def get_npix(self, c_idxs=None):
        """
        Extracts the number of pixels for each ROI from stat.

        Parameters:
            c_idxs: array or list
                Array or list of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
        Returns:
            npix: array (n_cells x 1) or list of arrays
                number of pixels for each ROI in each plane.
        """

        stat = self.get_stat_session(c_idxs=c_idxs)

        if self.n_planes == 1:
            npix = np.array([stat[i]['npix'] for i in range(len(stat))])

        elif self.n_planes > 1: 
            npix = []
            for i in range(self.n_planes):
                npix_pl = np.array([stat[i][j]['npix'] for j in range(len(stat[i]))])
                npix.append(npix_pl)

            npix = np.concatenate(npix, axis=0)
        return npix
    
    def get_zoom_img(self, c_idxs=None, img_type='mean', win_size=32):
        """
        Extracts the zoomed in FOV around the median pixel of the ROIs.

        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
            img_type: str
                type of image to extract. Can be 'meanImg', 'meanImg_chan2' or 'max_proj'
            win_size: int
                size of the window around the median pixel to extract
        
        Returns:
            zoomin_fov: array (n_cells x win_size x win_size) or list of arrays
                zoomed in FOV around the median pixel of the ROIs for each plane.
        """

        meds = self.get_meds_session(c_idxs=c_idxs)
        img_load = self.get_img_session(img_type=img_type)
        


        if self.n_planes == 1:

            img = np.zeros((img_load.shape[0] + 2*win_size, img_load.shape[1] + 2*win_size))
            img[win_size:img_load.shape[0] + win_size, win_size:img_load.shape[1] + win_size] = img_load

            zoom_img = np.zeros((len(meds), win_size, win_size))
            for i in range(len(meds)):
                y, x = meds[i]

                x += win_size # account for padding
                y += win_size

                zoom_img[i, :, :] = img[y-win_size//2:y+win_size//2, x-win_size//2:x+win_size//2]
            

        elif self.n_planes > 1:
            zoom_img = []
            for i in range(self.n_planes):

                img = np.zeros((img_load[i].shape[0] + 2*win_size, img_load[i].shape[1] + 2*win_size))
                img[win_size:img_load[i].shape[0] + win_size, win_size:img_load[i].shape[1] + win_size] = img_load[i]

                zoom_img_pl = np.zeros((len(meds[i]), win_size, win_size))
                for j in range(len(meds[i])):
                    y, x = meds[i][j]

                    x += win_size # account for padding
                    y += win_size

                    zoom_img_pl[j, :, :] = img[y-win_size//2:y+win_size//2, x-win_size//2:x+win_size//2]

                zoom_img.append(zoom_img_pl)

            zoom_img = np.concatenate(zoom_img, axis=0)

        return zoom_img

    def get_zoom_roi(self, c_idxs=None, win_size=32, force_med_recalc=False):
        """
        Extracts the binary mask for the zoomed in FOV around the median pixel of the ROIs.
        
        Parameters:
            c_idxs: list
                List of arrays of indices of the neurons to extract. Each list corresponds to a plane. None to extract all neurons
            win_size: int
                size of the window around the median pixel to extract
        
        Returns:
            zoomin_roi: array (n_cells x win_size x win_size) or list of arrays
                binary mask for the zoomed in FOV around the median pixel of the ROIs for each plane.
        """

        meds = self.get_meds_session(c_idxs=c_idxs)
        stat = self.get_stat_session(c_idxs=c_idxs)

        if self.n_planes == 1:

            cropped_rois = 0
            zoomin_roi = np.zeros((len(meds), win_size, win_size))

            for i in range(meds.shape[0]):
                

                xpix = np.array(stat[i]['xpix'])
                ypix = np.array(stat[i]['ypix'])

                y, x = meds[:, i] if not force_med_recalc else np.median(np.array([ypix, xpix]), axis=1).astype(int)

                xpix_zoom = xpix - x + win_size//2
                ypix_zoom = ypix - y + win_size//2

                for x, y in zip(xpix_zoom, ypix_zoom):
                    if x >= win_size or y >= win_size:
                        cropped_rois += 1
                    else:
                        zoomin_roi[i, y, x] = 1

            print(f'In get_zoom_roi {cropped_rois}/{len(meds)} ROIs were cropped (do not fit within the window size - This does not affect the analysis, only zoomed in visualisation)')

        elif self.n_planes > 1:
            zoomin_roi = []
            for i in range(self.n_planes):

                cropped_rois = 0
                zoomin_roi_pl = np.zeros((len(meds[i]), win_size, win_size))

                for j in range(meds[i].shape[0]):
                    
      
                    xpix = np.array(stat[i][j]['xpix'])
                    ypix = np.array(stat[i][j]['ypix'])

                    y, x = meds[i][j] if not force_med_recalc else np.median(np.array([ypix, xpix]), axis=1).astype(int)

                    xpix_zoom = xpix - x + win_size//2
                    ypix_zoom = ypix - y + win_size//2 

                    for x, y in zip(xpix_zoom, ypix_zoom):

                        if x >= win_size or y >= win_size or x < 0 or y < 0:
                            cropped_rois += 1
                        else:
                            zoomin_roi_pl[j, y, x] = 1

                print(f'{cropped_rois}/{len(meds[i])} ROIs were cropped (do not fit within the window size for plane{i} - This does not affect the analysis, only zoomed in visualisation)')

                zoomin_roi.append(zoomin_roi_pl)
            
            zoomin_roi = np.concatenate(zoomin_roi, axis=0)

        return zoomin_roi
    
