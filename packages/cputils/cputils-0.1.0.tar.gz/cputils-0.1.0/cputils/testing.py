#!/usr/bin/env python3
"""Test a set of problems against their samples"""
import os, sys
from glob import glob
import subprocess
import time

from .config import config


def get_format(folder):
    if config["sample_format"] == "auto":
        if config["source"] in {"kattis", "aceptaelreto"}:
            return "samples-in-ans"
        # TODO: Automatic detection
        if (
            os.path.isdir(os.path.join(folder, "samples"))
            and glob(os.path.join(folder, "samples", "*.in"))
            and glob(os.path.join(folder, "samples", "*.ans"))
        ):
            return "samples-in-ans"
        if (
            os.path.isdir(os.path.join(folder, "inputs"))
            and glob(os.path.join(folder, "inputs", "*"))
            and os.path.isdir(os.path.join(folder, "outputs"))
            and glob(os.path.join(folder, "outputs", "*"))
        ):
            return "inputs-outputs"
        raise NotImplementedError("Unable to detect sample format")
    return config["sample_format"]


def get_inputs(folder):
    sample_format = get_format(folder)
    if sample_format == "samples-in-ans":
        input_pattern = os.path.join("samples", "*.in")
    elif sample_format == "inputs-outputs":
        input_pattern = os.path.join("inputs", "*")
    else:
        raise NotImplementedError("Invalid sample format")

    return sorted(glob(input_pattern, root_dir=folder))


def input_to_output(folder, inp):
    sample_format = get_format(folder)
    if sample_format == "samples-in-ans":
        return inp[:-2] + "ans"
    elif sample_format == "inputs-outputs":
        return os.path.join("outputs", os.path.basename(inp))
    else:
        raise NotImplementedError("Invalid sample format")


supported_extensions = ["py", "c", "cpp", "rs"]


def test_code(code, verbose=False):
    """Test a code, returning a list with either float describing the running time or str describing error(s)"""
    folder = os.path.dirname(os.path.abspath(code))
    code = os.path.basename(code)
    language = code.rsplit(".", 1)[-1].lower()

    tests = get_inputs(folder)

    # Compilation
    if language in {"c", "cpp", "rs"}:
        if language in {"c"}:
            args = ["gcc", code, "-lm", "-o", "a.out"]

        elif language in {"cpp"}:
            args = ["g++", code, "-lm", "-o", "a.out"]
        elif language == "rs":
            args = ["rustc", code, "-o", "a.out"]

        proc = subprocess.Popen(
            args,
            cwd=folder,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        out, err = proc.communicate()
        if proc.returncode:
            return ["CE"] * len(tests)

    times = []
    for test in tests:
        t1 = time.time()
        if language == "py":
            args = ["python", code]
        elif language in {"c", "cpp", "rs"}:
            args = [os.path.join(folder, "a.out")]
        else:
            raise NotImplementedError

        proc = subprocess.Popen(
            args,
            cwd=folder,
            stdin=open(os.path.join(folder, test), "r"),
            stdout=subprocess.PIPE,
            shell=False,
        )

        try:
            out, err = proc.communicate(timeout=config["timeout"])
            t2 = time.time()
            times.append(t2 - t1)
            if proc.returncode != 0:
                times[-1] = f"IR({proc.returncode})"
                continue
            out = out.decode()
            reference = open(os.path.join(folder, input_to_output(folder, test))).read()
            if (
                out.strip() == reference.strip()
            ):  # Allow for differences in trailing or heading new lines
                if verbose:
                    print(".", end="")
            else:
                times[-1] = "WA"
                if verbose:
                    print(
                        "\nError in test %s. Expected output:\n%s\nCurrent output:\n%s"
                        % (test, reference, out),
                        file=sys.stderr,
                    )

        except subprocess.TimeoutExpired:
            times.append("TLE(>%g)" % config["timeout"])
            proc.kill()

    return times


def main():
    if len(sys.argv) < 2:
        name = os.path.basename(sys.argv[0])
        print(
            "Usage:\n%s file(s): test the given files\n"
            "%s folder: test every supported file in the folder" % (name, name)
        )
    else:
        files = sys.argv[1:]
        if len(files) == 1 and os.path.isdir(files[0]):
            d = files[0]
            files = []
            for ext in supported_extensions:
                files.extend(glob(os.path.join(d, "*." + ext)))
        for code in files:
            times = test_code(code)

            print(os.path.basename(code), end=", ")
            print(
                ", ".join("%.3f" % t if isinstance(t, float) else str(t) for t in times)
            )


if __name__ == "__main__":
    main()
