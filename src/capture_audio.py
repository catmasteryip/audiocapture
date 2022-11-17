import pyaudio
import wave
import numpy as np
from io import BytesIO
import time 
sound  = True
CHUNK = 50
FORMAT = pyaudio.paInt16
CHANNELS = 2
# RATE = 44100
RATE = 1000
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
input_index = 2
normalization_factor = 1
def bytes_to_array(b: bytes) -> np.ndarray:
    np_bytes = BytesIO(b)
    return np.load(np_bytes, allow_pickle=True)
for i in range(p.get_device_count()):
    # print(p.get_device_info_by_index(i)["name"])
    if "Stereo Mix" in p.get_device_info_by_index(i)["name"]:   
        input_index = i
        print("Stereo Mix is found")
        break

if i > p.get_device_count():
    raise Exception("Stereo Mix is not found.\nPlease check if it is enabled or the name is changed")
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = input_index,
                frames_per_buffer=CHUNK)
print("* recording")
frames = []
# every 1 second of audio, print out numpy array
# analyse presence heart sound
for second in range(RECORD_SECONDS):
    bytes_by_second = bytes()
    start = time.time()
    for i in range(0, int(RATE / CHUNK)):
        in_data = stream.read(CHUNK)

        bytes_by_second += in_data
    # convert to numpy array data_np
    data_np = np.frombuffer(bytes_by_second, dtype = np.int16)
    data_np = np.array(data_np, dtype = np.float32)
    data_np = data_np * normalization_factor
    print(f"{round(time.time() - start, 3)}s passed, {i + 1} chunks retrieved, 1st 5 digits:", data_np[:5])
    # import pdb;pdb.set_trace()
    frames.append(bytes_by_second)
print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()