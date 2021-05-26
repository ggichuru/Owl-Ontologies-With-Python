from owlready2 import *

onto = get_ontology("http://test.org/drug.owl#")

with onto:
    class Drug(Thing):
        pass
    class price(Drug >> float, FunctionalProperty):
        pass
    class nb_tablet(Drug >> int, FunctionalProperty):
        pass

    # class Drug(Thing):
    #     def get_price_per_tablet(self):
    #         return self.price / self.nb_tablet

    # my_drug = Drug(price = 850.0, nb_tablet = 38)
    # print(f'One tablet goes for: KSH {my_drug.get_price_per_tablet()}')

    ## CLASS METHODS

    class Drug(Thing):
        @classmethod
        def get_price_per_tablet(self):
            return self.price / self.nb_tablet
    
    class MyDrug(Drug): pass

    MyDrug.price = float(input("Enter the amount you paid: "))
    MyDrug.nb_tablet = int(input("How many tablets were there: "))

    print(f'One tablet costs KSH {MyDrug.get_price_per_tablet()}')