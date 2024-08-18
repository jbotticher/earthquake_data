import os
from pathlib import Path
from dagster_dbt import DbtCliResource, dbt_assets
from dagster import OpExecutionContext

# configure dbt project resource
dbt_project_dir = Path(__file__).joinpath("..", "..", "..", "..","..", "dbt_earthquake", "warehouse").resolve()
dbt_warehouse_resource = DbtCliResource(project_dir=os.fspath(dbt_project_dir))


# DBT_DIRECTORY = Path(__file__).joinpath("..", "..", "..", "..","..", "dbt_earthquake", "warehouse").resolve()
# dbt_manifest_path_static = os.path.join(DBT_DIRECTORY, "target", "manifest.json")



# generate manifest
dbt_manifest_path = (
    dbt_warehouse_resource.cli(
        ["--quiet", "parse"],
        target_path=Path("target"),
    )
    .wait()
    .target_path.joinpath("manifest.json")
)

# print(dbt_manifest_path)

# load manifest to produce asset defintion
@dbt_assets(manifest=dbt_manifest_path)
def dbt_warehouse(context: OpExecutionContext, dbt_warehouse_resource: DbtCliResource):
    yield from dbt_warehouse_resource.cli(["build"], context=context).stream()