.. image:: logo_hzb_big.png
   :align: right
   :target: http://www.helmholtz-berlin.de

======================================
Welcome to pyexpander's documentation!
======================================

pyexpander - a powerful turing complete macro processor
=======================================================

pyexpander is a macro processor that allows to embed python code in text files.

Some of the features are:

- Variables like ``~(VAR)`` are replaced.
- Valid python expressions like ``~(2+3/2)`` are evaluated.
- Arbitrary python code like in ``~py(import math; math.pi)`` can be executed.
- The functionality is available as a script and a python library.
- The program is availiable for python version 2 and version 3.

**Note**: Python 2 support of pyexpander is deprecated! Future versions will
require Python 3. See also 
`Python 2 or Python 3 <https://wiki.python.org/moin/Python2orPython3>`_.

See :doc:`introduction` for more information.

:Author:
    Goetz Pfeiffer (Goetz.Pfeiffer@helmholtz-berlin.de, goetzpf@googlemail.com)

Documentation
=============

Introduction
------------

This gives a first impression on pyexpander's capabilities:

:doc:`Introduction to pyexpander <introduction>`

Reference documents
-------------------

This is the reference of the pyexpander language:

:doc:`pyexpander reference <reference-expander>`

Full list of documents
----------------------

.. toctree::
   :maxdepth: 1

   introduction
   reference-expander
   epics-support
   python3
   expander-options
   msi2pyexpander-options
   pyexpander-install
   source-code-documentation
   license


License and copyright
=====================

Copyright (c) 2020 by `Helmholtz-Zentrum Berlin <https://www.helmholtz-berlin.de>`_.

This software of this project can be used under GPL v.3, see :doc:`license`.

Download and install
====================

By using `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`_, installing
pyexpander is a single line command. This and other installation methods
are described in

:doc:`Installing pyexpander <pyexpander-install>`

pyexpander at sourceforge
=========================

You find the sourceforge summary page for pyexpander at
`pyexpander <https://sourceforge.net/projects/pyexpander>`_.

pyexpander at Bitbucket (deprecated)
====================================

Bitbucket removes support for mercurial repositories in 2020 so pyexpander will
in the future no longer be hosted here.

The source
==========

You can browse the mercurial repository here:

`repository at Sourceforge <http://pyexpander.hg.sourceforge.net/hgweb/pyexpander/pyexpander>`_.

or clone it with this command:

Sourceforge::

  hg clone http://hg.code.sf.net/p/pyexpander/code pyexpander-code

You can then commit changes in your own repository copy. 

If you plan to share these changes you can create a mercurial 
`bundle <http://mercurial.selenic.com/wiki/Bundle>`_ and send it to my e-mail
address.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Introduction
============

Macro substitution
------------------

Note: The examples below use "expander.py", the python 3 implementation of
pyexpander. You have to call "expander2.py" if you installed the python 2
implementation of pyexpander. Note that python 2 is deprecated, it will not be
supported in future versions.

For some projects there is the need to replace macros in a text file with
values defined in other files or the command line. There are already other
macro replacement tools that can do this but if you want to calculations or
string operations and insert the results of this into your file, the list of
possible tools becomes much shorter.

Pyexpander combines the python programming language with a simple macro
replacement scheme in order to give the user both, ease of use and the
power of a full featured scripting language. 

Even without being familiar with python you can use pyexpander to perform
calculations or string operations and use the results in your macro
replacements.

Here is a very simple example, this is the content of file "letter.txt"::

  Dear ~(salutation) ~(surname),
  
  this is a simple pyexpander example.

Applying this command::

  expander.py --eval 'salutation="Mr";surname="Smith"' -f letter.txt

gives this result::

  Dear Mr Smith,
  
  this is a simple pyexpander example.


Here is more advanced example::

  ~py(start=0; end=5)\
   x |  x**2
  ---|------
  ~for(x in range(start,end+1))\
  ~("%2d | %3d" % (x,x*x))
  ~endfor\

Applying expander.py to a file with the content shown above gives the following
result::

   x |  x**2
  ---|------
   0 |   0
   1 |   1
   2 |   4
   3 |   9
   4 |  16
   5 |  25

And here we show how pyexpander compares with the well known m4 macro
processor. We have taken the 
`m4 <http://en.wikipedia.org/wiki/M4_(computer_language)>`_ example with small
modifications from Wikipedia::

  divert(-1)
  # This starts the count at ONE as the incr is a preincrement.
  define(`H2_COUNT', 0)
  # The H2_COUNT macro is redefined every time the H2 macro is used.
  define(`H2',
          `define(`H2_COUNT', incr(H2_COUNT))<h2>H2_COUNT. $1</h2>')
  divert(0)dnl Diversion to 0 means back to normal. dnl macro removes this line.
  H2(First Section)
  H2(Second Section)
  H2(Conclusion)

Here is the same example formulated in pyexpander::

  ~py(
  # This starts the count at ONE as the incr is a preincrement.
  H2_COUNT=0
  # H2_COUNT is incremented each time H2 is called.
  def H2(st):
      global H2_COUNT
      H2_COUNT+=1
      return "<h2>%d. %s</h2>" % (H2_COUNT,st)
  )\
  ~# the following makes H2 callable without another pair of enclosing brackets:
  ~extend(H2)\
  ~H2("First Section")
  ~H2("Second Section")
  ~H2("Conclusion")

