

class AgentsMemory:
    """Saving the agents state, Brand_Factor and count each year."""
    def __init__(self):
        self.agents = [] #index i of the list is year i
        self.Brand_Factor = [] #index i of the list is year i
        self.count = []

    def saveState(self, agents, Brand_Factor, count):
        self.agents.append(agents)
        self.Brand_Factor.append(Brand_Factor)
        self.count.append(count)
