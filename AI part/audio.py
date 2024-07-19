import sounddevice as sd
import numpy as np
import sys
import detection
# place holders and global variables
SOUND_AMPLITUDE = 0
AUDIO_CHEAT = 0

# sound variables
# SUS means next sound packet is worth analyzing
CALLBACKS_PER_SECOND = 40  # callbacks per sec(system dependent)
SUS_FINDING_FREQUENCY = 2  # calculates SUS *n* times every sec
SOUND_AMPLITUDE_THRESHOLD = 27  # amplitude considered for SUS calc

# packing *n* frames to calculate SUS
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)
AMPLITUDE_LIST = list([0] * FRAMES_COUNT)
SUS_COUNT = 0
count = 0


def print_sound(indata, outdata, frames, time, status):
    avg_amp = 0
    global SOUND_AMPLITUDE, SUS_COUNT, count, SOUND_AMPLITUDE_THRESHOLD, AUDIO_CHEAT
    vnorm = int(np.linalg.norm(indata) * 10)
    AMPLITUDE_LIST.append(vnorm)
    #print(AMPLITUDE_LIST)
    count += 1
    AMPLITUDE_LIST.pop(0)
    if count == FRAMES_COUNT:
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT
        SOUND_AMPLITUDE = avg_amp
        #print(SOUND_AMPLITUDE)
        #print(SUS_COUNT)

        if avg_amp > 10 and SUS_COUNT>=2 :
            print("Sorrounding sound is more ...")
            AUDIO_CHEAT = 1
        if SUS_COUNT >= 2:
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
        if avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            SUS_COUNT += 1
        else:
            SUS_COUNT = 0
            AUDIO_CHEAT = 0
        count = 0



def sound():
    if detection.cheat_count>=3:
        print('exiting from audio')
        sys.exit(1)
    with sd.Stream(callback=print_sound):
        sd.sleep(-1)



def sound_analysis():
    global AMPLITUDE_LIST, FRAMES_COUNT, SOUND_AMPLITUDE
    while True:
        AMPLITUDE_LIST.append(SOUND_AMPLITUDE)

        print(AMPLITUDE_LIST)

        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT

        if avg_amp > 5:
            print("Sorrounding sound is more ...")
        AMPLITUDE_LIST.pop(0)


if __name__ == "__main__":
    sound()
