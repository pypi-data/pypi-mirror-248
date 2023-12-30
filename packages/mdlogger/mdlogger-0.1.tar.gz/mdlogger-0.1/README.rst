mdlogger
========

A python logger wrapper project. Write log in markdown.

Features
--------

Three kinds of logs files:

-  Full log: ``DEBUG`` level log, use file rotating handler for this
   kind of log.
-  Error log: ``ERROR`` level log, use file rotating handler for this
   kind of log.
-  One time log: ``NOTSET`` level log, use write mode for this kind of
   log. Refresh content every time.

File logs will look like this:

``module``.\ ``func()``::``file.py``:``8`` - 2023-12-30 06:18:27.709:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ERROR** [PID:``68207``:THREAD:``MainThread``]

.. code:: plaintext

   error message

--------------

Console output will look like this:

      INFO [68207:MainThread] ``module.func()`` - 2023-12-30
      06:18:27.709: log info

This is just a simple wrapper for python logging module to log in
markdown format. Just for personal use in small projects for now.
