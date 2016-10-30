#!/usr/bin/python2.7
# -*-coding:utf-8 -*

"""
Main file of the Simudyne developer test project.

Author : Augustin De Champs, Date : 30/10/2016

Compile with python 2.7 if possible or python 2.x.
Python modules required : matplotlib, numpy
Execute python2.7 main.py to compile and launch.

For data importation, a CSV file is required :
The CSV file fields must be the following :
Agent_Breed;Policy_ID;Age;Social_Grade;Payment_at_Purchase;Attribute_Brand;Attribute_Price;Attribute_Promotions;Auto_Renew;Inertia_for_Switch
Float numbers must follow the X.XXX format (Y,YYY will raise an error).
The CSV dialect will be automatically deduced from the CSV file.
See data-example.csv as an example of correct importation file.
"""

from importer import *
from simulate import *
from gui import *

root = tk.Tk()
app = GUIApp(root)
root.mainloop()