Both produce this output::

  <h2>1. First Section</h2>
  <h2>2. Second Section</h2>
  <h2>3. Conclusion</h2>

The advantages of pyexpander are:

- simple syntax definition, all expander commands start with a dollar ("~")
  sign followed by word characters, parameters or python code enclosed in
  brackets or both.
- the full power of the python programming language can be used, all operators,
  functions and modules.
- *any* python expression can be used to insert text.
- There is also a python library, pyexpander.py, which you can use to develop
  other macro tools based on pyexpander.

If you are not familiar with the python programming language, you should have
a look at :doc:`python 3 introduction for pyexpander <python3>`. 

For a detailed description of the pyexpander language see 
:doc:`reference <reference-expander>`.
EPICS support
=============

`EPICS <http://www.aps.anl.gov/epics>`_ is a framework for control systems
used at many research facilities, including the 
`Helmholtz-Zentrum Berlin <https://www.helmholtz-berlin.de>`_.

Pyexpander has three commands in order to support EPICS macro substitution 
which is usually done by the 
`msi <http://www.aps.anl.gov/epics/extensions/msi/index.php>`_ tool. 
These commands may also be useful for other applications. 

The idea in msi is to have a template file with macro placeholders in it and
process this file several times with different macro values at each run. In
this mechanism, the filename has only to be mentioned once. 

Here is a simple example, test.template has this content::

  record(calcout, "U3IV:~(name)") {
    field(CALC, "~(calc)")
    field(INPA, "U3IV:P4:rip:cvt CPP MS")
    field(OUT,  "U3IV:P4:rip:calcLRip.A PP MS")
  }

test.substitution has this content::

  ~template("test.template")\
  ~subst(
    name="set", 
    calc="A+B",
  )\
  ~subst(
    name="set2",
    calc="C+D"
  )\

This is the result when test.template is processed::

  record(calcout, "U3IV:set") {
    field(CALC, "A+B")
    field(INPA, "U3IV:P4:rip:cvt CPP MS")
    field(OUT,  "U3IV:P4:rip:calcLRip.A PP MS")
  }
  record(calcout, "U3IV:set2") {
    field(CALC, "C+D")
    field(INPA, "U3IV:P4:rip:cvt CPP MS")
    field(OUT,  "U3IV:P4:rip:calcLRip.A PP MS")
  }

As you see, test.template was instantiated twice. In the pyexpander package
there is also a converter program, msi2pyexpander.py, which can be used to convert
substitution files from the EPICS msi format to the pyexpander format.

This is how the three commands work:

Setting the name of the template file
.....................................

The "template" command is used to define the name of an substitution file and
optional, it's encoding. It must be followed by one or two strings (or string
expressions) enclosed in brackets. 

The first string is always a filename, the optional second string is the
encoding of the file, e.g. "utf-8" or "iso8859-1". Valid encoding names can be
looked up here: 

`python encodings <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

Note that the filename is only defined within the current scope (see "variable
scopes"). 

Here is an example without an explicit encoding::

  ~template("test.template")

and here is an example for an iso8859 encoded template file::

  ~template("test-iso.template", "iso8859")

The "subst" command
...................

This command is used to substitute macros in the file whose name was defined
with the "template" command before. This command must be followed by an
opening bracket and an arbitrary list of named python parameters. This means
that each parameter definition consists of an unquoted name, an "=" and a
quoted string, several parameter definitions must be separated by commas. The
"subst" command takes these parameters and defines the variables in a new
scope. It then processes the file that was previously set with the "template"
command. Here is an example::

  ~subst(
          AMS= "ams_",
          BASE= "UE112ID7R:",
          BASE1= "UE112ID7R:",
          BASE2= "UE112ID7R:S",
          BaseStatMopVer= "9",
        )\

The "pattern" command
.....................

This command is an alternative way to substitute macros in a file. The pattern command must be followed by an opening round bracket, a list of python tuples and a closing round bracket. Each tuple is a comma separated list of quoted strings enclosed in round brackets. Tuples must be separated by commas. Here is an example::

  ~pattern(
            ( "DEVN", "SIGNAL"),
            ( "PAHRP", "PwrCavFwd"),
            ( "PAHRP", "PwrCavRet"),
            ( "PAHRP", "PwrCircOut"),
          )\

The first tuple defines the names of the variables, all following tuples define
values these variables get. For each following tuple the file defined by
"template" is included once. In the example above, the variable "DEVN" has
always the value "PAHRP", the variable "SIGNAL" has the values "PwrCavFwd",
"PwrCavRet" and "PwrCircOut". The file defined by the previous "template"
command is instantiated 3 times.

Differences to the EPICS msi tool
.................................

These are differences to msi:

- The file format of substitution files is different, but you can use
  msi2pyexpander.py to convert them.
- Macros must always be defined. If a macro should be expanded and it is not
  defined at the time, the program stops with an exception. If you want the
  program to continue in this case, use the "default" command to provide
  default values for the macros that are sometimes not defined.
- Variables defined in a "subst" command are scoped, they are only defined for
  that single instantiation of the template file. 
- The template file commands "include" and "substitute" as they are known from
  msi are not implemented in this form. However, "include" in pyexpander
  has the same functionality as "include" in msi and "py" in pyexpander can be
  used to do the same as "substitute" in msi.

Here is an example how to convert a template file from msi to pyexpander. Note
that in pyexpander there is no principal difference between a template and a
substitution file, both have the same syntax. The msi template file is this::

  A variable with a default ~(var=default value)
  Here we include a file:
  include "filename"
  Here we define a substitution:
  substitute "first=Joe,family=Smith"

Here is the same formulated for pyexpander::

  A variable with a default ~default(var="default value")~(var)
  Here we include a file:
  ~include("filename")
  Here we define a substitution:
  ~py(first="Joe";family="Smith")
======================
Useful Python 3 basics
======================

.. This text is RST (ReStructured Text), 
   see also http://docutils.sourceforge.net/rst.html

Introduction
------------

Pyexpander is based on the python programming language not just with respect to
it's implementation. Expressions and statements are, in fact, python code. This
page shows some simple use cases for pyexpander for users that do not yet know
python. If you are interested in learning python you can find some information
at the `official python documentation site <http://docs.python.org>`_ and at
the `Python tutorial <http://docs.python.org/tutorial/index.html>`_.

