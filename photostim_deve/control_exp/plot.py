import os 
import matplotlib.pyplot as plt

def plot_fov(mn_image, export_path, vmax=400):
    """
    Plot the mean FOV image.
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.imshow(mn_image, cmap='gray', vmin=0, vmax=vmax)
    plt.axis('off')
    plt.savefig(os.path.join(export_path, 'mean_fov.png'), dpi=300)

def plot_fov_meds(mn_image, meds, inds, export_path, vmax=400):
    """
    Plot the mean FOV image with all medians and the selected ones highlighted.
    """
    plt.figure(figsize=(5, 5), dpi=300)
    plt.scatter(meds[:,1], meds[:,0], c='C0', s=1)
    for i in inds:
        plt.scatter(meds[i,1], meds[i,0], c='C1', s=1)
        # add text of index and x and y coordinates
        plt.text(meds[i,1], meds[i,0]+5, i, fontsize=5, color='C1', ha='right', va='top')
    plt.imshow(mn_image, cmap='gray', vmin=0, vmax=vmax)
    plt.axis('off')
    plt.savefig(os.path.join(export_path, 'medians_selected.png'), dpi=300)