#! /usr/bin/env bash
set -e -u
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# -----------------------------------------------------------------------------
year='2024' # Year for this stable version 
release='0' # first release for each year starts with 0
# -----------------------------------------------------------------------------
if [ $# != 0 ]
then
   echo 'bin/new_release.sh does not expect any arguments'
   exit 1
fi
if [ "$0" != 'bin/new_release.sh' ]
then
   echo 'bin/new_release.sh: must be executed from its parent directory'
   exit 1
fi
if [ ! -e './.git' ]
then
   echo 'bin/new_release.sh: cannot find ./.git'
   exit 1
fi
# -----------------------------------------------------------------------------
# master
# -----------------------------------------------------------------------------
#
# branch
branch=$(git branch --show-current)
if [ "$branch" != 'master' ]
then
   echo 'bin/new_release.sh: must start execution using master branch'
   exit 1
fi
#
# tag
tag=$year.0.$release
if git tag --list | grep "$tag" > /dev/null
then
   echo "The tag $tag already exists"
   echo 'Use the follow commands to delete it ?'
   echo "   git tag -d $tag"
   echo "   git push -delete origin $tag"
   exit 1
fi
#
# pyproject.toml
sed -i pyproject.toml \
-e "s|version\\( *\\)= *'[0-9]\\{4\\}[.][0-9]*[.][0-9]*'|version\\1= '$tag'|"
version=$(
   sed -n -e '/^ *version *=/p' pyproject.toml | \
      sed -e 's|^ *version *= *||' -e "s|'||g"
)
if [ "$version" != "$tag" ]
then
   echo "bin/rew_release: branch = master."
   echo "Version number should be $tag in pyproject.toml"
   exit 1
fi
#
# check_version
# check_version.sh will use pyproject.toml version becasue it has 0 the form
# year.0.release.
bin/check_version.sh
#
# git_status
git_status=$(git status --porcelain)
if [ "$git_status" != '' ]
then
   echo 'bin/new_release: git staus --porcelean is not empty for master branch'
   echo 'use bin/git_commit.sh to commit its changes'
   exit 1
fi
# ----------------------------------------------------------------------------
# stable branch
# ----------------------------------------------------------------------------
#
# stable_branch
stable_branch=stable/$year
if ! git checkout $stable_branch
then
   echo "branch $stable_branch does not exist. Using following to create it ?"
   echo "   git branch $stable_branch"
   exit 1
fi
#
# version
version=$(
   sed -n -e '/^ *version *=/p' pyproject.toml | \
      sed -e 's|^ *version *= *||' -e "s|'||g"
)
if [ "$version" != "$tag" ]
then
   echo "bin/rew_release: branch = $stable_branch."
   echo "Version number should be $tag in pyproject.toml"
   exit 1
fi
#
# check_all
bin/check_all.sh
#
# stable_local_hash
pattern=$(echo " *refs/heads/$stable_branch" | sed -e 's|/|[/]|g')
stable_local_hash=$(
   git show-ref $stable_branch | \
      sed -n -e "/$pattern/p" | \
         sed -e "s|$pattern||"
) 
#
# stable_remote_hash
pattern=$(echo " *refs/remotes/origin/$stable_branch" | sed -e 's|/|[/]|g')
stable_remote_hash=$(
   git show-ref $stable_branch | \
      sed -n -e "/$pattern/p" | \
         sed -e "s|$pattern||"
) 
#
if [ "$stable_local_hash" == '' ] && [ "$stable_remote_hash" == '' ]
then
   empty_hash='yes'
   echo "bin/new_release: local $stable_branch does not exist."
   echo 'Use the following to create it ?'
   echo "   git checkout -b $stable_branch master"
   exit 1
fi
if [ "$stable_local_hash" == '' ] && [ "$stable_remote_hash" != '' ]
then
   empty_hash='yes'
   echo "bin/new_release: local $stable_branch does not exist."
   echo 'Use the following to create it ?'
   echo "   git checkout -b $stable_branch origin/$stable_branch"
   exit 1
fi
if [ "$stable_remote_hash" == '' ]
then
   empty_hash='yes'
   echo "bin/new_release: remote $stable_branch does not exist."
   echo 'Use the following to create it ?'
   echo "   git push origin $stable_branch"
   exit 1
fi
if [ "$stable_local_hash" == "$stable_remote_hash" ]
then
   empty_hash='yes'
   echo "bin/new_release: locan and remote $stable_branch differ."
   echo "local  $stable_local_hash"
   echo "remote $stable_remote_hash"
   echo 'try git push ?'
   exit 1
fi
#
# master_local_hash
pattern=$(echo " *refs/heads/master" | sed -e 's|/|[/]|g')
master_local_hash=$(
   git show-ref master | \
      sed -n -e "/$pattern/p" | \
         sed -e "s|$pattern||"
) 
#
# master_remote_hash
pattern=$(echo " *refs/remotes/origin/master" | sed -e 's|/|[/]|g')
master_remote_hash=$(
   git show-ref master | \
      sed -n -e "/$pattern/p" | \
         sed -e "s|$pattern||"
) 
#
if [ "$master_local_hash" != "$master_remote_hash" ]
then
   echo 'bin/new_release.sh: local and remote master differ'
   echo "local  $mster_local_hash"
   echo "remote $master_remode_hash"
   echo 'try git checkout master; git push'
   exit 1
fi
#
# push tag
read -p 'More testing or commit release [t/c] ?' response
if [ "$response" == 'c' ]
then
   echo "git tag -a -m 'created by new_release.sh' $tag $stable_remote_hash"
   git tag -a -m 'created by new_release.sh' $tag $stable_remote_hash
   #
   echo "git push origin $tag"
   git push origin $tag
fi
# -----------------------------------------------------------------------------
# master
# -----------------------------------------------------------------------------
git checkout master
echo 'bin/new_release.sh: OK'
exit 0
