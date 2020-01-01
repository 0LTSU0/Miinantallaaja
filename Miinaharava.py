import haravasto as ha
import random
import time
import datetime

parametrit = {
    "leveys": 0,
    "korkeus": 0,
    "miinojen_maara": 0
}

tila = {
    "kentta": [],
    "nakyvakentta": [],
    "klikkaukset": 0,
    "kulunutaika": 0,
    "lopputulos": 0,
    "liput": 0,
    "kulunutaikatiedostoon": 0,
    "avaamattomat": 0,
}

def alkuvalikko():
    '''
    Käytännössä vain tulostaa tekstiä alkuvalikkoon ja sitten kutsuu funktiota joka kysyy käyttäjän valinnan.
    '''
    print("\nTervetuloa pelaamaan miinaharavaa!")
    print("\nVoit valita joko valmiin vaikeusasteen (MS minesweeper) tai valita mitat ja miinojen määrän itse!")
    print("1. Helppo")
    print("2. Keskivaikea")
    print("3. Vaikea")
    print("4. Omat asetukset")
    print("\nVoit myös tarkastella aiempien pelien tilastoja valitsemalla 5 tai lopettaa ohjelman [q]. \n")
    valinta()

def valinta():
    '''
    Hieman kömpelösti toteutettu kyselyfunktio (kutsuu itseään), mutta toimii ja oli mielestäni tässä tilanteessa ihan kohtuullinen vaihtoehto.

    Valinann perusteella sitten joko sijoittaa valmiit arvot sanakirjaan tai kutsuu tiedonhankitafunktiota/tulostusfunktiota
    '''
    valintah = input("Anna valinta: ")
    if valintah == "q":
        exit()
    try:
        valintaint = int(valintah)
        if valintaint == 1:
            parametrit["leveys"] = 9
            parametrit["korkeus"] = 9
            parametrit["miinojen_maara"] = 10
            maineistamainein()
        if valintaint == 2:
            parametrit["leveys"] = 16
            parametrit["korkeus"] = 16
            parametrit["miinojen_maara"] = 40
            maineistamainein()
        if valintaint == 3:
            parametrit["leveys"] = 30
            parametrit["korkeus"] = 16
            parametrit["miinojen_maara"] = 99
            maineistamainein()
        if valintaint == 4:
            hanki_tiedot()
        if valintaint == 5:
            tulostin()
        if valintaint < 1 or valintaint > 5:
            print("Valintaa ei ole olemassa!")
            valinta()
    except ValueError:
        print("Valintaa ei ole olemassa!")
        valinta()
    
    
    


def hanki_tiedot():
    '''
    Jos pelaaja alkuvalikosta valitsee vaihtoehdon 4, tätä funktiota kutsutaan kysymään parametreille arvot. Kun kaikki tarvittavat tiedot on saatu, kutsutaan maineistamainein funktiota, joka sitten aloittaa pelin valmistelun
    '''
    while True:
        try:
            parametrit["leveys"] = int(input("Anna haluamasi kentän leveys: "))
            if parametrit["leveys"] < 1:
                print("Anna nollaa suurempi kokonaisluku")
                continue
            if parametrit["leveys"] > 100:
                print("Äläs nyt kovin isoa kenttää koita luoda; 100x100 on aikalailla maksimi mihin tämä miinaharava kykenee!")
                continue
        except ValueError:
            print("Anna nollaa suurempi kokonaisluku")
            continue
        break

    while True:
        try:
            parametrit["korkeus"] = int(input("Anna haluamasi kentän korkeus: "))
            if parametrit["korkeus"] < 1:
                print("Anna nollaa suurempi kokonaisluku")
                continue
            if parametrit["korkeus"] > 100:
                print("Äläs nyt kovin isoa kenttää koita luoda; 100x100 on aikalailla maksimi mihin tämä miinaharava kykenee!")
                continue
        except ValueError:
            print("Anna nollaa suurempi kokonaisluku")
            continue
        break
    
    while True:
        try:
            parametrit["miinojen_maara"] = int(input("Anna miinojen määrä: "))
            if parametrit["miinojen_maara"] < 1:
                print("Kyllä siellä kentällä täytyy jonkin positiivisen kokonaisluvun verran miinoja olla!")
                continue
            if parametrit["miinojen_maara"] >= parametrit["korkeus"] * parametrit["leveys"]:
                print("Näin monta miinaa ei mitenkään mahdu haluamallesi kentälle")
                continue
        except ValueError:
            print("Anna miinojen määärä nollaa suurempana kokonaislukuna!")
            continue
        break
    maineistamainein()

