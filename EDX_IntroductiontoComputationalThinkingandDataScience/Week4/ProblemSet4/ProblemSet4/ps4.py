# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances  = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        # TODO
        if drug in self.getResistances():
            if self.getResistances()[drug]:
                return True
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO
        if sum([self.getResistances()[drug] for drug in activeDrugs]) \
                ==len(activeDrugs): #check if virus is resistant to all drugs.
            if random.random() < self.maxBirthProb * (1 - popDensity):
                #build the resistance
                resist = {}
                for drug in self.resistances:
                    if self.resistances[drug]==True:#resistant
                        if random.random()<1-self.mutProb:
                            resist[drug]=True
                        else:
                            resist[drug]=False
                    elif self.resistances[drug]==False:#not resistant
                        if random.random()<self.mutProb:
                            resist[drug]=True
                        else:
                            resist[drug]=False
                return ResistantVirus(self.maxBirthProb, self.clearProb,
                                     resist,self.mutProb)
            else:
                raise NoChildException
        else:
            raise NoChildException


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.postcondition = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        temp = set(self.postcondition)
        temp.add(newDrug)
        self.postcondition = temp

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.postcondition

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        resistantPop = []
        num_drugs = len(drugResist)
        for virus in self.getViruses():
            if sum([virus.isResistantTo(drug) for drug in drugResist
                    if drug in virus.getResistances()])==num_drugs:
                resistantPop.append(virus)
        return len(resistantPop)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each
          virus particle should reproduce and add offspring virus particles to
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO

        self.viruses = [i for i in self.viruses if not i.doesClear()]
        population_density = float(self.getTotalPop())/self.getMaxPop()
        viruses_ = tuple(self.getViruses())
        for vir in viruses_:
            try:
                a = vir.reproduce(population_density,self.postcondition)
                self.viruses.append(a)
            except NoChildException:
                pass
        return self.getTotalPop()



def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    numViruses = 100
    maxPop = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {"guttagonol": False, "grimpex": False}
    mutProb = 0.005

    conditions = [300, 150, 75, 0]
    con_virus_pop = []
    for con in conditions:
        virus_pop = []
        for trial in range(numTrials):
            list_virus = [ResistantVirus(maxBirthProb, clearProb, resistances,
                                             mutProb) for i in range(numViruses)]
            patient = TreatedPatient(list_virus, maxPop)
            for time in range(con):#delay time steps
                patient.update()
            patient.addPrescription("guttagonol")
            for time in range(149):
                patient.update()
            virus_pop.append(patient.update())#append the virus pop at the last time
        con_virus_pop.append(virus_pop)
        pylab.figure()
        pylab.hist(virus_pop, label = "DelayTime:%f"%con)
        pylab.show()











#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    numViruses = 100
    maxPop = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {"guttagonol": False, "grimpex": False}
    mutProb = 0.005

    conditions = [300, 150, 75, 0]
    con_virus_pop = []
    for con in conditions:
        virus_pop = []
        for trial in range(numTrials):
            list_virus = [ResistantVirus(maxBirthProb, clearProb, resistances,
                                             mutProb) for i in range(numViruses)]
            patient = TreatedPatient(list_virus, maxPop)
            for time in range(150):
                patient.update()
            patient.addPrescription("guttagonol")
            for time in range(con):#delay time steps
                patient.update()
            patient.addPrescription("grimpex")
            for time in range(149):
                patient.update()
            virus_pop.append(patient.update())#append the virus pop at the last time
        con_virus_pop.append(virus_pop)
        pylab.figure()
        pylab.hist(virus_pop, label = "DelayTime:%f"%con)
        pylab.show()



