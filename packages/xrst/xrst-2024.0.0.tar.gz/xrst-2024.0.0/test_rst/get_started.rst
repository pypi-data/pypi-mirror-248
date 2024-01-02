.. _get_started-name:

!!!!!!!!!!!
get_started
!!!!!!!!!!!

.. meta::
   :keywords: get_started, title:, getting, started

.. index:: get_started, title:, getting, started

.. _get_started-title:

Title: Getting Started
######################
The name of this page is ``get_started`` and its title is
``Title: Getting Started`` .
All of the headings below begin with ``Heading:`` .

.. contents::
   :local:

.. meta::
   :keywords: heading:, steps

.. index:: heading:, steps

.. _get_started@Heading\: Steps:

Heading: Steps
**************

#. Use pip as follows to install the most recent stable version of xrst::

      pip install xrst

#. After installing the stable version, use the following command
   to install the leading edge version of xrst::

      pip install sphinx-copybutton
      pip uninstall -y xrst
      pip install --index-url https://test.pypi.org/simple/ xrst

#. Create an empty directory and make it your current working directory.

#. Create a file called ``xrst.toml`` (the xrst configure file)
   in the working directory with the following contents::

      [root_file]
      default = 'get_started.xrst'

   This is the xrst configure file.

#. Create a file called ``get_started.xrst``, in the working directory,
   with the contents of
   :ref:`this example file<get_started@Heading: This Example File>` .

#. Execute the following command::

      xrst

#. Use your web browser to open the file below
   (this file name above is relative to your working directory)::

      build/html/get_started.html

#. You may have gotten spelling warnings because the spell checker
   you are using is different from the one used to test xrst.
   You can fix these warning by adding or removing words in the
   spell command at the beginning of the get_started.xrst file.
   If you do this correctly and re-execute the xrst command,
   the spelling warnings should not appear.

#. You should have gotten a warning that none of the input_files commands
   succeeded. These commands are used to check if all the input files get used.
   You can remove this check by adding the text below at the end of your
   xrst.toml file::

      [input_files]
      data = [ ]

   If you then re-execute the xrst command, the input files
   warning should not appear.

.. meta::
   :keywords: heading:, links, page

.. index:: heading:, links, page

.. _get_started@Heading\: Links to this Page:

Heading: Links to this Page
***************************

- :ref:`get_started-name`

- :ref:`get_started-title`

- :ref:`get_started@Heading: Steps`

- :ref:`get_started@Heading: Links to this Page`

- :ref:`get_started@Heading: This Example File`

.. meta::
   :keywords: heading:

.. index:: heading:

.. _get_started@Heading\: This Example File:

Heading: This Example File
**************************
The file below demonstrates the use of
``xrst_begin``,  ``xrst_end``, ``xrst_spell``, ``xrst_literal``
and heading references :

.. literalinclude:: ../../example/get_started.xrst
   :language: rst
