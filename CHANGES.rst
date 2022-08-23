..
    This file is part of Web Land Trajectory Service.
    Copyright (C) 2020-21 INPE.

    Web Land Trajectory Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


=======
Changes
=======

Version 0.9.3 (2022-08-03)
--------------------------

- Bug Fix: Remove Z in date (`#79 <https://github.com/brazil-data-cube/wlts/issues/87>`_).

- Add the layers title in describe collection operation (`#90 <https://github.com/brazil-data-cube/wlts/issues/90>`_).

- Bug Fix: In get trajectory for multiples properties in Feature Collection (`#92 <https://github.com/brazil-data-cube/wlts/issues/92>`_).


Version 0.9.2 (2022-04-29)
--------------------------

- Adding datasource informations in describe operation (`#79 <https://github.com/brazil-data-cube/wlts/issues/79>`_).
- Separate temporal properties according to each date type in the collection (`#83 <https://github.com/brazil-data-cube/wlts/issues/83>`_).
- Add external host information (`#81 <https://github.com/brazil-data-cube/wlts/issues/81>`_)


Version 0.9.1 (2022-03-23)
--------------------------

- Remove OWSLib package (`#71 <https://github.com/brazil-data-cube/wlts/issues/71>`_).
- Bug fix: cannot import name 'soft_unicode' from 'markupsafe' (`#70 <https://github.com/brazil-data-cube/wlts/issues/70>`_).
- Add the title information in collection (`#69 <https://github.com/brazil-data-cube/wlts/issues/69>`_).
- Refactor the organization of datasets (`#72 <https://github.com/brazil-data-cube/wlts/issues/72>`_).
- Remove mandatory BDC Auth access token in operations (`#74 <https://github.com/brazil-data-cube/wlts/issues/74>`_).

Version 0.9.0 (2021-12-08)
--------------------------

- Add multiple layers to collection (`#65 <https://github.com/brazil-data-cube/wlts/issues/65>`_).
- Add deprecated information in describe collection (`#64 <https://github.com/brazil-data-cube/wlts/issues/64>`_).
- Add CORS properties (`#67 <https://github.com/brazil-data-cube/wlts/issues/67>`_).


Version 0.8.0 (2021-09-30)
--------------------------

- Add integration with BDC-Auth (`#53 <https://github.com/brazil-data-cube/wlts/issues/53>`_).
- Improve unittests (`#60 <https://github.com/brazil-data-cube/wlts/issues/60>`_).
- Review the configuration files (`#57 <https://github.com/brazil-data-cube/wlts/issues/57>`_).
- Fix invalid keyword label in WCS response object (`#61 <https://github.com/brazil-data-cube/wlts/issues/61>`_).
- Upgrade library to provide OAuth2 client integration to 0.2.3 (`#56 <https://github.com/brazil-data-cube/wlts/issues/56>`_).


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
