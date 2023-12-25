from cputils import testing
from cputils.config import config
from cputils.common import ensure_dir_exists


import os
import tempfile
import shutil


original_cwd = os.getcwd()

py_successor = "print(int(input())+1)"

c_successor = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+1);return 0;}"""

cpp_successor = r"""
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << n + 1 << endl;
    return 0;
}
"""

rs_successor = r"""
use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read line");
    let n: i32 = input.trim().parse().expect("Invalid input");
    println!("{}", n + 1);
}
"""


successor_codes = {
    "py": py_successor,
    "c": c_successor,
    "cpp": cpp_successor,
    "rs": rs_successor,
}


c_successor_WA = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+2);return 0;}"""

c_successor_IR = r"""
#include <stdio.h>
int main(){int n;scanf("%d",&n);printf("%d",n+1);return 1;}"""

sleep_python = "import time;time.sleep(100)"

def test_testing_success():
    config.config["sample_format"] = "inputs-outputs"
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_")

        os.chdir(temp_dir)

        ensure_dir_exists("inputs")
        ensure_dir_exists("outputs")

        with open("inputs/1.txt", "w") as file:
            file.write("1")
        with open("outputs/1.txt", "w") as file:
            file.write("2")

        for lang, code in successor_codes.items():
            with open(f"code.{lang}", "w") as file:
                file.write(code)

            times = testing.test_code(f"code.{lang}")
            assert len(times) == 1 and isinstance(times[0], float)

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def test_testing_errors():
    config.config["sample_format"] = "inputs-outputs"
    config.config["timeout"] = 1
    try:
        temp_dir = tempfile.mkdtemp(prefix="cputils_test_")

        os.chdir(temp_dir)

        ensure_dir_exists("inputs")
        ensure_dir_exists("outputs")

        with open("inputs/1.txt", "w") as file:
            file.write("1")
        with open("outputs/1.txt", "w") as file:
            file.write("2")

        
        with open("code_WA.c", "w") as file:
            file.write(c_successor_WA)

        times = testing.test_code("code_WA.c")
        assert len(times) == 1 and times[0]=="WA"

        with open("code_IR.c", "w") as file:
            file.write(c_successor_IR)

        times = testing.test_code("code_IR.c")
        assert len(times) == 1 and times[0]=="IR(1)"

        with open("code_TLE.py", "w") as file:
            file.write(sleep_python)

        times = testing.test_code("code_TLE.py")
        assert len(times) == 1 and times[0]=="TLE(>1)"

    finally:
        os.chdir(original_cwd)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)