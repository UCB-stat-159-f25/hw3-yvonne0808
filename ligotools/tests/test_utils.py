import sys, os
import numpy as np
from scipy.interpolate import interp1d

# make sure Python can find your ligotools package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from ligotools.utils import whiten, reqshift

def test_whiten_shape():
    """whiten() should return data with the same shape as input"""
    strain = np.random.randn(1000)
    freqs = np.linspace(0, 500, 501)
    psd_vals = np.ones_like(freqs)
    interp_psd = interp1d(freqs, psd_vals, fill_value="extrapolate")
    dt = 1/1024

    whitened = whiten(strain, interp_psd, dt)
    assert whitened.shape == strain.shape

def test_reqshift_length():
    """reqshift() should keep the same data length"""
    data = np.sin(2*np.pi*50*np.linspace(0, 1, 1024))
    shifted = reqshift(data, fshift=100, sample_rate=1024)
    assert len(shifted) == len(data)
