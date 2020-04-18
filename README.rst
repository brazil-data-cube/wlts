..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


===========================
Web Land Trajectory Service
===========================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com//brazil-data-cube/wlts/blob/master/LICENSE

.. image:: https://img.shields.io/badge/build-todo-success
        :target: https://travis-ci.org/brazil-data-cube/wlts

.. image:: https://img.shields.io/badge/tests-0%20passed,%200%20failed-critical
        :target: https://travis-ci.org/brazil-data-cube/wlts

.. image:: https://coveralls.io/repos/github/brazil-data-cube/wlts/badge.svg?branch=master
        :target: https://coveralls.io/github/brazil-data-cube/wlts?branch=master

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental

.. image:: https://img.shields.io/github/tag/brazil-data-cube/wlts.svg
        :target: https://github.com/brazil-data-cube/wlts-spec/releases
        :alt: Release

.. image:: https://badges.gitter.im/brazil-data-cube/community.svg/
        :target: https://gitter.im/brazil-data-cube/community#
        :alt: Join the chat


This is the server application.

About
=====

Land Use and Cover information is essential to support governments in decision making on the impact of human activities on the environment, for planning the use of natural resources, conservation of biodiversity, and monitoring climate change.


Currently, several projects systematically provide information on the dynamics of land use and cover. Well known projects include PRODES, DETER and TerraClass. These projects are developed by INPE and they produce information on land use and coverage used by the Brazilian Government to make public policy decisions. Besides these projects there are other initiatives from universities and space agencies devoted to the creation of national and global maps.


Although these projects adhere to open data policies and provide a rich collection of data, there still a gap in the integrated use of these collections: it requires from researchers, students and public officials a great effort to collect, organize and integrate all the datasets, prior to their use. In general, each collection adopts its own land use and cover classification system, with class names and meanings very different across the collections. Besides that, the collections have diffrent spatial and temporalresolutions, relies on different data representation (raster or vector) and served by diffrent systems or formats (files, database or web services).


In this context, the **W**\ eb **L**\ and **T**\ rajectory **S**\ ervice (WLTS) is a service that aims to facilitate the access to these various "land use and cover" data collections through a tailored API. The result is tool that allows researchers and specialists to spend their time in the analytical process, once the API provides the integration of these datasets and brings the concept of Land Use and Cover Trajectories as a high level abstraction. The WLTS approach is to use a data model that defines a minimum set of temporal and spatial information to represent different sources and types of data. WLTS can be used in a range of application, such as in validation of land cover data sets, in the selection of trainning samples to support Machine Learning algorithms used in the generation of new classification maps.


Free and Open Source implementations based on this service can be found in the `wlts <https://github.com/brazil-data-cube/wlts>`_ (server) and `wlts.py <https://github.com/brazil-data-cube/wlts.py>`_ (Python client). See also the service **LCCS-WS** (**L**\ and **C**\ over **C**\ lassification **S**\ystem **W**\eb **S**\ ervice) (`LCCS-WS <https://github.com/brazil-data-cube/lccs-ws-spec>`_) which is used to represent the classes associated with the resources retrieved in the queries.


Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.


Deploying
=========

See `DEPLOY.rst <./DEPLOY.rst>`_.


Developer Documentation
=======================

**Under Development!**


License
=======

.. admonition::
    Copyright (C) 2019 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
