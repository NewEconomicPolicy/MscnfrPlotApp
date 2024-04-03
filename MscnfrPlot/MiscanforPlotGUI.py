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
from os import getenv

from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, \
                                    QComboBox, QRadioButton, QButtonGroup, QPushButton, QCheckBox, QFileDialog
from plot_utilities import check_csv_files, generate_png_files
from initialise_mscnfr_plot import initiation, read_config_file, write_config_file

sleepTime = 5

class Form(QWidget):
    """

    """
    def __init__(self, parent=None):
        """

        """
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

        w_resol = QLabel('')
        w_resol.setAlignment(Qt.AlignLeft)
        helpText = 'resolution is in arc minutes or seconds'
        w_resol.setToolTip(helpText)
        grid.addWidget(w_resol, 6, 1)
        self.w_resol = w_resol

        # user actions
        # ============
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
        """

        """
        path_env = getenv('PATH')
        for dir_name in sorted(path_env.split(';')):
            print(dir_name)
        return

    def fetchCsvDir(self):
        """
        We pop up the QtGui.QFileDialog. The first string in the getOpenFileName()
        method is the caption. The second string specifies the dialog working directory.
        By default, the file filter is set to All files (*)
        """
        fname = self.w_lbl04.text()
        fname = QFileDialog.getExistingDirectory(self, 'Select directory', fname)
        if fname != '':
            if fname != self.w_lbl04.text():
                # reread new ref dir
                self.w_lbl04.setText(fname)
                check_csv_files(self)

    def generatePNGsClicked(self):
        """

        """
        generate_png_files(self)

    def exitClicked(self):
        """
        write last path selections
        """
        write_config_file(self)

        self.close()

def main():
    """

    """
    if len(sys.argv) > 1:
        app = QApplication(sys.argv)  # create QApplication object
        form = Form()     # instantiate form
        form.show()       # paint form
        sys.exit(app.exec_())  # start event loop
    else:
        form = lambda: None     # create blank object
        form.batch_mode_flag = True
        generate_png_files(form)
        sleep(sleepTime)

if __name__ == '__main__':
    main()
