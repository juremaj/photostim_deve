# Target stimulation 

TODO: This protocol is still very preliminary - I need to go through it once on the microscope

Goal: Stimulate the programmaticaly selected targets (see: [target_select](docs/protocols/target_select.md))
            
1) Perform all the necessary steps to select targets, generating the necessary microscope control and helper files (see: [target_select](docs/protocols/target_select.md))
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
15) Finally we are ready to launch the recording which is done as normally, the only difference is in the TSeries window you need to specify the synchrnisation with MarkPoints by choosing `current`
16) It is good as a sanity check to wait until for the stimulation epoch to start and see if the cells we are expecting to respond actually do when we hear the shutter. Usually I count the number of shutter sounds while looking at an upcoming spiral index.
