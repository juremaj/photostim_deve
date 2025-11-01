# photostim.md (Perform targetted photostimulation of selected cells)
This protocol is assiciated with photostim sessions, ending with suffix `_b` to `_f`.
See `.../...` for associated notebook.

For the associated protocols refer to calbration response protocols (`photostim_deve/docs/protocols/calibration_response`)


## 1) Target select

Global goal: To be able to choose targets in a more principled way - not only by sitting in the microscope and choosing some cells that look nice to us :)
            
For example:
    1) Choosing a random sample of cells (ensures they are IID, for example from a set detected by Suite2p on functional imaging or CellPose on isosbestic or opsin reporter channels etc.)
    2) Choosing functionally defined cells (for example cells that are most reponsive to a stimulus, cells that fire at a particular threadmill position / phase in a sequence etc.)
    3) Choosing good controls for 1) and 2) (for example cell that expresses gcamp but not opsin and vice versa)

### Suite2p

Goal: Use functional imaging to detect possible targets that can be used for photostim. Note that this does not guarantee that the detected cells express opsin. For now only adapted to use random cell indexes (as in goal 1) above) but it would be very easy to adapt for functionally defined cells.

1) Do a normal recording experiment, run preprocessing to get the suite2p preprocessed data, manually curate the ROIs if necessary
2) Run `target_select.ipynb` in the root of `photostim_deve` which allows you to set the path to the s2p folder and the number of random cells you want to select
3) This script will generate an `export/*subject*` folder in the root of `photostim_deve` where it will save the output files used to communicate to the microscope where to stimulate to target the chosen cells. This folder contains:

    a) `galvo_point_list_*subject*_s2p.gpl` (most important file that can be loaded directly in the prairie view GUI allowing the microscope to automatically generate the spirals centered on selected cells)

    b) `MarkPoints_*subject*_s2p.xml` (this is mostly obsolete - related to some strange handling of photostim metadata by bruker / prairie view)

    c) `mean_fov_s2p.png` (mean projection of the gcamp channel from suite2p, that can be used to find the same FOV between this experiment and the photostim)
    
    d) `medians_selected_s2p.png` (same image but with all s2p detected ROIs marked by points (at ROI centroid), with the ROIs selected for stim highlighted in orange and their s2p indexes written - this is used as a sanity check when doing the experiment to know that we are stimulating the correct cells by comparing what we see here to the prairie view gui with the spirals overlayed in the Mark Points view).


### Cellpose


1) Do an FOV recording at the wavelength that excites the tag of the opsin (usually 1100nm), making sure that you are at the correct z wrt the gcamp imaging plane (usually 920nm meaning about at 10 um shift in focus)
2) Run `target_select_cellpose.ipynb` in the root of `photostim_deve` which allows you to set the path to the FOV folder and the number of random cells you want to select
3) This script will generate an `export/*subject*` folder in the root of `photostim_deve` where there will be exactly the same documents as described above for Suite2p but with the appendix of `_cellpose` instead of `_s2p`

## 2) Target stim

TODO: This protocol is still very preliminary - I need to go through it once on the microscope

Goal: Stimulate the programmaticaly selected targets (see above
            
1) Perform all the necessary steps to select targets, generating the necessary microscope control and helper files (see above) or manually select cells for stimulation
2) Check that the calibration is working (see [calibrate](docs/protocols/calibrate.md)) 
3) Set up the stimulation laser / path correctly(see [calibrate](docs/protocols/calibrate.md) for more detail):

    a) ETL should be at -8 to be aligned to the imaging

    b) IR shutter should be open

    c) Brainbow dicroic should be out and replaced with the photostim filter (top of microscope)

    d) Power should be set accordingly at the polariser (see table below, for now I was using 3 - 53 mW)
    

Stim power calibration (22. 4. 2025):

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

<img src="/docs/protocols/media/2025-04-22_uncaging.png" width="50%">


4) In the prairie view gui load the imaging settings (from environment file) and the 'uncaging calibration' (the one done in [calibrate](docs/protocols/calibrate.md), there is a bug only allowing integer zooms, e. g. 1x or 2x but don't worry it is just a display issue)
5) Navigate to the same field of view as used for target selection (one way to do this is to use `export/*subject*/mean_fov.png` as a guide, or other images of FOV like isosbestic or opsin reporter).
6) Take fov pictures of green at 830 nm excitation and red channel at 1100 nm excitation to get isosbestic and opsin respectively. I do this by doing a 128 frame recording of each. IMPORTANT TODO: We need to check for imaging laser power and the z shift in both in comparison to 920 nm.
7) Open the `Mark Points` window to start defining the stimulation protocol
8) (Optional:) If it does not interfere with your experiment you can use this time to do a sanity check that stimulation works and the cells respond. This can be done in a similar way as the 'Check alignment' part of the [calibrate](docs/protocols/calibrate.md) protocol - just make sure to adjust the power and stim time accordingly (for example 3 - 53 mW and 50 ms). You can use the red and green channels to manually target a cell that expresses both and maybe a control and then you can run the protocol (Run Points) while looking at the FOV in Live view - you should hear the shutter open, see the response of the cell and potentially a bit of a stim artifact in live view.
9) To automatically select the cells based on [target_select](docs/protocols/target_select.md) load the configuration (`export/*subject*/galvo_point_list_*subject*.gpl` file) in the `Mark Points` window. This should position the spirals close to the selected cells.
10) Most likely the original FOV alignment was not 100% accurate, so you can align the stimulation points more precisely by looking at `export/*subject*/medians_selected.png` and shifting the FOV in x and y until the stimulation points align with neurons as seen in the image.
11) Especially if doing this in development across days there might be non-rigid changes in the FOV across days, due to growth or small lateral displacements of neurons -> this means that just by shifting in x and y we will not be able to see as good of an alignment as in `export/*subject*/medians_selected.png`. For now this means that a 'good enough' alignment is found as described above and then each individual points needs to be manually adjusted to really target the desired neuron, based on looking at `export/*subject*/medians_selected.png` as a reference.
12) Once you are happy with the alignment of the points you can also define some control points, for example opsin-negative or gcamp negative cells, neuropil, blood vessels etc.
13) The next step is to define the protocol in time (e. g. which point will be stimulated when and for how long) (TODO: add documentation on all parameters)
14) Once this is done it is good to export the final version of files with corrections - especially if doing stimulations across many days, so the latest version can be used for the next session.
15) Finally we are ready to launch the recording which is done as normally, the only difference is in the TSeries window you need to specify the synchronisation with MarkPoints by choosing `current`
16) It is good as a sanity check to wait until for the stimulation epoch to start and see if the cells we are expecting to respond actually do when we hear the shutter. Usually I count the number of shutter sounds while looking at an upcoming spiral index.

17) Map responses by running suite2p and the `resp_map.ipynb` notebook. TODO: automatise to run it immediately after suite2p (if session type input is `_b` to `_f`)