from owlready2 import *

#load ontology
onto = get_ontology("bacteriaOnto.owl").load()
print()
for p in onto.properties():
    print(p.name)

# Accessing entities
print(onto.unknown_bacterium.name)

# Individuals
print(onto.unknown_bacterium.is_a)
print(onto.unknown_bacterium.equivalent_to)

# Relations
print(onto.unknown_bacterium.gram_positive)
print(onto.unknown_bacterium.has_shape)
print(onto.unknown_bacterium.has_grouping.first())
##inverse taken into account    first() - retrieves first element in the list
print(onto.in_cluster1.is_grouping_of.first())
print()

# Classes
print(issubclass(onto.Coccus, onto.Bacterium))
for sc in onto.Bacterium.subclasses():
    print(f'{sc.name} is a subclass of Bacterium class')
print(onto.Bacterium.descendants(include_self = False))