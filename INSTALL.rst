..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Installation
============

``wlts`` implementation depends essentially on `Flask <https://palletsprojects.com/p/flask/>`_, `SQLAlchemy <https://www.sqlalchemy.org/>`_ ..

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

  - ``SQLALCHEMY_URI="postgresql://user:password@localhost:5432/dbname"``: The database URI to be used

The above command should output some messages in the console as showed below:

.. code-block:: shell

     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 184-616-293