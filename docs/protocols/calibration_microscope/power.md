# power.md (Power measurement for imaging and stim lasers)
See `calibration_notebooks/power.ipynb` for associated notebook.

## Purpose

To measure and document the imaging laser power output at different wavelengths on the Bruker Ultima two-photon microscope using a calibrated power meter.

## Materials

- ThorLabs power meter (can usually be found somewhere around the microscope, see picture)
- Optical mount (to position the sensor under the objective)

<img src="/docs/protocols/media/power_meter.png" width="50%">


## 1) Protocol for imaging/'pockels' laser

Measurement:

1) Follow the normal microscope on procedure (wait at least 30 min for laser to stabilise if it was turned off before)
2) Position the power meter sensor under the microscope objective using the optical mount. Make sure that all the light coming out of the objective falls onto the sensor.
3) Go to Prairie View and set up the specific imaging conditions for which you want to measure the power output. The best is to load these from prairie view presets, to be sure that exactly the same settings are used when doing the power measurement as when performing the experiment.
4) Usually (in photostim) we would measure power at 830 nm (isosbestic gcamp), 920 nm (Ca2+ bound gcamp, slightly blue shifted), 1100 nm (mScarlet to localise opsin). 
5) Click the lambda (&lambda;) symbol and select the appropriate wavelength that was chosen in 4)
6) Click the delta (&Delta;) symbol to make sure to zero the power measurement when the sensor is in place and the laser is off
7) In Prairie view click 'Live scan' to let the laser reach the objective, with the settings used in imaging.
8) Now adjust Pockels cell ouptut incrementally (e. g. 0 -> 100 -> 200 -> 300 ... -> 1000) and note down the measured power at each setting.
9) If you want to check the power at many different conditions or wevelngths keep repeating steps 3) -> 8) until you have a table of measurements for all desired conditions.
10) Make sure to turn everything off following the usual procedures.

Data and plotting: 

1) Transfer the notes to a `.csv` table saved in `utils/calibration_power/YYYY-MM-DD_pockels.csv` where YYYY - year, MM - month, DD - day. You can check the data conventions at the bottom of this protocol or you can simply copy and use one of the already saved tables as a template (such as `utils/calibration_power/2025-10-10_pockels.csv`).
2) You can then simply run the Jupyter notebook associated with this protocol (`calibration_notebooks/power.ipynb`), the only thing that needs to be changed is a single line defining the ID of the calibration (e. g. `2025-10-10_pockels`)
3) This will generate a calibration curve saved in `photostim_deve/utils/power_calibration` as a `/png` file with the same name as the data (e. g. `2025-10-10_pockels.png`). See below how this plot should look:
<img src="/docs/protocols/media/2025-10-10_pockels.png" width="50%">
4) After the calibration it's also nice to print the graph and tape it somewhere near the microscope (and if you can also push it to the GitHub repo so we have a digital backup)

## 2) Protocol for photostim/'uncaging' laser

Measurement:

1) Follow steps 1)-3) of above protocol
2) Set the pockels value to 0 to not let any of the imaging laser power through.
3) The photostim ('uncaging') laser is fixed at 1040 nm so we can just set the (&lambda;) of the power meeter to this wavelength
4)  Click the delta (&Delta;) (same as above)
5)  To adjust the power of the laser we use a polariser that can be changed either through the software of the black silhouette figure in the Bruker computer Windows toolbar or by manually adjusting it using the controller at the back of the microscope.
6)  Set the polariser to 0 deg to have the minimum power of the stim laser.
7)  To let the stimulation laser through in Prairie view go to `Tools > Maintenance` and set `Uncaging` to `Open`.

Data and plotting:

1) Follow the same steps as for the imaging laser, the only differece is the convention, in this using the appendix `_uncaging.csv` (full path: `utils/calibration_power/YYYY-MM-DD_uncaging.csv`), for more info see at the bottom of this notebook.
2) The Jupyter notebook will recognise it is a photostim calibration based on this file ending and plot the results properly. It will again be saved as a png using the same convention (in this case `utils/calibration_power/YYYY-MM-DD_uncaging.png`). It should look something like this:
<img src="/docs/protocols/media/2025-10-10_uncaging.png" width="50%">


## 3) Note on data saving convention (from `power.ipynb`)

The power of the imaging laser is controlled by a pockels cell that has a range 0-1000 in the GUI, for the photostim laser it is controlled by a polariser that has range between 0 and 360 degrees.

The convention is the first column should be called either 'pockels' or 'uncaging' (depending on which laser is being calibrated) and the values in that column correspond to the pockles cell setting or the angle of the polariser. All the additional collumns correspond to power (in mW) for different condtions, e. g. laser wavelengths, magnification, beam expander settings etc.

For example for pockels:
| pockels | 920nm_noscan | 920nm | 830nm | 1100nm |
|----------|---------------|-------|-------|---------|
| 0   | 0   | 0   | 0   | 0   |
| 100 | 18  | 7   | 36  | 2   |
| 200 | 28  | 21  | 59  | 6   |
| 300 | 50  | 41  | 89  | 11  |
| 400 | 78  | 66  | 120 | 18  |
| 500 | 109 | 92  | 148 | 26  |
| 600 | 140 | 117 | 172 | 34  |
| 700 | 170 | 140 | 188 | 43  |
| 800 | 196 | 160 | 193 | 51  |
| 900 | 216 | 173 | 189 | 58  |
| 1000| 228 | 178 | 176 | 63  |

or for uncaging:
| uncaging | 1040 nm |
|-----------|----------|
| 0         | 4.4      |
| 1         | 6.7      |
| 2         | 20.5     |
| 3         | 33.4     |
| 4         | 41.0     |
| 5         | 71.0     |
| 6         | 88.8     |
| 7         | 123.1    |


The file should be saved under `photostim_deve/utils/power_calibration` as a csv, for example in the format `YYYY-MM-DD_pockels.csv` (or `YYYY-MM-DD_uncaging.csv`). This notebook will output a graph with the same name in the same name as a `.png` file.
