# -*- coding=utf-8 -*-
"""The plugin of the pytest.

The pytest plugin hooks do not need to be imported into any test code, it will
load automatically when running pytest.

References:
    https://docs.pytest.org/en/2.7.3/plugins.html

"""

import pytest

from rayvision_utils.exception.exception import CGFileNotExistsError
from rayvision_terragen.analyze_terragen import AnalyzeTerragen
from unittest import mock

def test_check_local_os(terragen):
    """Test check_local_os function."""
    mock_return = "win"
    terragen.check_local_os = mock.Mock(return_value=mock_return)
    result = terragen.check_local_os()
    assert result == "win"

# def test_get_save_version(terragen, cg_file_h):
#     """Test get_save_version function."""
#     # result = houdini.get_save_version(cg_file_h["cg_file"])
#     with pytest.raises(CGFileNotExistsError):
#         terragen.get_save_version(cg_file_h["cg_file"])

# def test_find_location(terragen, mocker, tmpdir):
#     """Test find_location action """
#     mocker_cg_file = mocker.patch.object(AnalyzeTerragen, 'find_location')
#     mocker_cg_file.return_value = tmpdir.join('muti_layer_test.tgd')
#     assert terragen.find_location() == str(tmpdir.join('muti_layer_test.tgd'))
