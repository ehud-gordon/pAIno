from vpython import *
import numpy as np
import parameters

W_K = [0, 2, 4, 5, 7, 9, 11]  # the white keys in an octave in midi code.
NARROW_COEFF = 0.2  # makes the white keys a bit narrower visually, so a gap between them can be seen.


class Display:
    def __init__(self, keyboard, hand, midi_player=None):  # todo remove none from midi player.
        scene.width = scene.height = 700
        scene.background = color.gray(0.1)
        light = local_light(pos=vector(0, 4, 3), color=color.yellow)
        self.keyboard = keyboard

        self.v_keys = {}  # keys to be shown with vpython, midi value used as key, and the v_key as value.
        self.initiate_keyboard(keyboard)
        self.last_pressed = None  # the last pressed key, used to visualize the keys as they are pressed.

        self.v_bones = []
        self.initiate_hand(hand)

        self.midi_player = midi_player

    def initiate_hand(self, hand):
        for bone in hand.bones:
            v_bone = cylinder(pos=vec2v_vec(bone.pivot), axis=vec2v_vec(bone.axis), radius=bone.radius,
                              texture=textures.rough)
            self.v_bones.append(v_bone)

        if getattr(hand, "fingers", False):
            for finger in hand.fingers:
                v_bone = cylinder(pos=vec2v_vec(finger.pivot), axis=vec2v_vec(finger.axis), radius=finger.radius)
                self.v_bones.append(v_bone)

    def initiate_keyboard(self, keyboard):
        for key in keyboard.keys:
            if key.key_type == 'w':
                narrowed_key = vec2v_vec(key.size) - vector(NARROW_COEFF, 0, 0)
                v_key = box(pos=vec2v_vec(key.pos), size=narrowed_key,
                            texture=textures.metal)  # visual key for vpython.
            else:
                v_key = box(pos=vec2v_vec(key.pos), size=vec2v_vec(key.size), color=color.black)
            midi_num = key.midi_num
            self.v_keys[midi_num] = v_key

    def update_hand(self, hand):  # update the hand pos.
        for i in range(len(hand.bones)):
            self.v_bones[i].pos = vec2v_vec(hand.bones[i].pivot)
            self.v_bones[i].axis = vec2v_vec(hand.bones[i].axis)

        if getattr(hand, "fingers", False):
            for i in range(len(hand.fingers)):
                self.v_bones[len(hand.bones) + i].pos = vec2v_vec(hand.fingers[i].pivot)
                self.v_bones[len(hand.bones) + i].axis = vec2v_vec(hand.fingers[i].axis)

            # self.v_joints[i].pos = vec2v_vec(hand.bones[i].pivot)

    def key_pressed(self, key_midi):
        """
        if a key was pressed, changes its color. only the last pressed key has a different color.
        :param key:
        """
        if self.last_pressed:
            midi_num_previous = self.last_pressed
            if midi_num_previous % 12 in W_K:
                self.v_keys[midi_num_previous].color = color.white
            else:
                self.v_keys[midi_num_previous].color = color.black

        self.v_keys[key_midi].color = color.red
        self.last_pressed = key_midi

    def draw_keyboard_strike_positions(self):
        s = sphere(pos=vector(0, 0, 0), radius=(0.1), color=color.red)  # draw the center of the keyboard.
        for key in self.keyboard.keys:
            if key.key_type == 'w':
                s1 = sphere(pos=vec2v_vec(key.get_strike_position_round()), radius=(1), color=color.blue,opacity=0.3)
            else:
                s2 = sphere(pos=vec2v_vec(key.get_strike_position_round()), radius=(1), color=color.orange,opacity=0.3)


def vec2v_vec(vec):
    """ turn a 3 dimensional vector like array into a vpython array. """
    return vector(vec[0], vec[1], vec[2])


def draw_box(white_keys, third_box):
    """
    draws a box around each joint of the hand, which represents its boundaries of movement.
    :param white_keys: the amount of white keys in the keyboard. used to know how large the x axis of the box is.
    """
    W_K_M = np.array([2.2, 2, 14.3])
    x_side = (white_keys // 2 + parameters.x_const) * W_K_M[0]

    # box of movement for the finger.
    box(pos=vector(0, (parameters.up_y + parameters.down_y) / 2, (parameters.back_z + parameters.front_z) / 2),
        length=2 * x_side, height=parameters.up_y - parameters.down_y, width=parameters.front_z - parameters.back_z, color=color.red, opacity=0.2)

    # box of movement for the wrist.
    box(pos=vector(0, (parameters.up_y + parameters.base_y + parameters.down_y + parameters.base_y) / 2, (
    parameters.back_z + parameters.base_z + parameters.front_z + parameters.base_z) / 2),
        length=2 * x_side, height=parameters.up_y - parameters.down_y, width=parameters.front_z - parameters.back_z, color=color.blue, opacity=0.2)

    # box of movement for the shoulder
    if third_box:
        box(pos=vector(parameters.x_start, parameters.y_start, parameters.z_start),
            length=parameters.cube_length, height=parameters.cube_length, width=parameters.cube_length, color=color.purple, opacity=0.2)
