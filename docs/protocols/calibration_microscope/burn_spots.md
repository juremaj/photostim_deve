# burn_spots.md (Burn spots to register stim and imaging scanners))
There is no associated Jupyter notebook for this part (no graph outputs required).

## Burn spots for initial alignment calibration

Goal: make sure that where you tell the microscope to stimulate in the GUI corresponds to the place where it will actually stimulate. E. g. that the imaging and the stimulation scanners are aligned.

When to do it: If using a new set of imaging parameters (different zoom, different number of pixels, different number of planes etc.) or when noticing that the alignment is not good (based on the 'check alignemnt calibration' protocol described lower down)

Materials: a cover slip with a thin layer of a dried fluorescent marker on one side.

1) Start up the microscope
2) Orient the cover slip with the fluorescent side facing down and position it under the objective, as horizontal as possible (the side that we need to use for imaging is indicated also on the slide).
3) Add a drop of water to the objective and lower it until just before touching the cover slip
4) Switch to prairie view and first load the correct environment (e.g.: "File/load settings/jm_30Hz_1plane_template") set the z of ETL to -8 um -> We found this empirically, that basically the photostim laser (in this case set 1040nm) and the "recording" laser (set at 920nm) have 8 um apart (they are not focusing on the same Z value, see graph below):

![Stimulation Z Offset](/docs/protocols/media/img_stim_z_offset.jpeg)

***If we want to use this settings, it means that we will respect the size of the FOV, zoom etc, if we need to change them, we need to create an environment from scratch and adjust the rest of the settings accordingly.

5) Set the power to be very low (for example pockels 10 or so) since the slide is very bright and could damage the PMTs, increase if necessary
6) Now move the objective up with the z focus (manual / motor, not ETL; negative (-) is up) until you see the fluorescence slide in focus
7) If the slide is not well aligned (e. g. if you don't see it across the whole FOV) then maybe adjust it to be more perpendicular to the objective
8) Before you start the calibration make sure that you have the correct imaging settings loaded (best way to do this is using a pre-saved environment for consistency)
9) Also make sure that the photostim shutter is open ('IR shutter', next to the normal shutter, in prairie view gui)
10) Make sure that the dichroic Aurelie uses is out and replaced by the appropriate filter for photostim (on top of microscope) -> otherwise the power will not be sufficient to bleach for alignment or even to stimulate a cell
11) Choose the laser power using the custom GUI controlling the polariser (Windows Taskbar -> black silhouette of a person): choose in concordance with the uncaging table on the box of the Bruker

Stim power calibration (23. 10. 2025):

| Uncaging        | 1040 nm     |
|-----------------|----------------|
| 0               | 4.4            |
| 1               | 6.7            |
| 2               | 20.5           |
| 3               | 33.4           |
| 4               | 41.0           |
| 5               | 71.0           |
| 6               | 88.8           |
| 7               | 123.1          |

12) For the uncaging to properly work, we also need to change manually the polariser tp 7 by moving the wheel in the thorlabs of the picture:

| Polariser (deg) | Power (mW)     |
|-----------------|----------------|
| 0               | 9              |
| 1               | 19             |
| 2               | 34             |
| 3               | 53             |
| 4               | 78             |
| 5               | 107            |
| 6               | 140            |
| 7               | 177            |
| 8               | 218            |
| 9               | 262            |
| 10              | 310            |

<img width="302" height="402" alt="image" src="https://github.com/user-attachments/assets/4612e43f-e045-49d8-b922-4cbc48169d28" />


13) Launch the calibration in prairie view gui `Tools > Calibration/Alignment > Uncaging Galvo Calibration`
14) Select `Burn spots` and `Next`
15) Create a new file with name and date (this is where the calibration will be saved) and `Next`
16) When prompted if to use the current calibration choose `No` and `Next`
17) Choose the `Duration (ms)` (100 ms should be enough, but can also be increased) the laser power here doesn't do anything, since it is not controlled by prairie view (but by the GUI in step 11)) and `Next`
18) Follow the calibration steps by using Live scan, selecting the positions, burning and then realigning the points. Do this iteratively by following the instructions in prairie view.
19) If the calibration is sucessful you can save the calibration and apply it each subsequent time doing the photostim experiment.


## Burn spots to check alignment calibration

Goal: make sure that where you tell the microscope to stimulate in the GUI corresponds to the place where it will actually stimulate. E. g. that the imaging and the stimulation scanners are aligned.

Materials: a cover slip with a thin layer of a dried fluorescent marker on one side.

1) Follow steps 1) to 11) of the 'Alignment calibration' protocol above (if not done before), if done before then just load a `galvo calibration`
2) Click on Mark Points in prairie view (here you will be asked to load a `galvo calibration` if you haven't done so in the step above_ File/load uncaging calibration/load)
<img width="725" height="572" alt="image" src="https://github.com/user-attachments/assets/9ac42cbe-c3d2-40f8-b9fd-0aff0db0c7e0" />

   
4) Add several spirals of 15 um diameter arranged in a grid covering the FOV (for example 3x3 with one point in the middle, one in each corner and one on each side, make sure that you put points through all the field of view to be able that the burning is efficient everywhere):

![Mark Points Grid](/docs/protocols/media/markpoints_grid.png)

4) Group spirals together by selecting them and then choosing `Create group`
5) Define the protocol, in this case the exact parameters don't matter, just make sure to set `Duration (ms)` to around 100 ms when checking for alignment.
6) To run the protocol: Turn off the live scan and click `Run mark points`, you chould hear the shutter open for each stimulation
7) Turn on live scan after it finishes to check if the spirals were successfully burned (you should see black holes where the spirals were positioned)
8) If the alignment is off then re-run the protcol above
9) If you don't see any burning the most likely reasons are:

    a) Not setting the ETL to -8

    b) IR shutter is closed
    
    c) Polariser controlling the laser power is set too low (should be around 140 mW for this protocol)

IMPORTANT: for the photostim while recording, synchronize the photostimulation by clicking on synchronize with Mark points in the Prairie View GUI.
