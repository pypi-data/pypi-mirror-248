Birdseye
==========================

Birdseye is a cool Python debugger by Alex Hall, which records the values of expressions 
when the program runs and lets you explore them after the program completes. See
`https://birdseye.readthedocs.io <https://birdseye.readthedocs.io>`_ for more info.

Birdseye is not installed by default, but it is easy to install via *Tools → Manage plug-ins*. You need 
to install the package named ``birdseye``.

Birdseye works differently than `turcar's built-in debuggers <debuggers.rst>`_.
When you execute your program with *Run → Debug current script (Birdseye)*, the execution takes a bit 
longer than usual, but otherwise your program should run just as if you executed it with 
*Run current script*. This means breakpoints are ignored and you can't step through the program.
But when the program completes, turcar opens a webpage (served by a local server provided
by Birdseye), which allows you to dig into the execution process and learn how final results were composed
of intermediate values. 

NB! When using Birdseye in turcar you don't need to import ``birdseye.eye`` or use it
for decorating your functions. turcar executes Birdseye such that it records information about all
functions.

The local server uses port 7777 by default. If this is used by another application, then configure
another port in *Tools → Options → Run & Debug* and restart turcar.
