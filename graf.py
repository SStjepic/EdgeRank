import networkx
from datetime import datetime
from ucitavanje import dobavi_podatke

def napravi_graf(sviLjudi, sviStatusi, stariGraf = None):
    if stariGraf == None:
        Graf = networkx.DiGraph()
        Graf.add_nodes_from([(cvor, {"atributi": atributi}) for (cvor, atributi) in sviLjudi.items()])
    else:
        Graf = stariGraf
    br = 0
    for i in sviLjudi:
        for j in sviLjudi:
            if i != j:
                vrednost_tezine = odredi_svidjanje(sviLjudi[i], sviLjudi[j], sviStatusi)
                try:
                    prethodnaVrednost = Graf.get_edge_data(sviLjudi[i]["ime"], sviLjudi[j]["ime"])["tezina"]
                    br+=1
                    print(br)
                except:
                    prethodnaVrednost = 0
                Graf.add_edge(sviLjudi[i]["ime"], sviLjudi[j]["ime"], tezina = vrednost_tezine + prethodnaVrednost)

    return Graf


# odnos covek1 prema covek2
def odredi_svidjanje(covek1, covek2, sviStatusi):
    covek12 = 0 
    wows = 50
    loves =40
    hahas =45
    sads = 25
    angrys= -20
    likes= 10
    shares= 60
    special= 60
    komentari = 40
        
    for id in covek2["statusi"]:
        if id in covek1["wows"]:
            covek12 +=  (wows*vreme_raspada(sviStatusi[id]["datum"],covek1["wows"][id]["vreme"]))
            continue
            
        elif id in covek1["loves"]:
            covek12 +=  (loves*vreme_raspada(sviStatusi[id]["datum"],covek1["loves"][id]["vreme"]))
            continue
            
        elif id in covek1["hahas"]:
            covek12 +=  (hahas*vreme_raspada(sviStatusi[id]["datum"],covek1["hahas"][id]["vreme"]))
            continue
            
        elif id in covek1["sads"]:
            covek12 +=  (sads*vreme_raspada(sviStatusi[id]["datum"],covek1["sads"][id]["vreme"]))
            continue
            
        elif id in covek1["angrys"]:
            covek12 +=  (angrys*vreme_raspada(sviStatusi[id]["datum"],covek1["angrys"][id]["vreme"]))
            continue
            
        elif id in covek1["likes"]:
            covek12 +=  (likes*vreme_raspada(sviStatusi[id]["datum"],covek1["likes"][id]["vreme"]))
            continue
        
        elif id in covek1["special"]:
            covek12 +=  (special*vreme_raspada(sviStatusi[id]["datum"],covek1["special"][id]["vreme"]))
            continue
        
        elif id in covek1["shares"]:
            covek12 +=  (shares*vreme_raspada(sviStatusi[id]["datum"],covek1["shares"][id]["vreme"]))
            continue
        
        if id in covek1["komentari"]:
            covek12 +=  (komentari*vreme_raspada(sviStatusi[id]["datum"],covek1["komentari"][id]["vreme"]))
            continue
        
    if covek2["ime"] in covek1["prijatelji"]:
        covek12 += 150
    
    return covek12

def vreme_raspada(datum_objave,datum_reakcije):
    datum1 = datetime.strptime(datum_reakcije, "%Y-%m-%d %H:%M:%S")
    vreme = datum1-datum_objave
    dani = vreme.days
    if dani<3:
        return 1
    elif dani<10:
        return 0.8
    elif dani<15:
        return 0.6
    elif dani<20:
        return 0.4
    elif dani<26:
        return 0.3
    else:
        return 0.2
    
    
def azuriraj_graf(Graf):
    Ljudi, Statusi, Komentari = dobavi_podatke("dataset/friends.csv", "dataset/test_statuses.csv","dataset/test_comments.csv","dataset/test_reactions.csv","dataset/test_shares.csv")
    return napravi_graf(Ljudi, Statusi, Graf)