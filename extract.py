"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import dataclasses
import json
from typing import Callable

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path) -> list[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    with open(neo_csv_path, "r") as neo_csv:
        reader = csv.DictReader(neo_csv)
        # Filter out unused columns and remove potential duplicate entries
        field_mapping: list[tuple[str, str, Callable]] = [
            ("pdes", "designation", lambda x: x),
            ("name", "name", lambda x: x),
            ("diameter", "diameter", float),
            ("pha", "hazardous", lambda x: x == "Y"),
        ]
        return list(
            {
                NearEarthObject(
                    **{param_name: f(row[k]) for k, param_name, f in field_mapping if row[k]}
                )
                for row in reader
            }
        )


def load_approaches(cad_json_path) -> list[CloseApproach]:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """

    with open(cad_json_path, "r") as cad_json:
        data = json.load(cad_json)
        # Filter out unused columns and remove potential duplicate entries
        field_mapping: list[tuple[str, str, Callable]] = [
            ("des", "_designation", lambda d: d[0]),
            ("cd", "time", lambda d: d[3]),
            ("dist", "distance", lambda d: float(d[4])),
            ("v_rel", "velocity", lambda d: float(d[7])),
        ]
        return list(
            {
                CloseApproach(**{param_name: f(row) for _, param_name, f in field_mapping})
                for row in data["data"]
            }
        )
