# power.md (Power measurement for imaging and stim lasers)
See `calibration_notebooks/power.ipynb` for associated notebook.

## Purpose

To measure and document the imaging ('tunable') and stimulation ('1040nm') laser power output at different wavelengths on the Bruker Ultima two-photon microscope using a power meter.

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
8) Now adjust tunable cell ouptut incrementally (e. g. 0 -> 100 -> 200 -> 300 ... -> 1000) and note down the measured power at each setting.
9) If you want to check the power at many different conditions or wevelngths keep repeating steps 3) -> 8) until you have a table of measurements for all desired conditions.
10) Make sure to turn everything off following the usual procedures.

Data and plotting: 

0) Transfer notes into an Excel (or other spreadsheet software) table, you can check the data conventions at the bottom of this protocol or you can copy and use one of the already saved tables as a template (such as `utils/calibration_power/2026-01-21_pockels.csv`).
1) Export the notes to a `.csv` file and transfer the file to `utils/calibration_power/YYYY-MM-DD_pockels.csv` where YYYY - year, MM - month, DD - day. In Excel this can be done by going to `File` > `Save as...`, then set the appropriate title (`YYYY-MM-DD_pockels.csv`) and under `File format:` select `CSV UTF8 (Comma-delimited) (.csv)`.
2) You can then simply run the Jupyter notebook associated with this protocol (`calibration_notebooks/power.ipynb`), the only thing that needs to be changed is a single line defining the ID of the calibration (e. g. `2026-01-21_pockels`)
3) This will generate a calibration curve saved in `photostim_deve/utils/calibration_power` as a `.png` file with the same name as the data (e. g. `2026-01-21_pockels.png`). See below how this plot should look:
<img src="/utils/calibration_power/2026-01-21_pockels.png" width="50%">
4) If doing photostim calibration then follow 2) below and add those values into the table as well, for example as a `1040nm_stim` column.
4) After the calibration it's also nice to print the graph and tape it somewhere near the microscope (and if you can also push it to the GitHub repo so we have a digital backup)

## 2) Protocol for photostim/'1040nm' laser

Measurement:

1) Follow steps 1)-3) of above protocol
2) Set the pockels value to 0 to not let any of the imaging laser power through.
3) The photostim ('1040nm') laser is fixed at 1040 nm so we can just set the (&lambda;) of the power meeter to this wavelength
4) Click the delta (&Delta;) (same as above)
5) Make sure that the '1040nm' laser is in 'photostim mode' and that the 'IR shutter' is open in the GUI
6) Then open a 'Mark Points' window and define for example a spiral in the middle of the FOV and set it to be stimulated for e. g. 1 second or as much time as you need to read out the power from the power meter.
7) Select the '1040nm' laser for stimulation and set the power in the Mark Points window to the right of the stimulus duration.
8) Click 'Run mark points', read out the power from the power meter and write it down to a table.
9) Repeat steps 7 and 8 for each power you wish to measure (e. g. 0 -> 100 -> 200 -> 300 ... -> 1000).
10) Make sure to turn everything off following the usual procedures.

Data and plotting:

(Follow the instructions above (section 1)) for saving data as a `.csv` in `utils/calibration_power/YYYY-MM-DD_pockels.csv` and then running the script.)


## 3) Note on data saving convention (from `power.ipynb`)

The power of the imaging laser ('tunable') and the photostim ('1040nm') laser are both controlled by a pockels cell that has a range 0-1000 in the GUI.

The convention is the first column should be called 'pockels' and the values in that column correspond to the pockel cell setting in the GUI. All the additional collumns correspond to power (in mW) for different conditions, e. g. laser wavelengths, magnification, beam expander settings etc.

For example:
| pockels | 1040nm_stim | 920nm | 830nm | 1100nm |
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

The file should be saved under `photostim_deve/utils/power_calibration` as a csv, for example in the format `YYYY-MM-DD_pockels.csv` (or `YYYY-MM-DD_1040nm.csv`). This notebook will output a graph with the same name in the same name as a `.png` file.
