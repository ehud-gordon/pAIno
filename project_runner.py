import parameters, feature_extractor
import heuristics as h, numpy as np
import midi_handler, qlearningAgents, discrete_space
from keyboard import Keyboard
from hand import Hand
from data_analyzer import Data_Analyzer
from a_star_agent import SearchProblem, a_star_search
from midi_creator import midi_creator
from itertools import product
import copy, time, sys

if parameters.debug:
    from vpython import *
    import display as d


def decay_alpha(alpha, current_iteration, num_iterations):
    return alpha * (1 - current_iteration / num_iterations)

def decay_alpha_exp(alpha, current_iteration, num_iterations):
    """ Very bad especially low alpha, do not use at all"""
    return alpha**current_iteration

def run_discrete_iteration(qlearner, hand, keyboard, disp, midi, play):
    heuristic_list = [h.fingertip_distance, h.angle_pointing, h.heur_dist_from_boxes]
    notes_to_play = midi.get_notes(parameters.midi_file)
    num_of_actions = 0
    # run discrete iteration
    for note in notes_to_play:
        note_midi = note[0]
        key_position = keyboard.midi_to_pos[note_midi]
        # If APPROXIMATION AGENT
        if parameters.learner_type == parameters.APPQ_AGENT:
            feature_ex = feature_extractor.FeatureExtractor(key_position, heuristic_list)
            qlearner.feature_extractor = feature_ex
            old_hand = copy.deepcopy(hand)  # looks like hand before the last action

        key_block = discrete_space.get_block(key_position)
        fingertip_block = discrete_space.get_block(hand.get_fingertip_pos())

        while not np.array_equal(fingertip_block, key_block):
            if play and parameters.display:
                time.sleep(0.5)  # makes viewing it possible once training is complete
            num_of_actions += 1
            hand_state = discrete_space.get_hand_state(hand, key_position)
            if parameters.learner_type == parameters.Q_AGENT:
                action = qlearner.get_action(hand_state, hand)
            if parameters.learner_type == parameters.APPQ_AGENT:
                action = qlearner.get_action(hand, hand)
            hand.move(action)
            next_state = discrete_space.get_hand_state(hand, key_position)
            hand.move_to_discrete_position(discrete_space.get_hand_pos(hand))
            fingertip_block = discrete_space.get_block(hand.get_fingertip_pos())
            disp.update_hand(hand) if disp else None
            reward = reward_func(hand, fingertip_block, key_block)
            if parameters.learner_type == parameters.Q_AGENT:
                qlearner.update(hand_state, action, next_state, reward, hand)
            if parameters.learner_type == parameters.APPQ_AGENT:
                qlearner.update(old_hand, action, hand, reward, hand)
                old_hand.move(action)
                old_hand.move_to_discrete_position(discrete_space.get_hand_pos(old_hand))
        if disp:
            disp.key_pressed(note_midi)
        if parameters.sound or play:
            if parameters.display:
                midi.play_note(note_midi)
            else:
                print("hit note: ", note_midi)
    if play:
        data_analyzer.add_total_operations(num_of_actions)

def run_continuous_iteration(qlearner, hand, keyboard, disp, midi, play):
    heuristic_list = [h.fingertip_distance, h.angle_pointing, h.heur_dist_from_boxes]
    old_hand = copy.deepcopy(hand)  # looks like hand before the last action
    notes_to_play = midi.get_notes(parameters.midi_file)
    num_of_actions = 0
    for note in notes_to_play:
        note_midi = note[0]
        key_position = keyboard.midi_to_pos[note_midi]
        feature_ex = feature_extractor.FeatureExtractor(key_position, heuristic_list)
        qlearner.feature_extractor = feature_ex
        pos = hand.get_fingertip_pos()
        if parameters.debug:
            box(pos=d.vec2v_vec(key_position), length=1, height=1, width=1,
                color=color.red)
            time.sleep(5)
        # check hitting the key: the distance between key and fingertip is small
        while np.linalg.norm(key_position - pos) > parameters.radius_from_key_goal:
            if play and parameters.display:
                time.sleep(0.5)  # makes viewing it possible once training is complete
            num_of_actions += 1
            action = qlearner.get_action(hand, hand)
            hand.move(action)
            disp.update_hand(hand) if disp else None
            pos = hand.get_fingertip_pos()
            reward = reward_func(hand, pos, key_position)
            qlearner.update(old_hand, action, hand, reward, hand)
            old_hand.move(action)
        if disp:
            disp.key_pressed(note_midi)
        if parameters.sound or play:
            if parameters.display:
                midi.play_note(note_midi)
            else:
                print("hit note: ", note_midi)
    if play:
        data_analyzer.add_total_operations(num_of_actions)

