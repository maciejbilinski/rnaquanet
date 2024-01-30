# RNAQUANET

## środowisko
Aby w pełni i bezproblemowo wykorzystać nasz projekt należy [pobrać](https://docs.docker.com/get-docker/) i zainstalować Dockera, a następnie w sklonowanym katalogu wywołać poniższe polecenia: 

    docker compose up -d
    docker attach rnaquanet-python_cuda-1

Dodatkowo do wygodnej pracy polecamy [Dev Containers w VSCode](https://code.visualstudio.com/docs/devcontainers/containers).

## Przebieg pracy
### Tworzenie modelu
Główną częścią naszego projektu jest stworzenie modelu sieci grafowej. Aby uprościć i zautomatyzować cały proces stworzyliśmy CLI, które efektywnie pomaga w tym zadaniu. Wszystkie skrypty znajdują się w katalogu `cli` i uruchamiane są za pomocą polecenia `python cli/{nazwa_skryptu}.py`. Skrypty posiadają też wiele parametrów, które można przekazać, aby dostosować skrypt pod swój zbiór danych. Wszystkie możliwe parametry są opisane po wywołaniu polecenia `python cli/{nazwa_skryptu}.py -h`.

#### Przygotowanie danych
##### Struktura archiwum
Archiwum musi być w formacie `.tar.gz` i zawierać 3 katalogi (`train`, `val`, `test` - nazwy można dostosować w pliku konfiguracyjnym) oraz co najmniej 1 plik w formacie `separated values` np. `CSV`. Każdy katalog powinien zawierać pliki `.pdb` reprezentujące strukturę RNA. Plik CSV powinien zawierać co najmniej 2 kolumny - jedną z nazwą pliku struktury np. `157d_S_000004_minimize_001.pdb` i drugą z wartością RMSD dla tej struktury. Nazwy kolumn są konfigurowalne za pomocą pliku `config.yml`. Możliwe jest wykorzystanie jednego pliku CSV dla struktur ze wszystkich zbiorów (treningowego, walidacyjnego, testowego) lub podanie dla każdego zbioru innego pliku CSV. Jeżeli chcemy wykorzystać inny separator niż przecinek również można to osiągnąć w pliku `config.yml`.

##### Gotowy zbiór danych
Aby wykorzystać istniejący już zbiór danych trzeba stworzyć archiwum `.tar.gz` o odpowiedniej strukturze i wygenerować zgodny plik konfiguracyjny `config.yml`. Bardzo ważnym aspektem jest przestrzeganie wyżej opisanej struktury. Jeżeli celem jest stworzenie archiwum, które będzie działało z domyślnym plikiem konfiguracyjnym należy w archiwum umieści 3 katalogi o nazwach `train`, `val`, `test` i 3 pliki CSV `train.csv`, `val.csv`, `test.csv`. 

Jeżeli zbiór danych nie posiada danych walidacyjnych lub testowych to należy stworzyć te foldery, ale zostawić je puste oraz stworzyć pliki CSV z odpowiednimi kolumnami, ale bez rekordów. Takie podejście może jednak zakłócić pewne etapy tworzenia modelu i zaleca się zawsze stworzenie trzech zestawów danych np. z podziałem 60:20:20 i zwracając uwagę, aby ta sama struktura nie znalazła się w więcej niż jednym zestawie. 

Podejście z gotowym zbiorem wykorzystywaliśmy do dostosowania zbioru danych ARES, który zawiera 18 struktur RNA, po 1000 wariacji każdej. Ares nie posiadał zbioru walidacyjnego, a jedynie treningowy i testowy. Ustaliliśmy, że zbiorem walidacyjnym są 4 pierwsze4 struktury ze zbioru treningowego. Plik konfiguracyjny dostępny jest jako `configs/config_ares.yml`.

##### Generowanie zbioru danych
<Tutaj może niech Bartek coś napisze o przebiegu, podziale, przygotowywaniu archiwum i potencjalną automatyzacją tego procesu i umieszczeniu w repozytorium kroków reprodukcji - dla mnie najważniejsze jest, że otrzymaliśmy archiwum, które jest w idealnym formacie pod domyślny plik konfiguracyjny>

#### Wykorzystanie danych surowych
Aby wykorzystać archiwum w naszym projekcie należy albo wrzucić je do sieci i w pliku konfiguracyjnym skonfigurować adres do pobrania albo ręcznie umieścić archiwum w odpowiednim katalogu.

##### Za pomocą URL do pobrania
Ta opcja jest dużo prostsza - wystarczy w pliku konfiguracyjnym ustalić adres do pobrania `config.data.download.url` i odpalić skrypt `python cli/download_raw_data.py`. Można też nie zmieniać pliku konfiguracyjnego i po prostu wywołać skrypt z parametrem `python cli/download_raw_data.py --data-download-url={URL}`.

##### Ręcznie
Ta opcja jest trochę trudniejsza. Należy w pliku konfiguracyjnym ustalić adres do pobrania `config.data.download.url` jako `False`. Przenieść archiwum do katalogu `{config.data.path}/{config.name}` i nazwać go `archive.tar.gz`, a następnie odpalić skrypt `python cli/download_raw_data.py`. Można też nie zmieniać pliku konfiguracyjnego i po prostu wywołać skrypt z parametrem `python cli/download_raw_data.py --data-download-url=false`.

#### Preprocessing
Aby dane nadawały się do przetwarzania przez grafową sieć neuronową należy je najpierw przetworzyć i zapisać w innym formacie. Proces ten składa się z kilku etapów:
<Tutaj może Mikołaj lub Szymon by chciał opisać jak przebiega ten preprocessing, bo się tym głównie zajmowali>

Aby wykonać preprocessing należy wykonać skrypt `python cli/preprocess_data.py`.

Sam proces może być czasochłonny, ale efektem końcowym będzie otrzymanie trzech plików `.h5`, które reprezentują odpowiednie zestawy w odpowiednim formacie dla sieci neuronowej. Każdy plik H5 składa się z kilku grup, których nazwy są nazwami struktur, a wewnątrz każdej grupy zawiera 4 numpy'owe tablice dostępne pod kluczami x, edge_index, edge_attr, y.

#### Wykorzystanie danych po preprocessingu
Jeżeli preprocessing został już wcześniej wykonany i posiadamy pliki H5 to aby z nich skorzystać wystarczy przenieść je do katalogu `{config.data.path}`.

Dodatkowo przygotowaliśmy prosty skrypt, który pozwala pobierać pliki H5 znajdujące się na zewnętrznym serwerze - wystarczy podmienić adresy URL w pliku konfiguracyjnym `{config.data.download_preprocessed}` i wywołać skrypt `python cli/download_preprocessed_data.py`.

#### Trening modelu
Aby wytrenować sieć neuronową należy najpierw ustawić optymalne parametry sieci za pomocą pliku konfiguracyjnego, a następnie wywołać skrypt `python cli/train_network.py`. Wytrenowany model będzie znajdował się w katalogu `{model_output_path}/{timestamp}`.

Aby eksperymentować z parametrami sieci najwygodniej będzie wykorzystać gotowy Jupyter notebook znajdujący się w katalogu `notebooks` pod nazwą `train_network.ipynb`. 

#### Ewaluacja modelu
Aby sprawdzić jak nasz model radzi sobie na zbiorze testowym należy odpalić skrypt `python cli/eval_network.py -m {path_to_model}`.

### Wykorzystanie modelu
Wykorzystanie gotowego modelu różni się od powyższej sekcji, ponieważ przygotowane jest do przetworzeniu pojedynczego pliku `.pdb`. Oznacza to, że najpierw będziemy wykonywać preprocessing w locie, a następnie przekazywali sieci wejście w odpowiednim formacie. Nie wykorzystujemy już plików H5, bo nie ma to sensu.

Najwygodniejszym wykoszystaniem naszego modelu jest skorzystanie z naszego interfejsu webowego dostępnego pod adresem <Kiedyś dodamy>. Można też odpalić go lokalnie za pomocą: <Szymon tutaj musi opisać jak lokalnie odpalić interfejs webowy>.

Drugim sposobem jest wykorzystanie skryptu `python cli/get_rmsd.py -m {path_to_model} -i {path_to_pdb_file}`, który zwraca poojedynczą liczbę oznaczającą RMSD. 