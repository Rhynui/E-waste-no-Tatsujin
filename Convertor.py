""".osu File Format

Retrieved from: https://osu.ppy.sh/wiki/en/Game_mode/osu%21taiko
    The red notes refer to normal hit circle,
        large red notes needs a finish hitsound.
    The blue notes needs to have a whistle/clap hitsound on that hit circle,
        large blue notes need both finish and whistle together.
    The sliders represents the long yellow note (also known as drumroll)
    The spinner represents a shaker.

Retrieved from: https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_%28file_format%29
    Timing point syntax: time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects
        time (Integer): Start time of the timing section, in milliseconds from the beginning of the beatmap's audio. The end of the timing section is the next timing point's time (or never, if this is the last timing point).
        beatLength (Decimal): This property has two meanings:
            For uninherited timing points, the duration of a beat, in milliseconds.
            For inherited timing points, a negative inverse slider velocity multiplier, as a percentage. For example, -50 would make all sliders in this timing section twice as fast as SliderMultiplier.
        meter (Integer): Amount of beats in a measure. Inherited timing points ignore this property.
        sampleIndex (Integer): Custom sample index for hit objects. 0 indicates osu!'s default hitsounds.
        uninherited (0 or 1): Whether or not the timing point is uninherited.

    Hit object syntax: x,y,time,type,hitSound,objectParams,hitSample
        time (Integer): Time when the object is to be hit, in milliseconds from the beginning of the beatmap's audio.
        type (Integer): Bit flags indicating the type of the object.
            Hit object types are stored in an 8-bit integer where each bit is a flag with special meaning. The base hit object type is given by bits 0, 1, and 3 (from least to most significant):
                0: Hit circle
                1: Slider
                3: Spinner
        hitSound (Integer): Bit flags indicating the hitsound applied to the object.
            The hitSound bit flags determine which sounds will play when the object is hit:
                0: Normal
                1: Whistle
                2: Finish
                3: Clap
        objectParams (Comma-separated list): Extra parameters specific to the object's type.

    Slider syntax: x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample
        length (Decimal): Visual length in osu! pixels of the slider.
            The slider's length can be used to determine the time it takes to complete the slider. length / (SliderMultiplier * 100 * SV) * beatLength tells how many milliseconds it takes to complete one slide of the slider (where SV is the slider velocity multiplier given by the effective inherited timing point, or 1 if there is none).
    
    Spinner syntax: x,y,time,type,hitSound,endTime,hitSample
        endTime (Integer): End time of the spinner, in milliseconds from the beginning of the beatmap's audio.
"""


name = str()
artist = str()
creator = str()

timing_points_section = False
hit_objects_Section = False

timing_points = list()
hit_objects = list()

start = 0
beat_length = int()
sv = int()

song_name = input("Please enter the name of the song:\n")
f = open("Original Charts/%s.osu" % song_name, "r", encoding="UTF-8")

def bsearch(time: int, start: int):
    low = start
    high = len(timing_points) - 1
    while high - low > 1:
        mid = (high+low) // 2
        if timing_points[mid][0] < time:
            low = mid
        elif timing_points[mid][0] > time:
            high = mid - 1
        else:
            return mid, timing_points[mid]
    if timing_points[high][0] <= time:
        return high, timing_points[high]
    return low, timing_points[low]

for line in f.readlines():
    line = line.rstrip()
    if line == "[TimingPoints]":
        timing_points_section = True
        continue
    elif line == "[HitObjects]":
        hit_objects_Section = True
        continue

    if timing_points_section:
        if line == "":
            timing_points_section = False
            continue
        data = line.split(',')
        time = int(data[0])
        uninherited = int(data[6])
        if uninherited == 1:
            beat_length = float(data[1])
            sv = 1
        else:
            beat_length = timing_points[-1][1]
            sv = 1/(-float(data[1])/100)
        timing_points.append([time, beat_length, sv])
    elif hit_objects_Section:
        data = line.split(',')
        time = int(data[2])
        type = int(data[3])
        hitsound = int(data[4])
        if type & 1 == 1:
            if (hitsound>>2)&1 == 1:
                hit_objects.append([0, time, -1])
                hit_objects.append([1, time, -1])
            elif (hitsound>>1)&1 == 1 or (hitsound>>3)&1 == 1:
                hit_objects.append([1, time, -1])
            else:
                hit_objects.append([0, time, -1])
        elif (type>>1) & 1 == 1:
            length = float(data[7])
            slides = int(data[6])
            if length < 1:
                continue
            start, timing_point = bsearch(time, start)
            beat_length = timing_point[1]
            sv = timing_point[2]
            end_time = length * slides * beat_length / (slider_multi*sv*100) + time
            hit_objects.append([2, time, int(end_time)])
        elif (type>>3) & 1 == 1:
            end_time = int(data[5])
            hit_objects.append([2, time, end_time])
    else:
        data = line.split(':')
        if data[0] == "SliderMultiplier":
            slider_multi = float(data[1])
f.close()

f = open("Songs/%s/chart.csv" % song_name, "w")
for data in hit_objects:
    f.write(','.join(map(str, data))+'\n')
f.close()
