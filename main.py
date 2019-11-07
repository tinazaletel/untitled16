# kako se odpre prva stran

# kako polinka[ html datoteko


from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def prva_stran() :
    return render_template ("prva_stran.html")

#-----------------------------------------------------


#nova podstran

@app.route("/kontakt")
def kontakt ():
    emaili = [ "ime@example.com", "ime@egmail.com", "tretji@example.com"]
    return render_template("kontakt.html", emaili=emaili)
#-----------------------------------------------------


#nova podstran

@app.route("/cv")
def cv ():
    return render_template("cv.html")

#-----------------------------------------------------
#-----------------------------------------------------Nov prva_stran

@app.route("/poslji-sporocilo", methods=["POST"])
def poslji_sporocilo ():
    zadeva = request.form.get("zadeva")
    sporocilo = request.form.get("sporocilo")

    #tukaj bi shranili te spremenljivki v bazo.

    print("zadeva je: " + zadeva)
    return render_template("sporocilo_poslano.html", zadeva=zadeva)

#prva zadeva je povazana s html, druga pa s pythonom



if __name__== '__main__':
    app.run()


