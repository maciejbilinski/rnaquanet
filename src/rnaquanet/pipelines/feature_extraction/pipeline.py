"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import extract_features_from_structure_file_using_docker

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=lambda *args: extract_features_from_structure_file_using_docker(True, *args),
            inputs=["params:path", "params:structure_descriptor_params"],
            outputs=None,
            name="extract_features_from_train_structure_file_using_docker"
        ),
        node(
            func=lambda *args: extract_features_from_structure_file_using_docker(False, *args),
            inputs=["params:path", "params:structure_descriptor_params"],
            outputs=None,
            name="extract_features_from_test_structure_file_using_docker"
        ),
    ])
