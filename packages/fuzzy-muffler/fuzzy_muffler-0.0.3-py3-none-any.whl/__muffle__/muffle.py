import numpy as np
from matplotlib import pyplot as plt
import scipy.signal as sg
import librosa
import soundfile as sf
import pyrubberband

def read_mp3(path: str) -> tuple:
    data, sr = librosa.load(path, sr=None, mono=True)
    return data, sr


def lowpass_filter(audio: np.ndarray, sr: int, hz: float, roll: int=4) -> np.ndarray:
    # butterworth lp filter
    hz_norm = hz / (0.5*sr)
    b, a = sg.butter(roll, hz_norm, btype='lowpass')
    filtered = sg.lfilter(b, a, audio)
    return filtered


def pitch_shift(audio: np.ndarray, sr: int, tones: float=-3) -> np.ndarray:
    return pyrubberband.pitch_shift(audio, sr, tones)

def time_stretch(audio: np.ndarray, sr: int, rate: float=0.79) -> np.ndarray:
    return librosa.effects.time_stretch(audio, rate=rate)


# *** SIDE EFFECT VOID FUNCS *** 

# saves np.ndarray audio to path
def save_audio(audio: np.ndarray, sr: int, savep: str='') -> None:
    sf.write(savep, audio, sr, format='wav')


# graphs waveform from audio data given some sampling rate sr
def waveform(audio: np.ndarray, sr: int=44100, savep: str='') -> None:
    ts = np.linspace(0, len(audio)/sr, num=len(audio))
    plt.plot(ts, audio, color="blue")
    plt.grid()
    plt.savefig(savep) if savep else plt.show()


if __name__ == "__main__":
    audiop = './audios/romantic_homocide_jesse.mp3'
    data, sr = read_mp3(audiop)
    print(sr)
    waveform(data, sr=sr, savep='./waveforms/smthn.jpg')