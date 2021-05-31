import werkzeug.serving
from flask import Flask, request
from owlready2 import *
onto = get_ontology("blight_02.owl").load()

for c in onto.Resistance.subclasses():
    print(c.name)


app = Flask(__name__)


@app.route('/')
def entry_page():
    html = """<html><body>
    <h3> Enter weather conditions </h3>
<form action = "/result">
    <label for="temp">Temperature:</label>
    <br/>
        <input type="number" name="temp">
        <br/>
    <label for="humd">Humidty:</label>
    <br/>
        <input type="number" name="humd">
        <br/>
        <hr>
            <br/><h3> Select crop variety </h3><br/>
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
    """

    return html


ONTO_ID = 0


@app.route('/result')
def page_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    onto_tmp = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)

    temp = request.args.get("temp", type=int)
    humd = request.args.get("humd", type=int)

    if ((temp >= 15) and (humd >= 85)):
        bp = "True"
    else: bp = "False"


    cultivar = request.args.get("cultivar", "")

    with onto_tmp:
        blightPeriod = onto.BlightPeriod()

        if bp == "True":
            blightPeriod.blightPositive = True
        elif bp == "False":
            blightPeriod.blightPositive = False

        close_world(blightPeriod)
        sync_reasoner([onto, onto_tmp])

        resistance = onto.Resistance()

        if cultivar:
            cultivar_class = onto[cultivar]
            resistance.hasCultivar = cultivar_class()
            
        close_world(resistance)

        sync_reasoner([onto, onto_tmp])

        resistance_names = []
        period_names = []
        
        for resistance_class in resistance.is_a:
            if isinstance(resistance_class, ThingClass):
                resistance_names.append(resistance_class.name)

        for blight_class in blightPeriod.is_a:
            if isinstance(blight_class, ThingClass):
                period_names.append(blight_class.name)

        class_names = ",".join(period_names)
        res_names = ",".join(resistance_names)
        
        if class_names == "Healthy":
            html = """
            <html><body>
            <h2> Your potatoes are healthy </h2>
            </body></html>
            """
            return html
        
        elif class_names == "Diseased":
            html = """
            <html><body>
            <h2> Your potatoes are disease prone </h2>
            
            <hr>
            <p> Your crop resistance is <strong>%s</strong> </p>
            </body></html>
            """ % res_names

            return html

        onto_tmp.destroy()

        

werkzeug.serving.run_simple("localhost", 5000, app)