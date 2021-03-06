#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0111,C0326,C0103

import random
import sys
import tcllib

fc = tcllib.FotaCheck()
fc.cltp  = 10
fc.serid = "3531510"
#fc.osvs  = "7.1.1"

if len(sys.argv) == 3:  # python tclcheck.py $PRD $FV = OTA delta for $PRD from $FV
    fc.curef = sys.argv[1]
    fc.fv = sys.argv[2]
    fc.mode  = fc.MODE_OTA
elif len(sys.argv) == 2:  # python tclcheck.py $PRD = FULL for $PRD
    fc.curef = sys.argv[1]
    fc.fv = "AAA000"
    fc.mode = fc.MODE_FULL
    fc.cltp  = 2010
else:  # python tclcheck.py = OTA for default PRD, FV
    fc.curef = "PRD-63117-011"
    fc.fv    = "AAM481"
    fc.mode  = fc.MODE_OTA

check_xml = fc.do_check()
print(fc.pretty_xml(check_xml))
curef, fv, tv, fw_id, fileid, fn, fsize, fhash = fc.parse_check(check_xml)

req_xml = fc.do_request(curef, fv, tv, fw_id)
print(fc.pretty_xml(req_xml))
fileid, fileurl, slaves, encslaves = fc.parse_request(req_xml)

for s in slaves:
    print("http://{}{}".format(s, fileurl))

if fc.mode == fc.MODE_FULL:
    header = fc.do_encrypt_header(random.choice(encslaves), fileurl)
    if len(header) == 4194320:
        print("Header length check passed. Writing to header_{}.bin.".format(tv))
        with open("header_{}.bin".format(tv), "wb") as f:
            f.write(header)
    else:
        print("Header length invalid ({}).".format(len(header)))
