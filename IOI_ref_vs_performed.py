import glob
import pretty_midi as pm
import numpy as np
import matplotlib.pyplot as plt

path = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/C-sharp-transposed/Shuan_Hern_Lee/*.mid'

all_augFiles = []

j=0
for file in glob.glob(performerPath):
    print(file.split('/'))
    readfile = pm.PrettyMIDI(file)
    onsets = list(readfile.get_onsets())
    ioi=list()
    for i,elem in enumerate(onsets):
        if i<len(onsets)-1:
            ioi.append(onsets[i+1]-elem)
        else:
            break
    if file.split('/')[-1]=='Etude Op. 10 No. 4 in C-sharp Minor_Shuan Hern Lee.mid':
        idx = j
    all_augFiles.append(ioi[:100])
    j+=1

plt.style.use('seaborn-darkgrid')
my_dpi=96
plt.figure(figsize=(800/my_dpi, 400/my_dpi), dpi=my_dpi)
t=list(np.arange(0,100,1))
for column in all_augFiles:
    plt.plot(t, column, marker='', color='grey', linewidth=1, alpha=0.4)
plt.plot(t, all_augFiles[idx], marker='', color='orange', linewidth=4, alpha=0.7, label='Real Performance')
plt.ylim(-0.02,0.2)
plt.legend(loc='upper left')
plt.title("Shuan Hern Lee performed vs transposed", loc='center', fontsize=12, fontweight=0, color='Green')
plt.xlabel("Note")
plt.ylabel("Timing Deviation")
plt.show()
