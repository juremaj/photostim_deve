# now run cellpose on the images
from cellpose import models
from tqdm import tqdm
import numpy as np
from copy import deepcopy
import os 
from skimage.measure import regionprops


def segment_fov_cpsam(all_fov_image, diameter=None, flow_threshold=0.4, cellprob_threshold=0.0, resample=True, normalize=True, save_path=None, force_recompute=False, segment_only=None):
    '''
    Segment all FOV images using Cellpose 'cpsam' pretrained model.
    
    Parameters:
    ----------
    all_fov_image: dict
            Dictionary with FOV directory names as keys and corresponding mean images as values. Each FOV directory name corresponds to a different imaging wavelength. 
            An '_mn' suffix indicates the original mean image (non-motion corrected) if motion correction was applied, this will be skipped.
    diameter: int or None
        Estimated diameter of cells. If None, Cellpose will estimate it automatically.
    flow_threshold: float
        Flow error threshold for Cellpose segmentation.
    cellprob_threshold: float
        Cell probability threshold for Cellpose segmentation.
    resample: bool
        Whether to resample the image to have isotropic pixels.
    normalize: bool
        Whether to normalize the image intensity before segmentation.
    force_recompute: bool
        If True, forces recomputation of segmentation even if segmentation keys already exist in all_fov_image.
    save_path: str or None
        Path to save the segmentation results. If None, results are not saved.
    segment_only: list or None
        List of wavelength keys to segment. If None, all keys are segmented.

    Returns:
    -------
    all_fov_image_seg: 
        Dictionary with original keys plus additional keys for segmentation masks and number of labels.
        For each FOV directory name 'wl', two new entries are added:
        - 'wl_seg': The segmentation mask.
        - 'wl_nlabels': The number of detected objects.
    
    '''
    # 0.) check if segmentation has already been done
    if os.path.exists(os.path.join(save_path, 'all_fov_image_seg.npy')) and not force_recompute:
        print("Loading existing segmentation from file.")
        all_fov_image_seg = np.load(os.path.join(save_path, 'all_fov_image_seg.npy'), allow_pickle=True).item()
        return all_fov_image_seg


    # 1. instantiate the model (use GPU if available)
    model = models.CellposeModel(gpu=True, pretrained_model='cpsam')

    all_fov_image_seg = deepcopy(all_fov_image)

    for wl in tqdm(all_fov_image.keys()):

        # if segment_only is specified, skip wavelengths not in the list
        if segment_only is not None and wl not in segment_only:
            continue

        # if the key has '_mn' in it, skip (these are for plotting only when comparing motion correction)
        if '_mn' in wl:
            continue

        print("Processing wavelength:", wl)

        img = all_fov_image[wl]
        # 2. Cellpose expects a list of images, possibly with channel dimension(s).
        #    If your image is single-channel, wrap it in a list.
        imgs = [img]  # list of one image # TODO 

        # 3. Run segmentation
        #    You can tune e.g. flow_threshold, cellprob_threshold, diameter, etc.
        masks, _, _ = model.eval(
            imgs,
            diameter=diameter,
            flow_threshold=flow_threshold,
            cellprob_threshold=cellprob_threshold,
            resample=resample,
            normalize=normalize
        )

        # 4. masks[0] is the segmentation mask for your image
        seg = masks[0]
        nlabels = seg.max()
        print("Detected", nlabels, "objects")

        all_fov_image_seg[f'{wl}_seg'] = seg
        all_fov_image_seg[f'{wl}_nlabels'] = nlabels

    # save the images and segmentation dictionary as .npy file
    if save_path is not None:
        np.save(os.path.join(save_path, 'all_fov_image_seg.npy'), all_fov_image_seg, allow_pickle=True)

    return all_fov_image_seg


def get_cent_from_seg(fov_seg):
    """
    Compute ROI centroids from a segmentation mask.

    Parameters:
    ----------
    fov_seg : 2D numpy array
        Segmentation mask where each ROI is labeled with a unique integer.
    Returns:
    -------
    x_cent : 1D numpy array
        x-coordinates of the centroids of the ROIs.
    y_cent : 1D numpy array
        y-coordinates of the centroids of the ROIs.
    """

    props = regionprops(fov_seg)
    x_cent = np.array([prop.centroid[0] for prop in props])  # centroid returns (row, col)
    y_cent = np.array([prop.centroid[1] for prop in props])

    return x_cent, y_cent