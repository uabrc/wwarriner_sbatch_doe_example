import itertools
import json
from pathlib import PurePath

import pandas as pd


def generate_array_job(
    config_file: PurePath,
    payload_file: PurePath,
    treatment_count: int,
    output_file: PurePath,
):
    with open(config_file, "r") as f:
        config = json.load(f)
    num_same_time = config.pop("num_same_time")

    with open(payload_file, "r") as f:
        payload = f.readlines()

    sbatch = []
    sbatch.append("#!/bin/bash")
    sbatch.append("")

    for key, value in config.items():
        sbatch.append("#SBATCH --{:s}={:s}".format(key, str(value)))
    sbatch.append(
        "#SBATCH --array=0-{:d}%{:d}".format(treatment_count - 1, num_same_time)
    )
    sbatch.append("")

    sbatch.extend(payload)
    sbatch.append("")

    sbatch = [line.rstrip() for line in sbatch]
    sbatch = "\n".join(sbatch)

    with open(output_file, "w") as f:
        f.write(sbatch)


def generate_parameter_space(doe_file: PurePath, output_file: PurePath) -> int:
    with open(doe_file, "r") as f:
        parameters = json.load(f)

    keys = parameters.keys()
    values = [[(k, v) for v in parameters[k]] for k in keys]
    # Values looks like:
    # [
    #   [(key_1, value_1_1), ..., (key_1, value_1_m)],
    #   ...
    #   [(key_n, value_n_1), ..., (key_n, value_n_m)]
    # ]

    generator = itertools.product(*values)
    # itertools.product(*args) generates all possible Cartesian products formed
    # by selecting one item from each of its input sequences. This is precisely
    # a full-factorial DoE! Other experimental designs can be achieved by
    # careful manipulation of functions in the itertools library.

    treatments = []
    for item in generator:
        treatment = {key: parameter for key, parameter in item}
        treatments.append(treatment)
    # treatments is an array of entires that look like:
    # {
    #   "parameter_1": value_1,
    #   ...
    #   "parameter_n": value_n
    # }
    # which form the rows of a dataframe. Keys are columns, values are entries

    df = pd.DataFrame(data=treatments)
    df.to_csv(str(output_file), index=False)

    return len(df)


if __name__ == "__main__":
    treatment_count = generate_parameter_space(
        doe_file=PurePath("doe.json"), output_file=PurePath("doe.csv")
    )
    generate_array_job(
        config_file=PurePath("sbatch.json"),
        payload_file=PurePath("payload.sh"),
        treatment_count=treatment_count,
        output_file=PurePath("run.sh"),
    )
