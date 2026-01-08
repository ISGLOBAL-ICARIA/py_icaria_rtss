#!/usr/bin/env python

""" This script manages different RTSS related functions. Apart from a preliminary
estimation of the future RTSS doses administered to ICARIA participants, it also
contains a function to check the number of doses and the number of ICARIA participants
vaccinated with RTSS, giving a list of the number of ICARIA participants administered
with RTSS per dose per HF.
"""

import rtss
from datetime import datetime

__author__ = "Andreu Bofill"
__copyright__ = "Copyright 2024, ISGlobal Maternal, Child and Reproductive Health"
__credits__ = ["Andreu Bofill"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "20240418"
__maintainer__ = "Andreu Bofill"
__email__ = "andreu.bofill@isglobal.org"
__status__ = "Finished"

if __name__ == '__main__':
    """ ESTIMATION OF CHILD'S AFFECTED BY RTSS """
#    rtss.all_participants_grater_than()

    """ NUMBER OF PARTICIPANTS VACCINATED BY RTSS AND SUMMARY TOOL GENERATOR """
    rtss.rtss_counts()

    print(datetime.today().date())
