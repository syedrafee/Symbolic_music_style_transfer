import argparse
import collections
import logging
import math
import pickle
import re
import glob
import pretty_midi as pm

MIN_DURATION = 1e-5

def chop_midi(midi, bars_per_segment, instrument_re=None, programs=None, drums=None,
              min_notes_per_segment=1, include_segment_id=False, force_tempo=None, skip_bars=0):
    if isinstance(bars_per_segment, int):
        bars_per_segment = [bars_per_segment]
    bars_per_segment = list(bars_per_segment)

    if force_tempo is not None:
        normalize_tempo(midi, force_tempo)

    instruments = midi.instruments
    if instrument_re is not None:
        instruments = [i for i in instruments if re.search(instrument_re, i.name)]
    if programs is not None:
        instruments = [i for i in instruments if i.program + 1 in programs]
    if drums is not None:
        # If True, match only drums; if False, match only non-drums.
        instruments = [i for i in instruments if i.is_drum is drums]

    
    all_notes = [n for i in instruments for n in i.notes]
    all_notes.sort(key=lambda n: n.start)

    def is_overlapping(note, start, end):
        """Check whether the given note overlaps with the given interval."""
        # If a note's start "isclose" to a segment boundary, we want to include it
        # in the following segment only.
        # Note that if the note is extremely short, it might end before the segment starts!
        return ((note.end > start or math.isclose(note.start, start)) and
                note.start < end and not math.isclose(note.start, end))

    downbeats = midi.get_downbeats()[skip_bars:]
    for bps in bars_per_segment:
        note_queue = collections.deque(all_notes)
        notes = []  # notes in the current segment
        for i in range(0, len(downbeats), bps):
            start = downbeats[i]
            end = downbeats[i + bps] if i + bps < len(downbeats) else midi.get_end_time()
            if math.isclose(start, end):
                continue

            # Filter the notes from the previous segment to keep those that overlap with the
            # current one.
            notes[:] = (n for n in notes if is_overlapping(n, start, end))

            # Add new overlapping notes. note_queue is sorted by onset time, so we can stop
            # after the first note which is outside the segment.
            while note_queue and is_overlapping(note_queue[0], start, end):
                notes.append(note_queue.popleft())

            # Clip the notes to the segment.
            notes_clipped = [
                pm.Note(
                    start=max(0., n.start - start),
                    end=max(0., min(n.end, end) - start),
                    pitch=n.pitch,
                    velocity=n.velocity)
                for n in notes
            ]
            # Remove extremely short notes that could have been created by clipping.
            notes_clipped = [n for n in notes_clipped if n.end-n.start >= MIN_DURATION]

            if len(notes_clipped) < min_notes_per_segment:
                continue

            if include_segment_id:
                yield ((file_id, i, i + bps), notes_clipped)
            else:
                yield notes_clipped

def normalize_tempo(midi, new_tempo=60):
    if math.isclose(midi.get_end_time(), 0.):
        return

    tempo_change_times, tempi = midi.get_tempo_changes()
    original_times = list(tempo_change_times) + [midi.get_end_time()]
    new_times = [original_times[0]]

    # Iterate through all the segments between the tempo changes.
    # Compute a new duration for each of them.
    for start, end, tempo in zip(original_times[:-1], original_times[1:], tempi):
        time = (end - start) * tempo / new_tempo
        new_times.append(new_times[-1] + time)

    midi.adjust_times(original_times, new_times)

def main():
    input_files = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/aaron/*.mid'
    output_files = '/home/family/Documents/experiment1/MIDI-VAE-master/dataset/aaron2/'
    for file in glob.glob(input_files):
    	midi=pm.PrettyMIDI(file)
    	instruments = midi.instruments
    	time_signature_changes = midi.time_signature_changes
    	key_changes = midi.key_signature_changes
    	output = list(chop_midi(midi,
    				bars_per_segment=8,
                            	instrument_re=None,
                            	programs=None,
                            	drums=None,
                            	min_notes_per_segment=1,
                            	include_segment_id=False,
                            	force_tempo=None,
                            	skip_bars=0))
    	for split_index, split in enumerate(output):
        	split_instruments=[]
        	split_instrument = pm.Instrument(program=instruments[0].program,name=instruments[0].name)
        	split_instrument.notes = split
        	split_instruments.append(split_instrument)
        	split_score = pm.PrettyMIDI()
        	split_score.time_signature_changes = time_signature_changes
        	split_score.key_signature_changes = key_changes
        	split_score.instruments = split_instruments
        	split_score.write(output_files+file.split('/')[-1][:-4]+'_split-{}'.format(split_index + 1)+'.mid')
	
