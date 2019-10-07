import numpy as np
import parameters

if parameters.debug:
    from vpython import *

# the white keys in one octave in a piano. 0 is the note C.
W_K = [0, 2, 4, 5, 7, 9, 11]
# black keys on the piano are not dead even between white keys, some are a bit to the left
B_K_L = [1, 6]

# some are a bit to the right
B_K_R = [3, 10]

# and only one is exactly in the middle.
B_K_MID = [8]

# the ones that are a bit to the side need to be shifted slightly.
B_K_SHIFT = 0.2

# measurement from my own keyboard. 1 unit is 1 centimeter.
W_K_M = np.array([2.2, 2, 14.3])  # width, height and depth measurements of a white key.
B_K_M = np.array([1, 1.5, 9])

# base positions of white and black keys.
W_K_B_P = np.zeros(3)
B_K_B_P = np.array([0, W_K_M[1] / 2 + B_K_M[1] / 2, B_K_M[2] / 2 - W_K_M[2] / 2])


class Keyboard:
    # for midi key numberings see http://newt.phys.unsw.edu.au/jw/notes.html
    def __init__(self, mid_key=66, num_keys=13):  # mid is f#
        """
        create a virtual representation of a piano keyboard.
        :param mid_key: the key to be centered at (0,0,0). the number is the midi representation of that key.
        :param num_keys: amount of keys on the keyboard.
        """
        self.keys = []
        self.mid_key = mid_key
        self.num_keys = num_keys
        self.white_keys = 0
        self.create_keyboard(mid_key, num_keys)
        self.midi_to_pos = {k.midi_num: k.get_strike_position_round() for k in self.keys}  # maps a midi note to a coordinate.

    def create_keyboard(self, mid_key, num_keys):
        # build to the right of the middle.
        pos_x = 0
        for i in range(int(np.ceil(num_keys / 2))):
            midi_num = mid_key + i
            if midi_num % 12 in W_K:
                key = Key(pos_x + W_K_M[0] / 2, 'w', midi_num)
                pos_x += W_K_M[0]
                self.white_keys += 1
            else:
                key = Key(pos_x, 'b', midi_num)
            self.keys.append(key)

        # and to the left.
        pos_x = 0
        for i in range(0, int(np.floor(num_keys / 2))):
            midi_num = mid_key - (i + 1)
            if midi_num % 12 in W_K:
                key = Key(pos_x - W_K_M[0] / 2, 'w', midi_num)
                pos_x -= W_K_M[0]
                self.white_keys += 1
            else:
                key = Key(pos_x, 'b', midi_num)
            self.keys.append(key)

        # shift the black keys that need shifting.
        for key in self.keys:
            note = key.midi_num % 12
            shift_vec = np.array([B_K_SHIFT, 0, 0])
            if note in B_K_L:
                key.pos -= shift_vec
            elif note in B_K_R:
                key.pos += shift_vec

        # shift all keys on the x axis so that point (0,0,0) will be in the center of a white key, to the right of
        # the middle piano key.
        # (if there is a single white key: in the center of it.)
        # (if there is a single black key: in the center of the white key to the right of it.)
        for key in self.keys:
            key.pos[0] -= W_K_M[0] / 2


class Key:
    def __init__(self, pos_x, key_type, midi_num):
        """ a keyboard key.
        :param pos_x: the x position of the note. (y and z are known based on the type.)
        :param key_type: 'b' for black, 'w' for white.
        :param midi_num: midi numbering. used to recognize the key when it is struck.
        """
        self.key_type = key_type
        self.midi_num = midi_num

        if self.key_type == 'w':
            self.size = W_K_M
            self.pos = W_K_B_P + [pos_x, 0, 0]  # pos of center point

        else:
            self.size = B_K_M
            self.pos = B_K_B_P + [pos_x, 0, 0]

    def get_strike_position(self):
        """
        :return: the target position of the hand, to which it needs to arrive, in order to strike the key.
        it is located a bit above of the key. in black keys it is located above the key and a bit to the right,
        so that it will always be in the same specific cube in space and not between them. (see relevant file)
        """
        if self.key_type == 'w':
            return self.pos + np.array(
                [0, 0.6 * W_K_M[1], W_K_M[2] / 4])  # shifted a bit to the top, and a bit forward.
        else:
            return self.pos + np.array([0.1 * B_K_M[0], 0.6 * W_K_M[1], B_K_M[2] / 4])

    def get_strike_position_round(self):
        """ same as get_strike_position, only positions all the strike point on a circle instead of a straight line,
            thus maintaining symmetry between all the white notes, and another symmetry between all the black notes.
            #todo maybe change the positions to add symmetry between the white and black notes also, thus save space.
        """
        if parameters.num_bones == 1:
            end_pos_in_z = W_K_M[0] * 0  # the position of the strike point for
        else:
            end_pos_in_z = W_K_M[0] * 1.5  # the position of the strike point for
        # #todo! why does changing this parameter make the arm go in the completely wrong directions!!?!?!
        radius_white_keys = np.linalg.norm(parameters.pivot - end_pos_in_z)
        radius_black_keys = radius_white_keys + 1.5*W_K_M[0]

        if self.key_type == 'w':
            x = self.pos[0]
            y = self.pos[1] + 1 * W_K_M[1]
            p0 = np.array([x, y, 0])
            p1 = np.array([x, y, 1])
            strike_pos = self.get_line_sphere_intersection(p0, p1, parameters.pivot, radius_white_keys)
            return strike_pos
        else:
            x = self.pos[0] + 0.1 * B_K_M[0]
            y = self.pos[1] + 1 * W_K_M[1]
            p0 = np.array([x, y, 0])
            p1 = np.array([x, y, 1])
            strike_pos = self.get_line_sphere_intersection(p0, p1, parameters.pivot, radius_black_keys)
            return strike_pos

    def get_line_sphere_intersection(self, p0, p1, circleCenter, circleRadius):
        # based on https://www.codeproject.com/Articles/19799/Simple-Ray-Tracing-in-C-Part-II-Triangles-Intersec
        v = p1 - p0  # a vector on the line
        a = np.inner(v, v)
        b = 2 * (np.inner(p0, v) - np.inner(v, circleCenter))
        c = np.square(p0[0]) - 2 * p0[0] * circleCenter[0] + np.square(circleCenter[0]) + \
            np.square(p0[1]) - 2 * p0[1] * circleCenter[1] + np.square(circleCenter[1]) + \
            np.square(p0[2]) - 2 * p0[2] * circleCenter[2] + np.square(circleCenter[2]) + \
            - np.square(circleRadius)
        discriminant = np.square(b) - 4 * a * c
        if discriminant < 0:
            print("NO SOLUTION - line_sphere_intersection_failed")
            return -1
        t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
        solution1 = np.array([p0[0] * (1 - t1) + t1 * p1[0], p0[1] * (1 - t1) + t1 * p1[1],
                             p0[2] * (1 - t1) + t1 * p1[2]])
        if discriminant == 0:
            print("only one solution for intersection...")
        t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)
        solution2 = np.array([p0[0] * (1 - t2) + t2 * p1[0], p0[1] * (1 - t2) + t2 * p1[1],
                             p0[2] * (1 - t2) + t2 * p1[2]])

        if solution1[2] < W_K_M[2]:
            return solution1
        elif solution2[2] < W_K_M[2]:
            return solution2
        else:
            print("NO FEASIBLE INTERSECTION BETWEEN THE KEYBOARD AND THE HAND!")
            return -1
