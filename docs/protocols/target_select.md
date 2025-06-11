# Target selection 

Global goal: To be able to choose targets in a more principled way - not only by sitting in the microscope and choosing some cells that look nice to us :)
            
For example:
    1) Choosing a random sample of cells (ensures they are IID, for example from a set detected by Suite2p on functional imaging or CellPose on isosbestic or opsin reporter channels etc.)
    2) Choosing functionally defined cells (for example cells that are most reponsive to a stimulus, cells that fire at a particular threadmill position / phase in a sequence etc.)
    3) Choosing good controls for 1) and 2) (for example cell that expresses gcamp but not opsin and vice versa)

## Target selection (suite2p)

Goal: Use functional imaging to detect possible targets that can be used for photostim. Note that this does not guarantee that the detected cells express opsin. For now only adapted to use random cell indexes (as in goal 1) above) but it would be very easy to adapt for functionally defined cells.

1) Do a normal recording experiment, run preprocessing to get the suite2p preprocessed data, manually curate the ROIs if necessary
2) Run `target_select.ipynb` in the root of `photostim_deve` which allows you to set the path to the s2p folder and the number of random cells you want to select
3) This script will generate an `export/*subject*` folder in the root of `photostim_deve` where it will save the output files used to communicate to the microscope where to stimulate to target the chosen cells. This folder contains:
    a) `galvo_point_list_*subject*.gpl` (most important file that can be loaded directly in the prairie view GUI allowing the microscope to automatically generate the spirals centered on selected cells)
    b) `MarkPoints_*subject*.xml` (this is mostly obsolete - related to some strange handling of photostim metadata by bruker / prairie view)
    c) `mean_fov.png` (mean projection of the gcamp channel from suite2p, that can be used to find the same FOV between this experiment and the photostim)
    d) `medians_selected.png` (same image but with all s2p detected ROIs marked by points (at ROI centroid), with the ROIs selected for stim highlighted in orange and their s2p indexes written - this is used as a sanity check when doing the experiment to know that we are stimulating the correct cells by comparing what we see here to the prairie view gui with the spirals overlayed in the Mark Points view).


## Target selection (Cellpose on isosbestic or opsin reporter channel)

Goal: Use expression of gcamp and/or opsin to detect possible targets that can be used for photostim. This makes sure we are not biased for highly active cells, gives us insight into if a cells is likely to respond (e. g. if co-expressing both), and can be used to define control cells to target (for example cell that expresses gcamp but not opsin and vice versa) 

TODO...