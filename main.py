import ucitavanje
import graf
import pickle
from edgerank import *
from trie import *


# fajl2 = open("graf.pkl", "rb")
# trenutni_graf = pickle.load(fajl2)
# fajl2.close()

sviLjudi, sviStatusi, sviKomentari = ucitavanje.dobavi_podatke("dataset/friends.csv", "dataset/original_statuses.csv","dataset/original_comments.csv","dataset/original_reactions.csv","dataset/original_shares.csv")
korisnik = {}
trenutni_graf = graf.napravi_graf(sviLjudi, sviStatusi)
fajl = open("graf.pkl","wb")
pickle.dump(trenutni_graf, fajl, pickle.HIGHEST_PROTOCOL)
fajl.close()
# U reci su trenutno ucitani podaci iz originalnih statusa
reci = napravi_trie(sviStatusi)
fajl = open("trie.pkl","wb")
pickle.dump(reci, fajl, pickle.HIGHEST_PROTOCOL)
fajl.close()
# fajl = open("trie.pkl", "rb")
# reci = pickle.load(fajl)
# fajl.close()


def sortiraj(statusi):
    global sviStatusi
    global trenutni_graf
    global korisnik
    
    if statusi == {}:
        statusi = sviStatusi
    pretraga = EdgeRank(trenutni_graf,statusi, korisnik)
    pretraga = pretraga[-10:]
    pretraga.reverse()
    for rezultat in pretraga:  
        print("\n"+ rezultat["tekst"] + "\nDatum: " + rezultat["datum"] +"\nAutor: " + rezultat["autor"] +"\nPrijatelji: "+("DA" if rezultat["prijatelj"] else "NE")+ "\n")


def Prikazi_objave():
    sortiraj({})

def prioritet_pretrage(lista_statusa, lista_reci):
    konacna_lista = []
    for id in lista_statusa:
        prosledi = {}
        brojac = 0
        minimum = float('inf')
        prosledi[id] = sviStatusi[id]
        status_trie = napravi_trie(prosledi)
        for rec in lista_reci:
            privremena = 0
            rec1 = rec.lower()
            _, rez = status_trie.broj_pojavljivanja(rec1)
            privremena += rez
            rec1 = rec1[0].upper() + rec1[1:].lower()
            _, rez = status_trie.broj_pojavljivanja(rec1)
            privremena += rez
            rec1 = rec.upper()
            _, rez = status_trie.broj_pojavljivanja(rec1)
            privremena += rez
            brojac += privremena
            
            if privremena < minimum:
                minimum = privremena
                
        brojac += minimum*5
        konacna_lista.append({
            "id": id,
            "vrednost": brojac,
            "min": minimum
        })
    konacna_lista = sorted(konacna_lista,key=lambda i: i["vrednost"])
    konacna_lista = konacna_lista[-30:]
    statusi = {}
    for recnik in konacna_lista:
        statusi[recnik["id"]] = sviStatusi[recnik["id"]]
    sortiraj(statusi)
    
    


def Pretraga():
    unos = input("Pretraga(za autokomplit stavite * na kraju reci): ")
    if unos.find("*")!=-1:
        spisak = autokomplit(unos)
        if spisak == []:
            print("")
        else:
            for id in spisak:
                print("->" + id["rec"])
        print()
        Pretraga()
        return
    elif unos != "":
        unos = unos.split(" ")
    else:
        print("Pogrešan unos")
        Pretraga()
        return
    rezultat = []
    for rec in unos:
        rec1 = rec.lower()
        _, statusi_rec = reci.find_prefix(rec1)
        rezultat += statusi_rec
        rec1 = rec1[0].upper() + rec1[1:].lower()
        _, statusi_rec = reci.find_prefix(rec1)
        rezultat += statusi_rec
        rec1 = rec.upper()
        _, statusi_rec = reci.find_prefix(rec1)
        rezultat += statusi_rec
        
    if rezultat == []:
        print("\nNema razultata pretrage\n")
    else:
        statusi = {}
        for id in rezultat:
            statusi[id] = sviStatusi[id]
        prioritet_pretrage(statusi, unos)

def ispis_opcija(meni: dict):
        for kljuc,vredonst in meni.items():
            print(kljuc + ". " + (vredonst.__name__).replace("_"," "))
        print("="*100)

def ocisti_reci(spisak_reci):
    
    novi_spisak = []
    for rec in spisak_reci:
        nova_rec = ""
        for slovo in rec:
            if slovo.isalpha() or slovo == "'" or slovo == "":
                nova_rec+=slovo
            else:
                break
        nova_rec = nova_rec.lower()
        nova_rec = nova_rec[0].upper() + nova_rec[1:].lower()
        if novi_spisak.count(nova_rec) == 0:
            novi_spisak.append(nova_rec)
        
    return novi_spisak
        


def autokomplit(uneta_rec):
    rec = uneta_rec.replace("*", "")
    spisak_reci = []
    rec1 = rec.lower()
    spisak_reci += reci.autocomplete(rec1)
    rec1 = rec1[0].upper() + rec1[1:].lower()
    spisak_reci += reci.autocomplete(rec1)
    rec1 = rec.upper()
    spisak_reci += reci.autocomplete(rec1)
    spisak_reci = ocisti_reci(spisak_reci)
    
    konacni_spisak = []
    for id in spisak_reci:
        _,br = reci.broj_pojavljivanja(id) 
        konacni_spisak.append({
            "rec": id,
            "broj_pojavljivanja": br
        })
        
    konacni_spisak = sorted(konacni_spisak,key=lambda i: i["broj_pojavljivanja"])
    konacni_spisak = konacni_spisak[-6:]
    konacni_spisak.reverse()
    
    return konacni_spisak
    


if __name__ == '__main__':
    
    #azuriranje grafa sa test podacima za odbranu; trenutno zakomentarisano
    # trenutni_graf = graf.azuriraj_graf(trenutni_graf)
    
    opcije_korisnik={
        "1": Prikazi_objave,
        "2": Pretraga,
    }
    
    prekid = False
    while not prekid:
        x = input("Unesite ime ili prezime osobe(x za izlazak): ")
        if x == "x" or x == "X":
            prekid = True
            break
        if x in sviLjudi:
            korisnik = sviLjudi[x]
        else:
            korisnik = {}
        
        radi = True
        while radi:
            ispis_opcija(opcije_korisnik)
            unos = input("Unesite broj opcije(x za izlazak): ")
            if unos == "x" or unos == "X":
                radi = True
                break
            if unos in opcije_korisnik:
                opcije_korisnik[unos]()
            else:
                continue
    print("Kraj")