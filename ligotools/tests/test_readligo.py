import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ligotools import readligo as rl
import pytest

def test_loaddata_returns_expected_shapes():
    fn_H1 = "data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    strain, time, chan_dict = rl.loaddata(fn_H1, 'H1')
    assert len(strain) == len(time)
    assert isinstance(chan_dict, dict)

def test_loaddata_missing_file():
    result = rl.loaddata("data/fakefile.hdf5", 'H1')
    assert result == (None, None, None), "Expected None outputs for missing file"
