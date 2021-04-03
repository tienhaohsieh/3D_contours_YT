#! /usr/bin/python
from numpy import *
from header import *

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
    def v_idx(self):
        return [argmin(abs(self.vel_li-self.vel_lim[0])),argmin(abs(self.vel_li-self.vel_lim[1]))]
    def ra_idx(self):
        return [argmin(abs(self.ra_li-self.ra_lim[0])),argmin(abs(self.ra_li-self.ra_lim[1]))][::-1]
    def dec_idx(self):
        return [argmin(abs(self.dec_li-self.dec_lim[0])),argmin(abs(self.dec_li-self.dec_lim[1]))]
    def trimed_data(self):
        return self.arr[self.v_idx()[0]:self.v_idx()[1],self.dec_idx()[0]:self.dec_idx()[1],self.ra_idx()[0]:self.ra_idx()[1]]
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

