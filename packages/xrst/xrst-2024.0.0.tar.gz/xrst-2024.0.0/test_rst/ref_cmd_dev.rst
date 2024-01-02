.. _ref_cmd_dev-name:

!!!!!!!!!!!
ref_cmd_dev
!!!!!!!!!!!

.. meta::
   :keywords: ref_cmd_dev, remove, leading, trailing, white, space, from, ref, role, targets

.. index:: ref_cmd_dev, remove, leading, trailing, white, space, from, ref, role, targets

.. _ref_cmd_dev-title:

Remove Leading and Trailing White Space From ref Role Targets
#############################################################

.. contents::
   :local:

.. meta::
   :keywords: prototype

.. index:: prototype

.. _ref_cmd_dev@Prototype:

Prototype
*********

.. literalinclude:: ../../xrst/ref_command.py
   :lines: 70-71,137-139
   :language: py

.. meta::
   :keywords: data_in

.. index:: data_in

.. _ref_cmd_dev@data_in:

data_in
*******
is the data for this page.

.. meta::
   :keywords: data_out

.. index:: data_out

.. _ref_cmd_dev@data_out:

data_out
********
The return data_out is a copy of data_in except that white space
surrounding the target components has been removed .
