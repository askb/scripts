#!/bin/bash
#
# gdbline module image
#
# Outputs an add-symbol-file line suitable for pasting into gdb to examine
# a loaded module.
#
cd /sys/module/$1/sections
echo -n add-symbol-file $2 `/bin/cat .text`

for section in .[a-z]* *; do
   if [ $section != ".text" ]; then
       echo  " \\"
       echo -n "   -s" $section `/bin/cat $section`
   fi
done
echo
