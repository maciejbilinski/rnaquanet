from Bio.PDB import FastMMCIFParser, Structure
from Bio.PDB.PDBParser import PDBParser
from io import TextIOWrapper
from typing import Literal

# from backend.models import TemporaryFile
from Bio.PDB import PDBIO, Select
import json, os

from config import FILE_STORAGE_DIR, ALLOWED_FILE_TYPES


def resname(res):
    name = res.get_resname()
    while name[0] == "D":
        name = name[1:]
    return name


def analyze_structure(structure: Structure):
    dk: dict[str, dict[str, list[str]]] = {}
    for model in structure:
        model_name = str(int(model.id) + 1)
        # model_name = file.name.split(".")[0]+": "+str(int(model.id)+1)
        dk[model_name] = {}
        for chain in model:
            dk[model_name][chain.id] = []
            for residue in chain:
                if "P" in [i.name for i in residue.get_atoms()]:
                    dk[model_name][chain.id].append(resname(residue))
    return dk


def parse_file(file_handle: TextIOWrapper, file_type: Literal["pdb", "cif"]):
    match file_type:
        case "pdb":
            return PDBParser(PERMISSIVE=1, QUIET=True).get_structure("str", file_handle)
        case "cif":
            return FastMMCIFParser(QUIET=True).get_structure("str", file_handle)


def get_models_with_chains(task_id: str, file_name: str):
    dir_path = os.path.join(FILE_STORAGE_DIR, task_id)
    file_type = file_name.split(".")[-1].lower()

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            raise

        with open(os.path.join(dir_path, file_name)) as file_handle:
            return json.dumps(find_rna_chains(parse_file(file_handle, file_type)))

    except Exception:
        return None


class ChainsSelect(Select):
    chains = []

    def __init__(self, chains):
        self.chains = chains

    def accept_residue(self, residue):
        id: str = residue.get_parent().id
        return id.isnumeric() and int(id) in self.chains and residue.id[0] == " "


def process(
    task_id: str,
    file_name: str,
    end_file_name: str,
    model_no: int,
    chains_list: list[int],
):
    dir_path = os.path.join(FILE_STORAGE_DIR, task_id)
    file_type = file_name.split(".")[-1].lower()

    try:
        with open(os.path.join(dir_path, file_name)) as file_handle:
            structure_model = parse_file(file_handle, file_type)[int(model_no)]
            io = PDBIO()
            io.set_structure(structure_model)
            io.save(end_file_name, ChainsSelect(chains_list))

            return 0

    except Exception:
        return 1


dna_dict = ["DT", "DA", "DC", "DG"]


rna_dict = ["A", "C", "G", "U"]
protein_dict = [
    "ALA",
    "ARG",
    "ASN",
    "ASP",
    "CYS",
    "GLN",
    "GLU",
    "GLY",
    "HIS",
    "ILE",
    "LEU",
    "LYS",
    "MET",
    "PHE",
    "PRO",
    "SER",
    "THR",
    "TRP",
    "TYR",
    "VAL",
]


def find_rna_chains(structure: Structure, structure_models_with_chains=None):
    distribution = {}
    rna_chains = {}
    for model in structure:
        distribution[model.id] = {}
        for chain in model:
            distribution[model.id][chain.id] = {
                "RNA": 0,
                "DNA": 0,
                "Protein": 0,
            }
            for residue in chain:
                res = residue.get_resname().strip()
                if res in protein_dict:
                    distribution[model.id][chain.id]["Protein"] = (
                        distribution[model.id][chain.id].pop("Protein") + 1
                    )
                elif res in dna_dict:
                    distribution[model.id][chain.id]["DNA"] = (
                        distribution[model.id][chain.id].pop("DNA") + 1
                    )
                elif res in rna_dict:
                    distribution[model.id][chain.id]["RNA"] = (
                        distribution[model.id][chain.id].pop("RNA") + 1
                    )

            molecule_type = max(
                distribution[model.id][chain.id],
                key=distribution[model.id][chain.id].get,
            )
            if ("RNA" == molecule_type or "DNA" == molecule_type) and distribution[
                model.id
            ][chain.id]["RNA"] > 0:
                if structure_models_with_chains:
                    if (
                        str(model.id + 1) in structure_models_with_chains
                        and chain.id in structure_models_with_chains[str(model.id + 1)]
                    ):
                        if model.id not in rna_chains:
                            rna_chains[model.id] = []
                        rna_chains[model.id].append(chain.id)
                else:
                    if model.id not in rna_chains:
                        rna_chains[model.id] = []
                    rna_chains[model.id].append(chain.id)
    return rna_chains
