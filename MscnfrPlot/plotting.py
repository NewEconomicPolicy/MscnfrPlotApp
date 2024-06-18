# -------------------------------------------------------------------------------
# Name:        plotting.py
# Purpose:     script to create a map based on a regular angular grid
# @author: Mark Richards, University of Aberdeen, modified by Mark Pogson, homolgated by Mike Martin
# Created:     05/10/2010
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# -*- coding:utf-8 -*-

import csv
import matplotlib
matplotlib.use('Agg')
from matplotlib.pylab import nan, array, np
import matplotlib.pyplot as pyplot
from os.path import join

def plotting(metric, fdir, fdir_cb, suptitle):
    """
    use matplotlib plotting library to do plotting
    """
    fname = join(fdir, metric + '.csv')
    fname_png = join(fdir, metric +'.png')
    plot_flag = False
    png_fname = join(fdir_cb,'cb' + metric + '.png')
    color_scale_flag = False

    ret_code = read_mscnfr_csv_file(fname)
    if ret_code is None:
        return plot_flag, color_scale_flag

    scale_factor, vals, lats, longs = ret_code

    # Find max and min of the long lat axes
    # =====================================
    print('\nGenerating plot ' + fname_png)
    longmin = min(longs)
    latmin = min(lats)
    longlen = 1+int(round((max(longs) - longmin) / scale_factor))
    latlen = 1+int(round((max(lats) - latmin) / scale_factor))

    z_mn = min(vals)

    # temporarily adjust values to get maximum
    # ========================================
    for ic, val in enumerate(vals):
        if val ==   10000.0000000: vals[ic] = -10000.0000000
    z_mx = max(vals)
   
    for ic, val in enumerate(vals):
        if val == -10000.0000000: vals[ic] = 10000.0000000

    # build list then convert to an array
    # ===================================
    arr = [[nan for i in range(longlen)] for j in range(latlen)]
    for i in range(len(vals)):
        # Work out array indices from long/lat
        # ====================================
        iy = int(round((longs[i] - longmin)/scale_factor))
        ix = int(round((lats[i]  - latmin)/scale_factor))
        arr[ix][iy] = vals[i]
    a = array(arr)

    fhand = open(fname_png, 'wb')
    fig = pyplot.figure()  	# create figure
    fig.clf()				# clear figure
    ax = fig.add_subplot(1, 1, 1)   # add an Axes to the figure as part of a subplot arrangement
    ax.set_axis_off()
    mask_a = np.ma.array(a, mask = np.isnan(a))     #  Create masked array
    cm = matplotlib.cm.jet
    cm.set_over('0.75')         # set color to be used for high out-of-range values
    im = ax.imshow(mask_a, origin = 'lower', interpolation = 'nearest', cmap = cm, vmax = z_mx)
    cb = pyplot.colorbar(im,shrink = 0.5)		# fraction by which to multiply the size of the colorbar
    fig.suptitle(suptitle, fontsize=12)
    try:
        fig.savefig(fhand, format='png', dpi=500)
        plot_flag = True
    except:
        pass
    fig.clf()
    pyplot.close()
    fhand.close()
    print('Generated plot {} with {} latitudes and {} longitudes\tzmin {}\tzmax: {}'
                                                            .format(fname_png, latlen, longlen, z_mn, z_mx))
    # create color scales
    # ===================    
    fh = open(png_fname, 'wb')
    fig = pyplot.figure()
    fig.clf()
    ax = fig.add_subplot(1, 1, 1)

    b = [[0 for i in range(5)] for j in range(100)]
    for i in range(100):
        b[i][0] = i
        b[i][1] = i
        b[i][2] = i
        b[i][3] = i
        b[i][4] = i
    b = array(b)
    cm = matplotlib.cm.jet
    im = ax.imshow(b, origin='lower',cmap=cm)
    ax.set_yticks([0, 24, 49, 74, 99])
    zincr = (z_mx - z_mn)/4
    ax.set_yticklabels([round(z_mn,3), round(z_mn + zincr, 3), round(z_mn + 2*zincr, 3), round(z_mn + 3*zincr, 3),
                                                                                                    round(z_mx, 3)])
    ax.set_ybound(lower=0,upper=99)
    ax.set_xticks([])
    ax.set_xbound(lower=0,upper=4)
    ax.yaxis.set_ticks_position('right')
    try:
        fig.savefig(fh, format='png', dpi = 55, bbox_inches = 'tight', facecolor = 'w', edgecolor = 'k')
        color_scale_flag = True
    except:
        pass
    fig.clf()
    pyplot.close()
    
    return plot_flag, color_scale_flag

def read_mscnfr_csv_file(fname, quick_read = False):
    """

    """
    print('Reading file: ' + fname)
    with open(fname, 'r') as fhand:
        reader = csv.reader(fhand, delimiter=',', skipinitialspace=True)
        data = []
        data.extend(reader)
        if len(data) == 0:
             return None

        del (data[-2:])  # delete last two elements

        # create lists from data
        # ======================
        longs = [float(row[1]) for row in data]
        lats = [float(row[2]) for row in data]
        scale_factor, resol_mess = _calc_scale_factor(lats, longs)

        if quick_read:
            return len(data), resol_mess

    vals = [float(row[0]) for row in data]

    return scale_factor, vals, lats, longs

def _calc_scale_factor(lats, longs):
    """
    somewhat overwritten
    """
    from numpy import asarray, diff

    lat_set = sorted(set(lats))     # creates list
    arr = asarray(lat_set)
    diff_a = diff(arr)
    scale_factor_lat = diff_a.min()

    ndivs_lats = round(1.0/scale_factor_lat)
    scale_factor = 1 / ndivs_lats

    lon_set = sorted(set(longs))    # creates list
    arr = asarray(lon_set)
    diff_a = diff(arr)
    scale_factor_lon = diff_a.min()

    ndivs_lons = round(1.0 / scale_factor_lon)

    scale_factor = 1/ndivs_lons

    #
    narc_mins = 60/ndivs_lons
    if narc_mins >= 1:
        resol_mess = '{} arc minutes'.format(round(narc_mins))
    else:
        narc_secs = narc_mins * 60
        resol_mess = '{} arc seconds'.format(round(narc_secs))

    return scale_factor, resol_mess
