import glob
src_path = '/home/family/Documents/performer_identification/changed_tempo_dataset/Timur_Mustakimov/*.mid'

tar_path = '/home/family/Documents/performer_identification/shifted_data/Timur_Mustakimov/'

for file in glob.glob(src_path):
    m = pm.PrettyMIDI(file)
    old_onsets = m.get_onsets()
    new_onsets = old_onsets - old_onsets[0]
    m.adjust_times(old_onsets, new_onsets)
    m.write(tar_path+file.split('/')[-1])
