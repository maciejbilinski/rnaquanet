# RNAQuANet
## Environment
To fully and seamlessly access our project, [download and install Docker](https://docs.docker.com/get-docker) and then run the following commands in the cloned directory:

    docker compose up -d
    docker attach rnaquanet-python_cuda-1

For additional convenience we recommend using [Dev Containers in VS Code](https://code.visualstudio.com/docs/devcontainers/containers).

## Workflow
### Creating the model
The main part of our project is developing a graph neural network model. In order to simplify and automate the whole process, we created a command line interface (CLI) that streamlines this task. All scripts are located in the `cli` directory and are executed by simply using `python cli/{script_name}.py` command. The scripts also contain a number of parameters that can be passed to customise the script for a specific dataset. All possible parameters can be viewed through `python cli/{script_name}.py -h`.

#### Preparing the data
##### Archive structure
The archive must be in specified format (`tar.gz`, `tar.xz`) and contain exactly 3 directories: `train`, `val` and `test` (the names can be customised in the configuration file), as well as at least 1 `.csv` file. Each directory should contain `.pdb` files representing RNA structures. The CSV file should contain at least 2 columns – one with the file name of the structure, e.g. `157d_S_000004_minimize_001.pdb` and the other with the RMSD value for that structure. The column names are configurable usi55ng the provided `config.yml` file.

It is possible to use single CSV file for all datasets (training, validation, test) or to specify separate CSV files for each set. The separator character can also be set using the provided `config.yml` file.

##### Existing dataset
To use an existing dataset, you need to create a `.tar.gz`/`.tar.xz` archive and then generate compatible `config.yml` configuration file. It is crucial to follow the structure described above. If the goal is to create an archive that will work with the default configuration, you should include 3 directories: `train`, `val`, `test`; and 3 CSV files: `train.csv`, `val.csv`, `test.csv` in the archive.

If the dataset has no validation or test sets then create these folders but leave them empty; then create relevant CSV files with columns but no records. This approach however may disrupt certain stages of model creation and it is always advisable to create 3 datasets, e.g. with a 6:2:2 split and ensuring that the same structure is not included in more than one subset.

We used this approach to adapt the ARES dataset, which contains 18 RNA structures with 1000 variants each. ARES does not have a validation set, only the training and test sets; thus we decided that the validation set should consist of 4 first structures from ARES's training set. The relevant configuration file is available in `configs/ares.yml`.

##### Generating a new dataset
<!-- TODO: Breakdown of the process, the preparation of the archive and the potential automation of this process – the most important thing is that we get an archive that is in suitable format for the default configuration file -->

#### Using raw data
In order to use raw data you have to either upload it to the Internet and then configure URL in the configuration file, or manually copy the archive into respective directory.

##### Via download URL
This option is much easier. All you need to do is setup `config.data.download.url` in the configuration file and then run `python cli/download_raw_data.py`. You can also run `python cli/donwload_raw_data.py --data-download-url={URL}` without changing the configuration file.

##### Manually
This is more difficult. You have to set `config.data.download.url` to `False` in the configuration file. Then copy the archive into `{config.data.path}/{config.name}` directory with the filename `archive.tar.xz`, and then run `python cli/download_raw_data.py`. You can also run `python cli/download_raw_data.py --data-download-url=false` without changing the configuration file.

#### Preprocessing
In order for the data to be ready to be used in the training process, it needs to be properly processed and saved in a suitable format.

The process involves several stages:

1. Filtering: Each `.pdb` file is filtered, so that only lines starting with `ATOM` are considered to save both time and computing power.
2. Feature extraction: Using *RNAgrowth* (`tools/RNAgrowth`) on each `.pdb` file generates a new directory containing respective files representing relevant features. Especially important are:
   * `.3dn` – matrix of inter-residue distances in 3D space,
   * `.ang` – represents the bond angles of the sugar-phosphate backbone of RNA,
   * `.atr` – represents all torsion angles,
   * `.bon` – represents all bond distances,
   * `.sqn` – represents the immediate predecessor and successor of each residue in the sequence.
3. Coords and nucleobase: Using *PDBParser* we extract both coordinates and nucleobase. Each nucleobase (`A`, `C`, `G`, `U`) is represented using *one-hot encoding*. Coordinates are calculated using `config.features.atom_for_distance_calculations`.
4. Secondary structure: Using *RNApolis* annotator script we extract secondary structure information from the analysed 3D structure.
5. Edges: From `.3dn` file we read distances between nucleotides (nodes) – this forms our edges and edge features: spatial distance and sequential distance.
6. All this data is packed into PyTorch Geometric `Data` object, containing four attributes:
   * `x` – node features: nucleobase, coordinates, all bond angles, all torsion angles, base pairings.
   * `edge_index` – edge indices.
   * `edge_attr` – edge features: spatial distance, sequential distance.
   * `y` (optional) – target RMSD score (label) for a specified `.pdb` file.

In order to preprocess data, simply run `python cli/preprocess_data.py`.

The entire process can take quite some time, depending on the size of your dataset. In the end you are going to get three `.h5` files, representing three distinct datasets in the proper format for the neural network. Each H5 file contains multiple entries, grouped by structure names. Each entry contains 4 NumPy arrays: `x`, `edge_index`, `edge_attr`, `y`.

#### Using preprocessed data
If preprocessing has been already done on a dataset and you do have suitable H5 files, you can use them by placing them into `{config.data.path}` directory.

You can also download H5 files from a URL using a script. All it takes is specifying `{config.data.download_preprocessed}` in the configuration file and then running `python cli/download_preprocessed_data.py`.

#### Training
To train the neural network, you should set up parameters using configuration file. Then, run `python cli/train_network.py`. The trained model will be saved to a file in `{config.model_output_path}/{timestamp}`.

#### Evaluation
For evaluating a model using the test set, run an evaluation script `python cli/eval_network.py -m {model_file}`.

### Using the model
Using ready, trained model is different to the previous section, because in our context it applies to processing and running prediction on a single `.pdb` file. This means running preprocessing on a single file and then passing the input data to the network.

The most convenient way for assessing single structure is using our web interface<!-- TODO: URL -->. You can run it locally using `./web/start.sh` (it starts API, as well as React server). You can stop all running processes by using `./web/stop.sh` respectively.

Another possibility is using the CLI script `python cli/get_rmsd.py -m {model_file} -i {pdb_file}`, which returns a single number – RMSD score.
