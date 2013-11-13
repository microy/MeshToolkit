#!/bin/bash

#
# cleanup.sh
#
find . -type f -name *.pyc -exec rm {} \;
find . -type f -name *~ -exec rm {} \;