def piirra_kentta():
    '''
    Piirtää kentän ja muutokset siihen aina, kun se on tarpeellista.
    '''
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.aloita_ruutujen_piirto()
    for y in range(len(tila["kentta"][0])):
        for x in range(len(tila["kentta"])):
            ha.lisaa_piirrettava_ruutu(tila["nakyvakentta"][x][y], y * 40, x * 40)
    ha.piirra_ruudut()


def main():
    '''
    Entinen main funktio (nykyään maineistamainein). Tekee kaikki tylsät alustusjutu haravasto-moduulin avulla.
    '''
    ha.lataa_kuvat("spritet")
    ha.luo_ikkuna(int(parametrit["leveys"])*40, int(parametrit["korkeus"])*40)
    ha.aseta_piirto_kasittelija(piirra_kentta)
    ha.aseta_hiiri_kasittelija(kasittele_hiiri)
    ha.aseta_toistuva_kasittelija(sekuntikello, 1)
    ha.aloita()

def laske_miinat(x, y, lista):
    """
    Laskee tietyn, parametreina annettavan, ruudun ympärillä olevat miinat. Ei todellakaan tehokkain mahdollinen funktio siihen tarkoitukseen (luo joka kerta uuden lista ympärillä olevista ruuduista), mutta toimii!
    Lisäksi tämä funktio "piirtää" kentälle numeron, joka ruutuun kuuluu.
    """
    ymparillalista = [
    (x-1, y-1),
    (x-1, y),
    (x-1, y+1),
    (x, y-1),
    (x, y),
    (x, y+1),
    (x+1, y-1),
    (x+1, y),
    (x+1, y+1) ]
    
    laskuri = 0
    
    for x, y in ymparillalista:
        if 0 <= x < len(lista[0]) and 0 <= y < len(lista):
            if lista[y][x] == 'x':
                laskuri += 1
            #print(laskuri)
    if laskuri == 0:
        pass
    else:
        tila["kentta"][y-1][x-1] = "{}".format(laskuri)
        if tila["nakyvakentta"][y-1][x-1] == "f":
            tila["nakyvakentta"][y-1][x-1] == "f"
        else:
            tila["nakyvakentta"][y-1][x-1] = "{}".format(laskuri)


def sekuntikello(kulunut_aika):
    '''
    Yksinkertaisin funktio koko ohjelmassa; kutsutaan haravaston toimesta sekunnin välein, jolloin tämä lisää sanakirjassa olevaan arvoon yhden.
    '''
    tila["kulunutaika"] += 1
    #print(tila["kulunutaika"])

def lopetustoimintah():
    '''
    Olipa lopputulos voitto tai häviö, tätä funktiota kutsutaan aina. Funktio nimittäin ensin muuttaa kuluneen ajan (sekunteja) kivempaan muotoon (kutsumalla toista funktiota) ja sitten tallentaa tiedot pelatusta pelistä.
    '''
    sekatminuutiksi()
    try:
        with open("tilasto.txt", "a") as kohde:
            kohde.write("{}: Pelin kesto: {}, Siirtoja: {}, Lopputulos: {} (kentän mitat olivat {}x{} ja miinoja oli {}).".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), tila["kulunutaikatiedostoon"], tila["klikkaukset"], tila["lopputulos"], parametrit["leveys"], parametrit["korkeus"], parametrit["miinojen_maara"]) + '\n')
    except IOError:
        print("Kohteen aukasu ei nyt kyllä onnistunut")      
    tila["nakyvakentta"] = tila["kentta"]
    #piirra_kentta()
    
