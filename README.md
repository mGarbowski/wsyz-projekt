# WSYZ - Projekt


* Maksym Bieńkowski
* Michał Łuszczek
* Mikołaj Garbowski

Projekt jest poświęcony problemowi produkcji i dystrybucji podstawowych warzyw (ziemniaków, kapusty, buraków, marchwi)
w Warszawie i okolicach między grupą producentów, siecią magazynów-chłodni i siecią sklepów spożywczych.


<div style="page-break-after: always;"></div>

## Lokalizacje

### Sklepy

* **Złota 44** (52.23123538348719, 21.002334582862733)
* **Aleja Komisji Edukacji Narodowej 14** (52.12982562283376, 21.069531384711578)
* **Mińska 25A** (52.24921523643051, 21.059415840535483)
* **Częstochowska 4/6** (52.21497524319214, 20.978488664418016)
* **Ostrobramska 71** (52.23266813037208, 21.11443224907392)
* **Bulwary B. Grzymały Siedleckiego** (52.23673845375636, 21.036976869610385)
* **Sardyńska 1** (52.17787696451111, 21.05353804734241)
* **Pamiętajcie o Ogrodach 4** (52.257231606228096, 20.987110490415766)
* **Gen. Tadeusza Pełczyńskiego 14** (52.24282413331787, 20.9081047450922)
* **Aleja Niepodległości 162** (52.209244900152974, 21.008531883983533)

### Producenci

* **Błonie** (52.196210702994726, 20.623323179851976)
* **Książenice** (52.07895991519026, 20.696598439808064)
* **Góra Kalwaria** (51.98163892918433, 21.211795297678236)
* **Otwock** (52.1152108196775, 21.269433923138475)
* **Wołomin** (52.357299338110245, 21.250353828893264)
* **Legionowo** (52.40750915150292, 20.920774568903166)

### Magazyny

* **Pruszków** (52.175584628053144, 20.793660692851642)
* **Piaseczno** (52.095790995772646, 21.023008661957697)
* **Zielonka** (52.289563668216005, 21.235200160810102)

<div style="page-break-after: always;"></div>


## Procesy biznesowe

Diagramy BPMN przygotowane w programie Bizagi Modeler, zdefiniowane w pliku [Model-operacji.bpm](./Model-operacji.bpm)

### Sprzedaż do magazynów

![diagram bpmn](./docs/producent-magazyn.png)

<div style="page-break-after: always;"></div>


### Sprzedaż do sklepów

![diagram bpmn](./docs/magazyn-sklep.png)

<div style="page-break-after: always;"></div>


## Model optymalizacyjny
* Model optymalizacyjny wspomaga podejmowanie decyzji w zakresie
  * Wielkości corocznych dostaw od producentów do magazynów
  * Wielkości cotygodniowych dostaw z magazynów do sklepów
  * Ilości produktów przechowywanych w przysklepowych magazynach 
* Model wykorzystuje bibliotekę Pyomo dla Pythona 3.12
* Wyniki optymalizacji są zapisywane w formacie csv
* Model wykorzystuje Google Maps API dla uzyskania rzeczywistych odległości między lokalizacjami
* Szczegółowa dokumentacji dostępna w [optimization/README.md](./optimization/README.md)

### Dane wejściowe
* Precyzyjne dystanse między lokalizacjami
* Wygenerowane losowo na podstawie poniższych przedziałów prognozy popytu (w kg/tydzień na sklep), różniące się na przestrzeni czasu i w zależności od lokalizacji:
  * Marchewka: 200-400kg
  * Kapusta: 100-300kg
  * Buraki: 50-200kg
  * Ziemniaki: 300-550kg
* Pojemność magazynów, koszt transportu oraz moc przerobowa fabryk zgodnie z warunkami zadania
* Pojemność magazynów przysklepowych: dwukrotność górnej granicy popytu dla każdego warzywa
* Minimum zapasu ponad prognozę na każdy tydzień - 10% średniego popytu, w zależności od sklepu

### Dane wyjściowe
* Ilości warzyw przechowywanych w przysklepowych magazynach w kolejnych tygodniach
* Wielkości dostaw każdego z warzyw od producenta do magazynu
* Wielkości dostaw każdego z warzyw z magazynów do sklepów w kolejnych tygodniach

<div style="page-break-after: always;"></div>


### Parametry
* Produkty
* Liczba tygodni symulacji
* Ponumerowane tygodnie
* Producenci
* Możliwości przerobowe producentów
* Sklepy
* Prognozowany popyt
* Pojemność przysklepowych magazynów
* Minimum zapasu powyżej prognozy popytu
* Hurtownie
* Pojemności hurtowni
* Koszt transportu

### Zmienne
* Ilość warzyw wysyłana jesienią od poszczególnych producentów do magazynów
* Ilość warzyw wysyłana co tydzień z poszczególnych magazynów do sklepów
* Ilość warzyw pozostała po każdym tygodniu sprzedaży

### Ograniczenia
* Ograniczenie wiążące ilość pozostałych warzyw w każdym tygodniu ze stanem na początku tygodnia i popytem
* Ograniczenie zapewniające nieprzekroczenie mocy przerobowej producentów
* Ograniczenie zapewniające nieprzekroczenie pojemności magazynów 
* Ograniczenie zapewniające nieprzekroczenie pojemności magazynów na terenach sklepów
* Ograniczenie wiążące ilość produktów wysłanych od producentów z tymi wysłanymi do sklepów
* Ograniczenie zapewniające spełnienie popytu z określoną nadwyżką


<div style="page-break-after: always;"></div>


### Wyniki
* Minimalizowany całkowity roczny koszt transportu wynosi 91689.68 PLN
* Analizując wyniki widać, że dostawy odbywają się między najbliżej położonymi lokalizacjami - zgodnie z oczekiwaniem 
