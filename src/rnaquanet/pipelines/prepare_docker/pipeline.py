"""
This is a boilerplate pipeline 'prepare_docker'
generated using Kedro 0.18.8
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import download_structure_descriptor_docker_file,add_docker_image

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=download_structure_descriptor_docker_file,
            inputs=["params:structure_descriptor_docker_image", "params:docker_image_path"],
            outputs='prepare_docker_1',
            name="download_structure_descriptor_docker_file"
        ),
        node(
            func=add_docker_image,
            inputs=["params:docker_image_path", "params:raise_on_error",'prepare_docker_1'],
            outputs='prepare_docker_end',
            name="add_docker_image"
        ),
        
    ])
