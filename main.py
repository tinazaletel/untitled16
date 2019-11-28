# kako se odpre prva stran

# kako polinka[ html datoteko
import hashlib
import random
import uuid
import requests
import json
from flask import Flask, render_template, request, redirect, make_response
from modeli import Komentar, db, Uporabnik



app = Flask(__name__)
db.create_all()

@app.route("/")
def prva_stran() :
    sejna_vrednost =request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if uporabnik:
        ime = uporabnik.ime

    else:
        ime = None

    komentarji = db.query(Komentar) . all()

    return render_template ("prva_stran.html", ime=ime, komentarji=komentarji)


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

# nova funkcija prijava
@app.route("/prijava", methods=["POST"])
def prijava():
    ime = request.form.get("ime")
    originalno_geslo = request.form.get("geslo")
    geslo = hashlib.sha256(originalno_geslo.encode()).hexdigest()

    #  return render_template("prva_stran.html", ime)

    sejna_vrednost = str(uuid.uuid4 ())

    uporabnik = db.query(Uporabnik). filter_by(ime=ime).first()
    if not uporabnik:
        uporabnik = Uporabnik(ime=ime, email="", geslo=geslo, sejna_vrednost=sejna_vrednost)
    else:

        if uporabnik.je_blokiran:
            return "Uporabnik blokiran, prijava ni mogoca"

        if geslo == uporabnik.geslo:
                uporabnik.sejna_vrednost = sejna_vrednost
        else:
            return "Napacno geslo"
        uporabnik.sejna_vrednost = sejna_vrednost

        #geslo je potrebno sifrirati

    db.add(uporabnik)
    db.commit()
    #shranimo v sejno vrednost

    #section token = sejna vrednost


  #  ime = request.form.get("ime")
    odgovor = make_response(redirect("/"))
    odgovor.set_cookie("sejna_vrednost", sejna_vrednost)
    return odgovor

#ce napise ("/") bo [lo na tvojo prvo stran

@app.route("/komentar", methods=["POST"])
def poslji_komentar():
    vsebina_komentarja = request.form.get("vsebina")
    # Tukaj se bo shranil komentar v podatkovno bazo
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()
    komentar = Komentar(
        avtor=uporabnik.ime,
        vsebina=vsebina_komentarja
    )
    db.add(komentar)
    db.commit()



@app.route("/skrito-stevilo")
def skrito_stevilo():
    odgovor = make_response(render_template("skrito_stevilo.html"))

    if not request.cookies.get("SkritoStevilo"):
        stevilo = str(random.randint(1, 20))
        odgovor.set_cookie("SkritoStevilo", stevilo)
    return odgovor



@app.route("/poslji-skrito-stevilo", methods=["POST"])
def poslji_skrito_stevilo():
    skrito_stevilo = request.cookies.get("SkritoStevilo")
    vpisano_stevilo =request.form.get("stevilo")

    if skrito_stevilo == vpisano_stevilo:
        return "PRAVILNO"

    else:
        return "NI PRAVILNO"

@app.route("/profil")
def moj_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napacna seja"

    return render_template("profil.html", uporabnik=uporabnik)


@app.route("/profil/uredi", methods=["GET", "POST"])
def uredi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napacna seja"


    if request.method == "GET":
       return render_template("uredi_profil.html", uporabnik=uporabnik)
    elif request.method == "POST":
        uporabnik.ime = request.form.get("ime")
        uporabnik.email = request.form.get("email")


        db.add(uporabnik)
        db.commit()

        return redirect("/profil")


@app.route("/profil/izbris", methods=["GET", "POST"])
def izbrisi_profil():
    sejna_vrednost = request.cookies.get("sejna_vrednost")
    uporabnik = db.query(Uporabnik).filter_by(sejna_vrednost=sejna_vrednost).first()

    if not uporabnik:
        return "Napacna seja"

    if request.method == "GET":
        return render_template("izbrisi_profil.html")
    elif request.method == "POST":
        db.delete(uporabnik)
        db.commit()

        odgovor = make_response(redirect("/"))
        odgovor.set_cookie("sejna_vrednost", expires=0)
        return odgovor


@app.route("/uporabniki")
def uporabniki():
    users = db.query(Uporabnik).all()
    return render_template("uporabniki.html", uporabniki= users)

@app.route("/uporabniki/<uporabnik_id>", methods=["GET", "POST"])
def prikaz_uporabnika(uporabnik_id):
    uporabnik = db.query(Uporabnik).filter_by(id=uporabnik_id).first()

    if request.method == "POST":
        blokiran = False
        if request.form.get("je_blokiran") == "on":
            blokiran = True

        uporabnik.je_blokiran = blokiran
        db.add(uporabnik)
        db.commit()

    return render_template("prikaz_uporabnika.html", uporabnik=uporabnik)

# <uporabnik_id> to je spremenljivka ki bo dadala id stevilo uporabniku

# <dodali funkcijo vreme

@app.route("/vreme")
def vreme():
    odgovor_geo = json.loads(requests.get("https://geocode.xyz/" + mesto +"?json=1").text)
    lon = odgovor_geo["longt"]
    lat = odgovor_geo["latt"]
    mesto = "Maribor"


    url = "https://opendata.si/vreme/report/?lat=" + lat + "&lon=" + lon

    odgovor = json.loads(requests.get(url).text)

    dez = odgovor ["forecast"] ["data"] [0] ["rain"]
    return render_template("vreme.html", vreme=dez)







# return redirect("/") odpre novo stran
if __name__== '__main__':
    app.run(debug=True)