def sekatminuutiksi():
    '''
    Muuntaa sanakirjasta saatavat sekunnit minuuteiksi ja sekunneiksi.
    '''
    minuutit = tila["kulunutaika"] // 60
    sekunnit = tila["kulunutaika"] % 60

    if minuutit == 0:
        tila["kulunutaikatiedostoon"] = "{}s".format(tila["kulunutaika"])
    else:
        tila["kulunutaikatiedostoon"] = "{}min {}s".format(minuutit, sekunnit)

    

def kasittele_hiiri(hiirix, hiiriy, nappi, muoknap):
    '''
    Käsittelee hiiren klikkaukset haravasto moduulia hyödyntäen.-
    '''
    if nappi == ha.HIIRI_VASEN:
        tila["klikkaukset"] += 1
        vasenx = int(hiirix/40)
        vaseny = int(hiiriy/40)
        
        if tila["kentta"] == tila["nakyvakentta"]:
            piirra_kentta()
        
        elif tila["kentta"][vaseny][vasenx] == "x":
            tila["lopputulos"] = "Häviö"
            print("Hävisit pelin :-(")
            lopetustoimintah()
            
        elif tila["kentta"][vaseny][vasenx] != "x":
            laske_miinat(vasenx, vaseny, tila["kentta"])
            tulvataytto(tila["kentta"], vasenx, vaseny)
        
        
    if nappi == ha.HIIRI_OIKEA:
        tila["klikkaukset"] += 1
        if tila["kentta"] == tila["nakyvakentta"]:
            piirra_kentta()

        elif tila["kentta"] != "f":
            tila["liput"] += 1
            tila["nakyvakentta"][int(hiiriy/40)][int(hiirix/40)] = "f"
            #tila["kentta"][int(hiiriy/40)][int(hiirix/40)] = "f"

    tarkista_voitto()
    

def tarkista_voitto():
    '''
    Funktio tarkastaa jokaisen klikkauksen jälkeen (jos ei klikattu miinaa), että toteutuuko jokin voitto- tai häviöehto.
    '''
    #lista = tila["kentta"]
    
    
    
    yhtalaisyydet = 0
    if tila["liput"] == parametrit["miinojen_maara"]:
        for i in range(int(parametrit["korkeus"])):
            for j in range(int(parametrit["leveys"])):
                if tila["kentta"][i][j] == "x" and tila["nakyvakentta"][i][j] == "f":
                    yhtalaisyydet += 1
                    if yhtalaisyydet == parametrit["miinojen_maara"]:
                        print("Onneksi olkoon, voitit pelin (kaikki miinalliset ruudut liputettu)")
                        tila["lopputulos"] = "Voitto!"
                        lopetustoimintah()
        if yhtalaisyydet != parametrit["miinojen_maara"] and tila["liput"] == parametrit["miinojen_maara"]:
            print("Hävisit pelin (kaikki liput käytetty, mutta miinoja vielä liputtamatta)")
            tila["lopputulos"] = "Häviö"
            lopetustoimintah()

    else:
        tila["avaamattomat"] = 0
        for i in range(int(parametrit["korkeus"])):
            for j in range(int(parametrit["leveys"])):
                if tila["nakyvakentta"][i][j] == " " or tila["nakyvakentta"][i][j] == "f":
                    tila["avaamattomat"] += 1
        #print(tila["avaamattomat"])
                
    
        if tila["avaamattomat"] == parametrit["miinojen_maara"]:
            tila["lopputulos"] = "Voitto!"
            print("Onneksi olkoon, voitit pelin (kaikki miinattomat ruudut aukaistu)!")
            lopetustoimintah()


