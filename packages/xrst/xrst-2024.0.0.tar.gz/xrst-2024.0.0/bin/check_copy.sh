#! /usr/bin/env bash
set -e -u
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2023 Bradley M. Bell
# ----------------------------------------------------------------------------
if [ $# != 0 ]
then
   echo 'bin/check_copy.sh does not expect any arguments'
   exit 1
fi
if [ "$0" != 'bin/check_copy.sh' ]
then
   echo 'bin/check_copy.sh: must be executed from its parent directory'
   exit 1
fi
if [ ! -e './.git' ]
then
   echo 'bin/check_copy.sh: cannot find ./.git'
   exit 1
fi
# ---------------------------------------------------------------------------
ignore_list='
   .gitignore
   .readthedocs.yaml
   readme.md
   gpl-3.0.txt
   bin/input_files.sh
   python-xrst.spec
'
license='SPDX-License-Identifier: GPL-3.0-or-later'
missing='no'
for file_name in $(git ls-files | sed -e '/^test_rst\//d')
do
   if ! echo "$ignore_list" | tr '\n' ' ' | grep " $file_name " > /dev/null
   then
      if ! grep "$license\$" $file_name > /dev/null
      then
         if [ "$missing" == 'no' ]
         then
            echo "Cannotfind line that ends with:"
            echo "   $license"
            echo "In the following files:"
         fi
         echo "$file_name"
         missing='yes'
      fi
   fi
done
#
if [ "$missing" = 'yes' ]
then
   echo 'bin/check_copy.sh: See copyright errors above'
   exit 1
fi
echo 'bin/check_copy.sh: OK'
exit 0
