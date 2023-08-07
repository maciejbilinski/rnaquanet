# RNAQUANET

## Pipelines
Projekt składania się (póki co) z czterech pipeline'ów: `download_raw_data`, `preprocess_data`, `download_preprocessed_data`, `train_network`. Każdy pipeline można odpalić wywołując odpowiedni plik z folderu `src/scripts`.

### Pobieranie danych
Aby pobrać dane należy odpowiednio skonfigurować plik `config.yaml`, a następnie wywołać skrypt `python src/scripts/download_data.py`. Następnie dane należy poddać czasochłonnemu preprocessingowi. Alternatywnie można skorzystać z `python src/scripts/download_preprocessed_data.py` i **pominąć** preprocessing.

### Preprocessing
Aby wykonać preprocessing należy najpierw pobrć dane skryptem `python src/scripts/download_data.py`, a następnie odaplić bardzo czasochłonny skrypt `python src/scripts/preprocess_data.py`. Plikami wynikowymi są pliki H5, które są proste do odczytania i teoretycznie optymalne nawet do losowego odczytywania.

### Trenowanie sieci neuronowej
Trening sieci neuronowej jest w fazie rozwoju. Przygotowana jest architektura GraphQA pod RNA poprzez uproszczenie architektury (usunięcie embeddingów) i zmianę wyjścia tak, żeby zwracała tylko jedną liczbę rzeczywistą.

## Build and run docker image
```bash
docker compose up --build
```

it runs pipeline and monitor. To check progress visit http://127.0.0.1:8080

Polecam korzystać z [Dev Containers w VSCode](https://code.visualstudio.com/docs/devcontainers/containers)