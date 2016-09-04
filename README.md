### Subject
This project is about an autonomous taxicab trying to reach its destination in the alloted time while respecting traffic rules. The taxicab controlled in the program is the red car. This program uses pygame in order to display the graphical interface.

### How it works
The taxicab upadtes its knowledge of the environment regularly. The traffic lights and oncoming cars are observed as well as the direction and heading necessary to reach the destination (without taking the traffic into account). A reward is given to each action taken by the taxicab and memorized in order to improve next trips. The taxicab first needs to explore its environment and then is able to choose the best action. The Q-Learning algorithm is used to update the Q-Values with the reward, a learning rate alpha, a greedy parameter epsilon and a discount factor gamma.

### Results
By using gamma depending on time, a minimum success rate of 99% is obtained. 

### Running the simulation
In the main directory, enter for Linux systems:
python smartcab/agent.py

update_delay can be set to a lower value in order to speed up the simulation.


