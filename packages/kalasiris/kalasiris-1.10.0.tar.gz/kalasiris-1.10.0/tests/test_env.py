#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the environment variables in the `kalasiris` package."""

# Copyright 2023, Ross A. Beyer (rbeyer@seti.org)
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

# import importlib
import os
import unittest


@unittest.skip("Only works if run individually.")
class WithoutEnv(unittest.TestCase):
    def test_without(self):
        with self.assertRaises(KeyError):
            if "ISISDATA" in os.environ:
                del os.environ["ISISDATA"]

            # print(os.environ)
            import kalasiris.kalasiris

            # importlib.import_module("kalasiris.kalasiris")
            # importlib.reload(kalasiris)
