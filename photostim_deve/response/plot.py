import numpy as np
import matplotlib.pyplot as plt

def plot_xyoff(xoff, yoff, save_path=None):
    """
    Plot the x and y offsets from the suite2p motion correction.
    """

    plt.figure(figsize=(10, 1), dpi=300)
    plt.title('Movement correction offsets')
    plt.plot(xoff, label='x')
    plt.plot(yoff, label='y')
    plt.xlabel('Frame')
    plt.ylabel('Offset (px)')
    plt.legend(loc='upper right')

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

def plot_protocol(all_frame, all_point, n_frames=36000, save_path=None):
    """
    Plot the photostimulation protocol.
    """
    plt.figure(figsize=(10, 2), dpi=200)
    for point_idx in np.unique(all_point):
        x = all_frame[all_point == point_idx]
        y = np.ones_like(x) * point_idx
        plt.scatter(x, y, label=f'Point {point_idx}', s=1)
    plt.xlabel('Frame')
    plt.ylabel('Point')
    plt.title('Photostim protocol')
    plt.xlim(0, n_frames)
    # invert y axis
    plt.gca().invert_yaxis()

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

def plot_fov_diff_single(fov_diff, all_point, all_coords_x, all_coords_y, stim_idx, vlim=200, save_path=None):
    """
    Plot the difference image for a single stimulation trial.
    """
    point = all_point[stim_idx]
    
    plt.figure()
    plt.imshow(fov_diff[stim_idx, :, :], cmap='bwr', vmin=-vlim, vmax=vlim)
    
    plt.scatter(all_coords_y[stim_idx], all_coords_x[stim_idx], color='black', s=1, label='Stimulus Point')
    plt.title(f'point {point}')
    plt.axis('off')

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    

