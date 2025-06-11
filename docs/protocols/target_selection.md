# Target selection 

Global goal: To be able to choose targets in a more principled way - not only by sitting in the microscope and choosing some cells that look nice to us :)
            
                For example:
                    1) Choosing random cells (for example from a set detected by Suite2p on functional imaging or CellPose on isosbestic or opsin reporter channels etc.)
                    2) Choosing functionally defined cells (for example cells that are most reponsive to a stimulus, cells that fire at a particular threadmill position / phase in a sequence etc.)
                    3) Choosing good controls for 1) and 2) (for example cell that expresses gcamp but not opsin and vice versa)

## Target detection (using suite2p)

Goal: Use functional imaging to detect possible targets that can be used for photostim. Note that this does not guarantee that the detected cells express opsin. For now only adapted to use random cell indexes (as in goal 1) above) but it would be very easy to adapt for functionally defined cells

Materials: Mouse co-expressing gcamp and opsin. Code included in this repository.

1) Do a normal recording experiment, run preprocessing to get the suite2p preprocessed data, manually curate the ROIs if necessary
2) Run `roi_stim_select.ipynb` which allows you to set the path to the s2p folder and the number of random cells you want to select