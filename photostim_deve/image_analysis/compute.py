import numpy as np
import tifffile
import matplotlib.pyplot as plt
import os

from photostim_deve.image_analysis.plot import plot_resp_imgs

def get_resp_imgs(all_tiff_paths, stim_frames, stim_type, frame_avg_mode='mean', bsln_dur=500, resp_dur=2000, fov_shape=(512, 512), frame_period=0.033602476, plot_debug=False): 
    """ 
    Extract response images for each stimulation trail by taking the mean (or median) of the fluorescence of the frames in the 'baseline' and 'response' windows. 
    It also calculates the difference between the two. 
    Done for each trial type.
    
    
    Parameters: 
    ---------- 
    all_tiff_paths : list 
        List of paths to the registered tiff files for each trial. 
    stim_frames : list 
        List of frame indices for each stimulation. 
    stim_type : list 
        Evoked stim type index corresponding to each stimulation. 
    frame_avg_mode : str 
        Method to use for calculating the baseline and response images. Can be 'mean' or 'median'. Default is 'mean'.
    bsln_dur : int 
        Baseline duration in ms. Default is 500 ms. 
    resp_dur : int 
        Response duration in ms. Default is 2000 ms. 
    fov_shape : tuple
        Shape of the FOV in pixels. Default is (512, 512).
    frame_period : float 
        Exact frame period from metadata used to convert from time to frame index. Default is 0.033602476 (for '30Hz' acquisition). 
    plot_debug : bool
        Whether to plot the mean fluorescence across all pixels for each frame with the baseline and response windows overlaid for debugging and sanity checking the synchronisation. Default is False.
        

    Returns: 
    ------- 
    resp_bsln : np.ndarray
        Array of shape (n_stim_types, n_stim_repetitions, height, width) containing the baseline images for each stimulation type and repetition. 
    resp_resp : np.ndarray
        Array of shape (n_stim_types, n_stim_repetitions, height, width) containing the response images for each stimulation type and repetition.
    resp_diff : np.ndarray
        Array of shape (n_stim_types, n_stim_repetitions, height, width) containing the response - baseline images for each stimulation type and repetition.
    f_mean : np.ndarray
        The mean fluorescence across all pixels for each frame, used for debugging and sanity checking the synchronisation.
    """

    n_stim_types = len(np.unique(stim_type))
    n_stim_repetitions = len(stim_type) // n_stim_types # assuming equal number of repetitions for each stim type
    
    bsln_n_frames = int(np.ceil((bsln_dur/1000) / (frame_period))) # convert baseline duration from ms to number of frames
    resp_n_frames = int(np.ceil((resp_dur/1000) / (frame_period))) # convert response duration from ms to number of frames

    resp_bsln = np.zeros((n_stim_types, n_stim_repetitions, *fov_shape))
    resp_resp = np.zeros((n_stim_types, n_stim_repetitions, *fov_shape)) 
    resp_diff = np.zeros((n_stim_types, n_stim_repetitions, *fov_shape))

    f_mean = [] # used for debugging plot

    stim_idx_count = 0 # counter to keep track of the index of the current stimulation in the original stim_frames array to use for indexing the response arrays

    # 1) Loop thorough motion-corrected tiff files to extract response images
    for (i, tiff_path) in enumerate(all_tiff_paths):

        print(f'Processing tiff file: {tiff_path}')

        # Taking the current and +1th tiff file in case the stimulus time crosses into the next tiff file (due to chunking) (edge case)
        if i != len(all_tiff_paths) - 1:
            tiff_data = np.concatenate((tifffile.imread(tiff_path), tifffile.imread(all_tiff_paths[i+1])), axis=0) 
            f_mean.append(np.mean(tiff_data[:tiff_data.shape[0]//2], axis=(1, 2))) # for debugging plot
        else: 
            tiff_data = tifffile.imread(tiff_path) 
            f_mean.append(np.mean(tiff_data, axis=(1, 2))) # for debugging plot

        # 2) Loop through stim types (currently this only applies to photostim, since in evoked there is only one stim type) in the current tiff file
        for j in range(n_stim_types): 

            stim_type_j_frames = stim_frames[stim_type == j] # get the stim frames for the current stim type 
            
            # setting the bounds for stimulus times (add the bsln_nframes+1 in case the stimulus time crosses into the next tiff file (due to chunking) (edge case))
            frame_lims = (i * tiff_data.shape[0]//2, (i+1) * tiff_data.shape[0]//2 + bsln_n_frames + 1) 

            stim_type_j_frames_in_tiff = stim_type_j_frames[(stim_type_j_frames >= frame_lims[0]) & (stim_type_j_frames < frame_lims[1])] # get the stim frames that are in the current tiff file 
            stim_type_j_frames_in_tiff = stim_type_j_frames_in_tiff - frame_lims[0] # adjust the frame indices to be relative to the current tiff file (assuming each tiff file has the same number of frames except last one)
                        
            if plot_debug:
                plt.figure(figsize=(20, 2)) 
                plt.plot(f_mean[-1]) # plot the mean fluorescence for the current tiff file to check for synchronisation
            
            # 3) Loop through repetitions of stim type j in the current tiff file
            for k, stim_frame in enumerate(stim_type_j_frames_in_tiff): 
                stim_idx = stim_idx_count # get the index of the current stimulation in the original stim_frames array to use for indexing the response arrays
                bsln_start = stim_frame - bsln_n_frames
                bsln_end = stim_frame
                resp_start = stim_frame
                resp_end = stim_frame + resp_n_frames

                # add exception to skip the trial (in case the stimulus time crosses into the next tiff file (due to chunking) (edge case))
                if bsln_start < 0:
                    print(f"Skipping trial at frame {stim_frame} \nBaseline window extends beyond the start of the tiff file. \nTrial was accounted for in the previous loop iteration (tiff file).")
                    continue

                if plot_debug:
                    plt.axvline(bsln_start, color=f'C{k}', linestyle=':')
                    plt.axvline(resp_start, color=f'C{k}', linestyle='--', label=f's{j}, r{k}')
                    plt.axvline(resp_end, color=f'C{k}', linestyle=':')
                
                # 4) Calculate the baseline, response and the difference
                if frame_avg_mode == 'mean':
                    resp_bsln[j, stim_idx] = np.mean(tiff_data[bsln_start:bsln_end], axis=0)
                    resp_resp[j, stim_idx] = np.mean(tiff_data[resp_start:resp_end], axis=0)
                    resp_diff[j, stim_idx] = resp_resp[j, stim_idx] - resp_bsln[j, stim_idx]
                elif frame_avg_mode == 'median':
                    resp_bsln[j, stim_idx] = np.median(tiff_data[bsln_start:bsln_end], axis=0) 
                    resp_resp[j, stim_idx] = np.median(tiff_data[resp_start:resp_end], axis=0) 
                    resp_diff[j, stim_idx] = resp_resp[j, stim_idx] - resp_bsln[j, stim_idx] 
                else: 
                    raise ValueError(f"Invalid mode: {frame_avg_mode}. Mode should be 'mean' or 'median'.") 
                
                stim_idx_count += 1 # increment the stim index counter after processing each stimulation trial

            if plot_debug:
                plt.legend(loc='upper center', ncol=len(stim_type_j_frames_in_tiff), fontsize='small') if len(stim_type_j_frames_in_tiff) > 0 else None
                plt.show()
                for l in range(len(stim_type_j_frames_in_tiff)):
                    plot_resp_imgs(resp_bsln[j, l], resp_resp[j, l], resp_diff[j, l], j=j, l=l)
                    
                    
    return resp_bsln, resp_resp, resp_diff, np.concatenate(f_mean)