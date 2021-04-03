# 3D_contours_YT


A simple tool to visual the disk velocity at the line of sight. The model takes a simple thin disk with a Keplerian velocity field. 

To run it, set the data path, map and velocity range and type >> python Plot3D.py

The script reads fits file with axes of RA, Dec, and velocity.
However, this can also be modified for different data cube to use.

#### Requirments:
* Numpy
* Matplotlib
* astropy
* imageio
* scipy
* yt

### Example
A simple 3D contours HCO+ line twoard SVS13 (ALMA data from Hsieh et al. 2019).

![image](https://github.com/tienhaohsieh/3D_contours_YT/blob/main/animax.gif)
