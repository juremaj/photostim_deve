# Calcium Imaging Data Organization

This repository contains calcium imaging experiments conducted by **jm**.  
Each dataset is organized by **mouse**, then by **session**, and finally by acquisition type.
Each dataset also has corresponding metadata in **mouse** and **session** tables for example:
- for mouse: genotype, DOB, virus injected etc.
- for session: mouse age, mouse weight etc.
For live version of metadata see: https://docs.google.com/spreadsheets/d/1rl6-1a2jIe5BLdo5ZLTNi4wGKArYpwoj0SRAIn4cNn0/edit?gid=2134894366#gid=2134894366 
For automated analysis the **mouse** and **session** tables should be exported and saved in the **jm** folder.

The main division of the data is into raw (`data_raw`) and preprocessed (`data_proc`) with the specifics of each described below. As a guideline:
- `data_raw` contains the raw outputs of the imaging experiment transferred directly from the Bruker computer. This data should be read only (users should not add new 'raw' data, neither modify or delete any of the existing data). Includes for example imaging tiffs, camera tiffs, zstacks, data about opto/sensory stimuli etc.
- `data_proc` contains all the outputs of analysis scripts that operate on `data_raw` and/or `data_proc`. This is more flexible, new analyses can be added etc. Includes for example suite2p outputs, motion energy calculations, computed responses of cells to opto/sensory stimuli etc.

The basic convention of splitting by **mouse** and **session** is consistent across the two types, in order to maintain correspondance. For specific differences in the data format between the two see below.

## Modular Design of Experimental Pipelines

Before going to the nitty gritty of the file organisation first lets just go through the different session types that we can have during the course of the experiment and how these can form conmplex pipelines. To make things easier we can think of different 'session types', where each will be associated with a 'suffix'. We use this convention:

| Session Suffix | Name / Purpose             |
|----------------|----------------------------|
| `_a`           | Spontaneous activity       |
| `_b` – `_f`    | Photostimulation           |
| `_s`           | Sensory stimulation        |
| `_z`           | Z-stack imaging            |
| `_calib`       | Calibration (in vivo)      |

The folder structure described below is intentionally **modular**, making it easy to design and conceptualize experimental pipelines.  
Each session type (spontaneous, photostim, sensory, z-stack, calibration) is a **self-contained module** with predictable inputs and outputs. Each module can then also be associated with its specific analyses (for example computing spointaneous calcium event rates in `_a` sessions, mapping photostim responses in `_b` – `_f` sessions etc.)  

In terms of experimental design this modular structure is also nice to conceptualise experiments.
For example we can think of a simple experiment where we do a spontaneus session and then a zstack as `_a` -> `_z`

