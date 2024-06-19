#-------------------------------------------------------------------------------
# Name:
# Purpose:     set of functions performing Miscanfor related tasks
# Author:      Mike Martin
# Created:     07/05/2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

__prog__ = 'plot_utilities.py'
__version__ = '0.0.1'
__author__ = 's03mm5'

from os import mkdir, getcwd
from os.path import isdir, isfile, normpath, join, split, splitext
from glob import glob

from plotting import plotting, read_mscnfr_csv_file

def generate_unique_list(list_inp):
    """
    function to get unique values
    """
    unique_list = []

    # traverse for all elements
    # ========================
    for val in list_inp:
        if val not in unique_list:
            unique_list.append(val)

    return unique_list

def generate_png_files(form):
    """

    """
    suptitle_dict = {}
    year_span = '1971-1972'
    suptitle_dict['DM'] = 'Dry matter ' + year_span + ' [t/ha/y]'
    suptitle_dict['DM_sd'] = 'Dry matter ' + year_span + ' standard deviation [t/ha/y]'
    suptitle_dict['DM_pm'] = 'Dry matter peak mass ' + year_span + ' [t/ha/y]'
    suptitle_dict['w_use'] = 'Water use per yield mass ' + year_span + ' [fraction]'
    suptitle_dict['N_loss'] = 'Nitrogen loss ' + year_span + ' [kg/ha/y]'
    suptitle_dict['K_loss'] = 'Potassium loss ' + year_span + ' [kg/ha/y]'
    suptitle_dict['P_loss'] = 'Posphorus loss ' + year_span + ' [kg/ha/y]'
    suptitle_dict['CI'] = 'Carbon intensity ' + year_span + ' [g C /MJ/y]'
    suptitle_dict['EUE'] = 'Energy use efficiency ' + year_span + ' [fraction]'
    suptitle_dict['LUEI'] = 'Land use energy intensity (net energy) ' + year_span + ' [GJ/ha/y]'
    suptitle_dict['LUEIg'] = 'Gross energy ' + year_span + ' [GJ/ha/y]'
    suptitle_dict['k_cold'] = 'Number of frost kills ' + year_span + ' [number/y]'
    suptitle_dict['k_dry'] = 'Number of drought kills ' + year_span + ' [number/y]'
    suptitle_dict['sp'] = 'Solar panel LUEI ' + year_span + ' [GJ/ha/y]'
    suptitle_dict['cost'] = 'Cost ' + year_span + ' [$/GJ]'
    suptitle_dict['sp_cost'] = 'Solar panel cost ' + year_span + ' [$/GJ]'

    suptitle_dict['Met_MeanYrT'] = 'MeanYrlyMeanTemp  ' + year_span + ' [deg C]'
    suptitle_dict['Met_MeanYrPrec'] = 'MeanYrlyTotalPrecip ' + year_span + ' [mm]'
    suptitle_dict['MiscCm'] = 'CO2 emitted-crop+process+transport ' + year_span + ' [t/ha/y]'
    suptitle_dict['LAImean'] = 'Max LAI at start of senescence  ' + year_span
    suptitle_dict['LAIdaymean'] = 'Day no. at start of senescence ' + year_span
    suptitle_dict['kill'] = 'Combined frost-drought cropkill ' + year_span
    suptitle_dict['CropCOPerFarmCO'] = 'Crop CO2 per farm+transport CO2 ' + year_span + ' [t/ha/y]'
    suptitle_dict['DMavglive'] = 'DM yield, mean for non-cropkill yrs ' + year_span + ' [t/ha]'
    suptitle_dict['SoilAWC'] = 'Soil Water Capacity, FC-PWP ' + year_span
    suptitle_dict['SoilC'] = 'Soil carbon change ' + year_span + ' [t/ha/y]'
    
    # make sure color scale directory exists
    # ======================================
    if form.batch_mode_flag:
        fdir = getcwd()
        check_csv_files(form)
    else:
        fdir = form.w_lbl04.text()

    fdir_cb = join(fdir,'color_scale')
    if not isdir(fdir_cb):
        try:
            mkdir(fdir_cb)
        except PermissionError as err:
            print(err)
            return

    # step through CSV files
    # =====================
    ncreated = 0
    ncolor_files = 0
    for csv_fname in form.csv_files:
        fdir, short_fname = split(csv_fname)

        if short_fname == 'totals.csv':
           continue

        metric_name, dummy = splitext(short_fname)
        if metric_name in suptitle_dict:
            suptitle = suptitle_dict[metric_name]
        else:
            suptitle = 'No title for ' + metric_name

        ncrt, nclr = plotting(metric_name, fdir, fdir_cb, suptitle)
        ncreated += ncrt
        ncolor_files += nclr

    print('\nEnd of processing - created {} PNG files in: {}\n\tand {} color scales in: {}'
                                                                .format(ncreated, fdir, ncolor_files, fdir_cb))
    return

def check_csv_files(form):
    """

    """
    batch_mode_flag = form.batch_mode_flag
    if batch_mode_flag:
        csvs_dir = getcwd()
    else:
        csvs_dir = form.w_lbl04.text()

    csv_files = []
    for fname in glob(csvs_dir + '/*.csv'):
        fname = normpath(fname)
        if isfile(fname):
            csv_files.append(fname)

    ncsv_fns = len(csv_files)
    line_mess = '{} CSV files\t'.format(ncsv_fns)
    resol_mess = ''
    if ncsv_fns > 0:
        ret_code = read_mscnfr_csv_file(csv_files[0], quick_read = True)
        if ret_code is not None:
            nvals, resol_mess = ret_code
            fdir, short_fname = split(csv_files[0])
            line_mess += ' # of lines in first file {}: {:,}'.format(short_fname, nvals)

    if batch_mode_flag:
        print(line_mess + '\t\tResolution: ' + resol_mess)
    else:
        form.w_lbl05.setText(line_mess)
        form.w_resol.setText(resol_mess)
        if ncsv_fns > 0:
            form.w_png_gen.setEnabled(True)
        else:
            form.w_png_gen.setEnabled(False)

    form.csv_files = csv_files

    return
