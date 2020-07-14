import mido

### function to change the tempo
def change_tempo2(filename, data_path, target_path):
    mid = mido.MidiFile(data_path + filename)
    new_mid = mido.MidiFile()
    new_mid.ticks_per_beat = mid.ticks_per_beat
    for track in mid.tracks:
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)
        for msg in track:
            if msg.type == 'set_tempo':
                print(msg)
                msg.tempo = 454545
                print(msg)
                
            new_track.append(msg)
    new_mid.save(target_path + filename)

###alternative of the above one

target_path='/home/family/Documents/performer_identification/changed_tempo_dataset/Timur_Mustakimov/'
for file in glob.glob('/home/family/Dataset/Timur_Mustakimov/*.mid'):
    mid = mido.MidiFile(file)
    new_mid = mido.MidiFile()
    new_mid.ticks_per_beat = mid.ticks_per_beat
    filename = file.split('/')[-1]
    temp = mido.bpm2tempo(int(filename.split('_')[-1].split('.')[0][3:]))
    for track in mid.tracks:
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)
        for msg in track:
            if msg.type == 'set_tempo':
                msg.tempo = temp
            new_track.append(msg)
    new_mid.save(target_path + filename)  
