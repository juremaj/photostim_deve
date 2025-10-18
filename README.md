# photostim_deve
Photostim helper library and procols for using targetted 2p optogenetics during development (Cossart Lab).


----------------
----------------

### Organisation of protocols:

Each of these (except burn_spots.md) will be associated with a python notebook of the same name to plot the results.

- Calibration:
  - Microscope (purely optical calibration protocols):
    - [z_align_psf.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/z_align_psf.md) - Measure alignment and psf in z for different wavelengths (830nm, 920nm and 1100nm)
    - [burn_spots.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/burn_spots.md) - Align the scanning between imaging and photostim galvos by burning spots
    - [stim_timing.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/stim_timing.md) - Empirically measure the duration of stimulation based on the stim artefact
    - [power_measure.md](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/power.md) - Measure out of the objective power for imaging laser (at 830nm, 920nm and 1100nm) and the stim laser
  - Response (in vivo calibration protocols):
    - **param_optim.md** - Measure dF/F for different parameter values (e. g. time, laser power)
    - **phys_psf_xy.md** - Measure the 'physiological PSF' - how dF/F depends on distance between a cell and a photostim spot in x and y by doing a grid of spirals
    - **phys_psf_z.md** - Similar as above but by repeating a spiral fixed in x and y, but varying its z position

- Target selection (IN PROGRESS...):
  - [Target Selection](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/target_select.md)
  - [Target Stimulation](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/target_stim.md)
  - [Response Mapping](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/resp_map.md)

- Data organisation:
  - [Data Structure](https://github.com/juremaj/photostim_deve/blob/main/docs/data_structure.md)
