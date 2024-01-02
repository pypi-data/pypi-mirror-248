.. _toc_cmd_dev-name:

!!!!!!!!!!!
toc_cmd_dev
!!!!!!!!!!!

.. meta::
   :keywords: toc_cmd_dev, get, page, names, children, page

.. index:: toc_cmd_dev, get, page, names, children, page

.. _toc_cmd_dev-title:

Get file and page names for children of this page
#################################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _toc_cmd_dev@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/toc_commands.py
   :lines: 191-196,384-393
   :language: py

.. meta::
   :keywords: is_parent

.. index:: is_parent

.. _toc_cmd_dev@is_parent:

is_parent
*********
is this the parent page for other pages in the file specified by file_name.

.. meta::
   :keywords: data_in

.. index:: data_in

.. _toc_cmd_dev@data_in:

data_in
*******
is the data for the page before the toc commands have been processed.

.. meta::
   :keywords: file_name

.. index:: file_name

.. _toc_cmd_dev@file_name:

file_name
*********
is the name of the file that this data comes from. This is only used
for error reporting.

.. meta::
   :keywords: page_name

.. index:: page_name

.. _toc_cmd_dev@page_name:

page_name
*********
is the name of the page that this data is in. This is only used
for error reporting.

.. meta::
   :keywords: group_name

.. index:: group_name

.. _toc_cmd_dev@group_name:

group_name
**********
We are only including information for pages in this group.

.. meta::
   :keywords: data_out

.. index:: data_out

.. _toc_cmd_dev@data_out:

data_out
********
is a copy of data_in with the toc commands replaced by {xrst_command}
where command is TOC_hidden, TOC_list, or TOC_table depending on
which command was in data_in.
There is a newline directly before and after the {xrst_command}.

.. meta::
   :keywords: file_list

.. index:: file_list

.. _toc_cmd_dev@file_list:

file_list
*********
is the list of files in the toc command
(and in same order as in the toc command).

.. meta::
   :keywords: child_page_list

.. index:: child_page_list

.. _toc_cmd_dev@child_page_list:

child_page_list
***************
Is the a list of page names corresponding to the children of the
this page that are in the files specified by file_list.
If a file in file_list has a begin_parent command, there is only
one page in child_page_list for that file. Otherwise all of the
pages in the file are in child_page_list.

.. meta::
   :keywords: order

.. index:: order

.. _toc_cmd_dev@order:

order
*****
If *is_parent* is True, *order*
specifies if the pages in *child_page_list* come before or after
the rest of the children for this page.
