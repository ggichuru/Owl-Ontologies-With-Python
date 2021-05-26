# DECISION SUPPORT EXPLAINED

## First page

    Simple html page for data entry to define bacterium characteristics. 

## Second Page

    1. Create a new temporary ontology in order not to pollute the onto. Its IRI is in the form of "http://tmp.org/onto_XXX.owl#" where ``XXX`` is a number.

    2. Retrieve the values of the form parameters. This is done with functions `request.args.get()` and `.getList()`. 

    3. Create an individual bacterium corresponding to the values entered.

    4. Close the world for this new bacterium. This will prevent the reasoner from making assumptions about values other than those entered.

    5. Execute the reasoner on two onotlogies: the bacteria onto and the temporary onto. Inferences are placed in the temporary onotology.

    6. Retrieve the names of the classes to which the bacteria belong after reasoning. The condition `isinstance(bacterium_class, ThingClass)` allows you to limit yourself to true classes, excluding constructor and in particular restrictions created by close_world().

    7. Destroy the temporary ontology(this destroys the bacterium that we created but also its possible shape and groupings, as well as inferences).
