import itertools
import numpy as np
import parameters


# constants for number of bones, radius, starting positions
b_radius = [2, 1.4, 0.7]  # radius of bones
f_radius = 0.2  # radius of fingers
b_angle = [np.pi / 12, np.pi / 12, np.pi / 12]  # angles of movement for each bone in radians
b_axis = np.array([0, 0, -1])  # starting pos of bones
b_length = [29, 31, 9.5]
b_lim_const = [2.5, 2.5, 1]
b_range = [3, 0, 3, 0]  # max range of movement for each bone
f_length = 5
NO_MOVE = 0
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4
TAP = 5
W_K_M = np.array([2.2, 2, 14.3])


# The hand, which has several bones
class Hand:
    def __init__(self, pivot=np.array([-7, 34, 53]), num_bones=3, num_fingers=1, joint_pos=None, bone_angle=np.pi/12):
        """
        Creates a hand. The default number of bones is constant + num_fingers
        :param num_fingers: number of fingers
        :param pivot: the starting point of the first bone
        :param num_bones: amount of bones
        :param joint_pos: an array which hold the starting coordinate of each bone.
        """
        self.bones = []
        self.num_bones = num_bones
        self.white_keys = np.ceil(parameters.num_keys*7/12)
        self.x_side = (self.white_keys // 2 + parameters.x_const) * W_K_M[0]
        self.pivot = pivot
        self.num_bones = num_bones
        self.num_fingers = num_fingers
        self.joint_pos = joint_pos
        self.bone_angle = bone_angle
        start = pivot
        if self.joint_pos:
            # add the starting position of the joints if they exist.
            for i in range(self.num_bones):
                start = np.array(self.joint_pos[i])
                direction = np.array(self.joint_pos[i + 1]) - np.array(self.joint_pos[i])
                bone = Bone(pivot=start, axis=direction, radius=b_radius[i],
                            angle=self.bone_angle)
                self.bones.append(bone)
        else:  # add the bones
            for i in range(self.num_bones):
                bone = Bone(pivot=start, axis=b_length[i] * b_axis, radius=b_radius[i],
                            angle=self.bone_angle)
                self.bones.append(bone)
                start = bone.get_end()

        self.create_bone_boundaries()

    def reset_hand(self):
        start = self.pivot
        if self.joint_pos:
            # add the starting position of the joints if they exist.
            for i in range(self.num_bones):
                start = np.array(self.joint_pos[i])
                direction = np.array(self.joint_pos[i + 1]) - np.array(self.joint_pos[i])
                bone = Bone(pivot=start, axis=direction, radius=b_radius[i],
                            angle=self.bone_angle)
                self.bones.append(bone)
        else:  # add the bones
            for i in range(self.num_bones):
                bone = Bone(pivot=start, axis=b_length[i] * b_axis, radius=b_radius[i],
                            angle=self.bone_angle)
                self.bones.append(bone)
                start = bone.get_end()

    def move(self, actions):
        """
        Moves all bones in the hand according to the given list of actions
        :param actions: a list of actions: (UP, DOWN, RIGHT, LEFT, NO_MOVE) for each bone
        and (TAP, NO_MOVE) for each finger
        """
        start = self.bones[0].pivot
        for i in range(len(self.bones)):
            self.bones[i].pivot = start
            self.bones[i].move(actions[i])
            start = self.bones[i].get_end()  # start of next bone

    def move_to_discrete_position(self, discrete_position):
        """
        changes the position of the joints of the hand to fit the discrete positions they were mapped to by the space.
        it actually changes the length of the bones a bit, but we later normalize them so on average they stay the same.
        :param discrete_position: The end positions of all bones, in real vectors

        Note: only works for bones, fingers not included!!!
        """
        for i in range(len(self.bones) - 1):
            # change start of bone i+1 to center of block of end bone i
            self.bones[i+1].pivot = discrete_position[i]
            self.bones[i].axis = discrete_position[i] - self.bones[i].pivot
        self.bones[-1].axis = discrete_position[-1] - self.bones[-1].pivot

    def how_many_joints_out_of_boxes(self):
        """
        checks if any of the joints of the hand are out of their allowed boxes.
        :return: true if a joint is out of its box.
        """
        num_of_joints_out_of_box = 0
        for i in range(len(self.bones)):
            pos = self.bones[i].get_end()
            if pos[0] < self.bones[i].x_boundary_left:
                num_of_joints_out_of_box += 1
            if pos[0] > self.bones[i].x_boundary_right:
                num_of_joints_out_of_box += 1
            if pos[1] < self.bones[i].y_boundary_down:
                num_of_joints_out_of_box += 1
            if pos[1] > self.bones[i].y_boundary_up:
                num_of_joints_out_of_box += 1
            if pos[2] < self.bones[i].z_boundary_back:
                num_of_joints_out_of_box += 1
            if pos[2] > self.bones[i].z_boundary_front:
                num_of_joints_out_of_box += 1
        return num_of_joints_out_of_box

    def get_legal_actions(self):
        """
        Returns a list with all legal actions in the current state
        a movement in a certain direction is legal for a bone if it is not already too far off in that direction.
        """
        act = []
        for i in range(len(self.bones)):
            pos = self.bones[i].get_end()
            bone = self.bones[i]
            actions = []
            if pos[0] > bone.x_boundary_left and not (pos[0] < 0 and pos[2] > bone.z_boundary_front):
                actions.append(LEFT)
            if pos[0] < bone.x_boundary_right and not (
                    pos[0] > 0 and pos[2] > bone.z_boundary_front):
                actions.append(RIGHT)
            if pos[1] < bone.y_boundary_up and not (pos[1] > 0 and pos[2] > bone.z_boundary_front):
                actions.append(UP)
            if pos[1] > bone.y_boundary_down and not (pos[1] < 0 and pos[2] > bone.z_boundary_front):
                actions.append(DOWN)

            if not actions:
                print(" x ", pos[0], " y ", pos[1], " z ", pos[2])
            act.append(actions)

        actions = list(itertools.product(*act))
        return tuple(actions)

    def get_fingertip_pos(self):
        return self.bones[-1].get_end()

    def create_bone_boundaries(self):
        """ gives each bone its boundaries based on data from the constants file """
        num = len(self.bones)
        for i in range(num):
            # boolean arithmetic that adjusts the limit by the bone
            # num-i==1 for the finger, 2 for the wrist and 3 for the shoulder
            if num-i < 3:
                self.bones[i].x_boundary_left = -1 * self.x_side
                self.bones[i].x_boundary_right = self.x_side
                self.bones[i].y_boundary_up = parameters.up_y + (num - i == 2) * parameters.base_y
                self.bones[i].y_boundary_down = parameters.down_y + (num - i == 2) * parameters.base_y
                self.bones[i].z_boundary_back = parameters.back_z + (num - i == 2) * parameters.base_z
                self.bones[i].z_boundary_front = parameters.front_z + (num - i == 2) * parameters.base_z
            if num-i == 3:  # lock the shoulder in a small box to decrease the number of states
                self.bones[i].x_boundary_left = parameters.x_start - parameters.cube_length
                self.bones[i].x_boundary_right = parameters.x_start + parameters.cube_length
                self.bones[i].y_boundary_up = parameters.y_start + parameters.cube_length
                self.bones[i].y_boundary_down = parameters.y_start - parameters.cube_length
                self.bones[i].z_boundary_back = parameters.z_start - parameters.cube_length
                self.bones[i].z_boundary_front = parameters.z_start + parameters.cube_length


# Class for bones in the hand. Bones track their legal range of movement
class Bone:
    def __init__(self, pivot, axis, radius, angle):
        """
        :param pivot: the starting point (np.array)
        :param axis: the direction and length (np.array)
        :param radius: the width (real)
        :param angle: the angle (in radians) that the bone moves in each movement (real)
        """
        self.pivot = pivot
        self.axis = axis
        self.length = np.linalg.norm(self.axis)
        self.angle = angle
        self.radius = radius
        self.x_boundary_right = 0
        self.x_boundary_left = 0
        self.y_boundary_up = 0
        self.y_boundary_down = 0
        self.z_boundary_front = 0
        self.z_boundary_back = 0

    # get the end point of the bone
    def get_end(self):
        return self.pivot + self.axis

    def move(self, direction):
        """ Changes the axis of the bone according to direction and angle
            :param direction: UP, DOWN, RIGHT, LEFT """
        unit_axis = self.axis / np.linalg.norm(self.axis)
        self.axis = unit_axis * self.length

        if direction == UP:
            matrix = np.array([[1, 0, 0],
                               [0, np.cos(self.angle), -np.sin(self.angle)],
                               [0, np.sin(self.angle), np.cos(self.angle)]])
            self.axis = np.matmul(matrix, self.axis)

        elif direction == DOWN:
            matrix = np.array([[1, 0, 0],
                               [0, np.cos(self.angle), np.sin(self.angle)],
                               [0, -np.sin(self.angle), np.cos(self.angle)]])
            self.axis = np.matmul(matrix, self.axis)

        elif direction == RIGHT:
            matrix = np.array([[np.cos(self.angle), 0, -np.sin(self.angle)],
                               [0, 1, 0],
                               [np.sin(self.angle), 0, np.cos(self.angle)]])
            self.axis = np.matmul(matrix, self.axis)

        elif direction == LEFT:
            matrix = np.array([[np.cos(self.angle), 0, np.sin(self.angle)],
                               [0, 1, 0],
                               [-np.sin(self.angle), 0, np.cos(self.angle)]])
            self.axis = np.matmul(matrix, self.axis)
