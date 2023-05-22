"""
This is a boilerplate pipeline 'preprocessing_data'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import prepare_catalogs

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=prepare_catalogs,
            inputs='params:catalog_mappings',
            outputs=None,
            name='prepare_catalogs_node'
        )
    ])
