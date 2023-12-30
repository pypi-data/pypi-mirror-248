# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 11:18:38 2020

@author: Tyler King
"""

from .core import Spectrum, Series, RMSE, SpectralCorrelation, chiSquared, cat
from .spectra import PhotoSpectrum, RamanSpectrum, XRDSpectrum, CVSpectrum, XASSpectrum, XAFSSpectrum, XANESSpectrum, Chromatogram
from .series import PhotoSeries, RamanSeries, ConfocalSeries, XRDSeries, CVSeries, XASSeries, LCMSSeries
from .codecs import Horiba, BioLogic, MACCOR, Olis, Rigaku, Genesys, Athena, GSAS, LC, PeakFit, QAS, LCMS

name = "IESE Instruments"

# from .ref import h, h_bar, c, particle_masses, periodic_table

# from . import decomposition
