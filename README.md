# WSYZ - Projekt
https://github.com/mGarbowski/wsyz-projekt

* Maksym Bieńkowski
* Michał Łuszczek
* Mikołaj Garbowski

Projekt jest poświęcony problemowi produkcji i dystrybucji podstawowych warzyw (ziemniaków, kapusty, buraków, marchwi) w Warszawie i okolicach między grupą producentów, siecią magazynów-chłodni i siecią sklepów spożywczych.


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
### Zbiory
* Produkty $P$
* Producenci $M$
* Sklepy $S$
* Hurtownie $W$

### Parametry
* Liczba tygodni symulacji $NW \in \mathbb{N}+$
* Koszt transportu $FP \in \mathbb{R}+$
* Ponumerowane tygodnie $T = \{1 \ldots NW\}$ 
* Możliwości przerobowe producentów $MC \quad [M,P]$
* Prognozowany popyt $D \quad [S, T, P]$
* Pojemność przysklepowych magazynów $SWC \quad [S]$
* Minimum zapasu powyżej prognozy popytu $MS \quad [S,P]$
* Pojemności hurtowni $WC \quad [W]$

### Zmienne
* Ilość warzyw wysyłana jesienią od poszczególnych producentów do magazynów $SFM \quad [M,W,P]$
* Ilość warzyw wysyłana co tydzień z poszczególnych magazynów do sklepów $SFW \quad [T,W,S,P]$
* Ilość warzyw pozostała po każdym tygodniu sprzedaży $L \quad [T, S, P]$

### Ograniczenia
1. Ograniczenie wiążące ilość pozostałych warzyw w każdym tygodniu ze stanem na początku tygodnia i popytem
2. Ograniczenie zapewniające nieprzekroczenie mocy przerobowej producentów
3. Ograniczenie zapewniające nieprzekroczenie pojemności magazynów 
4. Ograniczenie zapewniające nieprzekroczenie pojemności magazynów na terenach sklepów
5. Ograniczenie wiążące ilość produktów wysłanych od producentów z tymi wysłanymi do sklepów
6. Ograniczenie zapewniające spełnienie popytu z określoną nadwyżką


<div style="page-break-after: always;"></div>
### Model matematyczny
#### (1) Pozostałe warzywa w magazynie przysklepowym
$$\forall_{s \in S} \forall_{p \in P} \quad l_{[1,s,p]} = 0$$
$$
\forall_{t \in T - \{1\}} 
\forall_{s \in S} 
\forall_{p \in P}
\quad
l_{[t,s,p]} = l_{[t-1,s,p]} - d_{[s,t,p]} + \sum_{w \in W} sfw_{[t, w, s, p]}
$$

#### (2) Ograniczenie mocy przerobowej producentów
$$
\forall_{m \in M}
\forall_{p \in P}
\quad
\sum_{w \in W} sfm_{[m,w,p]} \le mc_{[m,p]}
$$
#### (3) Ograniczenie pojemności magazynu
$$
\forall_{w \in W}
\sum_{m \in M}
\sum_{p \in P}
sfm_{[m,w,p]}
\le
wc_w
$$

#### (4) Ograniczenie pojemności przysklepowych magazynów
$$
\forall_{s \in S}
\sum_{w \in W}
\sum_{p \in P}
sfw_{[1,w,s,p]}
\le
swc_s
$$

$$
\forall_{t \in T-\{1\}}
\sum_{w \in W}
\sum_{p \in P}
sfw_{[t,w,s,p]}
+
\sum_{p \in P}
l_{[t-1,s,p]}
\le
swc_s
$$

#### (5) Ograniczenie dostaw do sklepów przez dostawy do magazynów
$$
\forall_{w \in W}
\forall_{p \in P}
\sum_{t \in T} \sum_{s \in S} sfw_[t,w,s,p]
\le
\sum_{m \in M} sfm_{[m,w,p]}
$$
#### (6) Ograniczenie zaspokojenia popytu
 $$
\forall_{s \in S}
\forall_{p \in P}
\sum_{w \in W} sfw_{[1,w,s,p]}
\ge
d_{[s,1,p]} + ms_{[s,p]}
$$

$$
\forall_{s \in S}
\forall_{t \in T-\{1\}}
\forall_{p \in P}
\sum_{w \in W} sfw_{[t,w,s,p]} + l_{[t-1,s,p]}
\ge
d_{[s,t,p]} + ms_{[s,p]}
$$
#### Koszt transportu
$$
\sum_{m \in M}
\sum_{w \in W}
\sum_{p \in P}
FP \cdot sfm_{[m,w,p]} \cdot dist_{[w,m]}
+
\sum_{t \in T}
\sum_{w \in W}
\sum_{s \in S}
\sum_{p \in P}
FP \cdot sfw_{[t,w,s,p]} \cdot dist_{[w,s]}
$$

### Wyniki
* Minimalizowany całkowity roczny koszt transportu wynosi 91689.68 PLN
* Analizując wyniki widać, że dostawy odbywają się między najbliżej położonymi lokalizacjami - zgodnie z oczekiwaniem 
