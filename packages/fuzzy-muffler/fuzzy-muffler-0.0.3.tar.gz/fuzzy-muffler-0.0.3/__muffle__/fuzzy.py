from .muffle import *
from .log import log
import logging

import os
import re

# ***SIDE EFFECT FUNCS ***
# @log
def fuzzify(path: str, dest: str='', _hz: float=1000.0, _roll: int=4, _tones: float=-3, _rate: float=0.79) -> np.ndarray:
    # fuzzifies audio at path and saves it to dest
    audio, sr = read_mp3(path)

    # slow -> muffle -> lower pitch
    audio = time_stretch(audio, sr, _rate)
    audio = lowpass_filter(audio, sr, _hz, _roll)
    audio = pitch_shift(audio, sr, _tones)

    save_audio(audio, sr, dest) if dest else save_audio(audio, sr, path)
    
    return audio

# IF NO dest_dir OVERWRITES FILES
def fuzzify_all(read_dir: str, write_dir: str='', _hz: float=1200, _roll: int=4, _tones: float=-3, _rate: float=0.79) -> None:
    for bname in os.listdir(read_dir):
        fname = os.path.join(read_dir, bname)
        # skipping non audiofiles
        if not re.match(r'.*.mp3|.*.wav|.*.ogg', bname):
            logging.warning(f'skipping *non audio file: {bname}')
            continue
        
        logging.info(f'reading: {bname}')
        dest = '' if not write_dir else os.path.join(write_dir, bname)
        logging.info(f'{"writing" if dest else "overwriting"}: {bname}')


        fuzzify(fname, dest=dest, _hz=_hz, _roll=_roll, _tones=_tones, _rate=_rate)

if __name__ == '__main__':
    fuzzify_all("./audios", write_dir='muffled')