#! /usr/bin/python
from numpy import *
from astropy import constants as con
from os import sys
sys.path.append('functions/')

def read_wave(header,lineFre=''):
    names=list(header.keys())
    NAXIS3=header['NAXIS3']
    CRVAL3=header['CRVAL3']
    CDELT3=header['CDELT3']
    CRPIX3=header['CRPIX3']
    if 'RESTFREQ' in names:
        RESTFREQ=header['RESTFREQ']
    elif 'RESTFRQ' in names:
        RESTFREQ=header['RESTFRQ']
    else:
        print('Error: check rest frequ')
    chan=arange(1,NAXIS3+1,1.)

    if header['CTYPE3']=='FREQ':
        freq_li=(chan-CRPIX3)*CDELT3+CRVAL3
        vel_li=-(freq_li-RESTFREQ)/RESTFREQ*con.c.to('km/s').value
    if header['CTYPE3']=='VRAD':
        vel_li=(chan-CRPIX3)*CDELT3+CRVAL3
        freq_li=RESTFREQ*(1-vel_li/con.c.to('m/s').value)

    if lineFre!='':
        vel_li=-(freq_li-lineFre)/lineFre*con.c.to('km/s').value
    return freq_li,chan,vel_li

def read_wcs_header(header):
    NAXIS1=header['NAXIS1']
    CRVAL1=header['CRVAL1']
    CDELT1=header['CDELT1']
    CRPIX1=header['CRPIX1']

    NAXIS2=header['NAXIS2']
    CRVAL2=header['CRVAL2']
    CDELT2=header['CDELT2']
    CRPIX2=header['CRPIX2']
    return NAXIS1, CRVAL1, CDELT1,CRPIX1,NAXIS2,CRVAL2,CDELT2,CRPIX2


def read_wcs_coord(header):
    NAXIS1, CRVAL1, CDELT1,CRPIX1,NAXIS2,CRVAL2,CDELT2,CRPIX2=read_wcs_header(header)

    bins_ra=arange(1,NAXIS1+1,1.)
    CDELT1=CDELT1/(cos(deg2rad(CRVAL2)))
    RA=(bins_ra-CRPIX1)*CDELT1+CRVAL1

    bins_dec=arange(1,NAXIS2+1,1.)
    Dec=(bins_dec-CRPIX2)*CDELT2+CRVAL2

    extent=[RA[0]+abs(CDELT1/2),RA[-1]-abs(CDELT1/2),Dec[0]-abs(CDELT2/2),Dec[-1]+abs(CDELT2/2)]
    return extent

def read_pv_coord(header):
    NAXIS1, CRVAL1, CDELT1,CRPIX1,NAXIS2,CRVAL2,CDELT2,CRPIX2=read_wcs_header(header)

    bins_ra=arange(1,NAXIS1+1,1.)
    RA=(bins_ra-CRPIX1)*CDELT1+CRVAL1

    names=list(header.keys())
    if 'RESTFREQ' in names:
        RESTFREQ=header['RESTFREQ']
    elif 'RESTFRQ' in names:
        RESTFREQ=header['RESTFRQ']
    else:
        print('Error: check rest frequ')
    lineFre=RESTFREQ
    bins_freq=arange(1,NAXIS2+1,1.)
    freq=(bins_freq-CRPIX2)*CDELT2+CRVAL2
    v=(lineFre-freq)/lineFre*con.c.to('km/s').value
    VDELT=average(v[1:]-v[:-1])

    extent=[RA[0]+abs(CDELT1/2),RA[-1]-abs(CDELT1/2),v[0]-abs(VDELT/2),v[-1]+abs(VDELT/2)]
    return extent


def read_wcs_coord2(header):
    NAXIS1, CRVAL1, CDELT1,CRPIX1,NAXIS2,CRVAL2,CDELT2,CRPIX2=read_wcs_header(header)

    bins_ra=arange(1,NAXIS1+1,1.)
    CDELT1=CDELT1/(cos(deg2rad(CRVAL2)))
    RA=(bins_ra-CRPIX1)*CDELT1+CRVAL1

    bins_dec=arange(1,NAXIS2+1,1.)
    Dec=(bins_dec-CRPIX2)*CDELT2+CRVAL2

    return RA,Dec

def read_wcs_coord3(header,precise=1):
    NAXIS1, CRVAL1, CDELT1,CRPIX1,NAXIS2,CRVAL2,CDELT2,CRPIX2=read_wcs_header(header)

    bins_ra=arange(1,NAXIS1+1,precise)
    CDELT1=CDELT1/(cos(deg2rad(CRVAL2)))
    RA=(bins_ra-CRPIX1)*CDELT1+CRVAL1

    bins_dec=arange(1,NAXIS2+1,precise)
    Dec=(bins_dec-CRPIX2)*CDELT2+CRVAL2

    return RA,Dec
