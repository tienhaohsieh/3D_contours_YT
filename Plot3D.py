#! bin/python
from numpy import *
from astropy.io import fits as pyfits
from glob import glob
from os import sys,system
sys.path.append('../../../../BandSpwLines/')
from Noise import *
from header import *
from pylab import *
from yt.visualization.volume_rendering.api import Scene, VolumeSource
import yt
import imageio as io

mol='DCN'

#fits_path='../../../../Maps/Channel_maps_robust/'+mol+'/'
fits_path='../../../../Maps/Channel_maps/'+mol+'/'
im_li=glob(fits_path+'*K.fits')
noi_chan_li=loadtxt(fits_path+'Noise_table',dtype=str)

class Zoom():
    def __init__(self,arr,header=''):
        """
        Put the ra, dec, and velocity range to your map.
        """
        self.ra_lim=[52.2649087,52.2663600]
        self.dec_lim=[31.2670571,31.2683054]
        self.vel_lim=[7,10]

        self.arr=arr
        self.header=header
        self.vel_li=read_wave(self.header)[2]
        self.ra_li,self.dec_li=read_wcs_coord2(self.header)

        self.v_idx=[argmin(abs(self.vel_li-self.vel_lim[0])),argmin(abs(self.vel_li-self.vel_lim[1]))][::-1]
        self.ra_idx=[argmin(abs(self.ra_li-self.ra_lim[0])),argmin(abs(self.ra_li-self.ra_lim[1]))][::-1]
        self.dec_idx=[argmin(abs(self.dec_li-self.dec_lim[0])),argmin(abs(self.dec_li-self.dec_lim[1]))]

        self.trimed_data=self.arr[self.v_idx[0]:self.v_idx[1],self.dec_idx[0]:self.dec_idx[1],self.ra_idx[0]:self.ra_idx[1]]
    def bound(self,li,idx_li):
        idx_st=idx_li[0]
        idx_end=idx_li[1]
        out=[ average(li[idx_st-1:idx_st+1]),average(li[idx_end:idx_end+2]) ]
        return out
    def b_v(self):
        out=self.bound(self.vel_li,self.v_idx)
        return out
    def b_ra(self):
        out=self.bound(self.ra_li,self.ra_idx)
        return out
    def b_dec(self):
        out=self.bound(self.dec_li,self.dec_idx)
        return out

peak=[226,224]
sig2FWHM=2*(2*log(2.))**0.5
for im in im_li:
    fits_name=im.split('/')[-1]
    print(fits_name)
    fits=pyfits.open(fits_path+fits_name)
    data=fits[0].data
    header=fits[0].header
    noi_chan=float(noi_chan_li[noi_chan_li[:,0]==fits_name][0][1])


    zoom_data=Zoom(data,header)
    data=dict(density = (zoom_data.trimed_data, "g/cm**3"))
    print(zoom_data.b_v(),zoom_data.b_ra(),zoom_data.b_dec())
    system('rm -rf *.png')
#    bbox = np.array([zoom_data.b_v(), zoom_data.b_dec(), zoom_data.b_ra()])
    bbox = np.array([[-1.5,1.5],[-1.5,1.5],[-1.5,1.5]])
    ds = yt.load_uniform_grid(data, zoom_data.trimed_data.shape,length_unit="Mpc", bbox=bbox)

    sc = yt.create_scene(ds, lens_type='perspective')
    sc.annotate_axes(alpha=0.1)

    source = sc[0]
    source.set_field('density')
    source.set_log(True)
    bounds=(0.15,0.68)
    tf = yt.ColorTransferFunction(np.log10(bounds))
    tf.add_layers(8, w=0.0001, colormap='cool',alpha=logspace(-0.1,0,12))
    source.tfh.tf = tf
    source.tfh.bounds = bounds
    source.tfh.plot('transfer_function.png', profile_field='density')

    cam = sc.add_camera()
    cam.switch_orientation((0.5,1.,1.))

    steps=5
    for x in arange(steps):
        cam.rotate(2*pi/steps,rot_vector=np.array([1.0, 0.0, 0.0]))
        sc.save('rendering'+'%d'%x+'.png', sigma_clip=2)

    with io.get_writer('animax.gif', mode='I', duration=0.2) as writer:
        for x in arange(steps):
            image=io.imread('rendering'+'%d'%x+'.png')
            writer.append_data(image)
    writer.close()

#    sc = Scene()
#    vol = VolumeSource(ds.all_data(), "density")
#    sc.add_source(vol)
#    cam = sc.add_camera(ds, lens_type="perspective")
#    im = sc.render()
#    sc.save('test.png',sigma_clip=3.0)
