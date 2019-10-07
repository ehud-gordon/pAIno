from collections import defaultdict
import parameters
import matplotlib.pyplot as plt
import numpy as np

# indices = np.array([i for i in range(len(iterations))])
# iter_times = np.array(iterations)
# plt.plot(indices, iter_times)
plt.plot((0,parameters.num_training), (5, 5), label="t")
plt.xlabel('training iterations')
plt.ylabel('time (s)')
plt.title("ti")
plt.grid(True)
plt.legend(loc='upper right')
plt.show()
plt.savefig("ti")
