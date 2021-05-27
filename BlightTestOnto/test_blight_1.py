from owlready2 import *
onto = get_ontology("blight_onto_01.owl").load()

# for c in onto.BlightPeriod.subclasses():
#     print(c.name)


from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def entry_page():
    html = """<html><body>
    <h1>Select conditions</h1>
<form action = "/result">
    Temperature: <br/>
            <input type="radio" name="temp" value="True"/> True<br/>
            <input type="radio" name="temp" value="False"/> False<br/>
    Humidity: <br/>
            <input type="radio" name="humd" value="True"/> True<br/>
            <input type="radio" name="humd" value="False"/> False<br/>

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

    temp = request.args.get("temp","")
    humd = request.args.get("humd", "")

    with onto_tmp:
        blightPeriod = onto.BlightPeriod()
        # good_temp = onto.Temparature()
       # good_humd = onto.Humidty()
        blightTemp = onto.BlightTemp()
        blightHumd = onto.BlightHumd()

        if temp == "True": blightTemp.isBlightTemp = True
        elif temp == "False": blightTemp.isBlightTemp = False

        if humd == "True": blightHumd.isBlightHumd = True
        elif humd == "False": blightHumd.isBlightHumd = False

        


        # close_world(blightPeriod)

        sync_reasoner([onto, onto_tmp])

        class_names = []
        for blight_class in blightPeriod.is_a:
            if isinstance(blight_class, ThingClass):
                class_names.append(blight_class.name)
        class_names = ",".join(class_names)

        html = """
        <html><body>
        <h3> Result: %s </h3>
    </body></html> 
        """ % class_names

        onto_tmp.destroy()

        return html


import werkzeug.serving
werkzeug.serving.run_simple("localhost", 4040, app)
