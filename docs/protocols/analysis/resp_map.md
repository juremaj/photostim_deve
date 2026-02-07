# resp_map.md
See `notebooks/resp_map.ipynb` for associated notebook.

This notebook is a **helper / exploratory analysis script** to visualise and quantify photostimulation-evoked responses at the FOV and ROI level after Suite2p processing. It links **MarkPoints stimulation metadata**, **motion-corrected TIFF data**, and **Suite2p outputs** to produce response maps, distance-dependent analyses, kernels, and ROI-aligned activity plots.

It is mainly intended for:

* sanity-checking photostim experiments,
* inspecting spatial structure of responses,
* generating figures for calibration and exploratory analysis.

## NOTE: UNDER CONSTRUCTION

This script is still a preliminary version, so there are still many changes to be implemented.
After that is done I (Jure) will also update this documentation.

---

## High-level workflow

1. Load experiment/session parameters and plotting configuration
2. Load Suite2p outputs (mean image, ROI medians, fluorescence traces, motion offsets)
3. Load photostimulation protocol (MarkPoints → CSV)
4. Extract baseline and response windows from motion-corrected TIFF stacks
5. Compute per-point FOV response maps (mean & median)
6. Analyse responses as a function of distance from stimulation site
7. Compute spatial kernels from distance–response profiles
8. Match stimulation points to nearest Suite2p ROIs (TODO: implement registration as in `match_stim_fov_t2p.ipynb`)
9. Visualise ROI-aligned raster plots and average responses
10. (Optional) Save calibration metrics for later analysis

---

## Inputs

## Key parameters (in notebook file)


* `data_dir` (str)
  The directory on where the data are saved (sub-directories are dedicated to each experimenter in `nn` format e. g. `jm`)
* `experimenter`
  The unique identifier for the experimenter (by convention `nn`, e. g. `jm`)
* `subject`
  The unique identifier for the subject (by convention `nn###`, e. g. `jm065`)
* `session` 
  The unique identifier for the session (by convention `YYYY-MM-DD_x`, e. g. `2026-02-07_b`, where the suffix should be related to a photostim session, meaning between `_b` - `_f`)


### Configuration file: `resp_map_config.yaml`

This configuration file contains parameters for response mapping from calcium imaging data. It controls data selection, baseline and response windows, spatial analysis, and visualization.

* `channel` (int)
  Imaging channel to use for analysis. Typical values are `1` or `2` depending on the acquisition.
* `plane` (int)
  Imaging plane index for Suite2p or raw data selection.
* `frame_period` (float)
  Time between frames in seconds. Derived from metadata (e.g., 0.0336 s for ~30 Hz acquisition).
* `fov_shape` (list of int)
  Shape of the field-of-view in pixels `[height, width]`. Example: `[512, 512]`.
* `bsln_n_frames` (int)
  Number of frames used for baseline calculation per trial.
* `resp_n_frames` (int)
  Number of frames used to quantify the response per trial.
* `bsln_sub_type` (`'trial_by_trial'`, `'session_wide'`)
  Method to subtract baseline:
  * `'trial_by_trial'`: subtract baseline independently for each trial of each point.
  * `'session_wide'`: subtract a session-wide baseline across all trials.
* `n_dist_bins` (int)
  Number of distance bins for spatial analysis. Typically set to the diagonal of the FOV (`sqrt(height^2 + width^2)`).
* `n_rows_fov` (int)
  Number of rows when plotting multiple FOVs or responses.
* `vlim` (int)
  Maximum value for colormap scaling in FOV plots.
* `txt_shift` (list of int)
  Pixel shift `[x_shift, y_shift]` for overlaying text labels on FOV plots.
* `sat_perc_fov` (float)
  Saturation percentile for FOV image contrast (e.g., `99.99`).
* `peristim_wind` (list of int)
  Number of frames before and after the stimulation frame to consider for peristimulus response window `[pre, post]`.
