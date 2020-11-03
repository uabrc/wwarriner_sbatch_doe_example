from pathlib import PurePath
import subprocess
import argparse


def run(command: str, treatment_file: PurePath, row: int):
    with open(treatment_file, "r") as f:
        lines = f.readlines()
        line = lines[row]
    line = line.replace(",", " ")
    process = "{:s} {:s}".format(command, line)
    print(process)
    # subprocess.run(process)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="run arbitrary command with parameters read from line"
    )
    parser.add_argument("command", type=str, nargs=1, help="command to run")
    parser.add_argument(
        "treatment_file", type=str, nargs=1, help="file with treatments"
    )
    parser.add_argument("row", type=int, nargs=1, help="row in treatment file")
    args = parser.parse_args()
    run(command=args.command[0], treatment_file=args.treatment_file[0], row=args.row[0])
