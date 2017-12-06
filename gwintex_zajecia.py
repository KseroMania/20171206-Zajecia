# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 17:47:03 2017

@author: P
"""

import numpy as np

#na poczatku deklarujemy stale i zmienne wykorzystane w modelu
N = 6 #ilosc maszyn
AVG_WORKING_TIME = 75 #sredni czas pracy bez usterki
AVG_REPAIR_TIME = 15 #sredni czas naprawy

m = 1 #ilosc zestawow narzedzi
horizon = 30 #horyzont analizy
iterations = 1000 #ilosc uruchomien symulacji

#tworzymy model
def model(horizon, avg_working_time, avg_repair_time, n, m, setup):
    #ustalamy interesujacy nas horyzont dzialania w minutach
    horizon = horizon * 24 * 60 
    
    #tworzymy odpowiednie wektory, ktore beda kontrolowaly stan symulacji:
    # momenty wystapienia kolejnych zdarzen, status narzedzi i maszyn, czas ich bezczynnosci
    # events- wektor zdarzen, ktore zmieniaja stan symulacji (zepsucie maszyny, czas naprawy, itp.)
    events = list(np.random.exponential(avg_working_time, n))
    
    #status - okresla aktualny stan maszyny W- pracuje Q- czeka na narzedzia R- jest naprawiona
    status = ["W"] * n

    #t_start - okresla poczatek bezczynnosci maszyny
    t_start = [0] * n

    #t_cum skumulowany czas bezczynnosci
    t_cum = [0] * n

    #tools_loc lokalizacja narzedzi- albo numer maszyny albo -1 czyli warsztat
    tools_loc = [-1] * m

    #tools_occupied czas zajecia zestawu przez naprawiana maszyne
    tools_occupied = [0] * m
    
    #ustawiamy zegar symulacji- najblizsze zadanie, ktore ma byc wykonane
    t = min(events)
    
    #rozpoczynamy symulacje "skaczac" po kolejnych zdarzeniach  
    while t <= horizon:
        #jezeli zestawy nie sa aktualnie zajete to przenosimy je z powrotem do warsztatu
        for i in range(m):
            if tools_occupied[i] <= t:
                tools_loc[i] = -1

        #wybieramy maszyne, ktorej dotyczy zdarzenie
        machine = events.index(t)
        
        """
        Gdy maszyna, ktorej dotyczy zdarzenie ma status "W":
            -to najpierw zaktualizuj wektor t_start  dla tej maszyny poczatek jej bezczynnosci t.
            -nastepnie sprawdz czy dostepny jest jakis zestaw naprawczy. Jezeli nie:
                * to ustaw status maszyny na "Q" 
                * zaktualizuj wektor events podajac mu najkrotszy czas oczekiwania na wolny zestaw.
            -Jezeli tak:
                * ustaw status maszyny na "R"
                * wyznacz czas  potrzebny na naprawe maszyny w zaleznosci od ukladu tasmociagu
                (czas transportu + czas naprawy)
                * ustaw koniec naprawy jako zdarzenie dla danej maszyny
                * zaktualizuj wektor tools_loc  dla odpowiedniego zestawu podajac numer maszyny, 
                ktora on obsluguje
                * zaktualizuj wektor tools_occupied czasem jaki mu to zajmie (2* transport + naprawa)
        """

                """
                Gdy maszyna ma status "Q":
                    -wybierz dostepny zestaw naprawczy
                    -ustal status maszyny na "R"
                    -zaktualizuj wektor tools_loc lokalizacja narzedzi i tools_occupied 
                    czasem jaki zajmie ich transport (w dwie strony) i naprawa maszyny
                    -zaktualizuj wektor zdarzen czasem potrzebnym na 
                    naprawe maszyny i transport narzedzi
                """

            """
            Gdy maszyna ma status "R":
                -ustal jej status na "W"
                -wyznacz czas kolejnej awarii i zaktualizuj wektor events
                -wylicz czas bezczynnosci i uzupelnij o niego liste t_cum
            """
            
        
        #ustalamy nowe t
        t = min(events)
        
    #ostatecznie zwracamy wynik - liste skumulowanych bezczynnosci dla kazdej z maszyn
    return (t_cum)
        
#definiujemy funkcje, ktora uruchamia symulacje odpowiednia ilosc razy

def run_model (iterations, horizon, avg_working_time, avg_repair_time, n, m, setup):
    avg_t_cum = []
    for i in range (iterations):
        avg_t_cum.append(model( horizon, avg_working_time, avg_repair_time, n, m, setup))
    return list(map(np.mean, np.transpose(avg_t_cum)))


a = run_model(1000, 30, AVG_WORKING_TIME,AVG_REPAIR_TIME,N,m,"L")









    
    

    