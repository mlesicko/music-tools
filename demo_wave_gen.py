#!/usr/bin/env python3

from wave_gen import build_wav, Note
from music_utils import flatten, enlengthen

tone1 = lambda duration=1: Note(170, duration)
tone2 = lambda duration=1: Note(175, duration)
silent_tone = lambda duration=1: Note(170,duration,0)
#tone1 = 147
#tone2 = 150


test1 = tone1(180)
test2 = tone2(180)
test3 = flatten([tone1(9), silent_tone(9), tone2(9), silent_tone(9)] * 10)
test4 = flatten([tone1(9), silent_tone(3), tone2(9), silent_tone(3)] * 10)
test5 = flatten([tone1(9), tone2(9)] * 30)
test6 = flatten([tone1(3), tone2(3)] * 50)
test7 = map(lambda freq: Note(freq), range(80,800))

test8 = Note(25, 180)
test9 = Note(35, 180)
test10 = Note(45, 180)

space = silent_tone(360)
track1 = flatten([
  test1,space,
  test2,space,
  test3,space,
  test4,space,
  test5,space,
  test6,space,
  test7,space,
  test8,space,
  test9,space,
  test10,space,
])


if __name__ == "__main__":
  build_wav("demo_wave_gen.wav", [track1])
