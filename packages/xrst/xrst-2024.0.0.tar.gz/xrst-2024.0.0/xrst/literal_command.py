# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Bradley M. Bell <bradbell@seanet.com>
# SPDX-FileContributor: 2020-23 Bradley M. Bell
# ----------------------------------------------------------------------------
r"""
{xrst_begin literal_cmd user}
{xrst_spell
   dir
   literalinclude
}

Literal Command
###############

Syntax
******

-  ``\{xrst_literal}``

-  | ``\{xrst_literal`` *separator*
   |     *display_file*
   |     *start_after_1* *separator* *end_before_1*
   |     *start_after_2* *separator* *end_before_2*
   |     ...
   | ``}``

-  | ``\{xrst_literal``
   |     *display_file*
   |     *start_after_1*
   |     *end_before_1*
   |     *start_after_2*
   |     ...
   | ``}``

Purpose
*******
Literal text, from any where in any file,
can be included using this command.

literalinclude
**************
This command is similar to the following sphinx directive
(see :ref:`dir_cmd-name`) :

| |tab| .. literalinclude:: \{xrst_dir *display_file*}
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


separator
*********
If *separator* is present, it must be a single character.
At most one *separator* can be in each line and it also separates tokens.

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

extension
=========
The *display_file* extension is used to determine what language
to use when highlighting the input block.
In the special case where *display_file* ends with ``.in`` ,
the final ``.in`` is not included when file name
when determining the extension.
This is done because configure files use the ``.in`` extension,
and usually create a file with the ``.in`` dropped.

No start or end
***************
In the case where there is no *start_after* or *end_before*,
the entire display file is displayed.
In the case of the ``\{xrst_literal}`` syntax,
the entire current input file is displayed.

start_after
***********
Each literal input block starts with the line following the occurrence
of the text *start_after* in *display_file*.
If this is the same as the file containing the command,
the text *start_after* will not match any text in the command.
There must be one and only one occurrence of *start_after* in *display_file*,
not counting the command itself when the files are the same.

end_before
**********
Each literal input block ends with the line before the occurrence
of the text *end_before* in *display_file*.
If this is the same as the file containing the command,
the text *end_before* will not match any text in the command.
There must be one and only one occurrence of *end_before* in *display_file*,
not counting the command itself when the files are the same.

Spell Checking
**************
Spell checking is **not** done for these literal input blocks.


Example
*******
see :ref:`literal_example-name` .

{xrst_end literal_cmd}
"""
# ----------------------------------------------------------------------------
import os
import re
import xrst
#
# ----------------------------------------------------------------------------
#
# extension_map
# map cases that pygments has trouble with
extension_map = {
   'xrst' : 'rst'    ,
   'hpp'  : 'cpp'    ,
   'm'    : 'matlab' ,
   'txt'  : ''       ,
}
def file_extension(display_file) :
   if display_file.endswith('.in') :
      display_file = display_file[: -3]
      index        = display_file.rfind('.')
   else :
      index = display_file.rfind('.')
   extension = ''
   if 0 <= index and index + 1 < len(display_file) :
      extension = display_file[index + 1 :]
      if extension in extension_map :
         extension = extension_map[extension]
   return extension
#
# pattern_literal
pattern_literal    = xrst.pattern['literal']
#
# pattern_arg
pattern_arg        = re.compile( r'([^\n]*)@xrst_line ([0-9]+)@\n|\n' )
#
# arg_list, line_list, start_command, end_command =
def next_literal_cmd(data_in, file_name, page_name, start_search) :
   assert type(data_in) == str
   assert type(file_name) == str
   assert type(page_name) == str
   assert type(start_search) == int
   #
   # arg_list, line_list
   arg_list   = list()
   line_list  = list()
   #
   # m_literal
   m_literal  = pattern_literal.search( data_in , start_search)
   if m_literal == None :
      return None, None, None, None
   #
   # separator, arg_text
   if m_literal.group(1) == None :
      separator = ''
      arg_text  = ''
   else :
      separator = m_literal.group(1).strip()
      arg_text  = m_literal.group(2)
   #
   if len(separator) > 1 :
      msg  =  '{xrst_literal separator\n'
      msg += f'separator = "{separator}" is more than one character'
      xrst.system_exit(
         msg,
         file_name = file_name,
         page_name = page_name,
         m_obj     = m_literal,
         data      = data_in
      )
   #
   # arg_list
   m_arg = pattern_arg.search( arg_text )
   while m_arg != None :
      if m_arg.group(1) == None :
         msg = 'There is an empty line inside a literal command.'
         xrst.system_exit(
            msg,
            file_name = file_name,
            page_name = page_name,
            m_obj     = m_arg,
            data      = arg_text
         )
      end    = m_arg.end()
      arg    = m_arg.group(1)
      line   = int( m_arg.group(2) )
      if len(separator) > 0 and arg.count(separator) > 1 :
         msg  =  f'xrst_literal separator = {separator}\n'
         msg += 'separator appears more than once in a line'
         xrst.system_exit(
            msg,
            file_name = file_name,
            page_name = page_name,
            m_obj     = m_arg,
            data      = m_arg.group(0)
         )
      if separator == '' or arg.count(separator) == 0 :
         arg_list.append( arg.strip() )
         line_list.append( line )
      else :
         assert arg.count(separator) == 1
         arg = arg.split(separator)
         arg_list.append( arg[0].strip() )
         arg_list.append( arg[1].strip() )
         line_list.append( line )
         line_list.append( line )
      m_arg  = pattern_arg.search( arg_text , end)
   #
   # start_command, end_command
   start_command = m_literal.start() + 1
   end_command   = m_literal.end()
   #
   assert len(arg_list) == len(line_list)
   for arg in arg_list :
      assert type(arg) == str
   for line in line_list :
      assert type(line) == int
   assert type(start_command) == int
   assert type(end_command) == int
   return arg_list, line_list, start_command, end_command
