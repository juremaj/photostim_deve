import matplotlib.pyplot as plt
import numpy as np

def plot_motcorr_comparison(all_fov_image, sat_perc=99.99, crop=(64, 64)):

    """
    Plots comparison between original mean image and motion corrected mean image for each FOV.

    Parameters:
    ----------
    all_fov_image: dict
        Dictionary with FOV directory names as keys and corresponding mean images as values.
    sat_perc: float
        Saturation percentile for image display. Default is 99.99.
    crop: tuple
        Tuple indicating the crop size (height, width) around the center of the image. Default is (64, 64).

    Returns:
    -------
    None
    """


    for key in all_fov_image.keys():
        if key.endswith('_mn'):
            continue
        
        session_fov_dir = key
        fov_image_mn = all_fov_image[session_fov_dir + '_mn']
        fov_image_motcorr_mn = all_fov_image[session_fov_dir]

        fig, axs = plt.subplots(1, 2, figsize=(10, 5), dpi=300)
        fov_image_mn_crop = fov_image_mn[fov_image_mn.shape[0]//2 - crop[0]:fov_image_mn.shape[0]//2 + crop[0], fov_image_mn.shape[1]//2 - crop[1]:fov_image_mn.shape[1]//2 + crop[1]]
        axs[0].imshow(fov_image_mn_crop, cmap='gray', vmin=np.percentile(fov_image_mn, 100 - sat_perc), vmax=np.percentile(fov_image_mn, sat_perc))
        axs[0].set_title('Original mean image (cropped)')
        axs[0].axis('off')

        fov_image_motcorr_mn_crop = fov_image_motcorr_mn[fov_image_motcorr_mn.shape[0]//2 - crop[0]:fov_image_motcorr_mn.shape[0]//2 + crop[0], fov_image_motcorr_mn.shape[1]//2 - crop[1]:fov_image_motcorr_mn.shape[1]//2 + crop[1]]
        axs[1].imshow(fov_image_motcorr_mn_crop, cmap='gray', vmin=np.percentile(fov_image_motcorr_mn, 100 - sat_perc), vmax=np.percentile(fov_image_motcorr_mn, sat_perc))
        axs[1].set_title('Motion corrected mean image (cropped)')
        axs[1].axis('off')
        plt.show()

def plot_segmentation_overlay_dict(all_fov_image_seg, sat_perc=99.99):
    '''
    Plot segmentation overlay for all FOVs in the all_fov_image_seg dictionary.

    Parameters:
    ----------
    all_fov_image_seg: dict
        Dictionary containing images and segmentation masks for all FOVs.
    sat_perc: float
        Saturation percentile for image display.
        
    Returns:
    -------
    None
    '''

    n_fov = len([key for key in all_fov_image_seg.keys() if key.endswith('nm')])
    
    fig, axs = plt.subplots(1, n_fov, figsize=(5*n_fov, 5), dpi=300)
    count=0
    for key in all_fov_image_seg.keys():
        if key.endswith('nm'):
            img = all_fov_image_seg[key]
            seg = all_fov_image_seg[f'{key}_seg']

            # now plot
            img_sat = np.percentile(img, sat_perc)
            axs[count].imshow(img, cmap='gray', vmin=0, vmax=img_sat)
            # axs[count].imshow(seg, cmap='jet', alpha=0.5)
            # plot the segmentation as contours
            axs[count].contour(seg>0, colors='C0', linewidths=0.4)
            axs[count].set_title(f'FOV {count+1} - {key}')
            axs[count].axis('off')

            count+=1

def plot_image_seg_xy_stim(image, x_stim=None, y_stim=None, segmentation=None, sat_perc=99.9, fov_s2p_px_fact=2):
    """
    Plots the given image with optional stimulation points and segmentation overlay.

    Parameters:
    ----------
    image : 2D array
        The image to be displayed.
    x_stim : 1D array, optional
        X coordinates of stimulation points (in Suite2p pixel coordinates).
    y_stim : 1D array, optional
        Y coordinates of stimulation points (in Suite2p pixel coordinates).
    segmentation : 2D array, optional
        Segmentation mask to overlay on the image.
    sat_perc : float, optional
        Saturation percentile for contrast adjustment (default is 99.9).
    fov_s2p_px_fact : float, optional
        Scaling factor from Suite2p pixels to FOV pixels (default is 2).
    
    Returns:
    -------
    None
    """
    
    plt.figure(figsize=(8, 8), dpi=300)
    vmin = np.percentile(image, 100 - sat_perc)
    vmax = np.percentile(image, sat_perc)
    plt.imshow(image, cmap='gray', vmin=vmin, vmax=vmax)
    if x_stim is not None and y_stim is not None:
        plt.scatter(y_stim * fov_s2p_px_fact, x_stim * fov_s2p_px_fact, c='C1', s=10, marker='x')
    if segmentation is not None:
        plt.contour(segmentation, colors='C0', linewidths=0.5)
    plt.title('Stimulation points on FOV image')
    plt.axis('off')
    plt.show()

def plot_keypoints_scatter(x_s2p, y_s2p, x_fov, y_fov, x_fov_reg=None, y_fov_reg=None):
    """
    Plot scatter of keypoints from s2p and fov images (including optionally registered fov keypoints).

    Parameters:
    -----------
    x_s2p: np.ndarray
        X coordinates of s2p keypoints.
    y_s2p: np.ndarray
        Y coordinates of s2p keypoints.
    x_fov: np.ndarray
        X coordinates of fov keypoints.
    y_fov: np.ndarray
        Y coordinates of fov keypoints.
    x_fov_reg: np.ndarray
        X coordinates of registered fov keypoints.
    y_fov_reg: np.ndarray
        Y coordinates of registered fov keypoints.
        
    Returns:
    -------
    None
    """

    plt.figure(figsize=(8, 8), dpi=300)
    plt.scatter(x_s2p, y_s2p, c='green', label='s2p keypoints')
    plt.scatter(x_fov, y_fov, c='magenta', label='fov 1100nm keypoints')
    if x_fov_reg is not None and y_fov_reg is not None:
        plt.scatter(x_fov_reg, y_fov_reg, c='magenta', label='fov 1100nm keypoints (registered)', marker='x')
    plt.xlabel('X (pixels)')
    plt.ylabel('Y (pixels)')
    plt.title('Keypoints scatter plot')
    plt.legend()
    plt.axis('equal')
    plt.show()