import itertools
import json
from pathlib import PurePath

import pandas as pd


def generate_array_job(
    payload_file: PurePath, treatment_count: int, output_file: PurePath
):
    with open(payload_file, "r") as f:
        payload = f.read()

    sbatch = [
        "#!/bin/bash",
        "",
        "#SBATCH --ntasks={:d}".format(1),
        "#SBATCH --cpus-per-task={:d}".format(1),
        "#SBATCH --mem-per-cpu={:d}G".format(1),
        "#SBATCH --partition={:s}".format("express"),
        "#SBATCH --output={:s}".format("%A_%4a.log"),
        "#SBATCH --error={:s}".format("%A_%4a.log"),
        "#SBATCH --array=1-{:d}%{:d}".format(treatment_count, 4),  # zero based
        "",
        "{:s}".format(payload),
        "",
    ]
    sbatch = [line.rstrip() for line in sbatch]
    sbatch = "\n".join(sbatch)

    with open(output_file, "w") as f:
        f.write(sbatch)


def generate_treatments(doe_file: PurePath, output_file: PurePath) -> int:
    with open(doe_file, "r") as f:
        parameters = json.load(f)

    keys = parameters.keys()
    values = [[(k, v) for v in parameters[k]] for k in keys]
    _pretty_print(values)
    print()
    # Values looks like:
    # [
    #   [(learning_rate, 0.0001), (learning_rate, 0.01), (learning_rate, 1.0)],
    #   [(batch_size, 10), (batch_size, 30), (batch_size, 100)],
    #   [(activation_function, relu), (activation_function, tanh), (activation_function, sigmoid)]
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
    _pretty_print(treatments)
    print()
    # treatments is an array of entires that look like:
    # {
    #   learning_rate: 0.0001,
    #   batch_size: 10,
    #   activation_function: relu
    # }
    # which form the rows of a dataframe. Keys are columns, values are entries

    df = pd.DataFrame(data=treatments)
    df.to_csv(str(output_file), index=False)
    print(df.to_string())

    return len(df)


def _pretty_print(v):
    print(json.dumps(v, indent=2, sort_keys=True))


if __name__ == "__main__":
    treatment_count = generate_treatments(
        doe_file=PurePath("doe.json"), output_file=PurePath("doe.csv")
    )
    generate_array_job(
        payload_file=PurePath("payload.sh"),
        treatment_count=treatment_count,
        output_file=PurePath("doe.sh"),
    )
