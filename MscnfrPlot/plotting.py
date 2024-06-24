# -------------------------------------------------------------------------------
# Name:        plotting.py
# Purpose:     script to create a map based on a regular angular grid
# @author: Mark Richards, University of Aberdeen, modified by Mark Pogson, homolgated by Mike Martin
# Created:     05/10/2010
# Licence:     <your licence>
# -------------------------------------------------------------------------------
# -*- coding:utf-8 -*-

from os.path import join
import csv
from numpy import asarray, diff

import matplotlib
matplotlib.use('Agg')
from matplotlib.pylab import nan, array, np
import matplotlib.pyplot as pyplot

MSCNFR_DFLT = 10000.0000000
OSGB_THRSHLD = 100

def _calc_scale_factor(ycoords, xcoords):
    """
    crucially,
    """
    ycrds_set = sorted(set(ycoords))     # creates list
    arr = asarray(ycrds_set)
    diff_a = diff(arr)
    y_incr = diff_a.min()

    xcrds_set = sorted(set(xcoords))    # creates list
    arr = asarray(xcrds_set)
    diff_a = diff(arr)
    x_incr = diff_a.min()

    # determine whether inputs are lat/longs or OSGB
    # ==============================================
    if x_incr < OSGB_THRSHLD and y_incr < OSGB_THRSHLD:

        ndivs_y = round(1.0/y_incr)
        ndivs_x = round(1.0/x_incr)

        #
        narc_mins = 60/ndivs_x
        if narc_mins >= 1:
            resol_mess = '{} arc minutes'.format(round(narc_mins))
        else:
            narc_secs = narc_mins * 60
            resol_mess = '{} arc seconds'.format(round(narc_secs))

        lat_long_flag = True
    else:
        resol_mess = 'OSGB Y/X increment: {} '.format(y_incr, x_incr)
        lat_long_flag = False

    return lat_long_flag, y_incr, x_incr, resol_mess

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

        del (data[-2:])  # delete last two lines

        # create lists from data
        # ======================
        xcoords = [float(row[1]) for row in data]
        ycoords = [float(row[2]) for row in data]
        lat_long_flag, y_incr, x_incr, resol_mess = _calc_scale_factor(ycoords, xcoords)

        if quick_read:
            return len(data), resol_mess

    vals = [float(row[0]) for row in data]

    return lat_long_flag, y_incr, x_incr, vals, ycoords, xcoords

def plotting(metric, fdir, fdir_cb, suptitle):
    """
    use matplotlib plotting library to do plotting
    """
    fname_csv = join(fdir, metric + '.csv')
    fname_png = join(fdir, metric + '.png')
    plot_flag = False
    png_fname = join(fdir_cb, 'cb' + metric + '.png')
    color_scale_flag = False

    ret_code = read_mscnfr_csv_file(fname_csv)
    if ret_code is None:
        return plot_flag, color_scale_flag

    lat_long_flag, y_incr, x_incr, vals, ycoords, xcoords = ret_code

    # Find max and min of the long lat axes
    # =====================================
    print('\nGenerating plot ' + fname_png)
    xmin = min(xcoords)
    ymin = min(ycoords)
    nxlen = 1 + int(round((max(xcoords) - xmin) / x_incr))
    nylen = 1 + int(round((max(ycoords) - ymin) / y_incr))

    z_mn = min(vals)

    # temporarily adjust values to get maximum
    # ========================================
    for ic, val in enumerate(vals):
        if val == MSCNFR_DFLT:
            vals[ic] = -MSCNFR_DFLT
    z_mx = max(vals)

    for ic, val in enumerate(vals):
        if val == -MSCNFR_DFLT:
            vals[ic] = MSCNFR_DFLT

    # build list then convert to an array
    # ===================================
    arr = [[nan for i in range(nxlen)] for j in range(nylen)]
    for i in range(len(vals)):
        # Work out array indices from long/lat
        # ====================================
        iy = int(round((xcoords[i] - xmin) / x_incr))
        ix = int(round((ycoords[i] - ymin) / y_incr))
        arr[ix][iy] = vals[i]
    img_arry = array(arr)

    fhand = open(fname_png, 'wb')
    fig = pyplot.figure()  # create figure
    fig.clf()  # clear figure
    ax = fig.add_subplot(1, 1, 1)  # add an Axes to the figure as part of a subplot arrangement
    ax.set_axis_off()
    mask_a = np.ma.array(img_arry, mask=np.isnan(img_arry))  # Create masked array
    cm = matplotlib.cm.jet_r
    cm.set_over('0.75')  # set color to be used for high out-of-range values
    im = ax.imshow(mask_a, origin='lower', interpolation='nearest', cmap=cm, vmax=z_mx)
    cb = pyplot.colorbar(im, shrink=0.5)  # fraction by which to multiply the size of the colorbar
    fig.suptitle(suptitle, fontsize=12)
    try:
        fig.savefig(fhand, format='png', dpi=500)
        plot_flag = True
    except:
        pass
    fig.clf()
    pyplot.close()
    fhand.close()

    # user feedback
    # =============
    mess = 'Generated plot ' + fname_png + '\n\t\twith '
    if lat_long_flag:
        mess += '{} latitudes and {} longitudes'.format(nylen, nxlen)
    else:
        mess += '{} northings and {} X eastings'.format(nylen, nxlen)

    print(mess + '\tZ axis extent: {} to {}'.format(z_mn, z_mx))

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
    cm = matplotlib.cm.jet_r
    im = ax.imshow(b, origin='lower', cmap=cm)
    ax.set_yticks([0, 24, 49, 74, 99])
    zincr = (z_mx - z_mn) / 4
    ax.set_yticklabels([round(z_mn, 3), round(z_mn + zincr, 3), round(z_mn + 2 * zincr, 3), round(z_mn + 3 * zincr, 3),
                        round(z_mx, 3)])
    ax.set_ybound(lower=0, upper=99)
    ax.set_xticks([])
    ax.set_xbound(lower=0, upper=4)
    ax.yaxis.set_ticks_position('right')
    try:
        fig.savefig(fh, format='png', dpi=55, bbox_inches='tight', facecolor='w', edgecolor='k')
        color_scale_flag = True
    except:
        pass
    fig.clf()
    pyplot.close()

    return plot_flag, color_scale_flag