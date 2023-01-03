import subprocess
import sys

import pytest
import regex as regex


def test_version_commnad_gives_description():
    result = subprocess.run(
        [sys.executable, "-m", "k8perf", "--version", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )




    assert "k8perf CLI Version: " in result.stdout

def test_version_includes_all_version_parts():
    result = subprocess.run(
        [sys.executable, "-m", "k8perf", "--version", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )

    # assert that there is a version number in the string
    version_numbers_string = regex.findall(r"\d\.\d\.\d", result.stdout)
    assert len(version_numbers_string) == 1