Comments
--------

Comments in python start with a "#" character and extend to the end of the
line. If you want to have several consecutive lines as a comment, each line has
to start with a "#" character. Here are some examples::

  ~py(
  a=1 # here is a comment
  # here is a comment
  # spanning several 
  # lines
  )

A word on indentation
---------------------

The indentation of lines (the number of spaces they start with) is part of the
syntax in python. This means that for python commands that span more than one
line, indentation matters. If you get an error message like "unexpected indent"
you know that the problem is the indentation of lines. As a rule of thumb,
python statements that follow a "~py" command should either all be in the same
line as the "~py" command and immediately follow the opening bracket or, if
there is more than one line, all should start in column one. Here are some
examples::

  ~py( a=1)     # indentation error due to the space between "(" and "a"
  ~py(a=1; b=1) # correct, spaces *within* the line are allowed
  ~py(a=1)      # correct
  ~py(     
    a=1         # indentation error since "a" is not in column 1 of the line
  )
  ~py(     
  a=1           # correct
  )
  ~py(
  a=1           # correct
  b=2
  )

Note that due to python indentation rules, the closing bracket ")" of the "~py"
command should be in column 1 if it is in a line of it's own. Otherwise, with
certain python statements, an indentation error may occur.

Defining variables
------------------

Python variable names start with a letter or a "_" and may be followed by an arbitrary number of letters, digits and the "_" character.

You define a variable by placing a variable name, a "=" character and a value. Here are some examples::

  ~py(my_number= 1)
  ~py(my_var1= 2)

Literals
++++++++

You often define variables with constant values, also called literals.
Integers, floating point numbers and strings can be written the same way as in
C. Here are some examples::

  ~py(my_integer=3)
  ~py(my_float1=1.23)
  ~py(my_float2=3.1E8)
  ~py(my_string="abc")
  ~py(my_line="This is a line with LF at the end.\n")

Setting more than one variable
++++++++++++++++++++++++++++++

Python statements are separated by a ";" character or by a newline character. You can define more than one variable like this::

  ~py(a=1; b=2; c=3)

or like this::
  
  ~py(
  a=1
  b=2
  c=3
  )

Simple expressions
++++++++++++++++++

Simple arithmetic expressions in python are the same as in c. Here are some examples::

  ~py(
  a=2+4
  b=1.4-3.8
  c=3*4
  d=a*b
  e=2**4 # 2**4==16
  )

Mathematical functions
++++++++++++++++++++++

Common mathematical functions are in the "math" package in python. You have to import this package once in order to be able to use these functions. Here is an example::

  ~py(
  from math import * # import mathematical functions
  e= exp(1)  # exponential function
  a= sqrt(2) # square root
  )

String expressions
++++++++++++++++++

Strings can be concatenated with "+"::

  ~py(a="ab"+"cd") # now a is "abcd"

The "%" operator works according to the string formatting rules for the
"printf" command in C. It is an infix operator, a format string must be
followed by a "%" and a single value or a tuple of values. A tuple is a comma
separated list of values enclosed in round brackets. Here are some examples::

  ~py(
  a= "%02d" % 3 # a=="03"
  b= "%d %3.4f" % (2, 123.456789) # b= "2 123.4568"
  )

For loops
---------

This section describes the "~for" statement of pyexpander which is very close
to the for-statement in python. 

For loops in python are a bit different from C. A typical loop statement
consists of a variable or a tuple of variables, the keyword "in" and an
"iterable" datatype, typically a list. If you simply want to have a loop
variable starting with a number, increase by 1 at each run, and end with
another number, you typically use the "range" function. In pure python a
for-loop running from 0 to 3 would look like this::

  for i in range(4):
      print("i is now:",i)

