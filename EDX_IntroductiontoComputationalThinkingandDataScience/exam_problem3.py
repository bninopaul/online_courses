import random
import pylab

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 50
CURRENTFOXPOP = 300

def rabbitGrowth():
    """
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up,
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP

    # TO DO
    for rabbit in range(CURRENTRABBITPOP):
        prob_reproduce = 1.0-(CURRENTRABBITPOP/float(MAXRABBITPOP))
        if random.random() <= prob_reproduce and CURRENTRABBITPOP < MAXRABBITPOP:
            CURRENTRABBITPOP += 1

def foxGrowth():
    """
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP
    global CURRENTFOXPOP

    # TO DO
    for fox in range(CURRENTFOXPOP):
        eat_prob = CURRENTRABBITPOP/float(MAXRABBITPOP)
        if random.random()<=eat_prob and CURRENTRABBITPOP > 10:
            CURRENTRABBITPOP -= 1
            if random.random()<= 1./3:
                CURRENTFOXPOP += 1
        else:
            if random.random()<= 1./10 and CURRENTFOXPOP > 10:
                CURRENTFOXPOP -= 1



def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """

    # TO DO
    rabbit_populations = []
    fox_populations = []
    for i in range(numSteps):
        rabbitGrowth()
        foxGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        fox_populations.append(CURRENTFOXPOP)
    return rabbit_populations, fox_populations
def plot(rabbits, foxes):
    N = len(rabbits)
    pylab.plot(range(N), rabbits, 'go', label = "rabbit pop")
    pylab.plot(range(N), foxes, 'ro', label = "foxes pop")
    rab_coeff = pylab.polyfit(range(N), rabbits, 2)
    fox_coeff = pylab.polyfit(range(N), foxes, 2)
    pylab.plot(pylab.polyval(rab_coeff, range(N)), 'g-', label = "rabbit polyfit")
    pylab.plot(pylab.polyval(fox_coeff, range(N)), 'r-', label = "fox polyfit")
    pylab.xlabel("Time")
    pylab.ylabel("Population")
    pylab.title("Dynamics of Rabbit and Fox Population")
    pylab.legend()
    pylab.show()

if __name__ == '__main__':
    rab, fox = runSimulation(200)
    print "Rabbit Population:\n {}\nFoxes Population:\n {}\n".format(rab, fox)
    plot(rab, fox)
