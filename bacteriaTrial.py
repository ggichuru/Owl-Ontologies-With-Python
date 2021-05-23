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
print()
print(onto.Coccus.is_a)

# change the name of property
onto.has_grouping.python_name = "groupings"
print(onto.unknown_bacterium.groupings, '\n')

# Searching for entities            #NB:/ is case sensitive by default
print(onto.search(iri = "*Coccus*"))                    #search all entities whose iri contains Coccus 
print(onto.search(iri = "*Coccus*", _case_sensitive = False))
r = onto.search(iri = "*Coccus*", _case_sensitive = False)  #lazy list
print(r)
# search multiple parameters
s = onto.search(type = onto.Bacterium, gram_positive = True)
print(s)
print(onto.search(type = onto.Bacterium, gram_positive = "*"))     #search for a bacteria whose gram status is known
# search for individuals having no relation
print(onto.search(type = onto.Bacterium, has_shape = None))
# search all ontologies incase multiple have been loaded
print(default_world.search(iri="*Coccus*"))
# Nested search
s = onto.search(type = onto.Bacterium, has_grouping = onto.search(type = onto.InChain))
# search_one is used to return one result instead of a list
print(onto.search_one(iri = "*Coccus*", _case_sensitive = False))