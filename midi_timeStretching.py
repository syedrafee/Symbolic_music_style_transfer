import glob
import os
from music21 import converter, pitch, interval

path='/home/family/Documents/experiment1/MIDI-VAE-master/dataset/C-sharp/*.mid'

root_path = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/C-sharp-time-stretched/'

#factor you want to stretch your midi

fctr = 1.05 #0.95 for 5% faster 

for file in glob.glob(path):
    score = converter.Converter()
    score.parseFile(file)
    newscore = score.stream.augmentOrDiminish(fctr)
    newfile_name=root_path+file.split('/')[-1][:-4]+'_fctr_'+str(fctr)+'.mid'
    newscore.write('midi',newfile_name)