This seems a bit unnecessary but it can be very nice for more complicated longitudinal experiments. For example we can visualise these as a table where rows are each possible session type, columns are mouse age (for example P8 to P14), and emtpy entry means this session was not performed and an index (1-#) corresponds to the order at which that particular session type was performed on that perticular day.

This might be more clear with this example (mouse jm039 from the Track2p paper) where `_a` and `z` were performed daily between P8 and P14:


| Session Type | P8 | P9 | P10 | P11 | P12 | P13 | P14 |
|--------------|----|----|-----|-----|-----|-----|-----|
| `_a`         | 1  | 1  | 1   | 1   | 1   | 1   | 1   |
| `_b` – `_f`  |    |    |     |     |     |     |     |
| `_s`         |    |    |     |     |     |     |     |
| `_z`         | 2  | 2  | 2   | 2   | 2   | 2   | 2   |
| `_calib`     |    |    |     |     |     |     |     |


This is still quite simple, but we can for example think of an experiment where the question is if early photostim affects the development of later sensory responses. In that case the table would look like:

| Session Type | P8 | P9 | P10 | P11 | P12 | P13 | P14 |
|--------------|----|----|-----|-----|-----|-----|-----|
| `_a`         | 1  | 1  | 1   | 1   | 1   | 1   | 1   |
| `_s`         | 2  | 2  | 2   | 2   | 2   | 2   | 2   |
| `_b` – `_f`  | 3  |    |     |     |     |     |     |
| `_z`         |    |    |     |     |     |     |     |
| `_calib`     |    |    |     |     |     |     |     |

And for example if we want to do the calibration first (before photostim); check again the responses at the last day and also do a z-stack on the last day to use it as a reference for ex-vivo alignemtn (e. g. for transcriptomics):

| Session Type | P8 | P9 | P10 | P11 | P12 | P13 | P14 |
|--------------|----|----|-----|-----|-----|-----|-----|
| `_a`         | 1  | 1  | 1   | 1   | 1   | 1   | 1   |
| `_s`         | 2  | 2  | 2   | 2   | 2   | 2   | 2   |
| `_b` – `_f`  | 4  |    |     |     |     |     | 3   |
| `_z`         |    |    |     |     |     |     | 4   |
| `_calib`     | 3  |    |     |     |     |     |     |

Now that we have a basic idea of the modular structure we can look a bit into how this structure is reflected in the folder structure of the data, first starting with raw data.

---

## Raw data (`data_raw`) folder Structure

### Top Level
- **jm0XX/** → Data for a single mouse (e.g., `jm048`, `jm049`).
- **jm_archived/** → Archived/old datasets.

---

### Mouse Folder (`jm0XX`)
Each folder corresponds to one mouse and contains all imaging sessions.  

**Example:**
```text
jm048/
├── 2025-05-06_a/
├── 2025-05-06_b/
├── 2025-05-07_c/
└── 2025-05-09_s/
```
---

### Session Folders
Session folders are named by **date** and an identifying **suffix**:  

**Format:**  
`YYYY-MM-DD_[suffix]`

#### Session Suffix Conventions (raw data) :
- **`_a` → Spontaneous activity session**  
  - Normal session of spontaneous activity  
  - May include a **/camera/** folder with videography recordings  

- **`_b` to `_f` → Photostimulation sessions**  
  - Up to 5 sessions per day where selected cells are photostimulated  
  - `TSeries` folder contains calcium imaging TIFFs **plus an additional file**:  
    - `_MarkPoints.xml` → Defines stimulation protocol  

- **`_s` → Sensory stimulation session**  
  - Includes additional files in the session root:  
    - `stim_protocol.npy` → Stimulus type information  
    - `stim_times.npy` → Timing of each stimulus  

- **`_z` → Z-stack session**  
  - Imaging across the whole volume  
  - May include acquisitions at different wavelengths and zoom levels  

- **`_calib` → Calibration session**  
  - Contains subfolders for **in vivo calibration protocols**:  
    - 'Parameter optimisation' (linked to the `param_optim.md` protocol and associated jupyter notebooks):
      - **power/** → Different stimulation powers (e.g., `010mw`, `020mw`, …)  
      - **time/** → Different stimulation durations (e.g., `004ms`, `008ms`, …)  
      - Each subfolder of **power/** or **power/** contains a `TSeries` folder with tiffs and `_MarkPoints.xml` for the stimulation protocol (similarly as a `_b` to `_f` session) for the stimulations conducted using the specified parameter setting.
    - 'Physiological PSF' (linked to the `phys_psd.md` protocol)
      - **ppsf_xy/** → Physiological PSF in x–y (grid stimulations around cells)  
      - **ppsf_z/** → Physiological PSF in z (spirals at different z depths)  
      - These (**ppsf_xy/** or **ppsf_z/**) will contain a subfolder something like `07grid_a` where `07` means it is a 7x7 grid (for ppsf_xy - 2d) or 7 z positions (for ppsf_z - 1d) and `_a` is there in case more ppsf calibrations are performed in the same session. This folder (e. g. `07grid_a`) will contain a `TSeries` folder with tiffs and `_MarkPoints.xml` for the stimulation protocol (similarly as a `_b` to `_f` session) for the stimulations conducted using the specified parameter setting.

---

### Inside a Session Folder
Each session folder typically contains:

- **fov/** → Field-of-view reference images  
  - `920nm/` → Images acquired at 920 nm  
  - `1100nm/` → Images acquired at 1100 nm  

- **SingleImage-XXXXXXXX-XXX/** → Single frame capture (reference/overview image) (this is not super important - not used for analysis).  

- **TSeries-XXXXXXXX-XXX/** → Two-photon calcium imaging TIFF files  
  - Each folder contains ~20 minutes of continuous calcium imaging data  

Here is the example file structure related to the above notes:

---

## Example Structure
```text
jm/
│
├── jm048/
│   ├── 2025-05-06_a/              # (a) spontaneous session
│   │   ├── fov/
│   │   │   ├── 920nm/
│   │   │   └── 1100nm/
│   │   ├── camera/                # optional videography (if recorded)
│   │   └── TSeries-10032023-1822-006/
│   │
│   ├── 2025-05-06_b/              # (b–f) photostim session
│   │   ├── fov/
│   │   ├── TSeries-10032023-1822-007/
│   │   │   └── TSeries-10032023-1822-007_MarkPoints.xml
│   │
│   ├── 2025-05-09_s/              # (s) sensory stim session
│   │   ├── fov/
│   │   ├── TSeries-10032023-1822-008/
│   │   ├── stim_protocol.npy      # stimulus identity
│   │   └── stim_times.npy         # stimulus timing
│   │
│   ├── 2025-05-12_z/              # (z) z-stack session
│   │   ├── 920nm/
│   │   │   ├── zoom1/
│   │   │   └── zoom2/
│   │   └── 1100nm/
│   │       └── zoom1/
│   │
│   └── 2025-07-10_calib/          # (calib) calibration session
│       ├── power/                 # param_optim.md
│       │   ├── 010mw/
│       │   │   └── TSeries-10032023-1822-020/
│       │   ├── 020mw/
│       │   ├── 040mw/
│       │   └── ...
│       │
│       ├── time/                  # param_optim.md
│       │   ├── 004ms/
│       │   │   └── TSeries-10032023-1822-015/
│       │   ├── 008ms/
│       │   ├── 016ms/
│       │   └── ...
│       │
│       ├── ppsf_xy/               # phys_psf_xy.md
│       │   └── 07grid_a/
│       │       └── TSeries-10032023-1822-026/
│       │
│       └── ppsf_z/                # phys_psf_z.md
│           └── 07grid_a/
│               └── TSeries-10032023-1822-028/
│
├── jm049/
├── jm050/
└── jm_archived/
```



### Best Practices for Saving New Raw Data

To maintain consistency and support automated analysis:

1. **Session Naming**
   - Always follow the format: `YYYY-MM-DD_suffix`
   - Use the correct suffix (`_a`, `_b–f`, `_s`, `_z`, `_calib`) depending on the session type.
   - If necessary to make a new type of experiment (for example cued or uncued treadmill) then make sure to assing a new suffix and update the documentation accordingly

2. **Spontaneous Sessions (`_a`)**
   - If videography was recorded, save files in a `/camera/` subfolder within the session root.  
   - Do not mix camera data with `TSeries` or `fov` folders.

3. **Photostimulation Sessions (`_b–f`)**
   - Ensure that each `TSeries` folder contains its corresponding `MarkPoints` file.  
   - Never rename the XML file — the filename links it to the imaging data.

4. **Sensory Stimulation Sessions (`_s`)**
   - Save `stim_protocol.npy` and `stim_times.npy` directly in the session root.  
   - Do not place them inside `TSeries` or `fov`.  

5. **Z-stack Sessions (`_z`)**
   - Clearly label acquisitions by wavelength and zoom level inside `fov/`.  

6. **General Notes**
   - Never alter automatically generated folder names (`SingleImage-*`, `TSeries-*`).  
   - Avoid spaces in folder or file names (underscores `_` are preferred).  
   - Keep raw data unmodified


## Processed data (`data_proc`) folder Structure

### Common data across session types:
- The only thing in common with all processed data folders is that they will contain a Suite2p folder
- Additionally if an `fov` folder exists in the raw data, the processed data should also include a copy of that folder

### Session type specific data (processed data):
NOTE: ... denotes that additional conventions are not strictly set as of now.

- **`_a` → Spontaneous activity session**  
  - These may additionally include a `move_deve` folder that contains the computed motion energy and outputs of analyses from the Majnik et al. 2025 paper.
  - ...

- **`_b` to `_f` → Photostimulation sessions**  
  - To compute responses of cells to photostim these sessions should additionally contain a copy of the `MarkPoints` file
  - ...

- **`_s` → Sensory stimulation session**  
  - To compute responses of cells to sensory stim these sessions should additionally contain a copy of `stim_protocol.npy` and `stim_times.npy`
  - ...

- **`_z` → Z-stack session**  
  - ...

- **`_calib` → Calibration session**  
  - ...