def tulostin():
    '''
    Lukee tiedot samassa kansiossa olevasta tiedostosta nimeltä "tilasto.txt" (joka luodaan ensimmäisen pelin yhteydessä) ja läsäyttää ne ruudulle
    '''

    try:
        tilastot = open('tilasto.txt', 'r').read()
        print(tilastot)
    except FileNotFoundError:
        print("Tilastotiedostoa ei ole olemassa (oletko pelannut yhtään peliä?)")
    print("Palataan alkuvalikkoon...")
    alkuvalikko()


def miinoita(kentta, miinat):
    '''
    Arpoo halutun määrän miinoja kentälle.
    '''
    kaytetyt = []
    miina = 0
    while miinat > miina:
        x = random.randint (0, len(kentta)-1)
        y = random.randint(0, len(kentta[0])-1)
        if ("({},{})".format(x,y)) in kaytetyt:
            #print("sama löyty")
            miina = miina
        else:
            kaytetyt.append("({},{})".format(x,y))
            miina += 1
            kentta[x][y] = "x"
        #print(tila["kaytetyt"])   

def tulvataytto(lista, ax, ay):
    '''
    Aukaisee ympärillä olevia ruutuja klikatusta kohdasta ulospäin, kuitenkin siten siten, että kentän rajoja ei ylitetä ja, että aukaisu lopetetaan, kun löytyy miinoja/numeroruutuja
    '''
    ymparillalista = [(ay, ax)]
    leveys = len(lista[0])
    korkeus = len(lista)
    if lista[ay][ax] == " ":
        while ymparillalista:
            y, x = ymparillalista.pop()
            lista[y][x] = "0"
            if tila["nakyvakentta"][y][x] == "f":
                pass
            else:
                tila["nakyvakentta"][int(y)][int(x)] = "0"       
            for yy in range(min(max(y-1, 0), korkeus), min(max(y+2, 0), korkeus)):
                for xx in range(min(max(x-1, 0), leveys), min(max(x+2, 0), leveys)):
                    laske_miinat(xx,yy, tila["kentta"])
                    if lista[yy][xx] == " ":
                        ymparillalista.append((yy, xx))
                        #print(ymparillalista)

def maineistamainein():
    '''
    Funktio, joka oli ennen pääohjelmana (siksi nimi maineistamainein). Jouduin muuttamaan erilliseksi funktioksi, jotta tietojen kysely käyttäjältä onnistui halutulla tavalla
    (en tarkkaan enää muista mikä oli ongelma)

    Joka tapauksessa tämä funktio luo kaksi listaa, jotka ovat näkyvä ja pelin käsittelemä kenttä (sis. miinat).

    Listojen luomisen käyttäjän haluamilla tiedoilla funktio kutsuu miinoitusfunktiota, joka sijoittaa miinat sattumanvaraisiin ruutuihin.
    '''
    try:
        kentta= []
        nakyvakentta = []

        for rivi in range(int(parametrit["korkeus"])):
            kentta.append([])
            nakyvakentta.append([])
            for sarake in range(int(parametrit["leveys"])):
                kentta[-1].append(" ")
                nakyvakentta[-1].append(" ")
        tila["kentta"] = kentta
        tila["nakyvakentta"] = nakyvakentta
        
        '''
        TÄTÄ EI KÄYTETÄ TÄSSÄ OHJELMASSA MUTTA EN USKALLA KOKONAAN POISTAA SILTÄ VARALTA ETTÄ JOSSAIN VAIHEESSA TARVIIKIN LAITTAA TAKAISIN!

        jaljella = []
        for x in range(int(parametrit["leveys"])):
            for y in range(int(parametrit["korkeus"])):
                jaljella.append((x, y))
        '''
        
        miinoita(tila["kentta"], int(parametrit["miinojen_maara"]))
        #print(tila["kentta"])
        main()
    except MemoryError:
        print("Jotain meni nyt vikaan, oliko kenttä typerän suuri?!?")
        print("Ohjelma käynnistyy nyt uudestaan:")
        alkuvalikko()

if __name__ == "__main__":
    alkuvalikko()

