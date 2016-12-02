# -*- coding: utf-8 -*-
from pisces.main import main
import codecs
import datetime
import os
os.environ["LANG"] = "en_US.UTF-8"

if __name__ == '__main__':
    # image search keyword: kitchen fire
	name_test = u'glasses'
	basetime_test = datetime.datetime(2009, 1, 1)
	endtime_test = datetime.datetime(2016, 6, 1)
	day_delta_test = 5
	last_end_test = 1

	main(name_test, basetime_test, endtime_test, day_delta_test, last_end_test, close=True)
    # similar to the below:
    # main(url, output_dir)
