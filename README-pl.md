# RNAQuANet
## Środowisko
Aby w pełni i bezproblemowo wykorzystać nasz projekt należy [pobrać](https://docs.docker.com/get-docker/) i zainstalować Dockera, a następnie w sklonowanym katalogu wywołać poniższe polecenia: 

    docker compose up -d
    docker attach rnaquanet-python_cuda-1

Dodatkowo do wygodnej pracy polecamy [Dev Containers w VSCode](https://code.visualstudio.com/docs/devcontainers/containers).

## Przebieg pracy
### Tworzenie modelu
Główną częścią naszego projektu jest stworzenie modelu sieci grafowej. Aby uprościć i zautomatyzować cały proces stworzyliśmy CLI, które efektywnie pomaga w tym zadaniu. Wszystkie skrypty znajdują się w katalogu `cli` i uruchamiane są za pomocą polecenia `python cli/{nazwa_skryptu}.py`. Skrypty posiadają też wiele parametrów, które można przekazać, aby dostosować skrypt pod swój zbiór danych. Wszystkie możliwe parametry są opisane po wywołaniu polecenia `python cli/{nazwa_skryptu}.py -h`.

#### Przygotowanie danych
##### Struktura archiwum
Archiwum musi być w określonym formacie (`tar.gz`, `tar.xz`) i zawierać 3 katalogi (`train`, `val`, `test` – nazwy można dostosować w pliku konfiguracyjnym) oraz co najmniej 1 plik w formacie `separated values` np. `CSV`. Każdy katalog powinien zawierać pliki `.pdb` reprezentujące strukturę RNA. Plik CSV powinien zawierać co najmniej 2 kolumny – jedną z nazwą pliku struktury np. `157d_S_000004_minimize_001.pdb` i drugą z wartością RMSD dla tej struktury. Nazwy kolumn są konfigurowalne za pomocą pliku `config.yml`. Możliwe jest wykorzystanie jednego pliku CSV dla struktur ze wszystkich zbiorów (treningowego, walidacyjnego, testowego) lub podanie dla każdego zbioru innego pliku CSV. Jeżeli chcemy wykorzystać inny separator niż przecinek również można to osiągnąć w pliku `config.yml`.

##### Gotowy zbiór danych
Aby wykorzystać istniejący już zbiór danych trzeba stworzyć archiwum `.tar.gz`/`.tar.xz` o odpowiedniej strukturze i wygenerować zgodny plik konfiguracyjny `config.yml`. Bardzo ważnym aspektem jest przestrzeganie wyżej opisanej struktury. Jeżeli celem jest stworzenie archiwum, które będzie działało z domyślnym plikiem konfiguracyjnym należy w archiwum umieści 3 katalogi o nazwach `train`, `val`, `test` i 3 pliki CSV `train.csv`, `val.csv`, `test.csv`. 

Jeżeli zbiór danych nie posiada danych walidacyjnych lub testowych to należy stworzyć te foldery, ale zostawić je puste oraz stworzyć pliki CSV z odpowiednimi kolumnami, ale bez rekordów. Takie podejście może jednak zakłócić pewne etapy tworzenia modelu i zaleca się zawsze stworzenie trzech zestawów danych np. z podziałem 6:2:2 i zwracając uwagę, aby ta sama struktura nie znalazła się w więcej niż jednym zestawie. 

Podejście z gotowym zbiorem wykorzystywaliśmy do dostosowania zbioru danych ARES, który zawiera 18 struktur RNA, po 1000 wariacji każdej. Ares nie posiadał zbioru walidacyjnego, a jedynie treningowy i testowy. Ustaliliśmy, że zbiorem walidacyjnym są 4 pierwsze struktury ze zbioru treningowego. Plik konfiguracyjny dostępny jest jako `configs/config_ares.yml`.

##### Generowanie zbioru danych
<!-- TODO: Tutaj może niech Bartek coś napisze o przebiegu, podziale, przygotowywaniu archiwum i potencjalną automatyzacją tego procesu i umieszczeniu w repozytorium kroków reprodukcji – dla mnie najważniejsze jest, że otrzymaliśmy archiwum, które jest w idealnym formacie pod domyślny plik konfiguracyjny -->

#### Wykorzystanie danych surowych
Aby wykorzystać archiwum w naszym projekcie należy albo wrzucić je do sieci i w pliku konfiguracyjnym skonfigurować adres do pobrania albo ręcznie umieścić archiwum w odpowiednim katalogu.

##### Za pomocą URL do pobrania
Ta opcja jest dużo prostsza – wystarczy w pliku konfiguracyjnym ustalić adres do pobrania `config.data.download.url` i odpalić skrypt `python cli/download_raw_data.py`. Można też nie zmieniać pliku konfiguracyjnego i po prostu wywołać skrypt z parametrem `python cli/download_raw_data.py --data-download-url={URL}`.

##### Ręcznie
Ta opcja jest trochę trudniejsza. Należy w pliku konfiguracyjnym ustalić adres do pobrania `config.data.download.url` jako `False`. Przenieść archiwum do katalogu `{config.data.path}/{config.name}` i nazwać go `archive.tar.xz`, a następnie odpalić skrypt `python cli/download_raw_data.py`. Można też nie zmieniać pliku konfiguracyjnego i po prostu wywołać skrypt z parametrem `python cli/download_raw_data.py --data-download-url=false`.

#### Preprocessing
Aby dane nadawały się do przetwarzania przez grafową sieć neuronową należy je najpierw przetworzyć i zapisać w innym formacie. Proces ten składa się z kilku etapów:

1. Filtrowanie: Każdy plik `.pdb` jest filtrowany tak, że jedynie linie zaczynające się od `ATOM` są brane pod uwagę aby oszczędzić czas i moc obliczeniową.
2. Ekstrakcja cech: Używając *RNAgrowth* (`tools/RNAgrowth`) dla każdego pliku `.pdb` generowany jest nowy katalog zawierający odpowiednie pliki reprezentujące istotne cechy struktury. Szczególnie ważne są:
   * `.3dn` – macierz odległości między resztami w przestrzeni 3D,
   * `.ang` – reprezentuje kąty wiązań szkieletu RNA,
   * `.atr` – reprezentuje wszystkie kąty torsyjne,
   * `.bon` – reprezentuje wszystkie odległości wiązań,
   * `.sqn` – reprezentuje poprzednika i następnika każdej reszty w sekwencji.
3. Współprzędne i typ zasady: Za pomocą *PDBParser* wyodrębniamy współrzędne oraz typ zasady azotowej. Każda zasada (`A`, `C`, `G`, `U`) jest reprezentowania przy użyciu *one-hot encoding*. Współrzędne są obliczane używając `config.features.atom_for_distance_calculations`.
4. Struktura drugorzędowa: Za pomocą *RNApolis* ekstraktujemy informacje o strukturze drugorzędowej z analizowanej struktury 3D.
5. Krawędzie: Z pliku `.3dn` odczytujemy odległości między nukleotydami (wierzchołkami) – tworzą one nasze krawędzie i cechy powiązane z krawędziami: odległość przestrzenną i odległość sekwencyjną.
6. Wszystkie te dane są zawarte w obiekcie typu `Data` PyTorch Geometric, zawierającego cztery atrybuty:
   * `x` – cechy wierzchołków: zasada, współrzędne, wszystkie kąty wiązań, wszystkie kąty torsyjne, struktura drugorzędowa.
   * `edge_index` – krawędzie.
   * `edge_attr` – cechy krawędzi: odległość przestrzenan, odległość sekwencyjna.
   * `y` (opcjonalnie) – docelowa wartość RMSD dla określonego pliku `.pdb`.

Aby wykonać preprocessing należy wykonać skrypt `python cli/preprocess_data.py`.

Sam proces może być czasochłonny, ale efektem końcowym będzie otrzymanie trzech plików `.h5`, które reprezentują odpowiednie zestawy w odpowiednim formacie dla sieci neuronowej. Każdy plik H5 składa się z wpisów, których nazwy są nazwami struktur, a każdy wpis zawiera 4 numpy'owe tablice dostępne pod kluczami `x`, `edge_index`, `edge_attr`, `y`.

#### Wykorzystanie danych po preprocessingu
Jeżeli preprocessing został już wcześniej wykonany i posiadamy pliki H5 to aby z nich skorzystać wystarczy przenieść je do katalogu `{config.data.path}`.

Dodatkowo przygotowaliśmy prosty skrypt, który pozwala pobierać pliki H5 znajdujące się na zewnętrznym serwerze – wystarczy podmienić adresy URL w pliku konfiguracyjnym `{config.data.download_preprocessed}` i wywołać skrypt `python cli/download_preprocessed_data.py`.

#### Trening modelu
Aby wytrenować sieć neuronową należy najpierw ustawić optymalne parametry sieci za pomocą pliku konfiguracyjnego, a następnie wywołać skrypt `python cli/train_network.py`. Wytrenowany model będzie znajdował się w katalogu `{model_output_path}/{timestamp}`.

Aby eksperymentować z parametrami sieci najwygodniej będzie wykorzystać gotowy Jupyter notebook znajdujący się w katalogu `notebooks` pod nazwą `train_network.ipynb`. 

#### Ewaluacja modelu
Aby sprawdzić jak nasz model radzi sobie na zbiorze testowym należy odpalić skrypt `python cli/eval_network.py -m {path_to_model}`.

### Wykorzystanie modelu
Wykorzystanie gotowego modelu różni się od powyższej sekcji, ponieważ przygotowane jest do przetworzeniu pojedynczego pliku `.pdb`. Oznacza to, że najpierw będziemy wykonywać preprocessing w locie, a następnie przekazywali sieci wejście w odpowiednim formacie. Nie wykorzystujemy już plików H5, bo nie ma to sensu.

Najwygodniejszym wykoszystaniem naszego modelu jest skorzystanie z naszego interfejsu webowego<!-- TODO: URL -->. Można odpalić go lokalnie za pomocą: `./web/start.sh` (uruchamia zarówno API, jak i serwer Reacta). Można przerwać wszystkie procesy używając analogicznego skryptu `./web/stop.sh`.

Drugim sposobem jest wykorzystanie skryptu `python cli/get_rmsd.py -m {path_to_model} -i {path_to_pdb_file}`, który zwraca pojedynczą liczbę oznaczającą RMSD.
