import pandas as pd
from rnapolis import parser, annotator, tertiary


from src.config.custom_types import PathType

def extract_basepairs(filtered_pdb_file_path: PathType,distinguish: bool = False):
    pairings = []
    """
    Extract basepairs from filtered pdb file.

    Args:
    - filtered_pdb_file_path - absolute path to filtered pdb file
    - distinguish - True if distinguish between opening and closing parentheses during one hot encoding

    Returns:
    - Pandas dataframe with basepair node features
    """
    
    with open(filtered_pdb_file_path, 'r') as f:
        structure3d = parser.read_3d_structure(f)
        structure2d = annotator.extract_secondary_structure(structure3d)
        mapping = tertiary.Mapping2D3D(structure3d, structure2d.basePairs, structure2d.stackings, False)
        temp = []
        for index, row in enumerate(mapping.dot_bracket.split('\n')):
            if (index % 3) == 2:
                temp.append(row)
        for i in ''.join(temp):
            pairings.append(i)
    pairings = pd.DataFrame({'pairings':pairings})
    series = pd.Categorical(
            pairings['pairings'] if distinguish
            else pairings['pairings'].replace({
                '\(': '()',    '\)': '()',
                '\{': '{}',    '\}': '{}',
                '\<': '<>',    '\>': '<>',
                '\[': '[]',    '\]': '[]',
            }, regex=True),
            categories=['.', '{', '}', '[', ']', '(', ')', '<', '>'] if distinguish
            else ['.', '{}', '()', '[]', '<>']
        )
    return pd.get_dummies(series, prefix='dot_bracket').astype(int)