The "~for" statement in pyexpander is a bit different, but the specification of
the loop limit and loop variable are the same::

  ~for(i in range(4))
  i now: ~(i)
  ~endfor

Note the the number given to "range" is *not* part of the iteration. In the
example above, i never has the value 4, the last value of i is 3.

If "range" is provided with two numbers, the first number is the start number
and the second number is the end number plus one.  Here is an example where i
runs from 3 to 5::

  ~for(i in range(3,6))
  i now: ~(i)
  ~endfor

If "range" is provided with 3 numbers, the first ist the start, the second is
the end plus the step and the third is the step. Here is an example where i
takes the values 10, 8 and 6::

  ~for(i in range(10, 4, -2))
  i now: ~(i)
  ~endfor

expander.py command line options
================================

``-h``
++++++

    Show help for command line options.

``--summary``
+++++++++++++

    Print a summary of the function of the program.

``-f FILE --file FILE``
+++++++++++++++++++++++

    Specify a FILE to process. This option may be used more than once to
    process more than one file but note than this option is not really needed.
    Files can also be specified directly after the other command line options.
    If not given, the program gets it's input from stdin.

``--encoding``
++++++++++++++
    Specify the encoding of the input to the program. This encoding is also the
    default for all files that are read by ``~include()`` or ``~subst()``. Note
    that both mentioned commands allow to specify a different encoding at each
    call. Known encodings can be found at 
    `python encodings <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

``--output-encoding``
+++++++++++++++++++++
    Specify the encoding of the output of the program. Known encodings can be
    found at 
    `python encodings <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

``--eval``
++++++++++

    Evaluate PYTHONEXPRESSION in global context.

``-I PATH --include PATH``
++++++++++++++++++++++++++

    Add PATH to the list of include paths.

``-s --simple-vars``
++++++++++++++++++++

    Allow variables without brackets.

``-a --auto-continuation``
++++++++++++++++++++++++++

    Assume '\' at the end of lines with commands.

``-i --auto-indent``
++++++++++++++++++++++++++
    
    Automatically indent macros.

``--no-stdin-msg``
++++++++++++++++++++

    Do not print a message on stderr when the program is reading it's input
    from stdin.


Installing pyexpander
=====================

Parts of pyexpander
-------------------

pyexpander consists of scripts, python modules, documentation and configuration
files. 

pyexpander is available on `pypi <https://pypi.python.org/pypi>`_, as a debian
or rpm package, as a tar.gz and zip file. The following chapters describe how 
to install pyexpander.

Requirements
------------

pyexpander requires python version 3 or python version 2.5 or newer.

Note that support for python version 2 (including 2.5) is deprecated. Future
versions of pyexpander will not support python 2.

pyexpander is tested on `debian <https://www.debian.org>`_ and 
`Fedora <https://getfedora.org>`_ linux distributions but should run on all
linux distributions. It probably also runs on other flavours of unix, probably
even MacOS, but this is not tested.

It may run on windows, escpecially the `Cygwin <https://www.cygwin.com>`_
environment, but this is also not tested.

Install from pypi with pip
--------------------------

In order to install pyexpander with `pip <https://en.wikipedia.org/wiki/Pip_(package_manager)>`_, 
you use the command [1]_ [2]_::

  pip3 install pyexpander

.. [1] This is the example for python 3, for python 2 the command is "pip"
.. [2] Your python 3 version of pip may have a different name, e.g. "pip-3", "pip-3.2" or just "pip"

You find documentation for the usage of pip at `Installing Python Modules
<https://docs.python.org/3/installing/index.html#installing-index>`_.

Install from a debian package
-----------------------------

There are packages for some of the recent debian versions. In order to see
what debian version you use enter::

  cat /etc/debian_version

Download the package here:

* `pyexpander downloads at Sourceforge <https://sourceforge.net/projects/pyexpander/files/?source=navbar>`_

and install with::

  dpkg -i <PACKAGENAME>

The packages may with other debian versions or debian package based
distributions like ubuntu, but this is not tested. 

Install from a rpm package
--------------------------

There are packages for some of the recent fedora versions. 
In order to see what fedora version you use enter::

  cat /etc/fedora-release

Download the package here:

* `pyexpander downloads at Sourceforge <https://sourceforge.net/projects/pyexpander/files/?source=navbar>`_

and install with::

  rpm -ivh  <PACKAGENAME>

The packages may work with other fedora versions or rpm package based
distributions like, redhat, scientific linux or opensuse, but this was not
tested. 

Install from source with setup.py
---------------------------------

You should do this only if it is impossible to use one of the methods described
above. 

Download the tar.gz or zip file here:

* `pyexpander downloads at Sourceforge <https://sourceforge.net/projects/pyexpander/files/?source=navbar>`_

unpack the tar.gz file with::

  tar -xzf <PACKAGENAME>

or unpack the zip file with::

  unzip <PACKAGENAME>

The pyexpander distribution contains the install script "setup.py". If you install
pyexpander from source you always invoke this script with some command line options. 