def reward_func(hand, fingertip_block, key_block):
    reward = 0
    dist = np.linalg.norm(np.array(fingertip_block) - np.array(key_block))
    joints_out_of_box = hand.how_many_joints_out_of_boxes()
    reward -= 0.2 * joints_out_of_box
    if parameters.make_space_discrete == parameters.DISCRETE:
        if np.array_equal(fingertip_block, key_block):
            reward += 1
        else:
            reward -= (dist / parameters.max_dist)
    else:
        if dist <= parameters.radius_from_key_goal:
            reward += 1
        else:
            reward -= (dist / parameters.max_dist)
    if parameters.debug:
        print(reward)
    return reward


def run_qlearner(data_analyzer, midi, keyboard, agent=parameters.Q_AGENT, angle=0):
    if agent == parameters.APPQ_AGENT:
        qlearner = qlearningAgents.ApproximateQAgent(epsilon=parameters.epsilon, alpha=parameters.alpha,
                                                     gamma=parameters.gamma)
    else:
        qlearner = qlearningAgents.QLearningAgent(epsilon=parameters.epsilon, alpha=parameters.alpha,
                                                  gamma=parameters.gamma)
    if agent == parameters.Q_AGENT and parameters.load_training == 1:
        load_q_table(qlearner)
    play = False  # when training is done, this becomes true
    disp = None

    for i in range(parameters.num_iterations):
        hand = Hand(pivot=parameters.pivot, num_bones=parameters.num_bones, num_fingers=parameters.num_of_fingers,
                    joint_pos=parameters.joint_pos, bone_angle=angle)

        if parameters.display_training and parameters.display:  # display vpython while in training mode.
            import display
            disp = display.Display(keyboard, hand, midi)
            display.draw_box(keyboard.white_keys, parameters.num_bones == 3)
            disp.draw_keyboard_strike_positions()
            time.sleep(2)
        if i % 4 == 0:
            print("iteration ", i)
        if i == parameters.num_training:                # stop training mode
            qlearner.epsilon = 0                  # stop random actions
            qlearner.alpha = 0                    # stop learning q-values
            if agent == parameters.Q_AGENT:
                qlearner.ignore_zero = True       # ignores unlearned states
            # data_analyzer.plot_iteration_times()  # print the training data.
            play = True
            # if not parameters.num_training == 0:
            #     input("hey! listen to me play. just press Enter, and magic will happen!")
            if not parameters.display_training and parameters.display:  # if display is off, turn it on.
                import display
                disp = display.Display(keyboard, hand, midi)
                display.draw_box(keyboard.white_keys, parameters.num_bones == 3)
                disp.draw_keyboard_strike_positions()
        start_time = time.time()
        if parameters.make_space_discrete == parameters.DISCRETE:
            run_discrete_iteration(qlearner, hand, keyboard, disp, midi, play)
        else:
            run_continuous_iteration(qlearner, hand, keyboard, disp, midi, play)
        end_time = time.time()
        run_time = end_time - start_time
        print("Q iteration runtime: ", run_time, " seconds.")

        if i < parameters.num_training:
            # qlearner.alpha = decay_alpha(alpha=alpha, current_iteration=i, num_iterations=parameters.num_iterations)
            qlearner.alpha = decay_alpha(alpha=alpha, current_iteration=i, num_iterations=parameters.num_iterations)
            data_analyzer.add_iter_time(run_time)
            data_analyzer.add_alpha_gamma(iter_time=run_time)
    if agent == parameters.Q_AGENT:
        save_q_table(qlearner)


def save_q_table(qlearner):
    trainings = open('trainings.txt', "w+")
    for k, v in qlearner.Q.items():
        trainings.write(str(k) + ' : ' + str(v) + '\n')
    trainings.close()
