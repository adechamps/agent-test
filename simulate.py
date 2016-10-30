
from agent import *

def simulate1year(listAgents, Brand_Factor):
    """Function simulating the agents evolution during 1 year."""
    for agent in listAgents:
        agent.Age +=1
        if not agent.Auto_Renew:
            if agent.Agent_Breed == "Breed_C":
                if agent.Affinity < (agent.Social_Grade * agent.Attribute_Brand):
                    """C -> NC : Breed_C Lost"""
                    agent.Agent_Breed = "Breed_NC"
                    agent.Breed_Last_Status = agent.Breed_Actual_Status
                    agent.Breed_Actual_Status = "Breed_C Lost"

            elif agent.Agent_Breed == "Breed_NC":
                if agent.Affinity < (agent.Social_Grade * agent.Attribute_Brand * Brand_Factor):
                    """NC -> C : Breed_C Gained (or Regained)"""
                    agent.Agent_Breed = "Breed_C"
                    agent.Breed_Last_Status = agent.Breed_Actual_Status
                    if agent.Breed_Last_Status == "Breed_C Lost":
                        """Lost then Gained : Regained"""
                        agent.Breed_Actual_Status = "Breed_C Regained"
                    else:
                        agent.Breed_Actual_Status = "Breed_C Gained"

def simulate(nbYears, listAgents, Brand_Factor):
    """Function simulating the agents evolution during nbYears years."""

    for y in range(nbYears):
        #print("######## YEAR "+str(y+1)+" ########")
        for agent in listAgents:
            agent.Age +=1
            if not agent.Auto_Renew:
                if agent.Agent_Breed == "Breed_C":
                    if agent.Affinity < (agent.Social_Grade * agent.Attribute_Brand):
                        """C -> NC : Breed_C Lost"""
                        agent.Agent_Breed = "Breed_NC"
                        agent.Breed_Last_Status = agent.Breed_Actual_Status
                        agent.Breed_Actual_Status = "Breed_C Lost"

                elif agent.Agent_Breed == "Breed_NC":
                    if agent.Affinity < (agent.Social_Grade * agent.Attribute_Brand * Brand_Factor):
                        """NC -> C : Breed_C Gained (or Regained)"""
                        agent.Agent_Breed = "Breed_C"
                        agent.Breed_Last_Status = agent.Breed_Actual_Status
                        if agent.Breed_Last_Status == "Breed_C Lost":
                            """Lost then Gained : Regained"""
                            agent.Breed_Actual_Status = "Breed_C Regained"
                        else:
                            agent.Breed_Actual_Status = "Breed_C Gained"

            #print(agent.Policy_ID + " : " + agent.Agent_Breed + " : " + agent.Breed_Actual_Status)

def printOutput(listAgents):
    """Function printing the number of agent with each breed and status"""
    nbBreed_C=0
    nbBreed_NC=0
    nbLost=0
    nbGained=0
    nbRegained=0
    nbUnchanged=0
    for agent in listAgents:
        if agent.Agent_Breed == "Breed_C":
            nbBreed_C+=1
        elif agent.Agent_Breed == "Breed_NC":
            nbBreed_NC+=1
        if agent.Breed_Actual_Status == "Breed_C Lost":
            nbLost+=1
        elif agent.Breed_Actual_Status == "Breed_C Gained":
            nbGained+=1
        elif agent.Breed_Actual_Status == "Breed_C Regained":
            nbRegained+=1
        elif agent.Breed_Actual_Status == "Unchanged":
            nbUnchanged+=1
    print("Number of agents : "+str(len(listAgents)))
    print("Breed_C : "+str(nbBreed_C))
    print("Breed_NC : "+str(nbBreed_NC))
    print("Breed_C Lost : "+str(nbLost))
    print("Breed_C Gained : "+str(nbGained))
    print("Breed_C Regained : "+str(nbRegained))
    print("Unchanged : "+str(nbUnchanged))
