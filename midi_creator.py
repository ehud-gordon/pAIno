from mido import Message, MidiFile, MidiTrack
import parameters


# write midi files, can be used to prepare the midi instructions quickly.
def little_jonathan(track):
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol


def OTJ_first_part(track):
    # Beethoven - 9th symphony (first part)
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=48))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=62, velocity=64, time=64))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=48))  # re
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do


def OTJ_full(track):
    # Bethoven - 9th symphony (full)
    # OTJ_first_part(track)
    track.append(Message('note_on', note=62, velocity=64, time=64))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=16))  # fa
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=16))  # fa
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=55, velocity=64, time=64))  # sol

    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=48))  # re
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do


def close_notes(track):
    # close to each other notes piece
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=64))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=48))  # do
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do

    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=64, velocity=64, time=64))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=48))  # do
    track.append(Message('note_on', note=62, velocity=64, time=16))  # re
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do


def far_notes(track):
    # far from each other notes piece
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do

    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do

    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=60, velocity=64, time=32))  # do
    track.append(Message('note_on', note=65, velocity=64, time=32))  # fa
    track.append(Message('note_on', note=60, velocity=64, time=16))  # do
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=67, velocity=64, time=32))  # sol
    track.append(Message('note_on', note=62, velocity=64, time=32))  # re
    track.append(Message('note_on', note=60, velocity=64, time=64))  # do


def OTJ_mi_major(track):
    # Beethoven - 9th symphony - Mi major
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=69, velocity=64, time=32))  # la
    track.append(Message('note_on', note=71, velocity=64, time=32))  # si
    track.append(Message('note_on', note=71, velocity=64, time=32))  # si
    track.append(Message('note_on', note=69, velocity=64, time=32))  # la
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=68, velocity=64, time=48))  # sol#
    track.append(Message('note_on', note=66, velocity=64, time=16))  # fa
    track.append(Message('note_on', note=66, velocity=64, time=64))  # fa
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=69, velocity=64, time=32))  # la
    track.append(Message('note_on', note=71, velocity=64, time=32))  # si
    track.append(Message('note_on', note=71, velocity=64, time=32))  # si
    track.append(Message('note_on', note=69, velocity=64, time=32))  # la
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=66, velocity=64, time=48))  # fa#
    track.append(Message('note_on', note=64, velocity=64, time=16))  # mi
    track.append(Message('note_on', note=64, velocity=64, time=64))  # mi

    track.append(Message('note_on', note=66, velocity=64, time=64))  # fa#
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=68, velocity=64, time=16))  # sol#
    track.append(Message('note_on', note=69, velocity=64, time=16))  # la
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=68, velocity=64, time=16))  # sol#
    track.append(Message('note_on', note=69, velocity=64, time=16))  # la
    track.append(Message('note_on', note=68, velocity=64, time=32))  # sol#
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=64, velocity=64, time=32))  # mi
    track.append(Message('note_on', note=66, velocity=64, time=32))  # fa#
    track.append(Message('note_on', note=59, velocity=64, time=64))  # si


def midi_creator(piece):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', program=12, time=0))
    if piece == parameters.LJ:
        little_jonathan(track)
    elif piece == parameters.OTJ_FIRST:
        OTJ_first_part(track)
    elif piece == parameters.OTJ_FULL:
        OTJ_full(track)
    elif piece == parameters.CLOSE_NOTES:
        close_notes(track)
    elif piece == parameters.FAR_NOTES:
        far_notes(track)
    mid.save('midi_file.mid')


if __name__ == "__main__":
    midi_creator(piece=parameters.OTJ_FULL)
