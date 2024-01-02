#! /usr/bin/env bash
set -e -u
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# -----------------------------------------------------------------------------
if [ $# != 0 ]
then
   echo 'bin/check_version.sh: does not expect any arguments'
   exit 1
fi
if [ "$0" != 'bin/check_version.sh' ]
then
   echo 'bin/check_version.sh: must be executed from its parent directory'
   exit 1
fi
if [ ! -e './.git' ]
then
   echo 'bin/check_version.sh: cannot find ./.git'
   exit 1
fi
# -----------------------------------------------------------------------------
#
# version
version=$(
   sed -n -e '/^ *version *=/p' pyproject.toml | \
      sed -e 's|.*= *||' -e "s|'||g"
)
if echo $version | grep '[0-9]\{4\}[.]0[.][0-9]*' > /dev/null
then
   response=''
   while [ "$response" != 'yes' ] && [ "$response" != 'no' ]
   do
      read -p \
      "In pyporject.toml version=$version. Use this version [yes/no] " response
   done
   if [ "$response" == 'no' ]
   then
      version=$(date +%Y.%m.%d | sed -e 's|\.0*|.|g')
   fi
else
   version=$(date +%Y.%m.%d | sed -e 's|\.0*|.|g')
fi
#
# version_ok
version_ok='yes'
#
# check_version
check_version() {
   sed "$1" -f temp.sed > temp.out
   if ! diff "$1" temp.out > /dev/null
   then
      version_ok='no'
      #
      if [ -x "$1" ]
      then
         mv temp.out "$1"
         chmod +x "$1"
      else
         mv temp.out "$1"
      fi
      echo_eval git diff "$1"
   fi
}
#
# version_files
version_files='
   pyproject.toml
   setup.py
   test_rst/user-guide.rst
   user/user.xrst
   xrst/run_xrst.py
'
#
# temp.sed
cat << EOF > temp.sed
#
# xrst/user.xrst
s|^xrst-[0-9]\\{4\\}[.][0-9]*[.][0-9]*|xrst-$version|
#
# pyproject.toml setup.py and xrst/run_xrst.py
s|version\\( *\\)= *'[0-9]\\{4\\}[.][0-9]*[.][0-9]*'|version\\1= '$version'|
EOF
#
# check_version
for file in $version_files
do
   check_version $file
done
#
# ----------------------------------------------------------------------------
if [ "$version_ok" == 'no' ]
then
   echo 'bin/check_version.sh: version numbers were fixed (see above).'
   echo "Re-execute bin/check_version.sh $version ?"
   exit 1
fi
echo 'check_version.sh OK'
exit 0
