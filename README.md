# agent-test
Simudyne programming test

Author : Augustin De Champs, Date : 30/10/2016

Compile with python 2.7 if possible or python 2.x.
Python modules required : matplotlib, numpy
Execute command "python2.7 main.py" to compile and launch the program.

For data importation, a CSV file is required :
The CSV file fields must be the following : 
Agent_Breed;Policy_ID;Age;Social_Grade;Payment_at_Purchase;Attribute_Brand;Attribute_Price;Attribute_Promotions;Auto_Renew;Inertia_for_Switch
Float numbers must follow the X.XXX format (Y,YYY will raise an error).
The CSV dialect will be automatically deduced from the CSV file.
See data-example.csv as an example of correct importation file. 

A standalone program is available : unzip dist-windows.zip and execute main.exe
