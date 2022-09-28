..
    This file is part of WLTS.
    Copyright (C) 2022 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.

Deploying
=========

WLTS implementation depends essentially on:

- `Flask <https://palletsprojects.com/p/flask/>`_

- `SQLAlchemy <https://www.sqlalchemy.org/>`_

- `OWSLib <https://www.osgeo.org/projects/owslib/>`_

- `Rasterio <https://rasterio.readthedocs.io/en/latest/>`_

- `JSONSchema <https://github.com/Julian/jsonschema>`_


Requirements
------------

Building the Docker Image
-------------------------

On the command line use the `docker build` command to create the docker image for the service::

    docker build -t wlts:0.6.0 . --no-cache

The above command will create a Docker image named `wlts` and tag `0.6.0`, as one can see with the `docker images` command::

        docker images

        REPOSITORY                                          TAG                 IMAGE ID            CREATED             SIZE
        wlts                                              0.6.0             ce2ba6a67896        16 hours ago          1.25GB


Preparing the Network for Containers
------------------------------------

If you have the PostgreSQL server running in a Docker container and you want to have it accesible to the WLTS, you can create a Docker network and attach your PostgreSQL container to it [#f1]_.

To create a new network, you ca use the `docker network` command::

        docker network create bdc_net


The above command will create a network named `bdc_net`. Now, it is possible to attach your database container in this network::

        docker network connect bdc_net bdc_pg


In the above command, we are supposing that your database container is named `bdc_pg`.


.. rubric:: Footnotes

.. [#f1] If you have a valid address for the PostgreSQL DBMS you can skip this section.

Launching the Docker Container with the WLTS
-----------------------------------------------

The `docker run` command can be used to launch a container from the image `wlts:0.6.0`. The command below shows an example on how to accomplish the launch of a container::

        docker run --detach \
             --name wlts \
             --publish 127.0.0.1:5000:5000 \
             --network=bdc_net \
             --env WLTS_URL="http://localhost:5000" \
             --env BDC_AUTH_CLIENT_ID=BDC_OAuth_ClientID \
             --env BDC_AUTH_CLIENT_SECRET=BDC_OAuth_ClientSecret \
             --env BDC_AUTH_ACCESS_TOKEN_URL=https://brazildatacube.dpi.inpe.br/dev/auth/v1/oauth/introspect \
             wlts:0.6.0

Let's take a look at each parameter in the above command:/

    - ``--detach``: tells Docker that the container will run in background (daemon).

    - ``--name wlts``: names the container.

    - ``--publish 127.0.0.1:5000:5000``: by default the WLTS will be running on port ``5000`` of the container. You can bind a host port, such as ``8080`` to the container port ``5000``.

    - ``--network=bdc_net``: if the container should connect to the database server through a docker network, this parameter will automatically attach the container to the ``bdc_net``. You can ommit this parameter if the database server address can be resolved directly from a host address.

    - ``--env WLTS_URL="http://localhost:5000"``: Base URI of the service.

    - ``--env BDC_AUTH_CLIENT_ID=BDC_OAuth_ClientID``: the OAuth 2 client id.

    - ``--env BDC_AUTH_CLIENT_SECRET=BDC_OAuth_ClientSecret``: the OAuth 2 client secret.

    - ``--env BDC_AUTH_ACCESS_TOKEN_URL=https://brazildatacube.dpi.inpe.br/dev/auth/v1/oauth/introspect``: OAuth 2 authentication url.

    - ``wlts:0.6.0``: the name of the base Docker image used to create the container.

If you have launched the container, you can check if the service has initialized::

        docker logs wlts

             * Environment: production
               WARNING: This is a development server. Do not use it in a production deployment.
               Use a production WSGI server instead.
             * Debug mode: off
             * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

Finally, to test if it is listening, use the ``curl`` command::

        curl localhost:5000/wlts/list_collections

        {"collections":["deter_amz"]}
