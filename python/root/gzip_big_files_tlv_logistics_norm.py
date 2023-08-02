#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# gzip big data files for upload to cloud
#

import shutil
import os
from pathlib import Path

cwd = Path.cwd()
print('********** gzip big data files for upload to cloud *************')

gzip_dir = cwd.parent.parent / 'tlv_logistics_norm_web_app' / 'tlv_logistics'

print(gzip_dir)

os.chdir(gzip_dir)

tooldirfilelist = os.listdir(gzip_dir)
print(tooldirfilelist)

for filename in tooldirfilelist :
    print(filename)
    filepath = gzip_dir / filename
    filesize = os.path.getsize(filepath)
    print(filepath, filesize)
    if filename.endswith(".js") and filesize > 500000 :
        print('  ',filepath, filesize)
        os.system('gzip -9 -k -f ' + filepath.as_posix())

print(os.listdir(gzip_dir))

