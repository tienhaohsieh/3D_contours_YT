#! bin/python
from numpy import *
from astropy.io import fits as pyfits
from glob import glob
from os import sys,system
sys.path.append('functions/')
from Noise import *
from ZoomIn import *
from header import *
from pylab import *
import yt
import imageio as io
from scipy.ndimage import gaussian_filter

fits_path='data/'
im_li=glob(fits_path+'J032903.7+311603_hcop.pbcor.fits')

for im in im_li:
    fits_name=im.split('/')[-1]
    fits=pyfits.open(fits_path+fits_name)
    data=fits[0].data[0]
    header=fits[0].header
    noi_chan=Noise(data,pl=False,start=-0.2,end=0.2,cell=0.004)

    zoom_data=Zoom(data,header)
    zoom_data.ra_lim=[52.26366592,52.26811729]
    zoom_data.dec_lim=[31.2656986,31.26924292]
    print(zoom_data.v_idx,zoom_data.ra_idx,zoom_data.dec_idx)
    sm_data=gaussian_filter(zoom_data.trimed_data, sigma=1)
    data=dict(density = (sm_data, "g/cm**3"))
#    bbox = np.array([zoom_data.b_v(), zoom_data.b_dec(), zoom_data.b_ra()])
    bbox = np.array([[-1.5,1.5],[-1.5,1.5],[-1.5,1.5]])
    ds = yt.load_uniform_grid(data, zoom_data.trimed_data.shape,length_unit="Mpc", bbox=bbox)

    sc = yt.create_scene(ds, lens_type='perspective')
    sc.annotate_axes(alpha=0.1)

    source = sc[0]
    source.set_field('density')
    source.set_log(True)
    bounds=(0.15,0.3)
    tf = yt.ColorTransferFunction(np.log10(bounds))
    tf.add_layers(5, w=0.0001, colormap='arbre',alpha=logspace(-0.1,0,12))
    source.tfh.tf = tf
    source.tfh.bounds = bounds
    source.tfh.plot('transfer_function.png', profile_field='density')

    cam = sc.add_camera()
    cam.switch_orientation((0.5,1.,1.))

    steps=15
    for x in arange(steps):
        cam.rotate(2*pi/steps,rot_vector=np.array([1.0, 0.0, 0.0]))
        sc.save('rendering'+'%d'%x+'.png', sigma_clip=2)

    with io.get_writer('animax.gif', mode='I', duration=0.2) as writer:
        for x in arange(steps):
            image=io.imread('rendering'+'%d'%x+'.png')
            writer.append_data(image)
    writer.close()

    system('mv *.png PNG')
