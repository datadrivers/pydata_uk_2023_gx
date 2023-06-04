""" This cloud function calls GX validation run on given resource and configuration
"""
import os
import functions_framework
from great_expectations.checkpoint import SimpleCheckpoint
from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
import ruamel.yaml as yaml
from typing import Any, Dict
from google.cloud import storage
from expectations import *

from flask import jsonify


def read_yml_from_gcs(
    bucket_name: str,
    blob_name: str,
    client: storage.Client = storage.Client(),
) -> Dict[str, Any]:

    bucket: storage.Bucket = client.get_bucket(bucket_name)
    content: bytes = bucket.blob(blob_name).download_as_string()
    decoded: str = content.decode("utf-8")

    return yaml.safe_load(decoded)


def build_data_context_config(config: Dict[str, Any]) -> DataContextConfig:
    return DataContextConfig(**config)


def build_data_context(config: DataContextConfig) -> BaseDataContext:
    return BaseDataContext(config, context_root_dir=".")


@functions_framework.http
def main(request):
    bucket = os.environ.get("GREAT_EXPECTATIONS_BUCKET_NAME")
    config_path = os.environ.get("GREAT_EXPECTATIONS_CONFIG_PATH")

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json:
        table_spec: dict = request_json
    elif request_args:
        table_spec: dict = request_args
    else:
        return "No table specification given."

    datasource_name: str = table_spec['datasource_name']
    data_asset_name: str = table_spec['data_asset_name']
    expectation_suite_name: str = table_spec['expectation_suite_name']

    project_config: dict = read_yml_from_gcs(bucket, config_path)
    context_config: DataContextConfig = build_data_context_config(project_config)
    context: BaseDataContext = build_data_context(context_config)

    batch_request: dict = dict(datasource_name=datasource_name,
                               data_connector_name='default_inferred_data_connector_name',
                               data_asset_name=data_asset_name)

    checkpoint_config: dict = {
        "class_name": "SimpleCheckpoint",
        "validations": [{"batch_request": batch_request,
                         "expectation_suite_name": expectation_suite_name}]
    }

    checkpoint_result = run_checkpoint(checkpoint_config, context, data_asset_name, expectation_suite_name)

    return jsonify(checkpoint_result.to_json_dict(), 200 if checkpoint_result["success"] else 417)


def run_checkpoint(checkpoint_config, context, data_asset_name, expectation_suite_name) -> CheckpointResult:

    checkpoint: SimpleCheckpoint = SimpleCheckpoint(f"{data_asset_name}_{expectation_suite_name}", context,
                                                    **checkpoint_config)
    checkpoint_result: CheckpointResult = checkpoint.run()

    return checkpoint_result
