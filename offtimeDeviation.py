import pretty_midi as pm

path = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/Frank_Dupree/DupreeF01.mid'

score= pm.PrettyMIDI(path)

allNotes=[]
for note in dm.instruments[0].notes:
    strtend = []
    strtend.append(note.start)
    strtend.append(note.end)
    allNotes.append(strtend)

offtimeDurations=[]
for i,elem in enumerate(allNotes):
    if i<len(allNotes)-1:
        offtimeDurations.append(allNotes[i+1][0]-elem[1])
