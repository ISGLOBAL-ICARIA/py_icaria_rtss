#!/usr/bin/env python
""" Python script to manage generate reports in the ICARIA Clinical Trial."""

import rtss

__author__ = "Andreu Bofill"
__copyright__ = "Copyright 2024, ISGlobal Maternal, Child and Reproductive Health"
__credits__ = ["Andreu Bofill"]
__license__ = "MIT"
__version__ = "0.0.1"
__date__ = "20240418"
__maintainer__ = "Andreu Bofill"
__email__ = "andreu.bofill@isglobal.org"
__status__ = "Dev"


if __name__ == '__main__':
    # ESTIMATION OF CHILD'S AFFECTED BY RTSS
    #rtss.all_participants_grater_than()

    # NUMBER OF PARTICIPANTS VACCINATED BY RTSS AND SUMMARY TOOL GEERATOR
    rtss.rtss_counts()
