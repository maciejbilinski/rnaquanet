"""
This is a boilerplate pipeline 'preprocessing_data'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import prepare_catalogs, filter_files

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=prepare_catalogs,
            inputs=['params:prepare_catalogs_src', 'params:prepare_catalogs_dest', 'params:mappings','extracted_ares_archive'],
            outputs='prepared_dir',
            name='prepare_catalogs_node'
        ),
        node(
            func=filter_files,
            inputs=['prepared_dir', 'params:filter_files_dest'],
            outputs='prepared_files',
            name='filter_files_node'
        )
    ])
