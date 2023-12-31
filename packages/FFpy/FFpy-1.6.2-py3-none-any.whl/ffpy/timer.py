#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor
from tabulate import tabulate

SCRIPT_VERSION = "1.6.2"


def execute_python(script_filename, silent):
    if not silent:
        subprocess.run([sys.executable, script_filename])
    else:
        subprocess.run(
            [sys.executable, script_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


def measure_execution_time(
    script_filename, mode, time_unit="ms", num_runs=1, silent=False
):
    if mode == "multi":
        start_time = time.time()
        with ThreadPoolExecutor() as executor:
            executor.map(
                lambda _: execute_python(script_filename, silent), range(num_runs)
            )
        end_time = time.time()
        execution_time = end_time - start_time
    else:
        start_time = time.time()
        for _ in range(num_runs):
            execute_python(script_filename, silent)
        end_time = time.time()
        execution_time = end_time - start_time

    if time_unit == "ms":
        execution_time = execution_time * 1000
    elif time_unit != "s":
        print("Invalid time unit: {}".format(time_unit))
        sys.exit(1)

    if num_runs == 1:
        print("Execution time: {:.4f} {}".format(execution_time, time_unit))
    else:
        average_execution_time = execution_time / num_runs
        print(
            "Average execution time ({} runs): {:.4f} {}".format(
                num_runs, average_execution_time, time_unit
            )
        )

    return execution_time


def list_files(folder_path):
    script_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.endswith(".py") and os.path.isfile(os.path.join(folder_path, f))
    ]
    return script_files


def display_help():
    print(
        "Usage: {} <filename/folder> [filename_2] [...] [-u <unit>] [-n <number>] [-s] [-m <mode>] [-V] [-H]".format(
            sys.argv[0]
        )
    )
    print("Options:")
    print("  -u, --unit    Specify time unit (ms or s, default is ms)")
    print("  -n, --number  Number of runs (default is 1)")
    print("  -s, --silent  Run script silently (suppress output)")
    print("  -m, --mode    Execution mode (single or multi, default is single)")
    print("  -V, --ver Display script version")
    print("  -H, --help    Display this help message")
    sys.exit(0)


def gather_script_filenames(inputs):
    script_filenames = []
    for script_input in inputs:
        if os.path.isdir(script_input):
            script_filenames.extend(list_files(script_input))
        else:
            script_filenames.append(script_input)

    return script_filenames


def display_results(script_filenames, time_unit, num_runs, args):
    if len(script_filenames) > 2:
        table_data = []
        for script_filename in script_filenames:
            print(script_filename)
            execution_time = measure_execution_time(
                script_filename, args.mode, time_unit, num_runs, args.silent
            )
            table_data.append([script_filename, execution_time / num_runs])

        sorted_table = sorted(table_data, key=lambda x: x[1])
        headers = ["Filename", "Average Execution Time ({})".format(time_unit)]
        print(tabulate(sorted_table, headers, tablefmt="fancy_grid"))

    elif len(script_filenames) == 2:
        print(script_filenames[0])
        time_file_1 = measure_execution_time(
            script_filenames[0], args.mode, time_unit, num_runs, args.silent
        )
        print(script_filenames[1])
        time_file_2 = measure_execution_time(
            script_filenames[1], args.mode, time_unit, num_runs, args.silent
        )
        percentage_difference = ((time_file_2 - time_file_1) / time_file_1) * 100

        if percentage_difference > 2:
            print(
                "{} is {:.2f}% faster than {}".format(
                    script_filenames[0], abs(percentage_difference), script_filenames[1]
                )
            )
        elif percentage_difference < -2:
            print(
                "{} is {:.2f}% slower than {}".format(
                    script_filenames[0], abs(percentage_difference), script_filenames[1]
                )
            )
        else:
            print(
                "{} and {} have almost the same execution time.".format(
                    script_filenames[0], script_filenames[1]
                )
            )

    else:
        measure_execution_time(
            script_filenames[0], args.mode, time_unit, num_runs, args.silent
        )


def main():
    parser = argparse.ArgumentParser(description="Measure script execution times.")
    parser.add_argument("scripts", nargs="+", help="Script filename(s) or folder(s)")
    parser.add_argument(
        "-u", "--unit", default="ms", choices=["ms", "s"], help="Time unit"
    )
    parser.add_argument("-n", "--number", type=int, default=1, help="Number of runs")
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Run script silently"
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["single", "multi"],
        default="single",
        help="Execution mode",
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Display script version"
    )
    args = parser.parse_args()

    if not args.scripts or args.scripts[0] in ("-H", "--help"):
        display_help()

    if args.version:
        print(f"Version: {SCRIPT_VERSION}")
        sys.exit(0)

    script_filenames = gather_script_filenames(args.scripts)
    display_results(script_filenames, args.unit, args.number, args)


if __name__ == "__main__":
    main()