# ----------------------------------------------------------------------------
# {xrst_begin literal_cmd_dev dev}
# {xrst_spell
#     dir
# }
# {xrst_comment_ch #}
#
# Process the literal commands in a page
# ######################################
#
# Prototype
# *********
# {xrst_literal ,
#    # BEGIN_DEF, # END_DEF
#    # BEGIN_RETURN, # END_RETURN
# }
#
# data_in
# *******
# is the data for a page before the
# :ref:`literal commands <literal_cmd-name>` have been removed.
#
# file_name
# *********
# is the name of the file that this data comes from. This is used
# for error reporting and for the display file (when the display file
# is not included in the command).
#
# page_name
# *********
# is the name of the page that this data is in. This is only used
# for error reporting.
#
# rst2project_dir
# ***************
# is a relative path from the :ref:`config_file@directory@rst_directory`
# to the :ref:`config_file@directory@project_directory` .
#
# data_out
# ********
# Each xrst literal command is converted to its corresponding sphinx commands.
#
# {xrst_end literal_cmd_dev}
# BEGIN_DEF
def literal_command(data_in, file_name, page_name, rst2project_dir) :
   assert type(data_in) == str
   assert type(file_name) == str
   assert type(page_name) == str
   assert type(rst2project_dir) == str
   # END_DEF
   #
   # data_out
   data_out = data_in
   #
   # arg_list, line_list, start_command, end_command
   start_search = 0
   arg_list, line_list, start_command, end_command = next_literal_cmd(
      data_out, file_name, page_name, start_search
   )
   #
   while arg_list != None :
      #
      # even
      even = len(arg_list) % 2 == 0
      #
      # display_file, arg_list
      if even :
         display_file = file_name
      else :
         display_file = arg_list.pop(0)
         if not os.path.isfile(display_file) :
            msg  = 'literal command: can not find the display_file.\n'
            msg += f'display_file = {display_file}'
            xrst.system_exit(msg,
               file_name = file_name,
               page_name = page_name,
               line      = line_list[0],
            )
         if os.path.samefile(display_file, file_name) :
            display_file = file_name
      #
      # cmd_line
      if len(arg_list) >= 2 :
         cmd_line = ( line_list[0], line_list[-1] )
      #
      # start_end_line_list
      assert len(arg_list) % 2 == 0
      start_end_line_list = list()
      for i in range(0, len(arg_list), 2) :
         start_after = arg_list[i]
         end_before  = arg_list[i+1]
         #
         # start_line, end_line
         start_line, end_line = xrst.start_end_file(
            file_cmd     = file_name,
            page_name    = page_name,
            display_file = display_file,
            cmd_line     = cmd_line,
            start_after  = start_after,
            end_before   = end_before
         )
         #
         # start_end_line_list
         start_end_line_list.append( (start_line + 1, end_line - 1) )
      #
      # cmd
      display_path = os.path.join(rst2project_dir, display_file)
      cmd          = f'.. literalinclude:: {display_path}\n'
      #
      # cmd
      for i in range( len(start_end_line_list) ) :
         start_line, end_line = start_end_line_list[i]
         if i == 0 :
            cmd += 3 * ' ' + f':lines: {start_line}-{end_line}'
         else :
            cmd += f',{start_line}-{end_line}'
      if( len(start_end_line_list) > 0 ) :
         cmd += '\n'
      #
      # cmd
      # Add language to literalinclude, sphinx seems to be brain
      # dead and does not do this automatically.
      extension = file_extension( display_file )
      if extension != '' :
         cmd += 3 * ' ' + f':language: {extension}\n'
      cmd = '\n' + cmd + '\n\n'
      if start_command > 0 :
         if data_out[start_command - 1] != '\n' :
            cmd = '\n' + cmd
      #
      # data_tmp, data_out
      data_tmp  = data_out[: start_command ]
      data_tmp += cmd
      data_out  = data_tmp + data_out[ end_command : ]
      #
      # start_search
      start_search = len(data_tmp)
      #
      arg_list, line_list, start_command, end_command = next_literal_cmd(
         data_out, file_name, page_name, start_search
      )
   # BEGIN_RETURN
   #
   assert type(data_out) == str
   return data_out
   # END_RETURN
