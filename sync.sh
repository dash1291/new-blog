#!/bin/sh
python build.py '/newblog' && rsync -avz --delete site/ /opt/lampp/htdocs/newblog/

