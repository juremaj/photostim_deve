# zstack.md (Record a zstack of the FOV)
This protocol is assiciated with zstack sessions, ending with suffix `_z`.
See `.../...` for associated notebook.

## 1) Find the FOV for imaging
1) Its a good idea to do the z-stack immediately after a 'spontaneous', 'evoked' or 'photostim' session, so the mouse is already mounted and the FOV already found. If not then see the steps [here](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/spontaneous.md)
2) Ideally do not move
   
## 2) Acquire z-stack (using an ETL)
1) Decide at which 'magnification' and resolution to acquire the Z-stack (recommended 1024x1024 either 1.5x or 0.85x)
2) Choose 'ETL' as the z-device in the main window of the GUI and move up (in negative (-) direction) to the maximum of the ETL range (around -150 um). 
3) Now move with the 'piezo z device' (e. g. the micromanipulator underneath the microscope screen until you are at the brain surface.
4) Then in the ZSeries part of the GUI set the current position to be the top position (red line above a zstack symbol)
5) Set the following settings:
   a) z device :         ETL
   b) z step:            3um       (niquist is ~5um since FWHM of PSF is ~10um as of 24.2.2026)
   c) fast acquisition:  yes
   d) delay:             15ms
6) Now in the main window make sure the device is 'ETL' and move all the way down to the deepest part of the z-stack that you want to acquire
7) Optionally if you want to compensate with the laser power for the depth, go to a sub-window of the Zseries window and choose 'compensation': 'relative'/exponential, then go back to the top plane, set the laser power and again click 'set current position to top position' and do the same for the bottom one, adjusting power and setting it again (to check if this works you can 'go to middle position' and the power should be in between the top and bottom ones based on the exponential function)
8) Go to the acquisition part of the GUI and click on 'add ZSeries'
9) Set the number of repetions based on the SNR (usually 8 or 16), this will be used for averaging in post-processing
10) In the mouse/session directory create a subfolder where the convention is `####nm_1.5x` or `####nm_0.85x` where `####` is the wavelength of the imaging laser
11) Set the acquisition path to: `eeNNN/YYYY-MM-DD_z/####nm_1.5x` where `NNN` is the mouse index for experimenter `ee` (initials) for example `jm070/2026-02-24_z/1100nm_1.5x`
12) Click 'run acquisition'

## 3) Do near-infrared branding (NIRB) and acquire a 'post-branding' z-stack (using an ETL)
1) Set up everything the same as you would if doing a photostim experiment (see [photostim.md > Target stim](https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/experiment/photostim.md#2-target-stim) protocol). Especially make sure that the ETL is set to the correct position (-15 as of 24.2.2026, this is measured using the [z_align_psf.md] protocol (https://github.com/juremaj/photostim_deve/blob/main/docs/protocols/calibration_microscope/z_align_psf.md))
2) First figure out parameters necessary to burn - draw a single 15um spiral and keep stimulating (for example for 1s) with gradually increasing the '1040nm' laser power until you see the desired branding effect (MarkPoints Run protocol). Make sure that the spiral is positioned somewhere near the corners of the FOC and in a part that is not black. Also make sure the spiral is moved slightly upon each stimulation to better see the effect. IMPORTANT: switch off the PMTs usign the physical switch on the PMT box during each stimulation epoch. If the max power is too low you can try increasing the stim duration.
3) Once you have found the required paramters you can set the stimulation pattern, the best is to add a 'grid' of eqidistant spirals separated by for example 10 or 20 um and to position a row of such spirals along minimum 2 but ideally all 4 edges of the FOV.
4) IMPORTANT: Turn off the PMT box using the physical switch and run the 'stimulation protocol'
5) Using 'Live view' check if it worked.
6) Acquire a 'post-branding' z-stack by following the same steps as described in step 2) above, the naming convention is the same as above just with the appendix of `_nirb`: in `eeNNN/YYYY-MM-DD_z/` make folder `####nm_1.5x_nirb` or `####nm_0.85x_nirb`
