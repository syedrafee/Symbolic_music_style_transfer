import glob
import os
from music21 import converter, pitch, interval

keyNames = ["A-","A","A#","B","C","C#","D","D#","E","F","F#","G"]

path='/home/family/Documents/experiment1/MIDI-VAE-master/dataset/C-sharp/*.mid'

root_path = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/C-sharp-transposed/'

for file in glob.glob(path):
    score = converter.parse(file)
    for keyname in keyNames:
        key = score.analyze('key')
        if key.tonic.name==keyname and key.mode=='minor':
            continue
        else:
            keyInterval = interval.Interval(key.tonic, pitch.Pitch(keyname))
            newScore = score.transpose(keyInterval)
            k=newScore.analyze('key')
            print(k.tonic.name, k.mode)
            newfile_name=root_path+file.split('/')[-1][:-4]+'_'+k.tonic.name+'_'+k.mode+'.mid'
            newScore.write('midi',newfile_name)
