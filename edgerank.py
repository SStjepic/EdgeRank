from datetime import datetime
import math

def EdgeRank(Graf, sviStatusi, korisnik):
    pretraga=[]
    for id in sviStatusi:
        if korisnik != {}:
            medjusobni_odnos = Graf.get_edge_data(korisnik["ime"], sviStatusi[id]["autor"])
        else:
            medjusobni_odnos = None
        if medjusobni_odnos != None:
            medjusobni_odnos = medjusobni_odnos["tezina"]
        else:
            medjusobni_odnos = 0
        if medjusobni_odnos == 0:
            popularnost = vreme_populatnosti(sviStatusi[id]["datum"]) * popularnost_objave(sviStatusi[id])
        else:
            popularnost = vreme_populatnosti(sviStatusi[id]["datum"]) * popularnost_objave(sviStatusi[id]) * medjusobni_odnos
        rezultat = {
            "status_id": id,
            "tekst": sviStatusi[id]["tekst"],
            "popularnost": popularnost,
            "prijatelj": True if korisnik !={} and sviStatusi[id]["autor"] in korisnik["prijatelji"] else False,
            "datum": datetime.strftime(sviStatusi[id]["datum"], "%Y-%m-%d %H:%M:%S"),
            "autor": sviStatusi[id]["autor"]
        }
        pretraga.append(rezultat)
            
    pretraga = sorted(pretraga,key=lambda i: i["popularnost"])
    
    return pretraga


def vreme_populatnosti(datum_objave):
    danas = datetime.now()
    razlika = danas-datum_objave
    return pow(math.e, -1*((razlika.days)//15))
    
def popularnost_objave(status):
    
    wows = 50
    loves =40
    hahas =30
    sads =20
    angrys= 5
    likes= 15
    shares= 50
    special= 35
    komentari = 30
    
    popularnost = 0
    if status["br_komentara"] !=0:
        popularnost += status["br_komentara"] * komentari
    if status["br_deljenja"] !=0:
        popularnost += status["br_deljenja"] * shares
    if status["br_svidjanja"] !=0:
        popularnost += status["br_svidjanja"] * likes
    if status["br_voli"] !=0:
        popularnost += status["br_voli"] * loves
    if status["br_wow"] !=0:
        popularnost += status["br_wow"] * wows
    if status["br_haha"] !=0:
        popularnost += status["br_haha"] * hahas
    if status["br_tuznih"] !=0:
        popularnost += status["br_tuznih"] * sads
    if status["br_besnih"] !=0:
        popularnost += status["br_besnih"] * angrys
    if status["br_posebnih"] !=0:
        popularnost += status["br_posebnih"] * special
    
    return popularnost  
    