The following chapters are just *examples* how you could install pyexpander. For a
complete list of all possibilities see 
`Installing Python Modules
<https://docs.python.org/3/installing/index.html#installing-index>`_.

The python interpreter you use to start setup.py determines the python version
(2 or 3) for which pyexpander is installed. 

Note that the python2 version of pyexpander is deprecated. Python 2 will not be
supported in future versions. 

In order to install for python 3.x use::

  python3 setup.py [options]

In order to install for python 2.x use::

  python2 setup.py [options]

Whenever ``python`` is mentioned in a command line in the following text remember
to use ``python2`` or ``python3`` instead.

Install as root to default directories
++++++++++++++++++++++++++++++++++++++

This method will install pyexpander on your systems default python library and
binary directories.

Advantages:

- You don't have to modify environment variables in order to use pyexpander.
- All users on your machine can easily use pyexpander.

Disadvantages:

- You must have root or administrator permissions to install pyexpander.
- Files of pyexpander are mixed with other files from your system in the same
  directories making it harder to uninstall pyexpander.

For installing pyexpander this way, as user "root" enter::

  python setup.py install

Install to a separate directory
+++++++++++++++++++++++++++++++

In this case all files of pyexpander will be installed to a separate directory.

Advantages:

- All pyexpander files are below a directory you specify, making it easy to uninstall
  pyexpander.
- If you have write access that the directory, you don't need root or
  administrator permissions.

Disadvantages:

- Each user on your machine who wants to use pyexpander must have the correct
  settings of the environment variables PATH and PYTHONPATH.

For installing pyexpander this way, enter::

  python setup.py install --prefix <DIR>

where <DIR> is your install directory.

In order to use pyexpander, you have to change the environment variables PATH and
PYTHONPATH. Here is an example how you could do this::

  export PATH=<DIR>/bin:$PATH
  export PYTHONPATH=<DIR>/lib/python<X.Y>/site-packages:$PYTHONPATH

where <DIR> is your install directory and <X.Y> is your python version number.
You get your python version with this command::

  python -c 'from sys import *;stdout.write("%s.%s\n"%version_info[:2])'

You may want to add the environment settings ("export...") to your shell setup,
e.g. $HOME/.bashrc or, if your are the system administrator, to the global
shell setup.

Install in your home
++++++++++++++++++++

In this case all files of pyexpander are installed in a directory in your home called
"pyexpander".

Advantages:

- All pyexpander files are below $HOME/pyexpander, making it easy to uninstall pyexpander.
- You don't need root or administrator permissions.

Disadvantages:

- Only you can use this installation.
- You need the correct settings of environment variables PATH and
  PYTHONPATH.

For installing pyexpander this way, enter::

  python setup.py install --home $HOME/pyexpander

You must set your environment like this::

  export PATH=$HOME/pyexpander/bin:$PATH
  export PYTHONPATH=$HOME/pyexpander/lib/python:$PYTHONPATH

You may want to add these lines to your shell setup, e.g. $HOME/.bashrc.

Reference
=========

A note on Python versions
-------------------------

Short version
+++++++++++++

Python 2 support in pyexpander is deprecated. Python 2 will not be supported in
future versions of the program.

If you don't already use pyexpander, or don't know the python language, simply
install the python 3 version of pyexpander. The program that does macro
substitutions is called "expander.py". 

If you need, for backwards compatibility, the python 2 version of pyexpander,
the program that does macro substitutions is called "expander2.py".

Background
++++++++++

Currently there exist two major branches of the python language, python version
2 and python version 3. Both have slight differences in syntax and not all
programs are compatible with both versions.

Pyexpander comes for now in a python 2 and a python 3 version. You can install one of
these versions or both at the same time. In order to distinguish the versions,
the expander script is named "expander2.py" for the python 2 version, and
"expander.py" for the python 3 version. 

Note that embedded python code like in the ``py(...)`` statement must use the
same major python version as the one pyexpander uses. So if you installed
pyexpander for python 3 your embedded python code must also be in the python 3
dialect. The same applies for python 2.

Python 2 support is deprecated, future versions of pyexpander will not support
python 2.

Syntax of the pyexpander language
---------------------------------

The meaning of the dollar sign
++++++++++++++++++++++++++++++

Note: in this fork the dollar sign has been changed to "~", but we didn't
update the literal string "dollar". so whenever documentation talks about
dollar, tilde ("~") is actually meant.

Almost all elements of the language start with a dollar "~" sign. If a dollar
is preceded by a backslash "\\" it is escaped. The "\\~" is then replaced with
a simple dollar character "~" and the rules described further down do not
apply.

Here is an example::
 
  an escaped dollar: \~

This would produce this output::

  an escaped dollar: ~

Comments
++++++++

A comment is started by a sequence "~#" where the dollar sign is not preceded
by a backslash (see above). All characters until and including the end of line
character(s) are ignored. Here is an example::

  This is ordinary text, ~# from here it is a comment
  here the text continues.

Commands
++++++++

If the dollar sign, which is not preceded by a backslash, is followed by a
letter or an underline "_" and one or more alphanumeric characters, including
the underline "_", it is interpreted to be an expander command. 

