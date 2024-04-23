from datetime import datetime

def ucitaj_osobe(putanja):
    sviLjudi = {}
    with open(putanja, "r",encoding='utf-8') as fajl:
        redovi = fajl.readlines()
        for i in range(1, len(redovi)):
            podaci = redovi[i][:-1].split(",")
            sviLjudi[podaci[0]] ={
                    "ime":podaci[0],
                    "prijatelji": podaci[2:],
                    "komentari": {},
                    "statusi": {},
                    "wows": {},
                    "loves": {},
                    "hahas": {},
                    "sads": {},
                    "angrys": {},
                    "likes": {},
                    "shares": {},
                    "special":{}
                }
    return sviLjudi 

def ucitaj_statuse(putanja, sviLjudi):
    sviStatusi = {}
    with open(putanja, "r",encoding='utf-8') as fajl:
        redovi = fajl.readlines()
        for i in range(1, len(redovi)):
            podaci = redovi[i][:-1].split(",")
            format = "%Y-%m-%d %H:%M:%S"
            datum = datetime.strptime(podaci[4], format)
            sviStatusi[podaci[0]] = {
                "id": podaci[0],
                "tekst": podaci[1],
                "link": podaci[2],
                "status":podaci[3],
                "datum": datum,
                "autor": podaci[5],
                "br_reakcija": int(podaci[6]),
                "br_komentara": int(podaci[7]),
                "br_deljenja": int(podaci[8]),
                "br_svidjanja": int(podaci[9]),
                "br_voli": int(podaci[10]),
                "br_wow": int(podaci[11]),
                "br_haha": int(podaci[12]),
                "br_tuznih": int(podaci[13]),
                "br_besnih": int(podaci[14]),
                "br_posebnih":int(podaci[15])
            }
            if podaci[5] in sviLjudi.keys():
                sviLjudi[podaci[5]]["statusi"][podaci[0]] = {
                    "vreme": podaci[4]
                }
    return sviStatusi, sviLjudi

def ucitaj_komentare(putanja, sviLjudi):
    sviKomentari = {}
    with open(putanja, "r",encoding='utf-8') as fajl:
        redovi = fajl.readlines()
        for i in range(1, len(redovi)):
            podaci = redovi[i][:-1].split(",")
            format = "%Y-%m-%d %H:%M:%S"
            datum = datetime.strptime(podaci[5], format)
            sviKomentari[podaci[0]] = {
                "id": podaci[0],
                "status_id": podaci[1],
                "roditelj": podaci[2],
                "tekst": podaci[3],
                "autor": podaci[4],
                "datum": datum,
                "br_reakcija": int(podaci[6]),
                "br_svidjanja": int(podaci[7]),
                "br_voli": int(podaci[8]),
                "br_wow": int(podaci[9]),
                "br_haha": int(podaci[10]),
                "br_tuznih": int(podaci[11]),
                "br_besnih": int(podaci[12]),
                "br_posebnih":int(podaci[13])
            }
            if podaci[4] in sviLjudi.keys():
                sviLjudi[podaci[4]]["komentari"][podaci[0]] = {
                    "vreme": podaci[5]
                }
    return sviKomentari, sviLjudi

def ucitaj_reakcije(putanja, sviLjudi):
    with open(putanja, "r",encoding='utf-8') as fajl:
        redovi = fajl.readlines()
        for i in range(1, len(redovi)):
            podaci = redovi[i][:-1].split(",")
            format = "%Y-%m-%d %H:%M:%S"
            datum = datetime.strptime(podaci[3], format)
            if podaci[2] in sviLjudi.keys():
                if podaci[1] == "wows":
                    sviLjudi[podaci[2]]["wows"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                elif podaci[1] == "loves":
                    sviLjudi[podaci[2]]["loves"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                elif podaci[1] == "hahas":
                    sviLjudi[podaci[2]]["hahas"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                elif podaci[1] == "sads":
                    sviLjudi[podaci[2]]["sads"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                elif podaci[1] == "angrys":
                    sviLjudi[podaci[2]]["angrys"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                elif podaci[1] == "likes":
                    sviLjudi[podaci[2]]["likes"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
                else:
                    sviLjudi[podaci[2]]["special"][podaci[0]] = {
                        "vreme": podaci[3]
                    }
    return sviLjudi

def ucitaj_deljenja(putanja, sviLjudi):
    with open(putanja, "r",encoding='utf-8') as fajl:
        redovi = fajl.readlines()
        for i in range(1, len(redovi)):
            podaci = redovi[i][:-1].split(",")
            format = "%Y-%m-%d %H:%M:%S"
            if podaci[1] in sviLjudi.keys():
                sviLjudi[podaci[1]]["shares"][podaci[0]] = {
                    "vreme": podaci[2]
                }
    return sviLjudi


def dobavi_podatke(fajlLjudi, faljStatusi, fajlKomentari, fajlRekcije, fajlDeljenja):
    Ljudi = ucitaj_osobe(fajlLjudi)
    Statusi, Ljudi = ucitaj_statuse(faljStatusi, Ljudi)
    Komentari,Ljudi = ucitaj_komentare(fajlKomentari, Ljudi)
    Ljudi = ucitaj_reakcije(fajlRekcije, Ljudi)
    Ljudi = ucitaj_deljenja(fajlDeljenja, Ljudi)

    return Ljudi, Statusi, Komentari