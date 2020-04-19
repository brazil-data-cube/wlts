..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============

WLTS implementation depends essentially on:

- `Flask <https://palletsprojects.com/p/flask/>`_

- `SQLAlchemy <https://www.sqlalchemy.org/>`_

- `GDAL <https://gdal.org/>`_ ``(Version 2+)``


Development Installation
------------------------

Clone the software repository:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wlts.git


Go to the source code folder:

.. code-block:: shell

     $ cd wlts


Install in development mode:

.. code-block:: shell

    $ pip3 install -e .[all]

.. note::

    | If you have problems during the GDAL Python package installation, please, make sure to have the GDAL library support installed in your system with its command line tools.
    |
    | You can check the GDAL version with:
    | ``$ gdal-config --version``.
    |
    | Then, if you want to install a specific version (example: 2.4.2), try:
    | ``$ pip install "gdal==2.4.2"``
    |
    | If you still having problems with GDAL installation, you can generate a log in order to check what is happening with your installation. Use the following ``pip`` command:
    | ``$ pip install --verbose --log my.log "gdal==2.4.2"``
    |
    | For more information, see [#f1]_ e [#f2]_.


Generate the documentation:

.. code-block:: shell

    $ python setup.py build_sphinx


Running in Development Mode
---------------------------

In the source code folder, enter the following command:

.. code-block:: shell

    $ FLASK_APP="wlts" \
      FLASK_ENV="development" \
      SQLALCHEMY_URI="postgresql://user:password@localhost:5432/dbname" \
      WLTS_URL="http://localhost:5000" \
      flask run

You may need to replace the definition of some environment variables:

  - ``FLASK_ENV="development``: used to tell Flask to run in `Debug` mode.

  - ``WLTS_URL="http://localhost:5000"``: Base URI of the service.

  - ``SQLALCHEMY_URI="postgresql://user:password@localhost:5432/dbname"``: The database URI to be used.


The above command should output some messages in the console as showed below:

.. code-block:: shell

     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 184-616-293


.. rubric:: Footnotes

.. [#f1]

    During GDAL installation, if you have a build message such as the one showed below:

    .. code-block::

        Skipping optional fixer: ws_comma
        running build_ext
        building 'osgeo._gdal' extension
        creating build/temp.linux-x86_64-3.7
        creating build/temp.linux-x86_64-3.7/extensions
        x86_64-linux-gnu-gcc -pthread -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g -fstack-protector-strong -Wformat -Werror=format-security -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2 -fPIC -I../../port -I../../gcore -I../../alg -I../../ogr/ -I../../ogr/ogrsf_frmts -I../../gnm -I../../apps -I/home/gribeiro/Devel/github/brazil-data-cube/wtss/venv/include -I/usr/include/python3.7m -I. -I/usr/include -c extensions/gdal_wrap.cpp -o build/temp.linux-x86_64-3.7/extensions/gdal_wrap.o
        extensions/gdal_wrap.cpp:3168:10: fatal error: cpl_port.h: No such file or directory
         #include "cpl_port.h"
                  ^~~~~~~~~~~~
        compilation terminated.
        error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
        Running setup.py install for gdal ... error
        Cleaning up...

    You can instruct ``pip`` to look at the right place for header files when building GDAL:

    .. code-block:: shell

        $ C_INCLUDE_PATH="/usr/include/gdal" \
          CPLUS_INCLUDE_PATH="/usr/include/gdal" \
          pip install "gdal==2.4.2"


.. [#f2]

    On Linux Ubuntu 18.04 LTS you can install GDAL 2.4.2 from the UbuntuGIS repository:

    1. Create a file named ``/etc/apt/sources.list.d/ubuntugis-ubuntu-ppa-bionic.list`` and add the following content:

    .. code-block:: shell

        deb http://ppa.launchpad.net/ubuntugis/ppa/ubuntu bionic main
        deb-src http://ppa.launchpad.net/ubuntugis/ppa/ubuntu bionic main


    2. Then add the following key:

    .. code-block:: shell

        $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6B827C12C2D425E227EDCA75089EBE08314DF160


    3. Then, update your repository index:

    .. code-block:: shell

        $ sudo apt-get update


    4. Finally, install GDAL:

    .. code-block:: shell

        $ sudo apt-get install libgdal-dev=2.4.2+dfsg-1~bionic0
