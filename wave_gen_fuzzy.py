#!/usr/bin/env python3

import math
import numpy
import scipy.io
import scipy.io.wavfile

bits = 16
default_sample_rate = 44100
default_time_step = 1.0/60

class Note:
  def __init__(self, frequency, duration=1, volume=1):
    self.frequency = frequency
    self.duration = duration
    self.volume = volume

def get_frequency(note):
  if type(note) == Note:
    return note.frequency
  elif type(note) == int or type(note) == float:
    return note
  else:
    raise TypeError("Notes must either be Notes or numbers")

def get_duration(note):
  return note.duration if type(note) == Note else 1

def get_volume(note):
  return note.volume if type(note) == Note else 1

def sample(note, t):
  return math.sin(2 * math.pi * get_frequency(note) * t) * get_volume(note)

def get_fuzzy_duration(note, duration):
  frequency = get_frequency(note)
  sampling_atom = 1/frequency if frequency > 0 else 1
  factor = 2
  duration *= get_duration(note)
  while factor * sampling_atom < duration:
    factor += 1
  candidate1 = (factor - 1) * sampling_atom
  candidate2 = factor * sampling_atom
  if abs(candidate1 - duration) < abs( candidate2 - duration):
    return candidate1
  else:
    return candidate2

def sample_audio(note, duration, volume, sample_rate):
  n_samples = int(round(get_fuzzy_duration(note, duration)*sample_rate))
  buf = numpy.zeros((n_samples), dtype = numpy.int16)
  max_sample = 2**(bits - 12 + volume) - 1
  time = 0
  for s in range(n_samples):
    buf[s] = 0
    t = time + float(s)/sample_rate
    buf[s] += int(round(max_sample * sample(note, t)))
  return buf

def write_wav(filename, sample_rate, l_data, r_data):
  len_data = min(len(l_data),len(r_data))
  data = numpy.transpose(
    numpy.concatenate(
      [l_data[0:len_data],r_data[0:len_data]],
    ).reshape(2,len_data)
  )
  scipy.io.wavfile.write(filename, sample_rate, data)
  print(f"Wrote data to {filename}")

def write_mono_wav(filename, sample_rate, data):
  scipy.io.wavfile.write(filename, sample_rate, data)
  print(f"Wrote data to {filename}")

def build_track_data(track, time_step_length, volume, sample_rate):
  data = numpy.empty(0, dtype = numpy.int16)
  for i in range(len(track)):
    next_data = sample_audio(track[i], time_step_length, volume, sample_rate)
    data = numpy.concatenate([data, next_data])
  return data

def build_channel_data(tracks, time_step_length, volume, sample_rate):
  data = numpy.empty(0, dtype = numpy.int16)
  track_data = []
  adjusted_volume = volume - len(tracks)
  for track in tracks:
    track_data.append(
      build_track_data(track, time_step_length, adjusted_volume, sample_rate)
    )
  # merge tracks
  max_length = max(map(len, track_data))
  output = numpy.zeros(max_length, dtype = numpy.int16)
  for track in track_data:
    track_copy = numpy.copy(track)
    track_copy.resize(max_length)
    output += track_copy
  return output


def build_wav(
    filename, 
    tracks=None, 
    time_step=default_time_step,
    volume=10,
    sample_rate=default_sample_rate,
    left_tracks=None,
    right_tracks=None
  ):
  if tracks and left_tracks == None and right_tracks == None:
    data = build_channel_data(tracks, time_step, volume, sample_rate)
    write_mono_wav(filename, sample_rate, data)
  else:
    left_tracks = left_tracks or tracks
    right_tracks = right_tracks or tracks
    if left_tracks == None or right_tracks == None:
      raise "Must provide either mono track or left and right tracks"
    l_data = build_channel_data(left_tracks, time_step, volume, sample_rate)
    r_data = build_channel_data(right_tracks, time_step, volume, sample_rate)
    write_wav(filename, sample_rate, l_data, r_data)
  

def test1():
  track1 = [100]*300
  track2 = [101]*300
  build_wav("wave_gen_fuzzy_tests/test1.wav", [track1, track2])


def test2():
  track1 = [100]*300
  track2 = [200]*300
  build_wav("wave_gen_fuzzy_tests/test2.wav", left_tracks=[track1], right_tracks=[track2])
def test3():
  track1 = [100]*30
  track2 = [Note(200, 0.5)]*300
  build_wav("wave_gen_fuzzy_tests/test3.wav", [track1, track2])

def test4():
  track1 = [Note(100)]*300
  track2 = [Note(200, 0.1)]*300
  build_wav("wave_gen_fuzzy_tests/test4.wav", left_tracks=[track1], right_tracks=[track2])

if __name__ == "__main__":
  test1()
  test2()
  test3()
  test4()
