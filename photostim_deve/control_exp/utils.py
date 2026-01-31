import numpy as np

def remove_edge_masks(fov_image, seg, edge_excl=0.10):
    '''
    Remove masks that touch the edges of the FOV image.
    
    Parameters:
    ----------
    fov_image: np.ndarray
        FOV image.
    seg: np.ndarray
        Segmentation mask.
    edge_excl: float
        Proportion of the image edges to exclude.

    Returns:
    -------
    seg: np.ndarray
        Updated segmentation mask with edge masks removed.
    '''
    seg_cur = np.copy(seg)
    for label in range(1, np.max(seg_cur) + 1):
        mask = (seg_cur == label)
        coords = np.column_stack(np.where(mask))
        if (np.any(coords[:,0] < edge_excl * fov_image.shape[0]) or 
            np.any(coords[:,0] > fov_image.shape[0] - edge_excl * fov_image.shape[0]) or 
            np.any(coords[:,1] < edge_excl * fov_image.shape[1]) or 
            np.any(coords[:,1] > fov_image.shape[1] - edge_excl * fov_image.shape[1])):
            seg_cur[mask] = 0
    return seg_cur