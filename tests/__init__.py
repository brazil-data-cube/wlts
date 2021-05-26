#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Test module."""

import pytest

if __name__ == "__main__":
    from tests_wlts.test_app import TestWLTS

    pytest.main(["--color=auto", "--no-cov", "-v"])