The *name* of the command consists of all alphanumeric characters including "_"
that follow. In order to be able to embed commands into a sequence of letters,
as a variant of this, the *name* may be enclosed in curly brackets. This
variant is only allowed for commands that do not expect parameters.

If the command expects parameters, an opening round bracket "(" must
immediately (without spaces) follow the characters of the command name. The
parameters end with a closing round bracket ")".

Here are some examples::
 
  this is not a command due to escaping rules: \~mycommand
  a command: ~begin
  a command within a sequence of letters abc~{begin}def
  a command with parameters: ~for(x in range(0,3))

Note that in the last line, since the parameter of the "for" command must be a
valid python expression, all opening brackets in that expression must match a
closing bracket. By this rule pyexpander is able to find the closing bracket
that belongs to the opening bracket of the parameter list.

Executing python statements
+++++++++++++++++++++++++++

A statement may be any valid python code. Statements usually do not return
values. All expressions are statements, but not all statements are 
expressions. In order to execute python statements, there is the "py" command.
"py" is an abbreviation of python. This command expects that valid python code
follows enclosed in brackets. Note that the closing bracket for "py" *must not*
be in the same line with a python comment, since a python comment would include
the bracket and all characters until the end of the line, leading to a
pyexpander parser error. The "py" command leads to the execution of the python
code but produces no output. It is usually used to define variables, but it can
also be used to execute python code of more complexity. Here are some
examples::

  Here we define the variable "x" to be 1: ~py(x=1)
  Here we define two variables at a time: ~py(x=1;y=2)
  Here we define a function, note that we have to keep
  the indentation that python requires intact:
  ~py(
  def multiply(x,y):
      return x*y
      # here is a python comment
      # note that the closing bracket below
      # *MUST NOT* be in such a comment line
     )

Line continuation
+++++++++++++++++

Since the end of line character is never part of a command, commands placed on
a single line would produce an empty line in the output. Since this is
sometimes not wanted, the generation of an empty line can be suppressed by
ending the line with a single backslash "\\". Here is an example::

  ~py(x=1;y=2)\
  The value of x is ~(x), the value of y is ~(y).
  Note that no leading empty line is generated in this example.

If you have an application that would always require backslashes at the end of
commands you can start the expander script with option "-a". This has the same
effect as appending a backslash to each line that ends with a command. See also
:doc:`expander-options`.

So with "-a" you expander script does not have to look look like this::

  ~py(
  a=True
  )\
  Here is a conditional:
  ~if(a)\
  a was True
  ~else\
  a was False
  ~endif\

but like this::

  ~py(
  a=True
  )
  Here is a conditional:
  ~if(a)
  a was True
  ~else
  a was False
  ~endif

Substitutions
+++++++++++++

A substitution consists of a dollar "~" that is not preceded by a backslash and
followed by an opening round bracket "(" and a matching closing round bracket
")". The string enclosed by the pair of brackets must form a valid python
expression. Note that a python expression, in opposition to a python statement,
always has a value. This value is converted to a string and this string is
inserted in the text in place of the substitution command. Here is an example::

  ~py(x=2) we set "x" to 2 here
  now we can replace "x" anywhere in the text
  like here ~(x) since "x" alone is already a python expression.
  Note that the argument of "py" is a python statement.
  We can also insert x times 3 here like this: ~(x*3). 
  We can even do calculations like: ~(x*sin(x)).

There is also a mode called "simple vars" in the expander tool, where the round
brackets around variable names may be omitted. Note that this is not possible
for arbitrary python expressions, since pyexpander would not know where the
expression ends without the brackets. Here is an example::

  We define x: ~py(x=1)
  In "simple vars" mode, we can use the variable as we know
  it: ~(x) but also without brackets: ~x. However, expressions that are
  not simple variable names must still use brackets: ~(x*2).

Default values for variables
++++++++++++++++++++++++++++

When an undefined variable is encountered, pyexpander raises a python exception
and stops. Sometimes however, we want to take a default value for a variable
but only if it has not yet been set with a value. This can be achieved with the
"default" command.  This command must be followed by an opening bracket and an
arbitrary list of named python parameters. This means that each parameter
definition consists of an unquoted name, a "=" and a quoted string, several
parameter definitions must be separated by commas. The "default" command takes
these parameters and sets the variables of these names to the given values if
the variables are not yet set with different values. Here is an example::

  We define a: ~py(a=1)
  Now we set a default for a and b: ~default(a=10, b=20)
  Here, ~(a) is 1 since is was already defined before
  and ~(b) is 20, it's default value since it was not defined before.

Variable scopes
+++++++++++++++

By default, all variables defined in a "py" command are global. They exist from
the first time they are mentioned in the text and can be modified at any place
further below.  Sometimes however, it is desirable to set a variable in a
certain area of the text and restore it to it's old value below that area. In
order to do this, variable scopes are used. A variable scope starts with a
"begin" command and ends with an "end" command. All variable definitions and
changes between "begin" and "end" are reverted when the "end" command is
reached. Some commands like "for", "while" and "include" have a variant with a
"_begin" appended to their name, where they behave like "begin" and "end" and
define a variable scope additionally to their normal function. Here is an
example of "begin" and "end"::
  
  ~py(a=1)
  a is now 1
  ~begin
  ~py(a=2)
  a is now 2
  ~end
  here, a is 1 again

