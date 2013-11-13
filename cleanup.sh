#!/bin/bash

#
# cleanup.sh
#
find . -type f -name *.pyc -exec rm -v {} \;
find . -type f -name *~ -exec rm -v {} \;
