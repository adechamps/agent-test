import csv,sys
from agent import *
import tkMessageBox

def importData(filename):
    """Function importing data from the csv file and constructing an agent object from each line of the file.
    Returns a list of Agent objects."""
    print("Opening file...")
    agents = []
    with open(filename, 'r') as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(1024)) #sniffing the csv format
            csvfile.seek(0)
            reader = csv.DictReader(csvfile,dialect=dialect)
            print("File opened.")
        except csv.Error as e:
            tkMessageBox.showerror("Error", "Error while detecting file format\n"+'file {} : {}'.format(filename, e))
        else:
            try:
                i=1
                print("Serializing data...")
                for row in reader:
                    agents.append(Agent(row["Agent_Breed"], row["Policy_ID"], row["Age"], row["Social_Grade"], row["Payment_at_Purchase"], row["Attribute_Brand"], row["Attribute_Price"], row["Attribute_Promotions"], row["Auto_Renew"], row["Inertia_for_Switch"]))
                    i+=1
                    """if i>10:
                        break"""
            except (csv.Error, ValueError) as e:
                tkMessageBox.showerror("Error", "Error while reading the file\n"+'file {}, line {}: {}'.format(filename, reader.line_num, e))
            else:
                print(str(len(agents))+" lines imported !")
    return agents

def exportData(path, listAgents):
    """Exports data as a csv file"""
    with open(path, 'w') as csvfile:
        print("File opened.")
        try:
            fieldnames = ["Agent_Breed","Policy_ID","Age","Social_Grade","Payment_at_Purchase","Attribute_Brand","Attribute_Price","Attribute_Promotions","Auto_Renew","Inertia_for_Switch"]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            print("Exporting data...")
            writer.writeheader()
            rows = [{
                "Agent_Breed": agent.Agent_Breed,
                "Policy_ID": agent.Policy_ID,
                "Age": str(agent.Age),
                "Social_Grade": str(agent.Social_Grade),
                "Payment_at_Purchase": str(agent.Payment_at_Purchase),
                "Attribute_Brand": str(agent.Attribute_Brand),
                "Attribute_Price": str(agent.Attribute_Price),
                "Attribute_Promotions": str(agent.Attribute_Promotions),
                "Auto_Renew": str(agent.Auto_Renew),
                "Inertia_for_Switch": str(agent.Inertia_for_Switch)
            } for agent in listAgents]
            writer.writerows(rows)
        except (csv.Error, ValueError) as e:
            tkMessageBox.showerror("Error", "Error while writing the file\n"+'file {}, line {}: {}'.format(filename, writer.line_num, e))
        else:
            print("File exported !")
