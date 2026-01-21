# stim_timing.md (Stimulation timing measurement)
See `notebooks/calibration_microscope/stim_timing.ipynb` for associated notebook.

1) Put rodamine slide in focus as in other protocols (e. g. measuring PSF)
2) Make sure that everything is ok with the stim laser (as in other protocols):
   - ETL -8
   - Laser IR shutter open
   - Laser power on
   - Photostim filter on (and not the one for brainbow)
3) With pockels on see the slide and use mark-points to define a spiral in (the middle) part of the FOV that is in focus on the pockels laser
4) Turn off the pockels laser (0) to reduce noise of the measurement
5) Trigger mark points initially at a low (how low?) laser power and tweak that until you see a high signal artefact but not saturating the PMT (make sure not to damage them with too high power!)
6) Once you've set the laser power make sure that you are using the correct timing settings for the stimulation. Importantly the minimum using the 'high speed/PMT shutter' control is 25ms, for stimulation times shorter than this you need to connect the cable to the 'voltageOut' pin and set the correct things in software (to trigger voltage output signal for each stimulation)
7) Make sure if using the voltageOut that the initial delay is correct (should be the same as the interpoint delay and the delay set in the voltageOut protocol
8) Make sure to set a few stimulations for example 10 to be able to analyse the reliability
10) Now set the save path and run the protocol with (using mark points current)
