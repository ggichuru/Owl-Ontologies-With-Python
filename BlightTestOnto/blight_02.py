import werkzeug.serving
from flask import Flask, request
from owlready2 import *
onto = get_ontology("BlightTestOnto/blight_02.owl").load()

for c in onto.Resistance.subclasses():
    print(c.name)


app = Flask(__name__)


@app.route('/')
def entry_page():
    html = """<html><body>
    <h1>Select conditions</h1>
<form action = "/result">
    Blight Period: <br/>
            <input type="radio" name="temp" value="True"/> True<br/>
            <input type="radio" name="temp" value="False"/> False<br/>
    <br/> <br/>
    <input type="submit"/>
</form>
</body></html>
    """

    return html


ONTO_ID = 0


@app.route('/result')
def page_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    onto_tmp = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)

    temp = request.args.get("temp", "")

    with onto_tmp:
        blightPeriod = onto.BlightPeriod()

        if temp == "True":
            blightPeriod.blightPositive = True
        elif temp == "False":
            blightPeriod.blightPositive = False

        close_world(blightPeriod)

        sync_reasoner([onto, onto_tmp])

        class_names = []
        for blight_class in blightPeriod.is_a:
            if isinstance(blight_class, ThingClass):
                class_names.append(blight_class.name)
        class_names = ",".join(class_names)

        if class_names == 'Healthy':
            class_names = 'Your potatoes are healthy, check again tomorrow.'
        elif class_names == 'Diseased':
            class_names = 'Unfortunately There is a posibility of Blight. Mitigate'

            html = """<html><body>
                <h3> Result: %s </h3>
                <br /> <br /><hr>
                <h1>Select conditions</h1>
                <form action = "/disease">
                    Select Variety:<br/>
                    <input type="radio" name="cultivar" value="Faulu"/> Kenya Faulu<br/>
                    <input type="radio" name="cultivar" value="Karibu"/> Kenya Karibu<br/>
                    <input type="radio" name="cultivar" value="Chaguo"/> Chaguo<br/>
                    <input type="radio" name="cultivar" value="Mavuno"/> Kenya Mavuno<br/>
                    <input type="radio" name="cultivar" value="Sifa"/> Kenya Sifa<br/>
                    <input type="radio" name="cultivar" value="Tigoni"/> Tigoni<br/>
                    <input type="radio" name="cultivar" value="Asante"/> Asante<br/>
                    <br/>
                    <br/>
                    <input type="submit"/>
                    </form>
                    </body></html>
                    """ % class_names
            return html

        html = """
        <html><body>
        <br/><hr>
        <h3> Result: %s </h3>
    </body></html> 
        """ % class_names

        onto_tmp.destroy()

        return html


@app.route('/diseased')
def diseased_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    onto_tmp1 = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)
    
    cultivar = request.args.get("cultivar", "")

    with onto_tmp1:
        resistance = onto.Resistance()

        if cultivar:
            cultivar_class = onto[cultivar]
            resistance.hasCultivar = cultivar_class()
            
        close_world(resistance)
        sync_reasoner([onto, onto_tmp1])

        class_names = []
        
        for resistance_class in resistance.is_a:
            if isinstance(resistance_class, ThingClass):
                class_names.append(resistance_class.name)
    
        class_names = ",".join(class_names)

        if class_names == "Good":
            class_names = 'The crops have high resitance'
        elif class_names == "Poor":
            class_names = 'The crops have low resitance'

        html = """
    <html><body>
    <br/><hr>
        <h3> Crop Resistance:</h3>
        <br/>
        <p> %s </p>
    </body></html>    
    """ % class_names

        onto_tmp1.destroy()

        return html


werkzeug.serving.run_simple("localhost", 4040, app)