def parse_line(line):
    lst = list(re.split(',| |\(|\)', line))
    while '' in lst :
        lst.remove('')
    lst = [float(i) for i in lst]
    triples = []
    for i in range(parameters.num_bones):
        triples.append(tuple(lst[3*i : 3*i + 3]))
    return tuple([tuple(triples), lst[3*parameters.num_bones:]])
def load_q_table(qlearner):
    training = open('trainings.txt', 'r')
    for line in training:
        temp = line.split(" : ")
        qlearner.Q[parse_line(temp[0])] = float(temp[1])
    training.close()


def run_astar_agent(data_analyzer, midi, keyboard, angle):
    import heuristics
    hand = Hand(pivot=parameters.pivot, num_bones=parameters.num_bones, num_fingers=parameters.num_of_fingers,
                joint_pos=parameters.joint_pos, bone_angle=angle)
    if parameters.display:
        import display
        disp = display.Display(keyboard, hand, midi)
        display.draw_box(keyboard.white_keys, parameters.num_bones == 3)
        disp.draw_keyboard_strike_positions()
    run_time, expanded, operations = 0, 0, 0
    notes_to_play = midi.get_notes(parameters.midi_file)
    for note in notes_to_play:
        start_time = time.time()
        note_midi = note[0]
        print("A star starts key", note_midi)
        key_position = keyboard.midi_to_pos[note_midi]
        problem = SearchProblem(hand=hand, end_pos=key_position)
        path = a_star_search(problem, heuristics.fingertip_distance)
        end_time = time.time()
        run_time += end_time - start_time
        expanded += problem.expanded
        if len(path) == 0:
            if parameters.display:
                midi.play_note(note_midi)
            else:
                print("hit key: ", note_midi)
        for move in path:
            operations += 1
            hand.move(move)
            if parameters.make_space_discrete == parameters.DISCRETE:
                hand.move_to_discrete_position(discrete_space.get_hand_pos(hand))
            if parameters.display:
                disp.update_hand(hand)
                time.sleep(0.5)  # to make seeing easier
            if problem.is_goal_state(hand):
                if parameters.display:
                    midi.play_note(note_midi)
                else:
                    print("hit key: ", note_midi)

    print("A* iteration runtime: ", run_time, " seconds.")
    data_analyzer.add_iter_time(run_time)
    data_analyzer.add_expanded(expanded)
    data_analyzer.add_total_operations(operations)


def runner(data_analyzer, keyboard, angle):
    """ run the learning agent """
    for piece in parameters.pieces:
        data_analyzer.piece = piece
        print("==", piece, "==")
        midi_creator(piece)
        if parameters.learner_type == parameters.Q_AGENT:
            run_qlearner(data_analyzer, midi, keyboard, agent=parameters.Q_AGENT, angle=angle)
        elif parameters.learner_type == parameters.APPQ_AGENT:
            run_qlearner(data_analyzer, midi, keyboard, agent=parameters.APPQ_AGENT, angle=angle)
        elif parameters.learner_type == parameters.A_STAR:
            run_astar_agent(data_analyzer, midi, keyboard, angle)

if __name__ == '__main__':
    midi = midi_handler.MidiHandler()
    data_analyzer = Data_Analyzer()
    for space_state in parameters.discrete_list:
        print("================================================", space_state, "================================================")
        data_analyzer.disc_state = space_state
        parameters.make_space_discrete = space_state
        for learner in parameters.learners_type:
            data_analyzer.learner, parameters.learner_type = learner, learner
            print("===========================", learner, "===========================")
            for num_bones in parameters.bones_list:
                data_analyzer.num_bones = num_bones
                print("====", num_bones, "BONES ====")
                for alpha, gamma in product(parameters.alpha_list, parameters.gamma_list):
                    parameters.update_params(num_bones, alpha, gamma)
                    keyboard = Keyboard(num_keys=parameters.num_keys, mid_key=parameters.mid_key)
                    angle = discrete_space.set_base_angle(keyboard)
                    if angle == 0:
                        print("There was an error")
                        exit(1)
                    runner(data_analyzer, keyboard, angle)
    if parameters.graph_producing:
        data_analyzer.plot_graphs()

    midi.close_player()
