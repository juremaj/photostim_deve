# photostim_deve
Photostim helper library and procols for using targetted 2p optogenetics during development (Cossart Lab).

----------------

### Documentation:

- Organisation of experiment-analysis pipeline:
  - [data_structure.md](https://github.com/juremaj/photostim_deve/blob/main/docs/data_structure.md) - It's useful to read this before checking the other protocols or code, since it outlines the organisation of the experimental-analysis pipeline.

- Experiment:
  - [spontaneous.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/spontaneous.md) (session suffix `_a`) (TODO: update based on new laser control) (code in longipy library)
  - [photostim.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/photostim.md) (session suffix `_b` to `_f`) [(code)](TODO: update based on new laser control)
  - [evoked.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/evoked.md) (session suffix `_s`) (code in longipy library - TODO)
  - [zstack.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/zstack.md) (session suffix `_z`) (code in longipy library - TODO)
  - [calibration.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/calibration.md) (session suffix `_calib`) [(code)]()
  - [treadmill.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/treadmill.md) (TODO: not yet integrated in data/code organisation) (code in longipy library - TODO)

- Analysis:
  - [stim_select_cp.md]()[(code)](https://github.com/juremaj/photostim_deve/blob/main/stim_select_cp.ipynb)
  - [match_stim_fov_t2p.md]()[(code)](https://github.com/juremaj/photostim_deve/blob/main/match_stim_fov_t2p.ipynb)
  - [resp_map.md][(code)][(code)](https://github.com/juremaj/photostim_deve/blob/main/resp_map.ipynb)
  - [...]

Each of these (except burn_spots.md) will be associated with a python notebook of the same name to plot the results.

- Calibration:
  - Microscope (purely optical calibration protocols):
    - [z_align_psf.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/z_align_psf.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_microscope/z_align_psf.ipynb) - Measure alignment and psf in z for different wavelengths (830nm, 920nm and 1100nm)
    - [burn_spots.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/burn_spots.md) - Align the scanning between imaging and photostim galvos by burning spots
    - [stim_timing.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/stim_timing.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_microscope/stim_timing.ipynb) - Empirically measure the duration of stimulation based on the stim artefact
    - [power.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/power.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_microscope/power.ipynb) - Measure out of the objective power for imaging laser (at 830nm, 920nm and 1100nm) and the stim laser
  - Response (in vivo calibration protocols, IN PROGRESS...):
    - [param_optim.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_response/param_optim.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_response/param_optim.ipynb) - Measure dF/F for different parameter values (e. g. time, laser power)
    - [phys_psf_xy.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_response/phys_psf_xy.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_response/phys_psf_xy.ipynb) - Measure the 'physiological PSF' - how dF/F depends on distance between a cell and a photostim spot in x and y by doing a grid of spirals
    - [phys_psf_z.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_response/phys_psf_z.md) [(code)](https://github.com/juremaj/photostim_deve/blob/main/notebooks/calibration_response/phys_psf_z.ipynb) - Similar as above but by repeating a spiral fixed in x and y, but varying its z position


