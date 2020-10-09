..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


.. role:: raw-html(raw)
    :format: html

===========================
Web Land Trajectory Service
===========================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/wlts/blob/master/LICENSE
        :alt: Software License

.. image:: https://travis-ci.org/brazil-data-cube/wlts.svg?branch=master
        :target: https://travis-ci.org/brazil-data-cube/wlts
        :alt: Build Status

.. image:: https://coveralls.io/repos/github/brazil-data-cube/wlts/badge.svg?branch=master
        :target: https://coveralls.io/github/brazil-data-cube/wlts?branch=master
        :alt: Code Coverage Test

.. image:: https://readthedocs.org/projects/wlts-server/badge/?version=latest
        :target: https://wlts-server.readthedocs.io/en/latest/
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle

.. image:: https://img.shields.io/github/tag/brazil-data-cube/wlts.svg/
        :target: https://github.com/brazil-data-cube/wlts/releases
        :alt: Release

.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====

Land Use and Cover information is essential to support governments in decision making on the impact of human activities on the environment, for planning the use of natural resources, conservation of biodiversity, and monitoring climate change.


Currently, several projects systematically provide information on the dynamics of land use and cover. Well known projects include PRODES, DETER and TerraClass. These projects are developed by INPE and they produce information on land use and coverage used by the Brazilian Government to make public policy decisions. Besides these projects there are other initiatives from universities and space agencies devoted to the creation of national and global maps.


Although these projects adhere to open data policies and provide a rich collection of data, there are still a gap however in tools that facilitate the integrated use of these collections: *it requires from researchers, students and public officials a great effort to collect, organize and integrate all the datasets, prior to their use*. In general, each data collection adopts its own land use and cover classification system, with class names and meanings very different across the collections. Besides that, the collections have different spatial and temporal resolutions, rely on different data representation (raster or vector), and are served by different systems in several formats (files, DBMS or web services).


In this context, the **W**\ eb **L**\ and **T**\ rajectory **S**\ ervice (WLTS) is a service that aims to facilitate the access to these various land use and cover data collections through a tailored API. The result is tool that allows researchers and specialists to spend their time in the analytical process, once the API provides the integration of these datasets and brings the concept of Land Use and Cover Trajectories as a high level abstraction. The WLTS approach is to use a data model that defines a minimum set of temporal and spatial information to represent different sources and types of data. WLTS can be used in a range of application, such as in validation of land cover data sets, in the selection of trainning samples to support Machine Learning algorithms used in the generation of new classification maps.


For more information on WLTS, see:

- `WLTS Specification <https://github.com/brazil-data-cube/wlts-spec>`_: the WLTS specification using `OpenAPI 3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`_ notation.

- `WLTS.py <https://github.com/brazil-data-cube/wlts.py>`_: Python Client Library for Web Land Cover Trajectory Service.

- `LCCS-WS Specification <https://github.com/brazil-data-cube/lccs-ws-spec>`_: which is used to represent the classes associated with the resources retrieved in WLTS queries.

- `LCCS.py <https://github.com/brazil-data-cube/lccs.py>`_: Python Client Library for Land Cover Classification System Web Service.

- `LCCS Server <https://github.com/brazil-data-cube/lccs-ws>`_: Python Web Server for LCCS.


Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.


Deploying
=========

See `DEPLOY.rst <./DEPLOY.rst>`_.


License
=======

.. admonition::
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
