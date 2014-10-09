
import numpy as _np
from scipy import signal as _signal

import misfit

def wtime(wsyn,wobs,nt,dt):
    # cross correlation traveltime
    # (Tromp et al. 2005, eq 45)
    wadj = _np.zeros(nt)
    wadj[1:-1] = (wsyn[2:] - wsyn[0:-2])/(2.*dt)
    wadj *= 1./(sum(wadj*wadj)*dt)
    wadj *= misfit.wtime(wsyn,wobs,nt,dt)
    return wadj

def wampl(wsyn,wobs,nt,dt):
    # cross correlation amplitude
    wadj = 1./(sum(wsyn*wsyn)*dt) * wsyn
    wadj *= misfit.wampl(wsyn,wobs,nt,dt)
    return wadj

def wdiff(wsyn,wobs,nt,dt):
    # waveform difference
    # (Tromp et al. 2005, eq 9)
    wadj = wsyn - wobs
    return wadj

def etime(wsyn,wobs,nt,dt):
    raise NotImplementedError

def ediff(wsyn,wobs,nt,dt,eps=0.05):
    # envelope difference
    esyn = abs(_signal.hilbert(wsyn))
    eobs = abs(_signal.hilbert(wobs))
    wadj = - (esyn - eobs)/(esyn + eps*esyn.max())
    return wadj

def cdiff(wsyn,wobs,nt,dt):
    # cross correlation difference
    cdiff = _np.correlate(wobs,wsyn) - _np.correlate(wobs,wobs)
    wadj = _np.convolve(wobs,cdiff)
    return 1e-10 * wadj

