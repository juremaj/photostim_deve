# Calibration 

## Alignment calibration

Goal: make sure that where you tell the microscope to stimulate in the GUI corresponds to the place where it will actually stimulate. E. g. that the imaging and the stimulation scanners are aligned.

Materials: a cover slip with a thin layer of a dried fluorescent marker on one side.

1) Start up the microscope
2) Orient the cover slip with the fluorescent side facing down and position it under the objective, as horizontal as possible
3) Add a drop of water to the objective and lower it until just before touching the cover slip
4) Switch to prairie view and first set the z of ETL to -8 um -> We found this empirically, that basically the photostim laser is focusing at a different z (see graph below):

![Stimulation Z Offset](/docs/protocols/media/img_stim_z_offset.jpeg)

5) Set the power to be very low (for example pockels 10 or so) since the slide is very bright and could damage the PMTs, increase if necessary
6) Now move the objective up with the z focus (manual / motor, not ETL; negative (-) is up) until you see the fluorescence slide in focus
7) If the slide is not well aligned (e. g. if you don't see it across the whole FOV) then maybe adjust it to be more perpendicular to the objective
8) Before you start the calibration make sure that you have the correct imaging settings loaded (best way to do this is using a pre-saved environment for consistency)
9) Also make sure that the photostim shutter is open ('IR shutter' in prairie view gui)
10) Make sure that the dichroic Aurelie uses is out and replaced by the appropriate filter for photostim (on top of microscope) -> otherwise the power will not be sufficient to bleach for alignment or even to stimulate a cell
11) Choose the laser power using the custom GUI controlling the polariser (Windows Taskbar -> black silhouette of a person): choose 6 for burning and 3 for photostim

Calibration (22. 4. 2025):

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

12) Launch the calibration in prairie view gui `Tools > Calibration/Alignment > Uncaging Galvo Calibration`
13) Select `Burn spots` and `Next`
14) Create a new file with name and date (this is where the calibration will be saved) and `Next`
15) When prompted if to use the current calibration choose `No` and `Next`
16) Choose the `Duration (ms)` (100 ms should be enough, but can also be increased) the laser power here doesn't do anything, since it is not controlled by prairie view (but by the GUI in step 11)) and `Next`
17) Follow the calibration steps by using Live scan, selecting the positions, burning and then realigning the points. Do this iteratively by following the instructions in prairie view.
18) You can then if the calibration was successful


## Check alignment calibration

Goal: make sure that where you tell the microscope to stimulate in the GUI corresponds to the place where it will actually stimulate. E. g. that the imaging and the stimulation scanners are aligned.

Materials: a cover slip with a thin layer of a dried fluorescent marker on one side.

1) Follow steps 1) to 11) of the 'Alignment calibration' protocol above
2) Click on Mark Points in prairie view 
3) Add several spirals of 15 um diameter arranged in a grid covering the FOV (for example 3x3 with one point in the middle, one in each corner and one on each side):

![Mark Points Grid](/docs/protocols/media/markpoints_grid.jpeg)

4) Group spirals together by selecting them and then choosing `Create group`
5) Define the protocol, in this case the exact parameters don't matter, just make sure to set `Duration (ms)` to around 100 ms when checking for alignment.
6) To run the protocol: Turn off the live scan and click `Run mark points`, you chould hear the shutter open for each stimulation
7) Turn on live scan after it finishes to check if the spirals were successfully burned (you should see black holes where the spirals were positioned)
8) If the alignment is off then re-run the protcol above
9) If you don't see any burning the most likely reasons are:
    a) Not setting the ETL to -8
    b) IR shutter is closed
    c) Polariser controlling the laser power is set too low (should be 6 - 140 mW for this protocol)