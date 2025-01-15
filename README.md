# MCMC-Metropolis-Hastings-Entschlüsselung
Im Folgenden wird der MCMC-Metropolis-Hastings-Algorithmus mit Anwendung auf die einfache Substitutionschiffre mit 26 Kleinbuchstaben des Alphabets erläutert.
```
class Distribution(dict):
    
    def __init__(self):
        self.clear()
        self._total = 0
    
    def __missing__(self, key):
        return 0  
    
    def __setitem__(self, key, value):
        self._total += value - self.get(key, 0)
        super().__setitem__(key, value)
```
Die Klasse Distribution initialisiert die Klasse „Distribution“ als spezielle Form des Dictionaries. Dieses Dictionary wird gereinigt und die Elemente werden auf null gesetzt. Ferner wird für missing key immer null ausgegeben.

- def_setitem
self._total interner Zähler wird aktuallisiert , dieser Zähler beinhaltet die Summe aller Werte in dem Dictionary

- super().__setitem__(key, value)
benutzt stdandard methode_setItem_ der Basisklasse dict, um Schlüssel-Wertpaar im Dictionary zu speichen.


``` def renormalize(self):
      
        self._total = float(sum(self.values()))
        if self._total <= 0:
            raise ValueError("Sum of probabilities must be positive")
        for key in self:
            self[key] /= self._total
