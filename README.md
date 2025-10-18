# photostim_deve
Photostim helper library and procols for using targetted 2p optogenetics during development (Cossart Lab).

----------------

### Organisation of protocols:

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

- Experiment (IN PROGRESS...):
  - [target_select.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/target_select.md) [(code)]() 
  - [target_stim.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/target_stim.md) [(code)]() 
  - [resp_map.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/resp_map.md) [(code)]() 

- Data organisation:
  - [data_structure.md](https://github.com/juremaj/photostim_deve/blob/main/docs/data_structure.md)
