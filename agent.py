

class Agent:
    """Class defining an agent defined by multiple attributes"""

    def __init__(self, Agent_Breed, Policy_ID, Age, Social_Grade, Payment_at_Purchase, Attribute_Brand, Attribute_Price, Attribute_Promotions, Auto_Renew, Inertia_for_Switch):
        """Agent constructor"""
        self.Agent_Breed = Agent_Breed
        self.Breed_Actual_Status = "Unchanged" #Unchanged, Lost, Gained, or Regained
        self.Breed_Last_Status = "Unchanged" #last breed status before actual status
        self.Policy_ID = str(Policy_ID)
        self.Age = int(Age)
        self.Social_Grade = int(Social_Grade)
        self.Payment_at_Purchase = int(Payment_at_Purchase)
        self.Attribute_Brand = float(Attribute_Brand)
        self.Attribute_Price = float(Attribute_Price)
        self.Attribute_Promotions = float(Attribute_Promotions)
        self.Auto_Renew = int(Auto_Renew)
        self.Inertia_for_Switch = int(Inertia_for_Switch)
        self.Affinity = self.Payment_at_Purchase/self.Attribute_Price + (2 * self.Attribute_Promotions * self.Inertia_for_Switch)

    """def affinity(self):
        Function calculating the agent affinity
        return self.Payment_at_Purchase/self.Attribute_Price + (2 * self.Attribute_Promotions * self.Inertia_for_Switch)"""
