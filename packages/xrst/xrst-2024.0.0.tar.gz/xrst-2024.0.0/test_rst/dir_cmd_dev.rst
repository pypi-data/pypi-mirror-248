.. _dir_cmd_dev-name:

!!!!!!!!!!!
dir_cmd_dev
!!!!!!!!!!!

.. meta::
   :keywords: dir_cmd_dev, convert, names, be, relative, rst, directory

.. index:: dir_cmd_dev, convert, names, be, relative, rst, directory

.. _dir_cmd_dev-title:

Convert File Names to be Relative to the RST Directory
######################################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _dir_cmd_dev@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/dir_command.py
   :lines: 71-73,97-99
   :language: py

.. meta::
   :keywords: data_in

.. index:: data_in

.. _dir_cmd_dev@data_in:

data_in
*******
is the data for this page.

.. meta::
   :keywords: rst2project_dir

.. index:: rst2project_dir

.. _dir_cmd_dev@rst2project_dir:

rst2project_dir
***************
is a relative path from the :ref:`config_file@directory@rst_directory`
to the :ref:`config_file@directory@project_directory` .

.. meta::
   :keywords: data_out

.. index:: data_out

.. _dir_cmd_dev@data_out:

data_out
********
The return data_out is a copy of data_in except that all the occurrences of
``{xrst_dir`` *file_name*\ ``}`` have been converted to the file name
relative to the rst directory.
