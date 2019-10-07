import matplotlib.pyplot as plt
from collections import defaultdict
import parameters as p
from itertools import product

class Data_Analyzer:
    """ general class to collect data about our learners and represent it in graphs. """
    def __init__(self):
        self.piece = None
        self.learner = None
        self.num_bones = 2
        self.disc_state = p.make_space_discrete
        self.alpha_gamma_dict = defaultdict(list)
        self.time_dict = defaultdict(list)
        self.expanded = defaultdict(list)
        self.operations = defaultdict(list)


    def add_iter_time(self, iter_time):
        self.time_dict[self.piece, self.learner, self.num_bones, self.disc_state].append(iter_time)

    def add_expanded(self, sum_exp):
        self.expanded[self.piece, self.num_bones, self.disc_state].append(sum_exp)

    def add_total_operations(self, num):
        self.operations[self.piece, self.learner, self.num_bones, self.disc_state].append(num)

    def add_alpha_gamma(self, iter_time):
        self.alpha_gamma_dict[p.alpha, p.gamma].append(iter_time)

    def plot_graphs(self):
        if p.ITER_TIME in p.stats:
            for learner in p.learners_type:
                self.iter_time_different_pieces_same_learner(learner)
                plt.clf()
            if len(p.learners_type) > 1:
                for piece in p.pieces:
                    self.iter_time_same_piece_different_learners(piece)
                plt.clf()
                if len(p.pieces) > 1:
                    self.iter_time_different_pieces_different_learners()

        if p.EXPANDED in p.stats:
            self.a_star_expanded_graph()
            plt.clf()
        if p.MEMORY in p.stats:
            pass
            plt.clf()
        if p.OPERATIONS in p.stats:
            self.operations_graph()
            plt.clf()
        if p.ALPHA_GAMMA in p.stats:
            self.iter_time_alpha_gamma()

    # Compare how a learner performs on different pieces
    def iter_time_alpha_gamma(self):
        for alpha, gamma in product(p.alpha_list, p.gamma_list):
            performance = self.alpha_gamma_dict[(alpha, gamma)]
            plt.plot(performance, label="α=" + str(alpha) + " γ=" + str(gamma))
        self.plot_graph(title="Compare iteration time for alpha and gamma ", grid=True,
                        ylabel="Iteration time (seconds)", xlabel="Number of iterations")

    # Compare how a learner performs on different pieces
    def iter_time_different_pieces_same_learner(self, learner):
        for piece in p.pieces:
            for num_bones in p.bones_list:
                for disc_state in p.discrete_list:
                    performance = self.time_dict[(piece, learner, num_bones, disc_state)]
                    if learner == p.A_STAR:
                        plt.plot((0, p.num_training), (performance[0], performance[0]),
                                 label=piece + " " + str(num_bones) + " bones " + disc_state)
                    else:
                        plt.plot(performance,
                                 label=piece + " " + str(num_bones) + " bones " + disc_state)
        self.plot_graph(title="Compare iteration time for " + learner + " pieces " + ', '.join(p.pieces),
                        grid=True, ylabel="Iteration time (seconds)", xlabel="Number of iterations")

    def iter_time_same_piece_different_learners(self, piece):
        for learner in p.learners_type:
            for num_bones in p.bones_list:
                for disc_state in p.discrete_list:
                    performance = self.time_dict[(piece, learner, num_bones, disc_state)]
                    if learner == p.A_STAR:
                        plt.plot((0, p.num_training), (performance[0], performance[0]),
                                 label=learner + " " + piece + " " + str(num_bones) + " bones " + disc_state)
                    else:
                        plt.plot(performance,
                                 label=learner + " " + piece + " " + str(num_bones) + " bones " + disc_state)
        self.plot_graph(title="Compare " + piece + " iteration time for learners " + ', '.join(p.learners_type),
                                grid=True, ylabel="Iteration time (seconds)", xlabel="Number of iterations")

    def iter_time_different_pieces_different_learners(self):
        for learner in p.learners_type:
            for piece in p.pieces:
                for num_bones in p.bones_list:
                    for disc_state in p.discrete_list:
                        performance = self.time_dict[(piece, learner, num_bones, disc_state)]
                        if learner == p.A_STAR:
                            plt.plot((0, p.num_training), (performance[0], performance[0]),
                                     label=learner + " " + piece + " " + str(num_bones) + " bones " + disc_state)
                        else:
                            plt.plot(performance,
                                     label=piece + " " + str(num_bones) + " bones " + disc_state)
        self.plot_graph(title="Compare iteration time for " + ', '.join(p.learners_type) + " on pieces:\n" +
                              ', '.join(p.pieces),
                        grid=True, ylabel="Iteration time (seconds)", xlabel="Number of iterations")

    def a_star_expanded_graph(self):
        for piece in p.pieces:
            for num_bones in p.bones_list:
                for disc_state in p.discrete_list:
                    plt.bar(piece + "\n" + str(num_bones) + " bones\n" + disc_state, self.expanded[piece,num_bones,
                                                                                                   disc_state])
        self.plot_graph(title="Compare A star expanded for pieces " + ','.join(p.pieces),
                        grid=False, ylabel="Number of nodes expanded")

    def operations_graph(self):
        for learner in p.learners_type:
            for piece in p.pieces:
                for num_bones in p.bones_list:
                    for disc_state in p.discrete_list:
                        plt.bar(learner + "\n" + piece + "\n" + str(num_bones) + " bones\n" + disc_state,
                                self.operations[piece, learner, num_bones, disc_state])
        self.plot_graph(title="Compare number of movements for learners " + ', '.join(p.learners_type),
                        grid=False, ylabel="Number of movements")

    def plot_graph(self, title, grid, xlabel="", ylabel=""):
        print("Called plot_graph for ", title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        if grid:
            plt.grid(True)
            plt.legend(loc='upper right')
        plt.show()
        plt.savefig(title)
