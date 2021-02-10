..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2019-2020 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Deploying
=========

WLTS implementation depends essentially on:

- `Flask <https://palletsprojects.com/p/flask/>`_

- `SQLAlchemy <https://www.sqlalchemy.org/>`_


Requeriments
------------

Building the Docker Image
-------------------------

On the command line use the `docker build` command to create the docker image for the service:

.. code-block:: shell

        $ docker build -t wlts:0.2.0 . --no-cache

The above command will create a Docker image named `wlts` and tag `0.2.0`, as one can see with the `docker images` command:

.. code-block:: shell

        $ docker images

        REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
        wlts                                              0.2.0             ce2ba6a67896        16 hours ago          1.25GB

Preparing the Network for Containers
------------------------------------

If you have the PostgreSQL server running in a Docker container and you want to have it accesible to the WLTS, you can create a Docker network and attach your PostgreSQL container to it [#f1]_.

To create a new network, you ca use the `docker network` command:

.. code-block:: shell

        $ docker network create bdc_net


The above command will create a network named `bdc_net`. Now, it is possible to attach your database container in this network:

.. code-block:: shell

        $ docker network connect bdc_net bdc_pg


In the above command, we are supposing that your database container is named `bdc_pg`.


.. rubric:: Footnotes

.. [#f1] If you have a valid address for the PostgreSQL DBMS you can skip this section.

Launching the Docker Container with the WLTS
-----------------------------------------------

The `docker run` command can be used to launch a container from the image `wlts:0.2.0-0`. The command below shows an example on how to accomplish the launch of a container:

.. code-block:: shell

        $ docker run --detach \
             --name wlts \
             --publish 127.0.0.1:5000:5000 \
             --network=bdc_net \
             --env SQLALCHEMY_DATABASE_URI="postgresql://user:password@localhost:5432/dbname" \
             --env WLTS_URL="http://localhost:5000" \
             wlts:0.2.0-0

Let's take a look at each parameter in the above command:/

    - ``--detach``: tells Docker that the container will run in background (daemon).

    - ``--name wlts``: names the container.

    - ``--publish 127.0.0.1:5000:5000``: by default the WLTS will be running on port ``5000`` of the container. You can bind a host port, such as ``8080`` to the container port ``5000``.

    - ``--network=bdc_net``: if the container should connect to the database server through a docker network, this parameter will automatically attach the container to the ``bdc_net``. You can ommit this parameter if the database server address can be resolved directly from a host address.

    - ``--env SQLALCHEMY_DATABASE_URI="postgresql://user:password@localhost:5432/dbname"``: The database URI to be used [#f1]_.

    - ``--env WLTS_URL="http://localhost:5000"``: Base URI of the service.

    - ``wlts:0.2.0-0``: the name of the base Docker image used to create the container.

If you have launched the container, you can check if the service has initialized:

.. code-block:: shell

        $  docker logs wlts
         * Environment: production
           WARNING: This is a development server. Do not use it in a production deployment.
           Use a production WSGI server instead.
         * Debug mode: off
         * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Finally, to test if it is listening, use the ``curl`` command:

.. code-block:: shell

        $ curl localhost:5000/wlts/list_collections

        {"collections":["deter_amz"]}
