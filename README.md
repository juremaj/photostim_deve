# photostim_deve
Photostim helper library and procols for using targetted 2p optogenetics during development (Cossart Lab).


----------------

Also includes documentation for experimental protocols:

1) [Calibration](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibrate.md)
2) [Target Selection](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/target_select.md)
3) [Target Stimulation](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/target_stim.md)
4) [Response Mapping](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/resp_map.md)


### Reorganisation of protocols (UNDER CONSTRUCTION):

Each of these (except burn_spots.md) will be associated with a python notebook of the same name to plot the results.

- Calibration:
  - Microscope (purely optical calibration protocols):
    - **z_align_psf.md** - Measure alignment and psf in z for different wavelengths (830nm, 920nm and 1100nm)
    - **burn_spots.md** - Align the scanning between imaging and photostim galvos by burning spots
    - **stim_timing.md** - Empirically measure the duration of stimulation based on the stim artefact
    - **power_measure.md** - Measure out of the objective power for imaging laser (at 830nm, 920nm and 1100nm) and the stim laser
  - Response (in vivo calibration protocols):
    - **param_optim.md** - Measure dF/F for different parameter values (e. g. time, laser power)
    - **phys_psf_xy.md** - Measure the 'physiological PSF' - how dF/F depends on distance between a cell and a photostim spot in x and y by doing a grid of spirals
    - **phys_psf_z.md** - Similar as above but by repeating a spiral fixed in x and y, but varying its z position

- Target selection:
  - ...
    - ...  
