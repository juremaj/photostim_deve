import os
import numpy as np
import xml.etree.ElementTree as ET

# 1) Functions to read segmentation results from Suite2p and Cellpose

def get_med_img_s2p(data_path):
    """
    Get the median values of all ROIs based on s2p segmentation and the mean image from s2p.

    Parameters
    ---------
    data_path : str
        Path to the data directory containing Suite2p segmentation results.


    Returns
    -------
    meds : np.ndarray
        Array of median values for each ROI.
    mn_image : np.ndarray
        Mean image used for Suite2p segmentation.
    s2p_idxs : np.ndarray
        Indices of the ROIs that were classified as cells based on the iscell manual curation.
    -------
    """

    print('Using Suite2p segmentation for cell ROIs...')

    s2p_path = os.path.join(data_path, 'suite2p', 'plane0')
    ops = np.load(os.path.join(s2p_path, 'ops.npy'), allow_pickle=True).item()
    stat = np.load(os.path.join(s2p_path, 'stat.npy'), allow_pickle=True)
    iscell = np.load(os.path.join(s2p_path, 'iscell.npy'), allow_pickle=True)

    # now filter stat based on the iscell manual curation
    iscell_bool = iscell[:,0].astype(bool)
    print(f'Found: {sum(iscell_bool)} cells based on iscell manual curation.')
    s2p_idxs = np.arange(iscell.shape[0])[iscell_bool]

    stat_iscell = []
    meds = []
    for i, s in enumerate(stat):
        if iscell_bool[i]:
            stat_iscell.append(s)
            meds.append(s['med'])

    mn_image = ops['meanImg']
    
    return np.array(meds), mn_image, s2p_idxs


def get_seg_img_cp(data_path):

    """
    Get the median values of all ROIs based on cellpose fov segmentation and the image used for cellpose segmentation.
    """
    return None, None


# 2) Functions to write the MarkPoints .xml file and the galvo point list .gpl files

def indent(elem, level=0):
    i = "\n" + level * "  "  # two spaces per level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def write_mp_file(meds, inds, mp_temp_path=None, export_path=None, mouse_str=None, fov_shape=(512, 512), SpiralWidth='0.0199325637636341', SpiralHeight='0.0199325637636341', SpiralSizeInMicrons='15.0000000000001'): 
  
  tree = ET.parse(mp_temp_path)
  root = tree.getroot()

  # clear the existing points in the template
  root[0][0].clear()

  for (i, s2p_i) in enumerate(inds):

      # in the PVGalvoPointElement add a new Point element
      point = ET.Element('Point')
      point.set('Index', str(i+1))
      point.set('X', str(meds[s2p_i, 1] / fov_shape[1]))
      point.set('Y', str(meds[s2p_i, 0] / fov_shape[0]))
      point.set('IsSpiral', 'True')
      point.set('SpiralWidth', SpiralWidth)
      point.set('SpiralHeight', SpiralHeight)
      point.set('SpiralSizeInMicrons', SpiralSizeInMicrons)

      # append the point to the root element  
      root[0][0].append(point)

  indent(root)

  tree.write(os.path.join(export_path, f'MarkPoints_{mouse_str}.xml'), encoding='utf-8', xml_declaration=True)

def write_gpl_file(meds, inds, gpl_temp_path=None, export_path=None, mouse_str=None, fov_shape=(512, 512), ActivityType="MarkPoints", UncagingLaser="Uncaging", UncagingLaserPower="1000", Duration="50", IsSpiral="True", SpiralSize="0.110870362837845", SpiralRevolutions="7", Z="807.424999999999", X_lim = 2.79639654844993, Y_lim = 3.09924006097119):
    """
    Write a galvo point list file (.gpl) based on the medians of the ROIs.

    Parameters
    ----------
    meds : np.ndarray
        Array of medians of the ROIs.
    mp_temp_path : str
        Path to the MarkPoints template file.
    -----------
    """

    tree = ET.parse(gpl_temp_path)
    root = tree.getroot()

    # remove the PVGalvoPointList elements
    root.clear()

    for (i, s2p_i) in enumerate(inds):
        # in the PVGalvoPointElement add a new Point element
        point = ET.Element('PVGalvoPoint')

        x_s2p_norm = meds[s2p_i, 1] / fov_shape[1]
        y_s2p_norm = meds[s2p_i, 0] / fov_shape[0]

        # now scale between -X_lim and X_lim
        x_gpl = (x_s2p_norm - 0.5) * 2 * X_lim
        y_gpl = (y_s2p_norm - 0.5) * 2 * Y_lim

        point.set('X', str(x_gpl))
        point.set('Y', str(y_gpl))
        point.set('Name', f'Point {i+1}')
        point.set('Index', str(i))
        point.set('ActivityType', ActivityType)
        point.set('UncagingLaser', UncagingLaser)
        point.set('UncagingLaserPower', UncagingLaserPower)
        point.set('Duration', Duration)
        point.set('IsSpiral', IsSpiral)
        point.set('SpiralSize', SpiralSize)
        point.set('SpiralRevolutions', SpiralRevolutions)
        point.set('Z', Z)

        # append the point to the PVGalvoPointElement
        root.append(point)

    # now add the group to the PVGalvoPointList
    group = ET.Element('PVGalvoPointGroup')
    group.set('Indices', ','.join([str(i) for i in range(len(inds))]))
    group.set('Name', 'Group 1')
    group.set('Index', str(len(inds)))
    group.set('ActivityType', ActivityType)
    group.set('UncagingLaser', UncagingLaser)
    group.set('UncagingLaserPower', UncagingLaserPower)
    group.set('Duration', Duration)
    group.set('IsSpiral', IsSpiral)
    group.set('SpiralSize', SpiralSize)
    group.set('SpiralRevolutions', SpiralRevolutions)
    group.set('Z', Z)

    root.append(group)

    # now save the file
    indent(root)

    tree.write(os.path.join(export_path, f'galvo_point_list_{mouse_str}.gpl'), encoding='utf-8', xml_declaration=True)