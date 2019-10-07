import keyboard
import numpy as np
import parameters

if parameters.debug:
    from vpython import *
    import display as d


UNIT = keyboard.W_K_M[0]  # white piano key width is the smallest unit in the discrete space.
change_angle = 0          # the angle that creates the blocks in the space
base_teta = 0
base_phai = 0
base_r = 0


""" Important: the spherical coordinates in this class do not use the standard 
    spherical coordinates but a slightly different version that creates the space
    in a better way """
""" Important: in this class, real vector refers to vectors that start at (0,0,0)
    relative vectors are vectors that start at the pivot's position """


class Block:
    def __init__(self, r, teta, phai):
        self.r = r
        self.teta = teta
        self.phai = phai

    def direction(self, other):
        """ return a vector pointing from the center of this block to the center of the other """
        return other.get_center() - self.get_center()

    def get_center(self):
        """ Returns a relative vector which is the center of this block"""
        return get_normal_coordinates([self.r + UNIT/2, self.teta + change_angle/2, self.phai + change_angle/2])


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2' """
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def get_sphere_coordinates(v):
    """ Gets a real vector and returns the r, teta, phai """
    teta = 0
    phai = 0
    if v[2] == 0:
        teta = np.pi/2
        phai = np.pi/2
    if v[2] > 0:
        teta = np.pi + np.arctan(v[1]/v[2])
        phai = np.arctan(v[0]/v[2])
    if v[2] < 0:
        teta = np.arctan(v[1]/v[2])
        phai = np.pi + np.arctan(v[0]/v[2])
    r = np.linalg.norm(v) / (np.cos(teta)**2 + (np.sin(teta)**2) * (np.cos(phai)**2))**0.5
    return r, teta, phai


def get_normal_coordinates(v):
    """ Gets the r, teta and phai of a real vector and returns that vector """
    x = v[0] * np.cos(v[1]) * np.sin(v[2])
    y = v[0] * np.sin(v[1]) * np.cos(v[2])
    z = v[0] * np.cos(v[1]) * np.cos(v[2])
    return np.array([x, y, z])


def set_base_angle(board):
    """ Returns the angle that creates the 'blocks' in the space based on the keyboard """
    global base_teta, base_phai, change_angle, base_r
    if board.num_keys <= 5:
        print("need at least 5 keys!")
        return 0
    # if mid key is white
    if board.mid_key % 12 in keyboard.W_K:
        s1 = board.keys[0].get_strike_position_round()
        if (board.mid_key + 1) % 12 in keyboard.W_K:
            s2 = board.keys[1].get_strike_position_round()
        else:
            s2 = board.keys[2].get_strike_position_round()
    else:
        s1 = board.keys[1].get_strike_position_round()
        if (board.mid_key - 1) % 12 in keyboard.W_K:
            s2 = board.keys[int(len(board.keys)/2)].get_strike_position_round()
        else:
            s2 = board.keys[int(len(board.keys)/2) + 1].get_strike_position_round()
    v1 = s1 - parameters.pivot
    v2 = s2 - parameters.pivot
    change_angle = angle_between(v1, v2)
    spherical = get_sphere_coordinates(v1)
    base_teta = spherical[1] - change_angle / 2
    base_phai = spherical[2] - change_angle / 2
    base_r = spherical[0] - int(spherical[0] / UNIT) * UNIT - UNIT / 2
    if base_r < 0:
        base_r = base_r + UNIT
    return change_angle  # success


def get_block_pos(v):
    """ Gets a real vector and returns the relative block """
    nv = v - parameters.pivot
    r, teta, phai = get_sphere_coordinates(nv)  # todo: is this working???
    nr = np.floor((r - base_r) / UNIT)*UNIT + base_r
    nteta = np.floor((teta - base_teta) / change_angle)*change_angle + base_teta
    nphai = np.floor((phai - base_phai) / change_angle)*change_angle + base_phai
    return Block(nr, nteta, nphai)


def get_block(v):
    """ Gets a real vector and returns a real vector which is the center of the
        block in which v is found. The returned value is a tuple, not np.array """
    ret = get_block_pos(v).get_center() + parameters.pivot
    return tuple(ret)


def get_hand_state(hand, next_key):
    """
    Returns the vector between the next key to be played (vector) and the blocks that the hand is in
    """
    dist = []
    key_block = get_block_pos(next_key)
    for i in range(len(hand.bones)):
        bone_block = get_block_pos(hand.bones[i].get_end())
        dist.append(bone_block.direction(key_block))
    if getattr(hand, "fingers", False):
        for i in range(len(hand.fingers)):
            finger_block = get_block_pos(hand.fingers[i].get_end())
            dist.append(finger_block.direction(key_block))

    dist = [tuple(pos.tolist()) for pos in dist]
    return tuple(dist)


def get_hand_pos(hand):
    """ Returns the discrete positions of the hand in real vectors """
    pos = []
    for i in range(len(hand.bones)):
        pos.append(np.array(get_block(hand.bones[i].get_end())))
    if getattr(hand, "fingers", False):
        for i in range(len(hand.fingers)):
            pos.append(np.array(get_block(hand.fingers[i].get_end())))
    return pos


def draw_vector(a, b):
    direction = get_block_pos(a).direction(get_block_pos(b))
    if parameters.debug:
        arrow(pos=vector(a[0], a[1], a[2]), axis=d.vec2v_vec(direction), shaftwidth=1, color=color.magenta)
    return direction


if __name__ == '__main__':
    """ run the learning agent. """
    import midi_handler, hand
    boardy = keyboard.Keyboard(num_keys=parameters.num_keys, mid_key=parameters.mid_key)
    handy = hand.Hand(pivot=parameters.pivot, num_bones=parameters.num_bones, num_fingers=parameters.num_of_fingers,
                      joint_pos=parameters.joint_pos)
    midi = midi_handler.MidiHandler()
    import display
    disp = display.Display(boardy, handy, midi)
    display.draw_box(boardy.white_keys)
    disp.draw_keyboard_strike_positions()
    set_base_angle(boardy)

    # center of blocks
    for l in range(-5, 5, 1):
        for j in range(-5, 5, 1):
            for k in range(-5, 5, 1):
                v = get_block(2*np.array([l, j, k]))
                # v = v - np.array(parameters.pivot)
                # arrow(pos=vector(parameters.pivot[0], parameters.pivot[1], parameters.pivot[2]),
                #       axis=vector(v[0], v[1], v[2]), shaftwidth=0.1, color=color.red, opacity=0.2)
                sphere(pos=vector(v[0], v[1], v[2]), radius=0.3, opacity=0.3)
