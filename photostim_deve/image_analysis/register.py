import numpy as np
from skimage.transform import AffineTransform
from scipy.optimize import linear_sum_assignment


def register_keypoints_affine(x_s2p, y_s2p, x_fov, y_fov):
    """
    Register keypoints from FOV to Suite2p image using an affine transformation.

    Parameters:
    ----------
    x_s2p: np.ndarray
        x-coordinates of keypoints in Suite2p image.
    y_s2p: np.ndarray
        y-coordinates of keypoints in Suite2p image.
    x_fov: np.ndarray
        x-coordinates of keypoints in FOV image.
    y_fov: np.ndarray
        y-coordinates of keypoints in FOV image.

    Returns:
    -------
    x_fov_reg: np.ndarray
        Registered x-coordinates of keypoints in FOV image.
    y_fov_reg: np.ndarray
        Registered y-coordinates of keypoints in FOV image.
    transform: AffineTransform
        The fitted affine transformation object.
    """

    transform = AffineTransform()
    transform.estimate(
        src=np.stack([x_fov, y_fov], axis=1),
        dst=np.stack([x_s2p, y_s2p], axis=1)
    )
    print('Transformation matrix:')
    print(transform.params)

    x_fov_reg, y_fov_reg = transform(np.stack([x_fov, y_fov], axis=1)).T

    return x_fov_reg, y_fov_reg, transform

def match_ref_moving(x_ref, y_ref, x_mov, y_mov, max_dist_px=7):
    """
    Match reference points to moving points using linear sum assignment and distance thresholding.

    Parameters:
    ----------
    x_ref : 1D numpy array
        x-coordinates of the reference points.
    y_ref : 1D numpy array
        y-coordinates of the reference points.
    x_mov : 1D numpy array
        x-coordinates of the moving points.
    y_mov : 1D numpy array
        y-coordinates of the moving points.
    max_dist_px : float
        Maximum distance in pixels for a valid match.

    Returns:
    -------
    row_ind : 1D numpy array
        Indices of matched reference points.
    col_ind : 1D numpy array
        Indices of matched moving points.
    """

    dists = np.sqrt((x_ref[:, np.newaxis] - x_mov[np.newaxis, :])**2 + (y_ref[:, np.newaxis] - y_mov[np.newaxis, :])**2)

    row_ind, col_ind = linear_sum_assignment(dists)

    # now filter matches based on hard threshold (e.g., 5 um (~7 pixels in upscaled space))
    max_dist_px = 7  # maximum distance in pixels for a valid match
    valid_matches = dists[row_ind, col_ind] <= max_dist_px
    row_ind = row_ind[valid_matches]
    col_ind = col_ind[valid_matches]
    print(f"Number of valid matches: {len(row_ind)}")

    return row_ind, col_ind