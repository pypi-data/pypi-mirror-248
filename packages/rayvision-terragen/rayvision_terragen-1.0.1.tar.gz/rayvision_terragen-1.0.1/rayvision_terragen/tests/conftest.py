# -*- coding=utf-8 -*-
"""The plugin of the pytest.

The pytest plugin hooks do not need to be imported into any test code, it will
load automatically when running pytest.

References:
    https://docs.pytest.org/en/2.7.3/plugins.html

"""
import os, sys
import pytest


@pytest.fixture()
def cg_file_h(tmpdir):
    """Get render config."""
    return {
        'cg_file': str(tmpdir.join('muti_layer_test.tgd'))
    }


@pytest.fixture()
def terragen(tmpdir):
    """Create an terragen object fixture."""
    from rayvision_terragen.analyze_terragen import AnalyzeTerragen
    if "win" in sys.platform.lower():
        os.environ["USERPROFILE"] = str(tmpdir)
    else:
        os.environ["HOME"] = str(tmpdir)
    analyze_terragen = AnalyzeTerragen(str(tmpdir), "17.5.293")
    return analyze_terragen
