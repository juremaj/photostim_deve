# param_optim.md (Optimise photostim parameters such as power and duration based on dF/F responses)
See `notebooks_resp_phtostim/resp_photostim_calib.ipynb` (compute responses), `notebooks_resp_phtostim/resp_photostim_calib_plot.ipynb` (plot a single session) and `notebooks_resp_phtostim/resp_photostim_calib_plot_longitudinal.ipynb` (plot across ages) for the associated notebooks.

## Purpose

To measure in vivo how the response of opsin-expressing neurons (ChRmine+) depends on a single photostimulation parameter (for example laser power or stimulation duration) while keeping everything else fixed. This lets us choose the lowest power / shortest duration that still reliably drives the targeted cells, which keeps off-target activation, heating and out-of-focus excitation (saturation) as low as possible.

This protocol is performed within a calibration session (suffix `_calib`, see [calibration.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/calibration.md) and [data_structure.md](https://github.com/juremaj/photostim_deve/blob/main/docs/data_structure.md)).

## Materials

- Mouse expressing GCaMP and a red-shifted opsin (e.g. Cre-dependent ChRmine-mScarlet), with a cranial window
- Recent microscope calibrations:
  - [z_align_psf.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/z_align_psf.md) (z offset between imaging and stim laser, ETL setting)
  - [power.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/power.md) (to convert the Mark Points power setting into mW out of the objective)


## Protocol

Preparation:
1) Follow the normal microscope on procedure (wait at least 30 min for the lasers to stabilise if they were turned off before) and set up the stim path as in [photostim.md > Target stim](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/photostim.md#2-target-stim) (ETL, IR shutter, photostim filter, '1040nm' laser in photostim mode).
2) Load the imaging settings from the Prairie View environment file (the analysis assumes 512x512 px, ~30 Hz, single plane; if you change any of this, update `resp_photostim_config.yaml` accordingly).
3) Find the FOV and take FOV pictures at 830nm (GCaMP), 920 nm (GCaMP) and 1100 nm (opsin reporter), keeping in mind the z shift between wavelengths (see [z_align_psf.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/z_align_psf.md)). Save these in `YYYY-MM-DD_calib/fov/830nm`, `YYYY-MM-DD_calib/fov/920nm` and `YYYY-MM-DD_calib/fov/1100nm`.

Defining the stimulation points:

4) Open the `Mark Points` window and define the stimulation points. By convention we use **20 points**:
   - points `0` - `14`: ChRmine+ (and GCaMP+) cells (chosen manually or with [stim_select_cp.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/analysis/stim_select_cp.md))
   - points `15` - `19`: controls (e.g. opsin-negative GCaMP+ cells). These indexes are used as `ctrl_idxs = [15, 16, 17, 18, 19]` in the plotting notebooks, so if you use a different number or order of control points make sure to change `ctrl_idxs`.
5) Export the point list (`.gpl`) and **use exactly the same point list (same order) for all conditions** of the calibration, and for the same mouse on the following days if doing a longitudinal calibration. The analysis matches responses across conditions and days by point index.
6) Define the stimulation protocol in `Mark Points` as a single sequence in which each point is stimulated in turn and the whole sequence is repeated (`Repetitions`). The analysis reconstructs the stim times only from `InitialDelay`, `Duration`, `InterPointDelay` and `Repetitions`, assuming the order point 0, 1, ..., 19, 0, 1, ... etc., so do not use randomised or grouped orders.
   - Keep the `InterPointDelay` long enough for the GCaMP response to decay before the next point is stimulated (the analysis uses 10 frames (~0.33 s) before and 10 frames after each stimulation).
   - Keep spiral size and number of revolutions constant across conditions.
   - TODO: add the values used in practice (spiral diameter, revolutions, `InitialDelay`, `InterPointDelay`, `Repetitions`).

Running the calibration:

