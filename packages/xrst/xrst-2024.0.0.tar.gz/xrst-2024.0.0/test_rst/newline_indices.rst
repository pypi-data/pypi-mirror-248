.. _newline_indices-name:

!!!!!!!!!!!!!!!
newline_indices
!!!!!!!!!!!!!!!

.. meta::
   :keywords: newline_indices, find, index, all, newlines, in, string

.. index:: newline_indices, find, index, all, newlines, in, string

.. _newline_indices-title:

Find index of all the newlines in a string
##########################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _newline_indices@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/newline_indices.py
   :lines: 33-34,43-47
   :language: py

.. meta::
   :keywords: data

.. index:: data

.. _newline_indices@data:

data
****
The string we are searching for newlines.

.. meta::
   :keywords: results

.. index:: results

.. _newline_indices@Results:

Results
*******

.. meta::
   :keywords: newline_list

.. index:: newline_list

.. _newline_indices@newline_list:

newline_list
************
The return newline_list is the list of indices in data that
represent all of the newlines; i.e. '\n'.
