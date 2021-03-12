..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2020-2021 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============

WLTS implementation depends essentially on:

- `Flask <https://palletsprojects.com/p/flask/>`_

- `SQLAlchemy <https://www.sqlalchemy.org/>`_

- `OWSLib <https://www.osgeo.org/projects/owslib/>`_

- `Rasterio <https://rasterio.readthedocs.io/en/latest/>`_



Development Installation - GitHub
---------------------------------

Clone the Software Repository
+++++++++++++++++++++++++++++

Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/wlts.git


Go to the source code folder::

    cd wlts


Install in development mode::

    pip3 install -e .[all]

.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    **1.** Create a new virtual environment linked to Python 3.7::

        python3.7 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools

    Or you can use Python Anaconda Environment:

    **1.** Create an virtual environment using conda with Python Interpreter Version +3::

        conda create --name bdc_wlts python=3

    **2.** Activate environment::

        conda activate bdc_wlts

Run the Tests
+++++++++++++

Run the tests::

    ./run-tests.sh


Build the Documentation
+++++++++++++++++++++++

Generate the documentation::

    python setup.py build_sphinx

The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/

You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html


Running in Development Mode
---------------------------

In the source code folder, enter the following command::

    FLASK_APP="wlts" \
    FLASK_ENV="development" \
    WLTS_URL="http://localhost:5000" \
    flask run

You may need to replace the definition of some environment variables:

  - ``FLASK_ENV="development``: used to tell Flask to run in `Debug` mode.

  - ``WLTS_URL="http://localhost:5000"``: Base URI of the service.

The above command should output some messages in the console as showed below::

     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 184-616-293


Running WLTS with a real data
-----------------------------

We will use **DETER Amazônia Legal** data to present how to configure and use WLTS to recover trajectories.
For this we use the data available by `TerraBrasilis <http://terrabrasilis.dpi.inpe.br/>`_ via GeoServer

In ``wlts/json_configs/datasources.json`` file the necessary settings must be added:

.. code-block:: js

     "datasources": {
        "webservice_source": [
          {
            "type": "WFS",
            "id": "3c20cbb4-ca94-4c1f-99af-6377f30bc683",
            "host": "http://terrabrasilis.dpi.inpe.br/geoserver",
            "workspace": "deter-amz"
          }
        ]
      }

You may need to replace definition of some information about database you loaded example data:

  - ``"type": "WFS"``: The Web Service Type (WCS or WFS).
  - ``"id": "3c20cbb4-ca94-4c1f-99af-6377f30bc683"``: unique identifier to identify the datasource.
  - ``"host"``: Geoserver data address.
  - ``"workspace": "deter-amz"``: the wokspace name containing the DETER data.

In ``wlts/json_configs/collections.json`` file the necessary settings must be added for accessing the collection :


If you want to check if the system is up and running, try the following URL in your web browser:

* http://localhost:5000/wlts/list_collections


You should see an output like:

.. code-block:: js

    {
      "collections": [
        "deter_amz"
      ]
    }


* http://localhost:5000/wlts/describe_collection?collection_id=deter_amz

.. code-block:: js

    {
      "classification_system": {
        "classification_system_id": null,
        "classification_system_name": null,
        "type": "Self"
      },
      "collection_type": "Feature",
      "description": "Alertas de Desmatamento",
      "detail": "http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/deter",
      "name": "deter_amz",
      "period": {
        "end_date": "2017",
        "start_date": "2006"
      },
      "resolution_unit": {
        "unit": "DAY",
        "value": "1"
      },
      "spatial_extent": {
        "xmax": -44.0003914444064,
        "xmin": -73.5490878282397,
        "ymax": 4.55537642867927,
        "ymin": -18.0364406523564
      }
    }


* http://localhost:5000/wlts/trajectory?latitude=-9.091&longitude=-66.031

.. code-block:: js

    {
      "query": {
        "collections": null,
        "end_date": null,
        "latitude": -9.091,
        "longitude": -66.031,
        "start_date": null
      },
      "result": {
        "trajectory": [
          {
            "class": "DEGRADACAO",
            "collection": "deter_amz",
            "date": "2016-10-06Z"
          }
        ]
        }
    }
