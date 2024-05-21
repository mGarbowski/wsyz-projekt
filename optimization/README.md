# Wstęp do systemów zarządzania 2024L - model optymalizacyjny

## Informacje o modelu, struktura projektu

### Lokalizacje

#### Sklepy
* **Złota 44**
  * Współrzędne: (52.23123538348719, 21.002334582862733)
  
* **Aleja Komisji Edukacji Narodowej 14**
  * Współrzędne: (52.12982562283376, 21.069531384711578)
  
* **Mińska 25A**
  * Współrzędne: (52.24921523643051, 21.059415840535483)
  
* **Częstochowska 4/6**
  * Współrzędne: (52.21497524319214, 20.978488664418016)
  
* **Ostrobramska 71**
  * Współrzędne: (52.23266813037208, 21.11443224907392)
  
* **Bulwary B. Grzymały Siedleckiego**
  * Współrzędne: (52.23673845375636, 21.036976869610385)
  
* **Sardyńska 1**
  * Współrzędne: (52.17787696451111, 21.05353804734241)
  
* **Pamiętajcie o Ogrodach 4**
  * Współrzędne: (52.257231606228096, 20.987110490415766)
  
* **Gen. Tadeusza Pełczyńskiego 14**
  * Współrzędne: (52.24282413331787, 20.9081047450922)
  
* **Aleja Niepodległości 162**
  * Współrzędne: (52.209244900152974, 21.008531883983533)

#### Producenci
* **Błonie**
  * Współrzędne: (52.196210702994726, 20.623323179851976)
  
* **Książenice**
  * Współrzędne: (52.07895991519026, 20.696598439808064)
  
* **Góra Kalwaria**
  * Współrzędne: (51.98163892918433, 21.211795297678236)
  
* **Otwock**
  * Współrzędne: (52.1152108196775, 21.269433923138475)
  
* **Wołomin**
  * Współrzędne: (52.357299338110245, 21.250353828893264)
  
* **Legionowo**
  * Współrzędne: (52.40750915150292, 20.920774568903166)

#### Magazyny
* **Pruszków**
  * Współrzędne: (52.175584628053144, 20.793660692851642)
  
* **Piaseczno**
  * Współrzędne: (52.095790995772646, 21.023008661957697)
  
* **Zielonka**
  * Współrzędne: (52.289563668216005, 21.235200160810102)

#### Parametry
* produkty
* liczba tygodni symulacji
* ponumerowane tygodnie
* producenci
* możliwości przerobowe producentów
* sklepy
* prognozowany popyt
* pojemność przysklepowych magazynów
* minimum zapasu powyżej prognozy popytu
* hurtownie
* pojemności hurtowni
* koszt transportu

#### Zmienne
* ilość warzyw wysyłana jesienią od poszczególnych producentów do magazynów
* ilość warzyw wysyłana co tydzień z poszczególnych magazynów
do sklepów
* ilość warzyw pozostała po każdym tygodniu sprzedaży

#### Ograniczenia
* ograniczenie powiązujące ilość pozostałych warzyw w każdym tygodniu ze stanem
na początku tygodnia i popytem
* ograniczenie zapewniające nieprzekroczenie mocy przerobowej producentów
* ograniczenie zapewniające nieprzekroczenie pojemności magazynów 
* ograniczenie zapewniające nieprzekroczenie pojemności magazynów na terenach
sklepów
* ograniczenie powiązujące ilość materiałów wysłanych od producentów
z tymi wysłanymi do sklepów
* ograniczenie zapewniające spełnienie popytu z określoną nadwyżką


#### Dane
* Precyzyjne dystanse między lokalizacjami
* Wygenerowane losowo na podstawie poniższych przedziałów prognozy popytu (w kg/tydzień na sklep),
różniące się na przestrzeni czasu i w zależności od lokalizacji:
       * Marchewka: 200-400kg
       * Kapusta: 100-300kg
       * Buraki: 50-200kg
       * Ziemniaki: 300-550kg
* Pojemność magazynów, koszt transportu oraz moc przerobowa fabryk zgodnie z warunkami zadania
* Pojemność magazynów przysklepowych: dwukrotność górnej granicy popytu dla każdego warzywa
* Minimum zapasu ponad prognozę na każdy tydzień - 10% średniego popytu, w zależności od sklepu



### Aspekty techniczne
* platforma: Pyomo w Pythonie 3.12
* w celu urzeczywistnienia otrzymanych wyników, dane dotyczące dystansów między lokalizacjami pozyskiwane są poprzez 
[Google Maps Api](https://developers.google.com/maps/documentation/distance-matrix) 

### Struktura projektu
* `src/` - pliki źródłowe
    * `abstract.py` - abstrakcyjny model, odpowiednik pliku `.mod` w amplu
    * `concrete.py` - konkretna instancja modelu na podstawie danych z katalogu `data/`
    * `objects.py` - obiekty reprezentujące lokalizacje i produkty
    * `constants.py` - stałe liczbowe oraz instancje obiektów z `objects.py` - konkretne lokalizacje
    ze współrzędnymi, limitami, itp.
    * `demand.py` - skrypt generujący losowo informacje dotyczące prognozy popytu na warzywa
    * `distances.py` - obsługa google maps api, obliczanie odległości między lokalizacjami
    * `generate_tables.py` - generuje pliki csv na podstawie danych otrzymanych z rozwiązanego modelu do wglądu
    * `debugging.py` - funkcjonalność do debugowania modelu, wykorzystywania przy poprawianiu działania

* `data/` - dane wejściowe modelu w formacie [Pickle](https://docs.python.org/3/library/pickle.html),
przechowywane, aby unikać generowania nowych danych przy każdym uruchomieniu modelu - są one generowane
ponownie tylko, jeśli pliki zostaną usunięte
    * `demand.pkl` - dane dotyczące prognozy popytu
    * `distances.pkl` - dane dotyczące dystansów między obiektami

* `output/` - wyniki optymalizacji w formacie CSV
    * `manufacturer_shipments.csv` - wysyłki od producentów do magazynów z podziałem na rodzaje warzyw
    * `warehouse_shipments.csv` - wysyłki z magazynów do sklepów na przestrzeni tygodni, także podzielone ze względu
    na rodzaje warzyw
    * `leftover_stock.csv` - ilość produktów pozostała w magazynie po każdym tygodniu sprzedaży

* `main.py` - skrypt rozwiązujący instancję modelu i wyświetlający informacje o otrzymanych wynikach oraz
generujący wynikowe pliki csv


## Instrukcja użycia 
* instalacja zależności - `pip -r install requirements.txt`, najlepiej przy użyciu `venv`
* instalacja solvera CBC - w przypadku ubuntu, `sudo apt-get install  coinor-cbc coinor-libcbc-dev`, w przypadku windowsa opisane
w [ jego repozytorium ]( https://github.com/coin-or/Cbc )
* uruchomienie aplikacji - `python -m main` wyświetla wartość funkcji celu
* aby zaktualizować dane wejściowe po modyfikacji modelu, należy wyczyścić katalog `data`: `rm data/*`
* do pobrania uaktualnionych danych dotyczących dystansów między lokalizacjami), należy w pliku
`.env` umieścić [Klucz do google maps API](https://developers.google.com/maps/documentation/javascript/get-api-key):
```
API_KEY = TWÓJ_KLUCZ_API  
```
