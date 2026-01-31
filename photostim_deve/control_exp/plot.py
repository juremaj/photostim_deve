import os 
import numpy as np
import matplotlib.pyplot as plt

def plot_fov(mn_image, export_path, vmax=400, use_seg='cellpose'):
    """
    Plot the mean FOV image.
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.imshow(mn_image, cmap='gray', vmin=0, vmax=vmax)
    plt.axis('off')
    plt.savefig(os.path.join(export_path, f'mean_fov_{use_seg}.png'), dpi=300)

def plot_fov_meds(mn_image, meds, inds, export_path, vmax=400, use_seg='cellpose', use_idx=False):
    """
    Plot the mean FOV image with all medians and the selected ones highlighted.
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.scatter(meds[:,1], meds[:,0], c='C0', s=1)
    count = 1 #pprairie view is 1-indexed
    for i in inds:
        plt.scatter(meds[i,1], meds[i,0], c='C1', s=1)
        # add text of index and x and y coordinates
        if use_idx:
            plt.text(meds[i,1], meds[i,0]+5, i, fontsize=5, color='C1', ha='right', va='top')
        else:
            # label with the count
            plt.text(meds[i,1], meds[i,0]+5, count, fontsize=5, color='C1', ha='right', va='top')
        count+=1

    plt.imshow(mn_image, cmap='gray', vmin=0, vmax=vmax)
    plt.axis('off')
    plt.savefig(os.path.join(export_path, f'medians_selected_{use_seg}.png'), dpi=300)

def plot_stim(fov_image, meds_stim, meds=None, sat_perc=99.9, title='Selected Stimulation Points', save_path=None):
    '''
    Plot the FOV image with selected stimulation points.

    Parameters:
    ----------
    fov_image: np.ndarray
        FOV image.
    meds_stim: np.ndarray
        Stimulation points (N x 2 array of (y, x) coordinates).
    meds: np.ndarray or None
        All cell centroids (N x 2 array of (y, x) coordinates). If provided, these will be plotted as well.
    sat_perc: float
        Saturation percentile for display.
    title: str
        Title for the plot.
    save_path: str or None
        Path to save the plot. If None, the plot is not saved.

    Returns:
    -------
    None      
    '''

    meds_stim_arange = np.arange(len(meds_stim)) + 1 # markpoints are 1-indexed in Bruker

    fig = plt.figure(figsize=(8, 8), dpi=300)
    plt.imshow(fov_image, cmap='gray', vmax=np.percentile(fov_image, sat_perc))
    if meds is not None:
        plt.scatter(meds[:,0], meds[:,1], c='C0', s=1)
    plt.scatter(meds_stim[:,0], meds_stim[:,1], c='C1', s=1)
    for i, (y, x) in enumerate(meds_stim):
        plt.text(y+3, x+3, str(meds_stim_arange[i]), color='C1', fontsize=8)
    plt.title(title)
    plt.axis('off')
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()

def plot_segmentation_overlay(fov_image, seg, sat_perc=99.9, title='', save_path=None):

    '''
    Segment all FOV images using Cellpose 'cpsam' pretrained model.
    
    Parameters:
    ----------
    fov_image: np.ndarray
        FOV image to segment.
    seg: np.ndarray
        Segmentation mask.
    sat_perc: float
        Saturation percentile for display.
    title: str
        Title for the plot.
    save_path: str or None
        Path to save the plot. If None, the plot is not saved.

    Returns:
    -------
    None
    '''

    fig = plt.figure(figsize=(8, 8), dpi=300)
    plt.imshow(fov_image, cmap='gray', vmax=np.percentile(fov_image, sat_perc))
    for label in range(1, np.max(seg) + 1):
        icolor = np.random.rand(3,)
        contour = np.where(seg == label, 1, 0)
        plt.contour(contour, colors=icolor, linewidths=0.5)
    plt.title(title)
    plt.axis('off')

    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
    plt.show()