All variable modifications and definitions within a variable scope are isolated
from the rest of the text. However, sometimes we want to modify variables
outside the scope. This can be done by declaring a variable as non-local with
the command "nonlocal". The "nonlocal" command must be followed by a comma
separated list of variable names enclosed in brackets. When the end of the
scope is reached, all variables that were declared non-local are copied to the
outer scope. Here is an example::

  ~py(a=1;b=2;c=3)
  a is now 1, b is 2 and c is 3
  ~begin
  ~nonlocal(a,b)
  ~py(a=10;b=20;c=30)
  a is now 10, b is 20 and c is 30
  ~end
  here, a is 10, b is 20 and c is 3 again

If scopes are nested, the "nonlocal" defines a variable to be non-local only in
the current scope. If the current scope is left, the variable is local again
unless it is defined non-local in that scope, too.

Extending the pyexpander language
+++++++++++++++++++++++++++++++++

All functions or variables defined in a "~py" command have to be applied in the
text by enclosing them in brackets and prepending a dollar sign like here::

  ~(myvar)
  ~(myfunction(parameters))

However, sometimes it would be nice if we could use these python objects a bit
easier. This can be achieved with the "extend" or the "extend_expr" command.
"extend" expects to be followed by a comma separated list of identifiers
enclosed in brackets. "extend_expr" must be followed by a python expression
that is an iterable of strings. The identifiers can then be used in the text
without the need to enclose them in brackets. Here is an example::

  ~extend(myvar,myfunction)
  ~myvar
  ~myfunction(parameters)

Note that identifiers extend the pyexpander language local to their scope. Here
is an example for this::

  ~py(a=1)
  ~begin
  ~extend(a)
  we can use "a" here directly like ~a
  ~end
  here the "extend" is unknown, a has always
  to be enclosed in brackets like ~(a)

You should note that with respect to the "extend" command, there is a
difference between including a file with the "include" command or the
"include_begin" command (described further below). The latter one defines a
new scope, and the rule shown above applies here, too.

Conditionals
++++++++++++

A conditional part consists at least of an "if" and an "endif" command. Between
these two there may be an arbitrary number of "elif" commands. Before "endif"
and after the last "elif" (if present) there may be an "else" command. "if" and
"elif" are followed by a condition expression, enclosed in round brackets.
"else" and "endif" do not have parameters. If the condition after "if" is true,
this part is evaluated. If it is false, the next "elif" part is tested. If it
is true, this part is evaluated, if not, the next "elif" part is tested and so
on. If no matching condition was found, the "else" part is evaluated. All of
this is oriented on the python language which also has "if","elif" and "else".
"endif" has no counterpart in python since there the indentation shows where
the block ends. Here is an example::

  We set x to 1; ~py(x=1)
  ~if(x>2)
  x is bigger than 2
  ~elif(x>1)
  x is bigger than 1
  ~elif(x==1)
  x is equal to 1
  ~else
  x is smaller than 1
  ~endif
  here is a classical if-else-endif:
  ~if(x>0)
  x is bigger than 0
  ~else
  x is not bigger than 0
  ~endif
  here is a simple if-endif:
  ~if(x==0)
  x is zero
  ~endif

While loops
+++++++++++

While loops are used to generate text that contains almost identical
repetitions of text fragments. The loop continues while the given loop
condition is true. A While loop starts with a "while" command followed by a
boolean expression enclosed in brackets. The end of the loop is marked by a
"endwhile" statement. Here is an example::

  ~py(a=3)
  ~while(a>0)
  a is now: ~(a)
  ~py(a-=1)
  ~endwhile

In this example the loop runs 3 times with values of a ranging from 3 to 1. 

The command "while_begin" combines a while loop with a scope::

  ~while_begin(condition)
  ...
  ~endwhile
  
and::

  ~while(condition)
  ~begin
  ...
  ~end
  ~endwhile

are equivalent. 
  
For loops
+++++++++

For loops are a powerful tool to generate text that contains almost identical
repetitions of text fragments. A "for" command expects a parameter that is a
python expression in the form "variable(s) in iterable". For each run the
variable is set to another value from the iterable and the following text is
evaluated until "endfor" is found. At "endfor", pyexpander jumps back to the
"for" statement and assigns the next value to the variable. Here is an
example::

  ~for(x in range(0,5))
  x is now: ~(x)
  ~endfor

The range function in python generates a list of integers starting with 0 and
ending with 4 in this example. 

You can also have more than one loop variable::

  ~for( (x,y) in [(x,x*x) for x in range(0,3)])
  x:~(x) y:~(y)
  ~endfor

or you can iterate over keys and values of a python dictionary::

  ~py(d={"A":1, "B":2, "C":3})
  ~for( (k,v) in d.items())
  key: ~(k) value: ~(v)
  ~endfor

The command "for_begin" combines a for loop with a scope::

  ~for_begin(loop expression)
  ...
  ~endfor
  
and::

  ~for(loop expression)
  ~begin
  ...
  ~end
  ~endfor

