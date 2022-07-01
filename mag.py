#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Mag v0.1
#Arena v0.2
#Bojovnik v0.4
#Kostka v0.2

class Kostka:
    """
    Třída reprezentující hrací kostku
    """

    def __init__(self, steny=6):
        self.__pocetSten = steny
    
    def getPocetSten(self):
        """
        Vrátí počet stěn kostky
        """
        return self.__pocetSten

    def hod(self):
        """
        Vykoná hod kostkou a vrátí číslo od 1 do počtu stěn.
        """

        import random as _random
        return _random.randint(1, self.__pocetSten)

    def __str__(self):
        """
        Vrací textovou reprezentaci kostky.
        """
        return str("Kostka s {0} stěnami.".format(self.__pocetSten))

class Bojovnik:
    """
    Trida Bojovnika...
    """

    def __init__(self, jmeno, zivot, utok, obrana, kostka):
        self._jmeno = jmeno
        self._zivot = zivot
        self._maxZivot = zivot
        self._utok = utok
        self._obrana = obrana
        self._kostka = kostka
        self._zprava = ""
    
    def __str__(self):
        return str(self._jmeno)

    @property
    def nazivu(self):
        if self._zivot > 0:
            return True
        else:
            return False
    
    def grafickyUkazatel(self, aktualni, maximalni):
        celkem = 20
        pocet = int(aktualni / maximalni * celkem)
        if (pocet == 0 and self.nazivu):
            pocet = 1
        return "[{0}{1}]".format("#"*pocet, " "*(celkem-pocet))
    
    def grafickyZivot(self):
        return self.grafickyUkazatel(self._zivot, self._maxZivot)

    def branSe(self, uder):
        zraneni = uder - (self._obrana + self._kostka.hod())
        if (zraneni > 0):
            zprava = "{0} utrpel poskozeni {1} hp.".format(self._jmeno, zraneni)
            self._zivot = self._zivot - zraneni
            if self._zivot < 0:
                self._zivot = 0
                zprava = zprava[:-1] + " a zemrel."
        else:
            zprava = "{0} odrazil utok.".format(self._jmeno)
        self._nastavZpravu(zprava)
    
    def utoc(self, souper):
        uder = self._utok + self._kostka.hod()
        zprava = "{0} utoci s uderem {1} dmg.".format(self._jmeno, uder)
        souper.branSe(uder)
        self._nastavZpravu(zprava)

    def _nastavZpravu(self, zprava):
        self._zprava = zprava
    
    def vratPosledniZpravu(self):
        return self._zprava

class Mag(Bojovnik):
    
    def __init__(self, jmeno, zivot, utok, obrana, kostka, mana, magickyUtok):
        super().__init__(jmeno, zivot, utok, obrana, kostka)
        self.__mana = mana
        self.__maxMana = mana
        self.__magickyUtok = magickyUtok
    
    def utoc(self, souper):
        # mana neni naplnena
        if (self.__mana < self.__maxMana):
            self.__mana = self.__mana + 10
            if (self.__mana > self.__maxMana):
                self.__mana = self.__maxMana
            super().utoc(souper)
        # mana je plna, jdeme ji pouzit
        else:
            uder = self.__magickyUtok + self._kostka.hod()
            zprava = "{0} pouzil magii za {1} dmg.".format(self._jmeno, uder)
            self._nastavZpravu(zprava)
            self.__mana = 0
            souper.branSe(uder)
    
    def grafickaMana(self):
        return self.grafickyUkazatel(self.__mana, self.__maxMana)

class Arena:

    def __init__(self, bojovnik1, bojovnik2, kostka):
        self.__bojovnik1 = bojovnik1
        self.__bojovnik2 = bojovnik2
        self.__kostka = kostka
    
    def __vykresli(self):
        self.__vycistiObrazovku()
        print("---------------------- Arena ---------------------- \n")
        print("Bojovnici: \n")
        self.__vypisBojovnika(self.__bojovnik1)
        self.__vypisBojovnika(self.__bojovnik2)
        print("")

    def __vycistiObrazovku(self):
        import sys as _sys
        import subprocess as _subprocess
        if _sys.platform.startswith("win"):
            _subprocess.call(["cmd.exe", "/t", "cls"])
        else:
            _subprocess.call(["clear"])
    
    def __vypisZpravu(self, zprava):
        import time as _time
        print(zprava)
        _time.sleep(0.75)
    
    def __vypisBojovnika(self, bojovnik):
        print(bojovnik)
        print("Zivot: {0}".format(bojovnik.grafickyZivot()))
        if isinstance(bojovnik, Mag):
            print("Mana: {0}".format(bojovnik.grafickaMana()))

    def zapas(self):
        import random as _random
        print("Vitejte v Arene!")
        print("Dnes se utkaji {0} a {1}!".format(self.__bojovnik1, self.__bojovnik2))
        print("Zapas muze zacit...")
        input()
        # prohozeni bojovniku
        if _random.randint(0,1):
            (self.__bojovnik1, self.__bojovnik2) = (self.__bojovnik2, self.__bojovnik1)
        # cyklus boje
        while (self.__bojovnik1.nazivu and self.__bojovnik2.nazivu):
            self.__bojovnik1.utoc(self.__bojovnik2)
            self.__vykresli()
            self.__vypisZpravu(self.__bojovnik1.vratPosledniZpravu())
            self.__vypisZpravu(self.__bojovnik2.vratPosledniZpravu())
            if self.__bojovnik2.nazivu:
                self.__bojovnik2.utoc(self.__bojovnik1)
                self.__vykresli()
                self.__vypisZpravu(self.__bojovnik2.vratPosledniZpravu())
                self.__vypisZpravu(self.__bojovnik1.vratPosledniZpravu())
            print("")


kostka = Kostka(10)
zalgoren = Bojovnik("Zalgoren", 100, 20, 10, kostka)
shadow = Bojovnik("Shadow", 60, 18, 15, kostka)
gandalf = Mag("Gandalf", 60, 15, 12, kostka, 30, 45)


arena = Arena(zalgoren, gandalf, kostka)
arena.zapas()


input()