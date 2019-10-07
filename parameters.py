# parameters for the learning algorithms.
# change all hyper parameters here for ease of use.
import numpy as np

# constants for different running parameters
CONTINUOUS, DISCRETE = "Continuous", "Discrete"
LJ, OTJ_FIRST, OTJ_FULL, CLOSE_NOTES, FAR_NOTES = "LJ", "ode to joy", "Ode To Joy", "Close Notes", "Far Notes"
Q_AGENT, APPQ_AGENT, A_STAR = "Q_AGENT", "Approximate", "A STAR"
ITER_TIME, MEMORY, EXPANDED, OPERATIONS, ALPHA_GAMMA = "ITER_TIME", "MEMORY", "EXPANDED", "OPERATIONS", "ALPHA_GAMMA"

# change keyboard settings
mid_key = 64   # when using discrete, don't forget to change to white key
num_keys = 18

# change display and sound settings
debug = 0
display = 0
sound = 0
display_training = 0
graph_producing = True

# change algorithm parameters
epsilon = 0.1
num_training = 50
num_performances = 2
num_iterations = num_training + num_performances
radius_from_key_goal = 2      # when space is continuous
radius_crit_zone = 0.5        # for the fingertip heuristic
learners_type = [A_STAR]      # Choose Q_AGENT, APPQ_AGENT, A_STAR
pieces = [OTJ_FIRST]           # Choose LJ / OTJ_FIRST / OTJ_FULL / CLOSE_NOTES / FAR_NOTES
bones_list = [3]
discrete_list = [DISCRETE, CONTINUOUS]  # Choose DISCRETE / CONTINUOUS
stats = [OPERATIONS, EXPANDED]           # for graphs. Choose ITER_TIME, MEMORY, EXPANDED, OPERATIONS, ALPHA_GAMMA
alpha_list = [0.2]
gamma_list = [0.5]
# alpha gamma for q_learner should be high (0.8, 0.8)
# alpha gamma for approximate should be low (0.2, 0.5)

def update_params(num_of_bones, a, g):
    """ Changes certain parameters between multiple runs """
    global num_bones, joint_pos, pivot, alpha, gamma, x_start, y_start, z_start
    num_bones = num_of_bones
    if num_of_bones == 1:
        joint_pos = [[0, 2, 30], [0, 3, 0], [3, 6.5, 12], [0, 3, 0]]
    if num_of_bones == 2:
        joint_pos = [[10, 2, 39], [3, 6.5, 12], [0, 3, 0]]
    if num_of_bones == 3:
        joint_pos = [[-7, 2, 53], [10, 1.5, 39], [3, 6.5, 12], [0, 3, 0]]
    pivot = joint_pos[0]
    x_start = joint_pos[1][0]
    y_start = joint_pos[1][1]
    z_start = joint_pos[1][2] + W_K_M[2] / 4
    alpha = a
    gamma = g

# these are for internal use, do NOT change them here
make_space_discrete = None
joint_pos = [[10, 2, 39], [3, 6.5, 12], [0, 3, 0]]
pivot = joint_pos[0]
num_bones = 3
learner_type = A_STAR
W_K_M = np.array([2.2, 2, 14.3])
alpha = 0.8
gamma = 0.8
load_file = 0
load_training = 0
num_of_fingers = 0

# for midi, do NOT change
midi_file = "midi_file.mid"
QUARTER = 32
EIGHTH = 16
HALF = 64

# constants that affect limitations on bone movements
up_y = 10 * W_K_M[1]
down_y = -0.5 * W_K_M[1]
back_z = -1 * W_K_M[2]
front_z = W_K_M[2]
base_y = 1.5 * W_K_M[1]
base_z = 3 * W_K_M[0]
x_const = 7
x_start = joint_pos[1][0]
y_start = joint_pos[1][1]
z_start = joint_pos[1][2] + W_K_M[2] / 4
cube_length = W_K_M[0] * 4
white_keys = np.ceil(num_keys*7/12)
max_dist = 2 * (white_keys // 2 + x_const) * W_K_M[0]
