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
11) 
12) Set the axquisition path to: `eeNNN/YYYY-MM-DD_z/####nm_1.5x` where `NNN` is the mouse index for experimenter `ee` (initials) for example `jm070/2026-02-24_z/1100nm_1.5x`
13) Click 'run acquisition'

## 3) Do near-infrared branding (NIRB)




## 4) Acquire a 'post-branding' z-stack (using an ETL)
