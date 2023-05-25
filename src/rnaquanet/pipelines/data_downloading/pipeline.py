"""
This is a boilerplate pipeline 'data_downloading'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import download_ares_archive, extract_ares_archive

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=download_ares_archive,
            inputs=["params:ares_dataset_url", "params:ares_archive_path"],
            outputs='ares_archive',
            name="download_ares_archive_node"
        ),
        node(
            func=extract_ares_archive,
            inputs=["params:ares_archive_path", "params:ares_dataset_path",'ares_archive'],
            outputs='extracted_ares_archive',
            name="extract_ares_archive_node"
        )
    ])
