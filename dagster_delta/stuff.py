from datetime import datetime
from pathlib import Path
import os
from dagster import asset, IOManager, graph, io_manager
from polars import DataFrame
import polars as pl


class PolarsDeltaIOManager(IOManager):
    def _get_path(self, context):
        p = Path("data") / context.step_key / context.name 
        return p

    def handle_output(self, context, obj):
        p = self._get_path(context)
        p.parent.mkdir(exist_ok=True, parents=True)
        obj.write_csv(p)
        context.log.info(f"{self} Wrote to {p}")

    def load_input(self, context):
        p = self._get_path(context.upstream_output)
        context.log.info(f"{self} Reading from {p}")
        return pl.read_csv(p)


@io_manager
def pl_io_manager():
    return PolarsDeltaIOManager()


@asset
def source() -> DataFrame:
    df = pl.DataFrame(
        {
            "integer": [1, 2, 3],
            "date": [
                (datetime(2022, 1, 1)),
                (datetime(2022, 1, 2)),
                (datetime(2022, 1, 3)),
            ],
            "float": [4.0, 5.0, 6.0],
        }
    )
    print(df)
    return df


@asset
def dates(df: DataFrame) -> DataFrame:
    result = df.select(pl.col("date"))
    print(result)
    return result


@graph
def my_dag():
    dates(source())


if __name__ == "__main__":
    result = my_dag.to_job(
        resource_defs={"io_manager": pl_io_manager}
    ).execute_in_process()
    for n in my_dag.node_dict:
        print(result.asset_materializations_for_node("dates"))
        # print(result.asset_value("dates"))