* `zoomin_npix` (int)
  Number of pixels to zoom in when plotting detailed regions of FOV or kernel maps.
* `dist_bins_xlim` (int)
  Maximum x-axis value for distance bin plots. Often `n_dist_bins // 2`.
* `dist_bins_xlim_zoom` (int)
  Maximum x-axis value for zoomed-in distance bin plots. Often `n_dist_bins // 16`.

### Data locations

* `data_proc/<experimenter>/<mouse>/<session>/`
* Suite2p output under:

  * `suite2p/plane{plane}/`
  * `reg_tif_chan{channel}/` (motion-corrected TIFFs)

### Photostimulation metadata

* MarkPoints files parsed directly from the session directory
* Converted to CSV:

  * `photostim_protocol.csv`
  * saved in the session root

---

## Major processing steps

### 1. Motion quality control

* Load Suite2p motion offsets (`xoff`, `yoff`)
* Plot drift traces (`xyoff.png`)

### 2. Photostimulation protocol parsing

* Parse MarkPoints metadata
* Convert to a unified stimulation list (time, frame, point ID, x/y coordinates)
* Optional coordinate inversion for legacy datasets

### 3. FOV response extraction

* Load motion-corrected TIFF stacks
* Extract baseline and response windows around each stimulation frame (baseline (`fov_bsln`), response (`fov_resp`) and difference images (`fov_diff`))

### 4. Per-point FOV maps

* Compute trial-average or tial-median response maps per stimulation point
* Supports trial-by-trial baseline subtraction

### 5. Distance-dependent analysis

* Bin pixels by distance to stimulation site
* Compute mean and variance of ΔF/F as a function of distance
* Derive 1D and 2D spatial kernels

### 6. ROI matching (stim → Suite2p)

* For each stimulation point find closest Suite2p ROI centroid
* Extract ROI-level fluorescence responses
* Compute baseline-subtracted and z-scored responses

---

## Output plots

All plots are saved under:

```
<session>/photostim_deve/fig/
```

### Figures (fig/)

* `xyoff.png` – Suite2p motion offsets
* `stim_protocol.png` – stimulation timing and point order
* `diff_single_trial*.png` – single-trial FOV response maps
* `fov_mn_markpoints.png` – mean image with stimulation points
* `dist_dff.png` – distance vs response plot
* `kernel_2d.png` – 2D spatial kernel
* `kernel_2d_zoomin.png` – zoomed-in kernel
* `fov_map.png` – mean FOV response per point
* `fov_map_md.png` – median FOV response per point
* `fov_map_zoomin64.png` – zoomed FOV maps
* `fov_map_avg.png` – averaged FOV map across points
* `raster_matched_rois.png` – ROI raster plots
* `raster_matched_rois_avg.png` – averaged ROI rasters
* `response_matched_rois.png` – ROI response traces
* `response_matched_rois_heatmap.png` – ROI response heatmap

### Outputs

TODO1: Find a good way to match the 'fov_map' data onto suite2p ROIs to get the responses of the cell stimulated and other ('off target') cells 
TODO2: Think about what is the best way of exporting the data from here to longipy
---

## Interactive inspection

Napari is used for:

* visual inspection of images and responses
* manual sanity checks of spatial alignment

---

## Known limitations / TODOs

* Baseline subtraction logic is duplicated and should be unified
* Trial dynamics averaging/median not fully implemented
* Better integration with Suite2p pipeline (automatic run after `_b` sessions)
* More robust handling of stimulation frames across TIFF batch boundaries
* Clean up and refactor ROI response extraction code
* Also make sure to have it compatible with the new stimulation protocol

---

## Intended usage

This notebook is **not a clean end-to-end pipeline**, but a flexible analysis sandbox for:

* checking photostim response structure
* generating exploratory figures
* debugging stimulation–response alignment

For publication-quality or batch processing, results should be extracted and refactored into dedicated pipeline modules (TODO).
