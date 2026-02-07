# stim_select_cp.md
See `notebooks/stim_select_cp.ipynb` for associated notebook.
Also see (photostim.md)[https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/photostim.md], which is the experimental protocol that uses the results of this analysis.

This notebook generates randomly selected **photostimulation target points** from a field‑of‑view (FOV) imaging session using **Cellpose (cpsam)** segmentation. Starting from raw or motion‑corrected FOV images.

## Overview

1. Loads and (optionally) motion‑corrects FOV images
2. Runs Cellpose segmentation on the mean FOV image
3. Optionally allows **manual curation** of segmentation in napari
4. Computes cell centroids from curated masks
5. Randomly selects a subset of cells for stimulation
6. Exports **Bruker‑compatible MarkPoints (.xml) and Galvo Point List (.gpl)** files
7. Saves intermediate results (images, masks, centroids) for reproducibility and QC

---

## Expected Inputs

### 1. Configuration file

## Inputs

## Key parameters (in notebook file)

* `subject`
  The unique identifier for the subject (by convention `nn###`, e. g. `jm065`)

### Configuration file: `stim_select_cp_config.yaml`

This notebook is controlled by a YAML configuration file. Below is a description of each parameter and how it affects the pipeline.

General parameters:
* `session_type` (`'_a'`, `'_b'`, etc.)
  Session suffix will decide in which folder the script will look for the fov image (normally this should be `_a`).
* `session_reg_idx` (int)
  Index of the session used as the reference. Typically `0`, corresponding to the first session.
* `fov_imsize_onedim` (int)
  Size of the full-field-of-view for `fov` images in pixels (assumed square).
* `s2p_imsize_onedim` (int)
  Image size used during Suite2p processing. Used to compute scaling factors between FOV and Suite2p coordinates.
* `n_stim_cell` (int)
  Number of cellular targets selected for photostimulation.
* `seed` (int)
  Random seed used when selecting stimulation targets to ensure reproducibility.
* `edge_excl` (float, 0–1)
  Fraction of the image excluded from each edge when selecting cells for stimulation. Prevents choosing targets near borders where motion correction or brain growth may introduce errors.
* `run_motcorr` (bool)
  Whether to perform motion correction on raw FOV data using Suite2p’s algorithm.
* `nimg_init` (int)
  Number of frames used to compute the reference image for motion correction.
* `force_recompute` (bool)
  If `True`, forces recomputation of motion correction and segmentation even if cached results already exist.
* `use_seg` (`'cp'`)
  Segmentation method used for FOV images. Currently Cellpose-based segmentation.
* `manually_curate` (bool)
  Whether to apply manual curation steps (e.g. removing edge ROIs) after segmentation.
* `sat_perc` (float)
  Upper percentile used for image intensity saturation when plotting.
* `mp_temp_path` (str)
  Path to the MarkPoints XML template used to generate stimulation files.
* `gpl_temp_path` (str)
  Path to the galvo point list (GPL) template.

MarkPoints XML and Galvo point list (GPL) parameters:
* `SpiralWidth`, `SpiralHeight`
  Width and height of the spiral as a proportion of the FOV.
* `SpiralSizeInMicrons`
  Physical diameter of the spiral stimulation pattern in microns.
* `ActivityType`
  MarkPoints activity type.
* `UncagingLaser`, `UncagingLaserPower`
  Laser name and power used for photostimulation.
* `Duration`
  Stimulation duration per point (ms).
* `IsSpiral`, `SpiralSize`, `SpiralRevolutions`
  Parameters defining the spiral trajectory.
* `Z`
  Z-position of stimulation plane.
* `X_lim`, `Y_lim`
  Empirically determined galvo voltage limits corresponding to the corners of the FOV.


### 2. Data layout

The notebook assumes the following directory structure:

```
data_proc/
  jm/
    <subject>/
      <session_type*>/
        fov/
          <wavelengths>/
```

where FOV images are discoverable via `get_all_fov_image(...)`.

---

## Processing Steps

1. **Load configuration and session paths**

   * Select subject and session
   * Create output directories

2. **Load FOV images**

   * Optionally run motion correction
   * Compute mean FOV images per wavelength

3. **Segmentation (Cellpose cpsam)**

   * Run Cellpose on the 1100 nm mean FOV image
   * Save raw segmentation
   * Remove edge‑touching masks (`edge_excl`) (to avoid issues with movement and brain growth)

4. **Manual curation (optional)**

   * Launch napari with image + label layers
   * User edits segmentation
   * Notebook halts until napari is closed
   * When napari is closed the user must manually launch the subsequent blocks of code to continue with the analysis.

5. **QC visualizations**

   * Motion‑correction comparison
   * Segmentation overlays (raw vs curated)
   * Centroid and stimulation point plots
   * Save the segmentation and plots for reporducibility and QC

6. **Centroid extraction & target selection**

   * Compute median (x, y) for each curated mask
   * Randomly select `n_stim_cell` centroids
   * Convert coordinates if Suite2p/FOV pixel sizes differ
   * Save all medians, chosen medians and plots for reporducibility and QC

7. **Export for Bruker photostimulation**

   * Write MarkPoints `.xml`
   * Write Galvo Point List `.gpl`

---

## Outputs / Saved Files

All outputs are saved under:

```
<session_path>/stim_select_cp/
```

### Numpy files (`.npy`)

* `cfg.npy` - saved YAML config file as a dictionary based (including random seed) for reproducibility
* `all_fov_image.npy` - FOV images for all wavelengths (optionally also including motion-corrected or non-motion corrected averages)
* `fov_image.npy` – mean FOV image used for segmentation
* `seg.npy` – raw Cellpose segmentation
* `seg_cur.npy` – curated segmentation (edge‑filtered and/or manually edited)
* `meds.npy` – centroids of all curated masks
* `meds_stim.npy` – selected stimulation centroids

### Figures (`figures/`)

The following QC figures are saved automatically:

* `motcorr_<wavelength>.png` – comparison of raw vs motion‑corrected FOV images for each wavelenght in the `fov` folder
* `cp_seg.png` – Cellpose segmentation overlay (before curation)
* `cp_seg_cur.png` – Cellpose segmentation overlay (after edge removal / manual curation)
* `meds_all.png` – all curated cell centroids with selected stimulation points highlighted
* `meds_stim.png` – selected stimulation points only

### Bruker files

* `MarkPoints_<subject>_cp.xml`
* `galvo_points_list_<subject>_cp.gpl`

These are generated using templates specified in the YAML config and are ready to load into Bruker software.

---

## Manual Curation Notes

* If `manually_curate = True`, the notebook will intentionally raise a `RuntimeError` after opening napari.
* Edit the **labels layer only**.
* Close napari once finished, then re‑run the next cell.

---

## Typical Use Case

1. Update `stim_select_cp_config.yaml` based on the specifics of your experiment
2. Run notebook top‑to‑bottom
3. Curate segmentation in napari (if enabled)
4. Inspect QC plots
5. Load exported `.xml` / `.gpl` files into Bruker software and run the photostimulation experimental protocol: (photostim.md)[https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/photostim.md].