def plot_fov_all_point(mn_image, all_point, all_coords_x, all_coords_y, txt_shift=(7, 7), save_path=None, sat_perc=99):
    """
    Plot the mean image map with the stimulation points.
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(mn_image, cmap='gray', vmin=0, vmax=np.percentile(mn_image, sat_perc))

    for i in np.unique(all_point):
        plt.scatter(all_coords_y[i], all_coords_x[i], color='C0', s=1, label='stim point')
        plt.text(all_coords_y[i] + txt_shift[0], all_coords_x[i] + txt_shift[1], str(i), color='C0', fontsize=8, ha='center', va='center')
        plt.axis('off')

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

def zscore_act(act):
    """
    Z-score the rows of a 2D array for visualization.
    """
    act_mean = np.mean(act, axis=1, keepdims=True)
    act_std = np.std(act, axis=1, keepdims=True)
    return (act - act_mean) / act_std
    

def plot_dist_dff(dist_diff_mn, n_points=40, dist_bins_xlim=362, dist_bins_xlim_zoom=45, save_path=None):
    """
    Plot the mean df/f as a function of distance from the stimulus point.

    ------------------

    Parameters:

        dist_diff_mn : (np.ndarray)
            Each row corresponds to the mean of the pixel values for all pixels within a distance bin from a stimulus point. Rows correspond to different stimulus points.
        n_points : (int)
            Number of unique stimulus points in the experiment.
        dist_bins_xlim : (int)
            The x-axis limit for the main plot.
        dist_bins_xlim_zoom : (int)
            The x-axis limit for the zoomed-in plot.
        save_path : (str or None)
            Path to save the plot. If None, the plot will not be saved.
            
    """

    fig, axs = plt.subplots(n_points+1, 2, figsize=(10, 2*(n_points+1)), gridspec_kw={'width_ratios': [5, 1]})
    for i in range(n_points):
        axs[i, 0].plot(dist_diff_mn[i, :], label='mn', c='grey')
        axs[i, 0].set_xlim(0, dist_bins_xlim)
        axs[i, 0].set_ylabel(f'point {i}')

        # now same as above but zoomed in   
        axs[i, 1].plot(dist_diff_mn[i, :], label='mn', c='grey')
        axs[i, 1].set_xlim(0, dist_bins_xlim_zoom)

        # remove all top and right spines
        axs[i, 0].spines['top'].set_visible(False)
        axs[i, 0].spines['right'].set_visible(False)
        axs[i, 1].spines['top'].set_visible(False)
        axs[i, 1].spines['right'].set_visible(False)

        # only put x tick labels on the bottom row
        axs[i, 0].set_xticklabels([])
        axs[i, 1].set_xticklabels([])

    axs[i+1, 0].plot(dist_diff_mn.T,c='grey', alpha=0.1)
    axs[i+1, 0].plot(np.nanmean(dist_diff_mn, axis=0))
    axs[i+1, 0].set_xlim(0, dist_bins_xlim)
    
    axs[i+1, 1].plot(dist_diff_mn.T,c='grey', alpha=0.1)
    axs[i+1, 1].plot(np.nanmean(dist_diff_mn, axis=0))
    axs[i+1, 1].set_xlim(0, dist_bins_xlim_zoom)
    axs[i+1, 0].set_ylabel('mean')

    axs[i+1, 0].set_xlabel('Dist (pixels)')
    axs[i+1, 1].set_xlabel('Dist (pixels)')

    axs[i+1, 0].spines['top'].set_visible(False)
    axs[i+1, 0].spines['right'].set_visible(False)
    axs[i+1, 1].spines['top'].set_visible(False)
    axs[i+1, 1].spines['right'].set_visible(False)

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

def plot_fov_map(fov_plot, all_coords_x, all_coords_y, vlim=200, save_path=None, n_rows=8):
    """
    Plot the fov_map with all stim points overlaid.

    Parameters:
        fov_plot : (np.ndarray)
            The response map with shape (n_stim_points, height, width) where each slice corresponds to a mean pixel response to a stimulus point.
        all_coords_x : (np.ndarray)
            X coordinates of the stimulus point corresponding to each stimulation
        all_coords_y : (np.ndarray)
            Y coordinates of the stimulus point corresponding to each stimulation
        vlim : (int)
            Saturation limits for visualizing fov_map.
    """

    n_cols = int(fov_plot.shape[0] / n_rows)
    
    if fov_plot.shape[0] % n_rows != 0:
        n_cols += 1

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*4, n_rows*4), dpi=300)

    for i in range(n_rows):
        for j in range(n_cols):
            idx = i * n_cols + j
            if idx < fov_plot.shape[0]:
                axs[i, j].imshow(fov_plot[idx, :, :], cmap='bwr', vmin=-vlim, vmax=vlim)
                axs[i, j].scatter(all_coords_y[idx], all_coords_x[idx], color='black', s=0.5, label='Stimulus Point')
                axs[i, j].set_title(f'point {idx}')
            axs[i, j].axis('off')
       

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=600)

def plot_kernel_2d(k2d, fov_shape=(512, 512), n_dist_bins=724, vlim=200, save_path=None):
    """
    Plot the 2D kernel.
    
    Parameters:
        k2d : (np.ndarray)
            The 2D kernel to plot.
        fov_shape : (tuple)
            Shape of the field of view (height, width).
        vlim : (int)
            Saturation limits for visualizing the kernel.
    """

    # Display
    plt.imshow(k2d, cmap='bwr', vmin=-vlim, vmax=vlim)
    plt.colorbar()

    cent_xy = n_dist_bins//2

    plt.scatter(cent_xy, cent_xy, color='black', s=1, label='Stimulus Points')
    plt.title("2D Rotated Measured Kernel")
    plt.xlim(cent_xy - fov_shape[1]//2, cent_xy + fov_shape[1]//2)
    plt.ylim(cent_xy - fov_shape[0]//2, cent_xy + fov_shape[0]//2)
    plt.axis('off')
    
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)

def plot_fov_map_avg(fov_map, all_coords_x, all_coords_y, all_point, all_point_s2p_idx, meds, s2p_idxs, txt_shift=10, sat_perc_fov=99.9, save_path=None):
    
    """
    Plot the average fluorescence map for the field of view (FOV) across all stimulation points, with markers for the stimulation points and their matched ROIs.
    This allows the user to visualise which parts of the FOV were stimulated/responded in a single plot.
    """

    plt.figure(figsize=(10, 10))
    # plt.imshow(np.mean(np.abs(fov_map), axis=0), cmap='gray', vmin=0, vmax=np.percentile(np.mean(np.abs(fov_map), axis=0), sat_perc_fov))
    plt.imshow(np.mean(fov_map, axis=0), cmap='gray', vmin=0, vmax=np.percentile(np.mean(fov_map, axis=0), sat_perc_fov))

    for i in np.unique(all_point):
        plt.scatter(all_coords_y[i], all_coords_x[i], color='C0', s=1, label='stim point')
        plt.text(all_coords_y[i] + txt_shift[0], all_coords_x[i] + txt_shift[1], str(i), color='C0', fontsize=8, ha='center', va='center')

        s2p_cent_y = meds[np.where(s2p_idxs == all_point_s2p_idx[i])[0], 1]
        s2p_cent_x = meds[np.where(s2p_idxs == all_point_s2p_idx[i])[0], 0]

        plt.scatter(s2p_cent_y, s2p_cent_x, color='C1', s=1, label='matched ROI')
        plt.text(s2p_cent_y + txt_shift[0], s2p_cent_x - txt_shift[1], str(all_point_s2p_idx[i]), color='C1', fontsize=8, ha='center', va='center')

        # only include first two elements in the legend
        if i == 0:
            plt.legend()

        plt.axis('off')

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

def plot_raster_matched_rois(f, all_point_s2p_idx, all_frame, save_path=None):
    """
    Plot the raster of the matched ROIs to the stimulation points during the stimulation protocol (period).
    """

    # now plot the traces corresponding to the stimulus (of raw fluorescence)
    f_point_s2p = f[all_point_s2p_idx, :]

    plt.figure(figsize=(20, 2), dpi=300)
    # zscore rows
    # restrict to the stim period

    f_point_s2p_stim_epoch = f_point_s2p[:, all_frame[0]:all_frame[-1]]  # restrict to the stim period

    plt.imshow(zscore_act(f_point_s2p_stim_epoch), aspect='auto', cmap='gray_r', vmin=0, vmax=2)
    
    if save_path is not None:
        plt.savefig(save_path)
    
def plot_raster_matched_rois_avg(f, all_point_s2p_idx, all_frame, all_point, save_path=None):
    """
    Plot the raster of the matched ROIs to the stimulation points during the stimulation protocol (period).
    Average across all repetitions of each stimulation point.
    """
    f_point_s2p = f[all_point_s2p_idx, :]

    f_point_s2p_stim_epoch = f_point_s2p[:, all_frame[0]:all_frame[-1]]  # restrict to the stim period

    n_frames_repetition = int(all_frame[np.where(all_point==0)][1] - all_frame[np.where(all_point==0)][0] + 1)
    print(f"Number of frames per repetition: {n_frames_repetition}")

    f_point_s2p_stim_epoch_mn = np.zeros((f_point_s2p_stim_epoch.shape[0], n_frames_repetition))

    offset = 0
    for i in range(sum(all_point == 0)-1):
        mask = np.arange(offset, offset + n_frames_repetition)
        f_point_s2p_stim_epoch_mn += f_point_s2p_stim_epoch[:, mask]
        offset += n_frames_repetition


    f_point_s2p_stim_epoch_mn /= sum(all_point == 0)


    plt.figure(figsize=(2, 2), dpi=300)
    plt.imshow(zscore_act(f_point_s2p_stim_epoch_mn), aspect='auto', cmap='gray_r', vmin=0, vmax=5, interpolation='nearest')

    if save_path is not None:
        plt.savefig(save_path)

def plot_response_matched_rois(s2p_resp, all_point_s2p_idx, n_points, peristim_wind, n_rows_fov=10, save_path=None):
    """
    Plot the responses of matched ROIs to the stimulation points during the stimulation protocol. Each trial is shown as a grey line, the mean across trials is shown as a blue line.
    """
    
    n_cols = n_rows_fov
    n_rows = n_points // n_cols
    if n_points % n_cols != 0:
        n_rows += 1

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*2, n_rows*2), dpi=300)

    for i in range(n_rows):
        for j in range(n_cols):
            idx = i * n_cols + j
            if idx < n_points:
                axs[i, j].plot(s2p_resp[idx, :, :].T, color='grey', alpha=0.1)
                axs[i, j].plot(np.mean(s2p_resp[idx, :, :], axis=0), color='black', alpha=0.5, zorder=10)
                axs[i, j].axvline(peristim_wind[0], color='k', linestyle='--')
                axs[i, j].set_xticks([peristim_wind[0], (peristim_wind[1])/2 + peristim_wind[0], peristim_wind[1] + peristim_wind[0]])
                axs[i, j].set_xticklabels([0, 0.5, 1])
                axs[i, j].set_title(f'ROI {all_point_s2p_idx[idx]} (point {idx})', fontsize=8)

                # remoeve all top and right spines
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)

                # only put x tick labels and axis label on the bottom row
                if i == n_rows - 1:
                    axs[i, j].set_xlabel('Time (s)')
                else:
                    axs[i, j].set_xticklabels([])
                
                # remove all y tick labels
                if j == 0:
                    axs[i, j].set_ylabel('F (a.u.)')
                
                axs[i, j].set_yticklabels([])
            else:
                axs[i, j].axis('off')
    # reduce the spacing between the subplots
    plt.tight_layout()
    # now add suptitle with a bit of padding
    plt.suptitle('Response of s2p ROI nearest to stim point', fontsize=16, y=1.02)

    if save_path is not None:
        plt.savefig(save_path)


def plot_response_matched_rois_heatmap(s2p_resp, all_point_s2p_idx, n_points, peristim_wind, n_rows_fov=10, vlim_std=8, save_path=None):
    """
    Plot the responses of matched ROIs to the stimulation points during the stimulation protocol. Each trial is shown as a line of a heatmap.
    Plotting the same data as plot_response_matched_rois but as a heatmap.
    """

    # now the same but with the diferent visualsiation
    plt.figure(figsize=(2, 2), dpi=300)

    # take the cell above as the template and plot again a 4 by 10 grid of the responses
    n_cols = n_rows_fov
    n_rows = n_points // n_cols

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(n_cols*2, n_rows*2), dpi=300)

    for i in range(n_rows):
        for j in range(n_cols):
            idx = i * n_cols + j
            if idx < n_points:
                
                axs[i, j].imshow(s2p_resp[idx, :, :], aspect='auto', cmap='bwr', vmin=np.median(s2p_resp[idx, :, :]) - vlim_std * np.std(s2p_resp[idx, :, :]), vmax=np.median(s2p_resp[idx, :, :]) + vlim_std * np.std(s2p_resp[idx, :, :]))
                axs[i, j].axvline(peristim_wind[0], color='k', linestyle='--')
                axs[i, j].set_xticks([peristim_wind[0], (peristim_wind[1])/2 + peristim_wind[0], peristim_wind[1] + peristim_wind[0]])
                axs[i, j].set_xticklabels([0, 0.5, 1])
                axs[i, j].set_title(f'ROI {all_point_s2p_idx[idx]} (point {idx})', fontsize=8)
                


                # remoeve all top and right spines
                axs[i, j].spines['top'].set_visible(False)
                axs[i, j].spines['right'].set_visible(False)

                # only put x tick labels and axis label on the bottom row
                if i == n_rows - 1:
                    axs[i, j].set_xlabel('Time (s)')
                else:
                    axs[i, j].set_xticklabels([])
                
                # remove all y tick labels
                if j == 0:
                    axs[i, j].set_ylabel('Repetition')
                
                axs[i, j].set_yticklabels([])

    # reduce the spacing between the subplots
    plt.tight_layout()
    # now add suptitle with a bit of padding
    plt.suptitle('Response of s2p ROI nearest to stim point', fontsize=16, y=1.02)
    
    if save_path is not None:
        plt.savefig(save_path)

def plot_response_matched_rois_avg(s2p_resp, peristim_wind=[10, 30], vlim_std=8,save_path=None):
    """
    Plot the summary responses for all ROIs averaged across all trial repetitions for that ROI. Shown as a heatmap.
    """
    s2p_resp_mn = np.mean(s2p_resp, axis=1)
    plt.figure(figsize=(2, 2), dpi=300)
    plt.imshow(s2p_resp_mn, aspect='auto', cmap='bwr', vmin= - vlim_std * np.std(s2p_resp_mn), vmax= vlim_std * np.std(s2p_resp_mn))
    plt.axvline(peristim_wind[0], color='k', linestyle='--')
    plt.ylabel('Point')
    plt.xlabel('Time (s)')
    plt.title('Mean F of s2p ROI')
    plt.colorbar(label='F (a.u.)')

    if save_path is not None:
        plt.savefig(save_path)