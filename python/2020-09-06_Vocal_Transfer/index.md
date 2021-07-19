[Main Page](/) / [Python Projects](/python) / [Vocal Transfer](/python/2020-05-29_HungerGames_recreation_betting_simulator_Remake_(5-29-2020))

# Vocal Transfer

## Date: 2020-09-06

The original idea was that I'd take any song, as well as a recording of anyone's voice, and then have a program map the frequencies in the voice and apply them to the song, creating a new file that sounded as if the person was singing that song.

Unfortunately, I believed those "voice frequencies" were represented in the file as the file's bytes, and that a higher byte value was indicative of a higher frequency. I thought that a recording of a person with a lower voice would have lower byte values, and when mapped to the song would produce a lower sounding song. This was **incorrect**. 

Additionally, the MP3 files had a section at the beginning that contained every possible byte value. The whole idea of using lower frequencies would not work because of this section. This led me to not work on the project anymore.

-----

## Files

[main.py](main.py)