are equivalent. 

macros
++++++

Macros provide a way to group parts of your scripts and reuse them at other
places. Macros can have arguments that provide values when the macro is
instantiated. You can think of a macro as a way to copy and paste a part of
your script to a different location. Note that a macro invocation must always
be followed by a pair of brackets, even if the macro doesn't get any arguments.

Here is an example::

  ~macro(snippet)
  This is a macro that just 
  adds some text.
  ~endmacro
  \
  ~macro(underline, line)
  ~(line)
  ~("-" * len(line))
  ~endmacro
  \
  ~underline("My heading")
  ~snippet()

If you run this with expander.py or expander2.py with option -a (see 
`Line continuation`_), this is the output::

  My heading
  ----------
  This is a macro that just 
  adds some text.

Arguments to macros are given the same way as in python, except you cannot use
default values for arguments.

With option -i (see :doc:`expander-options`) pyexpander indents lines according to the row where the macro invocation was placed. Here is an example::

  ~macro(subsnippet)
  This is another
  snippet.
  ~endmacro
  \
  ~macro(snippet)
  This is a macro that just 
  adds some text and contains
  a subsnippet from here
      ~subsnippet()
  to here.
  Snippet end.
  ~endmacro
  \
  ~macro(underline, line)
  ~(line)
  ~("-" * len(line))
  ~endmacro
  \
  ~underline("My heading")
      ~snippet()

If you run this with expander.py or expander2.py with option -a and -i,
you get the following output::

  My heading
  ----------
      This is a macro that just 
      adds some text and contains
      a subsnippet from here
          This is another
          snippet.
      to here.
      Snippet end.

As you see, the text of the macro has the same indentation level as the macro
itself. This is also true for macros that contain other macros.

Include files
+++++++++++++

The "include" command is used to include a file at the current position. It
must be followed by one string or two strings (or string expressions) enclosed
in brackets. 

The first string is always a filename, the optional second string is the
encoding of the file, e.g. "utf-8" or "iso8859-1". Valid encoding names can be
looked up here: 

`python encodings <https://docs.python.org/3/library/codecs.html#standard-encodings>`_.

The given file is then interpreted until the end of the file is reached, then
the interpretation of the text continues after the "include" command in the
original text.

Here is an example without an explicit encoding::

  ~include("additional_defines.inc")

and here is an example for an iso8859 encoded include file::

  ~include("additional_defines-iso.inc", "iso8859")

The command "include_begin" combines an include with a scope. It is equivalent
to the case when the include file starts with a "begin" command and ends with
an "end" command.

Here is an example::

  ~include_begin("additional_defines.inc")

Safe mode
+++++++++

The "safemode" command enables restrictions on commands. You start the safe
mode like this::

  ~safemode

The following features of pyexpander are disabled in safe mode and stop the
program::

- ``~(EXPRESSION)``
- ``~py(...)``
- ``~extend(...)``
- ``~extend_expr(...)``

Note that ``~(VARIABLENAME)`` can still be used. 

The safe mode can only be switched on, there is no command to switch it off. It
is, however, only active within the current variable scope (see `Variable
scopes`_) as shown here::

  ~begin
  ~safemode
  ~# here safemode is on
  ~end
  ~# here safemode is off

Commands for EPICS macro substitution
+++++++++++++++++++++++++++++++++++++

`EPICS <http://www.aps.anl.gov/epics>`_ is a framework for building control
systems. pyexpander has three more commands for this application, that
are described here:

:doc:`EPICS support in pyexpander <epics-support>`.

Internals
---------

This section describes how pyexpander works. 

pyexpander consists of the following parts:

pyexpander.parser
+++++++++++++++++

A python module that implements a parser for expander files. This is the
library that defines all functions and classes the are used for 
pyexpander.

Here is a link to the :py:mod:`pyexpander.parser`.

pyexpander.lib
++++++++++++++

A python module that implements all the functions needed to 
implement the pyexpander language.

Here is a link to the :py:mod:`pyexpander.lib`.

Scripts provided by the package
-------------------------------

expander.py
+++++++++++

This script is used for macro substitution in text files. They have
command line options for search paths and file names and use pyexpander 
to interpret the given text file.

You will probably just use one of these for your application. However, you
could write a python program yourself that imports and uses the pyexpander
library.

Here is a link to the `expander.py command line options <expander-options.html>`_.

Note that if you installed the python 2 version of pyexpander, this script is
called "expander2.py" instead. (Note that python 2 support is deprecated).

msi2pyexpander.py
+++++++++++++++++

This script is used to convert `EPICS <http://www.aps.anl.gov/epics>`_ `msi
<http://www.aps.anl.gov/epics/extensions/msi/index.php>`_ template files to the
format of pyexpander. You only need this script when you have an `EPICS
<http://www.aps.anl.gov/epics>`_ application and want to start using pyexpander
for it.

Here is a link to the `command line options of msi2pyexpander.py
<msi2pyexpander-options.html>`_.

Note that if you installed the python 2 version of pyexpander, this script is
called "msi2pyexpander2.py" instead. (Also note that python 2 support is
deprecated).

