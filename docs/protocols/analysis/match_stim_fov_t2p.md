# match_stim_fov_t2p.md ()
See `notebooks/match_stim_fov_t2p.ipynb` for associated notebook.

Because of the experimental pipeline the suite2p/track2p data (referred to as `t2p`) is not aligned to the opsin expression data (`fov`) / Bruker photostim metadata (`stim`) (the latter two are aligned, since the `stim` coordinates are chosen based on the segmentation of the `fov`).

The goal of this script is to align the three modalities and to match cells and stim positions across the different modalities in the general case.

For my (Jure's) specific use case I use it mostly to determine which cells were tracked across all days AND express the opsin AND were tracked across all days.

---

## Goals

The script performs the following high-level tasks:

1. Identify cells that **express ChRmine** (from FOV segmentation) **and** were **successfully tracked across all days** (Track2p → Suite2p ROIs).
2. Identify cells that were **stimulated** (photostimulation coordinates) **and** were **successfully tracked across all days**.
3. Export a **registered 1100 nm image** and associated metadata for downstream visualisation and analysis.

---

## Overview of the Pipeline

1. Load all FOV images (typically 830 nm, 920 nm, 1100 nm), Suite2p mean FOV, and photostimulation coordinates.
2. Optionally perform motion correction on raw FOV data using Suite2p’s motion correction algorithm.
3. Segment all FOV images using **cpsam** (Cellpose-based segmentation).
4. If not already present, manually annotate corresponding keypoints between:
   * the 1100 nm FOV image, and
   * the Suite2p mean image.
5. Compute an **affine transform** registering the 1100 nm FOV (moving image) to the Suite2p mean FOV (reference).
6. Apply affine transforms to:
   * keypoints,
   * photostimulation coordinates,
   * the 1100 nm image,
   * and the 1100 nm segmentation mask,
     so that all data are expressed in the Suite2p coordinate system.
7. Load Suite2p ROIs that were successfully tracked across days using Track2p.
8. Match:
   * stimulated coordinates → Suite2p ROIs, and
   * 1100 nm segmented cell centroids → Suite2p ROIs,
     using the Hungarian algorithm with Euclidean distance as the cost metric.
9. Apply a distance threshold (`max_dist_px`) to retain valid matches.
10. Visualise overlays of all registered data and highlight matched cells.
11. Export matched indices and registered images for downstream analysis.

---

## Inputs

## Key parameters (in notebook file)

* `subject`
  The unique identifier for the subject (by convention nn###, e. g. jm065)

### Configuration file: `match_stim_fov_t2p_config.yaml`

This configuration file contains parameters for motion correction, Suite2p ROI selection, stimulation info, session registration, matching, and plotting. These settings are used to process calcium imaging sessions and identify matched ROIs across sessions.

* `session_type` (`'_a'`, `'_s'`, etc.)
  Session suffix will decide in which folder the script will look for the FOV image. Typically, `_a` for spontaneous or `_s` for evoked sessions. **Make sure this matches the `track2p_dirname` if using track2p-based filtering.**
* `session_reg_idx` (int)
  Index of the session used as the reference for FOV registration across sessions. Usually `0` for the first session.
* `fov_imsize_onedim` (int)
  Size of the full field-of-view in pixels (assumed square) for FOV images.
* `s2p_imsize_onedim` (int)
  Size used for Suite2p processing (assumed square). Typically smaller than the full FOV to speed up processing.
* `n_stim_cell` (int)
  Number of 'cell' points that were stimulated.
* `n_stim_ctrl` (int)
  Number of 'control' points that were stimulated.
* `force_recompute` (bool)
  Whether to force recomputation of motion correction and segmentation even if processed files already exist.
* `run_motcorr` (bool)
  Whether to perform motion correction on the imaging data.
* `nimg_init` (int)
  Number of frames used to compute the reference image for motion correction.
* `filt_by` (`'t2p'`, `'iscell_cell_prob'`, `'iscell_manual_cur'`)
  Method to filter Suite2p ROIs for matching:
  * `'t2p'`: use track2p matching indices
  * `'iscell_cell_prob'`: use Suite2p cell probability
  * `'iscell_manual_cur'`: use manual curation
* `track2p_dirname` (str)
  Directory name containing track2p results. Only used if `filt_by` is `'t2p'`.
* `cell_prob_thr` (float)
  Threshold for Suite2p `iscell` probability to consider an ROI as a cell. Only used if `filt_by` is `'iscell_cell_prob'`.
* `max_dist_px` (int)
  Maximum distance (in pixels) allowed between points when matching coordinates between two sets.
* `sat_perc` (float)
  Saturation percentile used for plotting images to adjust contrast (e.g., `99.9`).


### Required data

* **FOV images** (e.g. 830 nm, 920 nm, 1100 nm)
* **Suite2p output**, including the mean image and ROI masks
* **Photostimulation coordinates** (e.g. Bruker MarkPoints)
* **Track2p outputs** identifying ROIs tracked across days

---

## Manual Keypoint Annotation

If no saved keypoints are found (or if `force_recompute=True`), the notebook opens a **Napari** viewer to manually add corresponding keypoints between:

* the upscaled Suite2p mean image (reference), and
* the 1100 nm FOV image (moving).

The annotated keypoints are saved to:

```
<experimenter>/<subject>/<session>/match_stim_fov_t2p/fov_reg_keypoints.csv
```

and reused in subsequent runs.

---

## Matching Strategy

* Centroids are extracted from:
  * 1100 nm segmentation masks, and
  * Suite2p ROIs (filtered to Track2p-tracked cells).
* Photostimulation coordinates loaded (already aligned to FOV)
* Stim coordinates and 1100nm segmentation masks are transformed into Suite2p space (registration).
* Matching is performed using the **Hungarian algorithm**, minimizing Euclidean distance.
* Matches exceeding `max_dist_px` are discarded.

---

## Outputs

All outputs are saved under:

```
<session_path>/match_stim_fov_t2p/
```

### Saved files

* `fov_s2p_keypoints.csv`
  A set of matched, manually annotated keypoints for registration of the `fov` image to the `s2p` one.
* `is_stim_and_t2p.npy`
  Boolean/index array identifying Suite2p ROIs that were both stimulated and tracked.
* `is_stim_and_t2p_idx.npy`
  Indices of stimulated ROIs (relative to stimulation order).
* `is_fov_and_t2p.npy`
  Boolean/index array identifying Suite2p ROIs that express opsin and were tracked.
* `is_fov_and_t2p_idx.npy`
  Indices of matched FOV-segmented cells.
* `fov_image_reg.npy`
  Registered 1100 nm image in Suite2p coordinate space.

---

## Visualisation

### Output figures
* `motcorr_<wl>.png`
  Cropped images showing the computation of mean `fov` image with or without motion correction.
* `fov_segmentation_overlay.png`
  Overlay of the Cellpose segmentations computed individually on each `fov` image (usually 830nm, 920nm and 1100nm)
* `fov_stim_segmentation_overlay.png`
  Overlay of the 1100nm `fov` segmentation and the stim points from Bruker metadata (MarkPoints)
* `keypoints_scatter.png`
  Manually labelled keypoints for `fov` and `suite2p` before and after registration


### Napari
The notebook uses **Napari** to visualise:

* Registered 1100 nm FOV image
* Registered Suite2p mean image
* Registered segmentation masks
* Suite2p ROI centroids
* Registered stimulation points
* Highlighted matched cells

This allows manual inspection and quality control of the registration and matching.

---

## Notes and Limitations

* Currently, the 1100 nm segmentation is recomputed using cpsam.
* Registration assumes a global affine transform (no non-linear warping).

---

## TODO

* Replace recomputed 1100 nm segmentation with manually curated segmentation from day 1 of each experiment.
* Export matching results in a format directly compatible with downstream tools (e.g. `longipy`).
