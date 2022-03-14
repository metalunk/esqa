# -*- coding: utf-8 -*-
"""Console script for esqa."""
import json
from dataclasses import is_dataclass, asdict

import click

from esqa.save import RankingSaver
from esqa.validation_config import load
from esqa.validator import Validator


@click.group()
def main():
    pass


# To serialize class object
# Ref https://pod.hatenablog.com/entry/2018/09/29/222455
def custom_default(o):
    if is_dataclass(o):
        return asdict(o)
    raise TypeError(f"{o!r} is not JSON serializable")


def _dump(data):
    return json.dumps(
        data,
        indent=2,
        default=custom_default,
        ensure_ascii=False,
    )


@main.command()
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("--index", type=str, help="target index name", required=True)
def check(config, index):
    runner = Validator()
    results = runner.run(config=load(config), index_name=index)
    print(_dump(results))


@main.command()
@click.option("-c", "--config", type=str, help="configuration file")
@click.option("--index", type=str, help="target index name", required=True)
def save(config, index):
    runner = RankingSaver()
    results = runner.run(config=load(config), index_name=index)
    print(_dump(results))


if __name__ == "__main__":
    main()
