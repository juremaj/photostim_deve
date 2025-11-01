# spontaneous.md (Perform a baseline spontaneous recording)
This protocol is assiciated with spontaneous sessions, ending with suffix `_a`.
See `.../...` for associated notebook.

Note: if it is the first day of a longitudinal recording this protocol will usually also involve choosing the FOV for the rest of the days.

## 1) Find the FOV for imaging

1) Turn on the microscope and head-fix the mouse
2) Make sure that the objective is as perpendicular to the brain surface as possible (first do it by eye - angle between headplate holder, then you can adjust this by using 1p or 2p imaging by making sure the focus is homogenous across the FOV)
3) Find the FOV for imaging:
  - *First day* of longitudinal imaging:
    - Choose an area for imaging based on factors relevant for the experiment (e. g. response to whisker stim, expression of gcamp/opsin, clarity/signal of imaging FOV etc.)
    - In that case it can also be beneficial to take zoomed out version of FOV images (see below), both at the imaging depth but also at the brain surface, since this can help you find the FOV on subsequent days more easily (you can do this by simply taking screenshots, no need to do it super properly, it is only to help you find the FOV)
  - *Not first day* of longitudinal imaging (describing the current protocol used by me (Jure) for gcamp/chrmine(oScarlet) mice on 1. 11. 2025, but this may vary depending on type of experiment of course):
    - Navigate to the `fov` folder of the first day of longitudinal imaging
    - Choose an initial wavelength to align by, a good idea is `830nm` - isosbestic calcium. This makes sure that ongoing activity will not be confusing when trying to figure out if we have a good FOV match.
    - Identify rough x-y coordinates by looking at the blood vessel pattern
    - Identify the rough z coordinates by looking at the blood vessel patterns + some landmarks, like neurons that stand out from the gcamp background more clearly.
    - Now find a final x-y by looking at some clear landmarks (vessels or neurons) that are at the very edge of the FOV along the vertical and horizontal axes. 
    - The best idea is to align to one corner of the FOV (I use bottom right) to have a fixed reference for ongoing growth (in this case we loose a bit of cells on the top and on the left side of FOV with ongoing brain growth).
    - Set the current x-y and z to 0 
    - Switch to red imaging configuration to find a more refined alignemnt in z - this is easier in red since oScarlet is soma-membrane bound so it gives more fine higher frequency features and less background compared to isosbestic calcium.
    - When switching configuration make sure to account for shifts in z between imaging laser wavelengths (from 830nm - 920nm + 4 um in z, from 920nm -1100nm + 10 um in z) (calibration below is from 10. 10. 2025):
    <img src="/docs/protocols/media/2025-10-10_zpsf.png" width="50%">
    - Also make sure to change the laser wavelength (wait until laser is mode locked), turn on the PMT for the desired emission color, select the channel to visualise in gui and adjust imaging laser power in the Pockels cell (green is much more powerful than red) (calibration below is from 10. 10. 2025):
    <img src="/docs/protocols/media/2025-10-10_pockels.png" width="50%">
    - Now move a few microns up or down until the alignment matches as much as possible - the best strategy is too try to see some landmark cells matching in each of the corners.
    - Once satisfied set this position as the new 0 in z


## 2) Capture FOV images
(here again describing the current protocol used by me (Jure) for gcamp/chrmine(oScarlet) mice on 1. 11. 2025, but this may vary depending on type of experiment of course)

1) Prepare subfolders of session directory for each imaging laser wavelength (by convention: `YYYY-MM-DD_a/fov/###nm` where ### is the wavelength, for example `2025-11-01_a/fov/1100nm`).
3) Go to the red configuration paying attention to the things described above (shift in z, setting red imaging parameters)
4) If first day choose the laser power (pockels) and PMT gain in a way as not to saturate (these should then be kept fixed across all days of longitudinal protocol!) if not first day then of course reuse the same settings as on previous recordings.
5) Set number of frames to 128 and the path to the folder of the current imaging laser 
6) Launch the recording
7) During the acquisition keep an eye out that the FOV doesn't move too much, since this will cause blur if not motion-corrected. If you see some movement the best idea is to just overwrite the recording (press the (-) sign and relaunch the recording pressing ('ok') when asked if you want to overwrite it).
8) You can also do a live view of a 128 frame averaged FOV and freeze this in the GUI to keep as reference to check co-expression and make sure the z position is the same across wavelengths.
9) After an acquisition move in z to the appropriate position for the next wavelength and repeat the whole process.
10) After you are done with all the FOV acqusitions make sure to return to the z position and imaging parameters used for gcamp imaging.

## 3) Launch the recordings
(here again describing the current protocol used by me (Jure) for gcamp/chrmine(oScarlet) mice on 1. 11. 2025, but this may vary depending on type of experiment of course)

1) Set the z position and the parameters for gcamp imaging
2) Set the number of frames to match the duration of recording (36000 - 20 min)
3) Launch the script for camera and navigate to the folder where output frames will be saved
4) Check water and add more if there isnt enough under objective
5) Turn off the option to automatically fix the phase offset of resonant scanner (this can mess up recording mid-way through)
6) Make sure the ethernet cable is disconnected from the wall (can cause recordings to fail for some strange reason)
7) Navigate to the root of the session folder (`YYYY-MM-DD_a/`, for example `2025-11-01_a/`) and launch the recording
8) Check by eye that the FOV still looks ok (matched to previous days, pixels not saturating)
9) Check the frame of the camera to see if it looks good (to make sure that the position, focus, or aperture wasnt changed by someone since last recordings, or that the LED might be off etc.)
10) Come back at the end of the recording and its again good practice to check that the FOV looks similar (matched to previous days) - mostly as a sanity check for z drift.