7) Create the folder for the parameter you are going to vary: `YYYY-MM-DD_calib/power/` (laser power) or `YYYY-MM-DD_calib/time/` (stimulation duration). The name of the folder will be used when generating the plots.
8) For each value of the parameter:
   - a) Set the value in `Mark Points` (for example the first value of power to test if `YYYY-MM-DD_calib/power/`), keeping all other parameters fixed.
   - b) Make a subfolder named by the value, zero-padded with units, for example `010mw`, `020mw`, `040mw`... or `004ms`, `008ms`, `016ms`... (the analysis reads the number from the folder name and sorts conditions by it, so the name should contain only one number).
   - c) Set this subfolder as the save path for the TSeries, set synchronisation with Mark Points to `current` in the TSeries window and launch the recording.
   - d) As a sanity check, watch the targeted cells during the stimulation epoch and check if they respond.
   - e) Repeat for the next value. It is best to go from low to high power (or short to long duration) so that high-power stimulation does not affect the responses measured afterwards, and to recheck the FOV between conditions (the z position in particular).
9) Note the power setting of each condition and convert it to mW using the most recent [power.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/power.md) calibration.
10) Transfer the data to the server in `data_jm/data_raw/jm0XX/YYYY-MM-DD_calib/`. The final structure should look like this (each TSeries folder contains its `_MarkPoints.xml`):
```text
YYYY-MM-DD_calib/
├── fov/
│   ├── 920nm/
│   └── 1100nm/
├── power/
│   ├── 010mw/
│   │   └── TSeries-XXXXXXXX-XXXX-XXX/
│   ├── 020mw/
│   └── ...
└── time/
    ├── 004ms/
    │   └── TSeries-XXXXXXXX-XXXX-XXX/
    ├── 008ms/
    └── ...
```

Data and plotting:

1) Run suite2p separately on each condition folder, with the processed output in `data_proc/jm/jm0XX/YYYY-MM-DD_calib/<protocol>/<condition>/suite2p/`. There is a helper script for running specifically data in this format on the 2p room server. **Registered tiffs need to be saved** (`reg_tif = True`), since the responses are computed from `suite2p/plane0/reg_tif_chan2`. Also copy the `TSeries-..._MarkPoints.xml` file into the condition folder in `data_proc` (e.g. `data_proc/jm/jm0XX/YYYY-MM-DD_calib/power/010mw/`).
3) Run `resp_photostim_calib.ipynb`. The only things to change are `mouse`, `session` (e.g. `2025-12-08_calib`) and `protocol` (`power` or `time`). For each condition this:
   - reads the Mark Points file and writes the stim times to `photostim_protocol.csv` in the session folder,
   - computes the response map of each point as the mean of the 10 frames after stimulation minus the mean of the 10 frames before (averaged over repetitions, `trial_by_trial` baseline),
   - saves diagnostic figures in `<condition>/photostim_deve/fig/` (motion `xyoff.png`, points on the FOV `fov_mn_markpoints.png`, response maps `fov_map*.png`, response vs distance `dist_dff.png` and the 2D kernel `kernel_2d*.png`). It is worth checking these, especially that the points are on the intended cells and that there is no large motion,
   - saves a suite2p-independent summary `resp_px_<condition>.npy` (e.g. `resp_px_010mw.npy`) in the protocol folder: an array with one value per stimulation point, the mean response of the pixels within ~10 px of the spiral centre.
4) Run `resp_photostim_calib_plot.ipynb` with the same `mouse`, `session` and `protocol` (and `ctrl_idxs` if different). This plots the response of each point against the parameter value (ChRmine+ points in colour, controls in grey, thick lines = means).
5) (Optional, longitudinal) If the calibration was repeated on several days with the same points, run `resp_photostim_calib_plot_longitudinal.ipynb`, setting `all_session` and the corresponding `all_age` (e.g. `['P8', ..., 'P13']`). For each parameter value this plots the response of each point across ages.
6) After the calibration, note the chosen parameters (and the date and mouse) in the photostim protocol, and push the figures to the GitHub repo so we have a digital backup.

Notes / known issues:
- The response is the raw fluorescence difference (response - baseline, a.u.), not normalised by the baseline, even though the plots are labelled dF/F. Keep this in mind when comparing sessions with different imaging power or expression levels.
- `resp_photostim_calib.ipynb` loads `resp_map_config.yaml`, but the config in the repo root is `resp_photostim_config.yaml`, and the notebooks assume they are run from the repo root. Either rename or adjust the path before running.
