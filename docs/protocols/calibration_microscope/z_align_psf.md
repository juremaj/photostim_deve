# z_align_psf.md (Align and measure PSF in z for imaging and stim laser at different wavelengths)
See `calibration_notebooks/z_align_psf.ipynb` for associated notebook.

## Purpose

To measure and document the imaging ('pockels') and stimulation ('uncaging') position and shape of the PSF in Z at different wavelengths on the Bruker Ultima two-photon microscope using a power meter. This is needeed to know the Z resolution as well as to account for the z shift when using different laser wavelengths.

## Materials

- Rhodamine-coated slide (very thin homogeneous fluorescent layer, see picture below)
- Optical mount (to position the slide under the objective)

<img src="/docs/protocols/media/rhodamine_slide.jpeg" width="50%">


## Protocol

Measurement for imaging/'pockels' laser:
1) Follow the normal microscope on procedure (wait at least 30 min for laser to stabilise if it was turned off before)
2) Position the rhodamine slide under the microscope with the coated side facing down, making sure the slide is as perpendicular with respect to the objective as possible.
3) Add a few drops of water and immerse the objective by moving down in Z
4) To avoid confustion set the ETL (electro-tunable lens) to 0 in Prairie View.
5) Find the exact focus either with widefield or even better directly with Prairie View. If the slide is not flat enough under the objective make sure to readjust it before proceeding (a mis-aligned slide will inflate the estimate of PSF, especially with a large FOV).
6) Go to Prairie View and set up the specific imaging conditions for which you want to make measurements. The best is to load these from prairie view presets, to be sure that exactly the same settings are used when doing the measurement as when performing the experiment.
7) Usually (in photostim) we would do these measurements at 830 nm (isosbestic gcamp), 920 nm (Ca2+ bound gcamp, slightly blue shifted), 1100 nm (mScarlet to localise opsin).
8) Choose the first wavelength to measure and set the paramteres of the z-stack:
   - a) Center the rhodamine slide around the central slice of the z-stack
   - b) Make sure the z step is at the order / resolution at which you want to measure the PSF (a step size of 0.5 um is a good value, giving ~ 20 samples at FWHM if psf is ~ 10 um FWHM)
   - c) Make sure that the top and bottom slices have enough range to capture all wavelengths despite the shifts (+- 50 um should be fine)
   - d) When doing photostim measurements it is better to use z-focus (mechanical) to be consistent (since ETL can not be used to change the z position of the photostim beam).
   - e) In terms of detection it's best to use the red PMT - it will have the highest signal
   - f) create a folder where all zstacks will be stored, the naming convention is `YYYY-MM-DD_zpsf`
10) Once this is set up proceed to record a z-stack at each laser wavelength by performing the following steps for each wavelength, while making sure to not move the sample or the z alignment of the microscope during the procedure:
  - a) Set the laser wavelength to the desired one and wait for the laser to be mode locked
  - b) Navigate to the the slice in the z stack volume with the highest brightness and make sure it is not saturating or too dim by adjusting the laser (pockels) power
  - c) Make a subfolder in the `YYYY-MM-DD_zpsf` naming it by the laser setting that is used, for example (`1100nm`) and set this as the save path for the Zstack
  - d) Run zstack acquisition
  - e) Repeat steps from a) onwards for each laser setting
11) If measuring the shift between the imaging and stim laser make sure to again not move the z and proceed to the second part of the protocol.
12) If that's all the measurments then transfer the data to the server in `data_jm/data_raw/calibration/YYYY-MM-DD_zpsf`

Measurement for photostim/'uncaging' laser (optional):
1) Ideally this is done as a follow-up to measuring the imaging laser, so follow steps 1) - 11) above first
2) Keep the same z-stack parameters as before to have the recordings co-registered (making sure to use z focus since ETL does not change photostim focus).
3) Turn off the 
4) The issue here is that we do not scan with the photostim laser, so we need to do a 'hack' that will allow us to estimate the PSF based on the stim 'artefact' - e. g. descanned light that reaches the PMT when we are shining photostim laser onto the rhodamine slide. We can do this by performing the following steps:
    - a) Open 'Mark points' the part of the GUI where photostim protocols are defined
    - b) Define a large spiral in the center of the FOV, for example 64x64 um and many spiral rotations, for example 20
    - c) Click 'Run protocol' and move in z to the part where the stim artefact is the largest and again adjust the laser power (this time using the polariser - see `power.md` protocol) in a way that the PMT is not saturating, but that the signal is strong enough). Note: You might see some striping artefacts which I think are due to the spiral scanning but am not 100% of their origin.
    - d) Check the duration required for Z-stack acquisition and set the duration of this spiral to be larger than that (to ensure the spiral is being continuously scanned as the microscope moves in z)
    - e) Click the 'Run protocol' button in 'Mark points'
    - f) Once you hear the photostim shutter open run the Z-stack acquisition, saving the zstack in the same folder as the zstacks for the imaging laser, ideally with the name `1040nm_stim` (full path: `YYYY-MM-DD_zpsf/1040nm_stim`)
5) If that's all the measurments then transfer the data to the server in `data_jm/data_raw/calibration/YYYY-MM-DD_zpsf`


Data and plotting:

1) If your data has been transferred to the server at `data_jm/data_raw/calibration/YYYY-MM-DD_zpsf` and this folder contains subfolders for different calibrations (e.g. `830nm`, `920nm`, `1100nm`, `1040nm_stim`. You can then simply run the Jupyter notebook associated with this protocol (`calibration_notebooks/z_align_psf.ipynb`), the only thing that needs to be changed is a single line defining the ID of the calibration (e. g. `2025-10-10_zpsf`)
2) This will generate a calibration plot saved in `photostim_deve/utils/calibration_z_align_psf` as a `.png` file with the same name as the root data folder (e. g. `2025-10-10_zpsf.png`). See below how this plot should look (NOTE: here the slide moved before recording the imaging and stim, which is why the stim section is shifted):
<img src="/docs/protocols/media/2025-10-10_zpsf.png" width="75%">

3) There are some additional lines in the notebook that allows the user to look at the data in Napari, which can be good to visualise other things such as field curvature and look at different projections of the data (for example in 3D or X-Z or Y-Z).
   
4) After the calibration it's also nice to print the graph and tape it somewhere near the microscope (and if you can also push it to the GitHub repo so we have a digital backup).
