#-------------------------------------------------------------------------------
# Name:        initialise_mscnfr_plot.py
# Purpose:     initialision script
# Author:      Mike Martin
# Created:     31/07/2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

__prog__ = 'initialise_mscnfr_plot.py'
__version__ = '0.0.0'

# Version history
# ---------------
# 
from os import getenv, getcwd
from os.path import exists, normpath, join
from json import dump as json_dump, load as json_load
from sys import platform as _platform
from plot_utilities import check_csv_files

def initiation(form):
    """

    """
    if _platform == 'win32':
        if getenv('USERNAME') == 'mmartin':
            root_dir = 'C:\\'
        else:
            root_dir = 'E:\\'
    else:
        pass

    if getenv('USERNAME') == 'mmartin':
        root_dir = 'C:\\AbUniv\\'
        data_dir = 'C:\\'
    else:
        root_dir = 'E:\\'
        data_dir = 'H:\\'
    form.root_dir = root_dir
    form.data_dir = data_dir
    form.menuEntries = {}

    form.fpng = join(getcwd(), 'images', 'World_small.PNG')
    form.config_file = join(getcwd(), 'mscnfr_utils_config.txt')

    return

def read_config_file(form):
    """
    read names of files used in the previous programme session from the config file if it exists
    or create default using the current selections if config file does not exist
    """
    config_file = form.config_file
    if exists(config_file):
        try:
            with open(config_file, 'r') as fconfig:
                config = json_load(fconfig)
        except (OSError, IOError) as e:
                print(e)
                return False
    else:
        # stanza if config_file needs to be created
        _default_config = {
            'CsvDir': {
                 'ref_dir': getcwd()
            }
        }

        # if config file does not exist then create it...
        with open(config_file, 'w') as fconfig:
            json_dump(_default_config, fconfig, indent=2, sort_keys=True)
            config = _default_config

    grp = 'CsvDir'
    ref_dir = config[grp]['ref_dir']
    form.w_lbl04.setText(ref_dir)
    form.w_lbl05.setText(check_csv_files(form))

    return

def write_config_file(form):
    """

    """
    config_file = form.config_file
    config = {
        'CsvDir': {
            'ref_dir': normpath(form.w_lbl04.text())
            }
        }

    with open(config_file, 'w') as fconfig:
        json_dump(config, fconfig, indent=2, sort_keys=True)

    return
