.. _literal_cmd-name:

!!!!!!!!!!!
literal_cmd
!!!!!!!!!!!

.. meta::
   :keywords: literal_cmd, literal

.. index:: literal_cmd, literal

.. _literal_cmd-title:

Literal Command
###############

.. contents::
   :local:

.. _literal_cmd@Syntax:

Syntax
******

-  ``{xrst_literal}``

-  | ``{xrst_literal`` *separator*
   |     *display_file*
   |     *start_after_1* *separator* *end_before_1*
   |     *start_after_2* *separator* *end_before_2*
   |     ...
   | ``}``

-  | ``{xrst_literal``
   |     *display_file*
   |     *start_after_1*
   |     *end_before_1*
   |     *start_after_2*
   |     ...
   | ``}``

.. _literal_cmd@Purpose:

Purpose
*******
Literal text, from any where in any file,
can be included using this command.

.. meta::
   :keywords: literalinclude

.. index:: literalinclude

.. _literal_cmd@literalinclude:

literalinclude
**************
This command is similar to the following sphinx directive
(see :ref:`dir_cmd-name`) :

| |tab| .. literalinclude:: {xrst_dir *display_file*}
| |tab| |tab| :start-after: *start_after_1*
| |tab| |tab| :end-before: *end_before_1*

The xrst literal command has the following difference:

#. If the *display_file* is not specified, the current input file is used.
#. The *start_after* and *end_before* in the command are not considered
   a match for the corresponding text. This makes it possible to put the
   command above the text when *display_file* is the current input file.
#. It is an error for there to be more than one copy of each *start_after*
   or *end_before* in the *display_file* (not counting the copy in the
   command when the display file is the current input file).
   This makes sure that the intended section of *display_file* is displayed.
#. It is possible to specify multiple sections of a file using
   the start after and end before patterns. (These automatically get converted
   to line numbers in a sphinx literalinclude directive.)

.. meta::
   :keywords: tokens

.. index:: tokens

.. _literal_cmd@Tokens:

Tokens
******
#. Leading and trailing spaces are not included in
   *separator*, *display_file*, each *start_after*, and each *end_before*.
#. Each *start_after* must have a corresponding *end_before*.
#. If there are an even number of tokens (not counting *separator*),
   the *display_file* is not present and the current input file is used.
#. The new line character separates the tokens.
#. If there are multiple lines in the command, the last line contains
   the ``}`` and must have nothing else but white space.

.. meta::
   :keywords: separator

.. index:: separator

.. _literal_cmd@separator:

separator
*********
If *separator* is present, it must be a single character.
At most one *separator* can be in each line and it also separates tokens.

.. meta::
   :keywords: display_file

.. index:: display_file

.. _literal_cmd@display_file:

display_file
************
If *display_file* is not present,
the literal input block is in the current input file.
Otherwise, the literal input block is in *display_file*.
The file name *display_file* is relative to the
:ref:`config_file@directory@project_directory` .

1. This may seem verbose, but it makes it easier to write scripts
   that move files and automatically change references to them.
2. Note that if you use the sphinx ``literalinclude`` directive,
   the corresponding file name will be relative to the
   :ref:`config_file@directory@rst_directory` , which is a path relative
   to the project_directory; see :ref:`dir_cmd-name` .

.. meta::
   :keywords: extension

.. index:: extension

.. _literal_cmd@display_file@extension:

extension
=========
The *display_file* extension is used to determine what language
to use when highlighting the input block.
In the special case where *display_file* ends with ``.in`` ,
the final ``.in`` is not included when file name
when determining the extension.
This is done because configure files use the ``.in`` extension,
and usually create a file with the ``.in`` dropped.

.. meta::
   :keywords: no, start, or, end

.. index:: no, start, or, end

.. _literal_cmd@No start or end:

No start or end
***************
In the case where there is no *start_after* or *end_before*,
the entire display file is displayed.
In the case of the ``{xrst_literal}`` syntax,
the entire current input file is displayed.

.. meta::
   :keywords: start_after

.. index:: start_after

.. _literal_cmd@start_after:

start_after
***********
Each literal input block starts with the line following the occurrence
of the text *start_after* in *display_file*.
If this is the same as the file containing the command,
the text *start_after* will not match any text in the command.
There must be one and only one occurrence of *start_after* in *display_file*,
not counting the command itself when the files are the same.

.. meta::
   :keywords: end_before

.. index:: end_before

.. _literal_cmd@end_before:

end_before
**********
Each literal input block ends with the line before the occurrence
of the text *end_before* in *display_file*.
If this is the same as the file containing the command,
the text *end_before* will not match any text in the command.
There must be one and only one occurrence of *end_before* in *display_file*,
not counting the command itself when the files are the same.

.. meta::
   :keywords: spell, checking

.. index:: spell, checking

.. _literal_cmd@Spell Checking:

Spell Checking
**************
Spell checking is **not** done for these literal input blocks.

.. _literal_cmd@Example:

Example
*******
see :ref:`literal_example-name` .
