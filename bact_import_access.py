from owlready2 import *

onto = get_ontology("bacteriaOnto.owl").load()

import bact_import

my_bacterium = onto.Staphylococcus()
print(my_bacterium.my_method(), '\n')

my_bacterium = onto.Bacterium()
print(my_bacterium.my_method(), '\n')