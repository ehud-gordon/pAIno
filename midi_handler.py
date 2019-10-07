import pygame.midi
import time
import mido


class MidiHandler:
    """
    used for midi reading and playing.
    """

    def __init__(self):

        pygame.midi.init()  # used to play midi notes.
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)

    def get_notes(self, file_name):
        """
        :param file_name: name of midi file
        :return: a list of lists, each one of format [cmd_type, note, time]
        """
        notes = []
        mid = mido.MidiFile(file_name)
        for msg in mid.tracks[0]:
            if not msg.is_meta and msg.type == 'note_on':
                notes.append([msg.note, msg.time])
        return notes

    def play_note(self, midi_num):
        self.player.note_on(midi_num, 127)

    def close_player(self):
        # todo needed?
        del self.player
        pygame.midi.quit()
