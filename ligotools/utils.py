# ligotools/utils.py
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
from scipy.fftpack import rfft, irfft

# --------------------------------------------------
# Whiten function
# --------------------------------------------------
def whiten(strain, interp_psd, dt):
    Nt = len(strain)
    freqs = np.fft.rfftfreq(Nt, dt)
    freqs1 = np.linspace(0, 2048, Nt // 2 + 1)

    # whitening: transform to freq domain, divide by asd, then transform back, 
    # taking care to get normalization right.
    hf = np.fft.rfft(strain)
    norm = 1./np.sqrt(1./(dt*2))
    white_hf = hf / np.sqrt(interp_psd(freqs)) * norm
    white_ht = np.fft.irfft(white_hf, n=Nt)
    return white_ht


# --------------------------------------------------
# Write WAV file function
# --------------------------------------------------
def write_wavfile(filename,fs,data):
    d = np.int16(data/np.max(np.abs(data)) * 32767 * 0.9)
    wavfile.write(filename,int(fs), d)



# --------------------------------------------------
# Frequency shift function
# --------------------------------------------------
def reqshift(data,fshift=100,sample_rate=4096):
    """Frequency shift the signal by constant
    """
    x = np.fft.rfft(data)
    T = len(data)/float(sample_rate)
    df = 1.0/T
    nbins = int(fshift/df)
    # print T,df,nbins,x.real.shape
    y = np.roll(x.real,nbins) + 1j*np.roll(x.imag,nbins)
    y[0:nbins]=0.
    z = np.fft.irfft(y)
    return z



import matplotlib.pyplot as plt


def plot_match_results(time, timemax, tevent, SNR, strain_whitenbp, template_match, 
                       det, eventname, plottype, datafreq, template_fft, d_eff, 
                       freqs, data_psd, fs, pcolor='r'):
    """
    Plot matched-filter SNR, whitened data, residuals, and frequency-domain PSD.
    
    Parameters
    ----------
    time : np.ndarray
        Time array for the detector data.
    timemax : float
        Time corresponding to the SNR peak.
    tevent : float
        Approximate event time.
    SNR : np.ndarray
        Signal-to-noise ratio array.
    strain_whitenbp : np.ndarray
        Whitened and band-passed strain data.
    template_match : np.ndarray
        Whitened, phase/time-aligned template.
    det : str
        Detector name ('H1' or 'L1').
    eventname : str
        Event name (e.g., 'GW150914').
    plottype : str
        File format for saving plots (e.g., 'png').
    datafreq, template_fft, d_eff, freqs, data_psd, fs : various
        Frequency-domain arrays and scaling factors for the PSD plots.
    pcolor : str, optional
        Plot color for the detector.
    """
    # ----- Plot SNR -----
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - timemax, SNR, pcolor, label=f"{det} SNR(t)")
    plt.grid(True)
    plt.ylabel("SNR")
    plt.xlabel(f"Time since {timemax:.4f}")
    plt.legend(loc="upper left")
    plt.title(f"{det} matched filter SNR around event")

    plt.subplot(2, 1, 2)
    plt.plot(time - timemax, SNR, pcolor, label=f"{det} SNR(t)")
    plt.grid(True)
    plt.ylabel("SNR")
    plt.xlim([-0.15, 0.05])
    plt.xlabel(f"Time since {timemax:.4f}")
    plt.legend(loc="upper left")
    plt.savefig(f"figures/{eventname}_{det}_SNR.{plottype}")

    # ----- Plot whitened strain vs template -----
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time - tevent, strain_whitenbp, pcolor, label=f"{det} whitened h(t)")
    plt.plot(time - tevent, template_match, "k", label="Template(t)")
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f"Time since {timemax:.4f}")
    plt.ylabel("whitened strain (noise stdev units)")
    plt.legend(loc="upper left")
    plt.title(f"{det} whitened data around event")

    plt.subplot(2, 1, 2)
    plt.plot(time - tevent, strain_whitenbp - template_match, pcolor, label=f"{det} resid")
    plt.ylim([-10, 10])
    plt.xlim([-0.15, 0.05])
    plt.grid(True)
    plt.xlabel(f"Time since {timemax:.4f}")
    plt.ylabel("whitened strain (noise stdev units)")
    plt.legend(loc="upper left")
    plt.title(f"{det} Residual whitened data after subtracting template")
    plt.savefig(f"figures/{eventname}_{det}_matchtime.{plottype}")

    # ----- Plot PSD -----
    plt.figure(figsize=(10, 6))
    template_f = np.abs(template_fft) * np.sqrt(np.abs(datafreq)) / d_eff
    plt.loglog(datafreq, template_f, "k", label="template(f)*sqrt(f)")
    plt.loglog(freqs, np.sqrt(data_psd), pcolor, label=f"{det} ASD")
    plt.xlim(20, fs / 2)
    plt.ylim(1e-24, 1e-20)
    plt.grid(True)
    plt.xlabel("frequency (Hz)")
    plt.ylabel("strain noise ASD (strain/rtHz), template h(f)*rt(f)")
    plt.legend(loc="upper left")
    plt.title(f"{det} ASD and template around event")
    plt.savefig(f"figures/{eventname}_{det}_matchfreq.{plottype}")

