..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2020-21 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=======
Changes
=======

Version 0.6.0 (2021-04-13)
--------------------------

- Add Drone integration (`#31 <https://github.com/brazil-data-cube/wlts/issues/31>`_).

- Bug fix: Validate the ``get_coverage`` return (`#35 <https://github.com/brazil-data-cube/wlts/issues/35>`_).

- Add automatic deploy on dev and production sites (`#39 <https://github.com/brazil-data-cube/wlts/issues/39>`_).

- Integration with Rasterio (`#30 <https://github.com/brazil-data-cube/wlts/issues/30>`_).

- Integration with OWSLib in WFS (`#29 <https://github.com/brazil-data-cube/wlts/issues/29>`_).

- Add geometry field in Trajectory (`#21 <https://github.com/brazil-data-cube/wlts/issues/21>`_).

- Review api tests (`#42 <https://github.com/brazil-data-cube/wlts/issues/42>`_).

- Support for the `WLTS specification version 0.6.0 <https://github.com/brazil-data-cube/wlts-spec>`_.

- Bug fix: Update Dockerfile Change app to create_app (`#46 <https://github.com/brazil-data-cube/wlts/issues/46>`_).

- Bug fix: Check for null returns in datasources (`#48 <https://github.com/brazil-data-cube/wlts/issues/48>`_).

- Bug fix: WFS get_class_system() does not exist (`#50 <https://github.com/brazil-data-cube/wlts/issues/50>`_).

Version 0.4.0-0 (2020-12-11)
----------------------------

- First experimental version.

- Support for OGC WFS and OGC WCS datasource.

- Support for vector and raster data.

- Documentation system based on Sphinx.

- Documentation integrated to ``Read the Docs``.

- Package support through Setuptools.

- Installation and use instructions.

- Travis CI support.

- Source code versioning based on `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- License: `MIT <https://raw.githubusercontent.com/brazil-data-cube/bdc-db/b-0.2/LICENSE>`_.