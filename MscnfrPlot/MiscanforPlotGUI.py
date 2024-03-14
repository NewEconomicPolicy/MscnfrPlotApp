#-------------------------------------------------------------------------------
# Name:
# Purpose:     GUI front end to enable checking of Fortran modules
# Author:      Mike Martin
# Created:     25/7/2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Creates an Excel file consisting of redundant subroutines

__prog__ = 'DelSimsGUI.py'
__version__ = '0.0.1'
__author__ = 's03mm5'

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, \
                                    QComboBox, QRadioButton, QButtonGroup, QPushButton, QCheckBox, QFileDialog
from plot_utilities import check_csv_files, generate_png_files
from initialise_mscnfr_plot import initiation, read_config_file, write_config_file
import os

class Form(QWidget):

    def __init__(self, parent=None):

        super(Form, self).__init__(parent)

        initiation(self)
        # define two vertical boxes, in LH vertical box put the painter and in RH put the grid
        # define horizon box to put LH and RH vertical boxes in
        hbox = QHBoxLayout()
        hbox.setSpacing(10)

        # left hand vertical box consists of png image
        # ============================================
        lh_vbox = QVBoxLayout()

        # LH vertical box contains image only
        lbl20 = QLabel()
        pixmap = QPixmap(self.fpng)
        lbl20.setPixmap(pixmap)

        # add LH vertical box to horizontal box
        # =====================================
        lh_vbox.addWidget(lbl20)
        hbox.addLayout(lh_vbox)

        # right hand box consists of combo boxes, labels and buttons
        # ==========================================================
        rh_vbox = QVBoxLayout()

        # The layout is done with the QGridLayout
        grid = QGridLayout()
        grid.setSpacing(10)	# set spacing between widgets

        # line 4 - option to use CSV file of coords
        # =========================================
        w_csv_dir = QPushButton("CSVs path")
        grid.addWidget(w_csv_dir, 4, 0)
        w_csv_dir.clicked.connect(self.fetchCsvDir)

        w_lbl04 = QLabel()
        grid.addWidget(w_lbl04, 4, 1, 1, 5)
        self.w_lbl04 = w_lbl04

        w_lbl05 = QLabel('')
        grid.addWidget(w_lbl05, 5, 1, 1, 5)
        self.w_lbl05 = w_lbl05

        # line 6
        # ======
        lbl06 = QLabel('Resolution:')
        lbl06.setAlignment(Qt.AlignRight)
        grid.addWidget(lbl06, 6, 0)

        w_low_res = QRadioButton("low")
        helpText = 'If this option is selected, then a scale_factor of .0833333, equivalent to 5 arc minutes, is applied'
        w_low_res.setToolTip(helpText)
        grid.addWidget(w_low_res, 6, 1)

        w_high_res = QRadioButton("high")
        helpText = 'If this option is selected, then a scale_factor of .00833333, equivalent to 5 arc seconds, is applied'
        w_high_res.setToolTip(helpText)
        grid.addWidget(w_high_res, 6, 2)

        w_option_choice = QButtonGroup()
        w_option_choice.addButton(w_low_res)
        w_option_choice.addButton(w_high_res)
        w_low_res.setChecked(True)

        # assign check values to radio buttons
        w_option_choice.setId(w_high_res, 2)
        w_option_choice.setId(w_low_res, 1)

        self.w_low_res  = w_low_res
        self.w_high_res = w_high_res
        self.w_option_choice = w_option_choice

        # line 19
        # =======
        w_png_gen = QPushButton("Generate PNGs")
        helpText = 'Generate PNGs from CSV files'
        w_png_gen.setToolTip(helpText)
        w_png_gen.clicked.connect(self.generatePNGsClicked)
        self.w_png_gen = w_png_gen
        grid.addWidget(w_png_gen, 19, 0)

        w_list_path = QPushButton("List paths")
        helpText = 'set of directories where executable programs are located making up the PATH environment variable'
        w_list_path.setToolTip(helpText)
        w_list_path.clicked.connect(self.listPathsClicked)
        grid.addWidget(w_list_path, 19, 4)

        exit = QPushButton("Exit", self)
        grid.addWidget(exit, 19, 5, 1, 2)
        exit.clicked.connect(self.exitClicked)

        # add grid to RH vertical box
        rh_vbox.addLayout(grid)

        # vertical box goes into horizontal box
        hbox.addLayout(rh_vbox)

        # the horizontal box fits inside the window
        self.setLayout(hbox)

        # posx, posy, width, height
        self.setGeometry(300, 300, 300, 250)
        self.setWindowTitle('generate PNG files from Miscanfor CSVs')

        # reads and set values from last run
        # ==================================
        read_config_file(self)


    def listPathsClicked(self):

        path_env = os.getenv('PATH')
        for dir_name in sorted(path_env.split(';')):
            print(dir_name)
        return

    def fetchCsvDir(self):

        # We pop up the QtGui.QFileDialog. The first string in the getOpenFileName()
        # method is the caption. The second string specifies the dialog working directory.
        # By default, the file filter is set to All files (*)
        fname = self.w_lbl04.text()
        fname = QFileDialog.getExistingDirectory(self, 'Select directory', fname)
        if fname != self.w_lbl04.text():
            # reread new ref dir
            self.w_lbl04.setText(fname)
            self.w_lbl05.setText(check_csv_files(self))

    def generatePNGsClicked(self):

         generate_png_files(self)

    def exitClicked(self):

        # write last path selections
        write_config_file(self)

        self.close()

def main():

    app = QApplication(sys.argv)  # create QApplication object
    form = Form()     # instantiate form
    form.show()       # paint form
    sys.exit(app.exec_())   # start event loop

if __name__ == '__main__':
    main()
