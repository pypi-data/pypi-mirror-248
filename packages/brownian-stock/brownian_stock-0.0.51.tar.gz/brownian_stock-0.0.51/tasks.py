import io
import re

from invoke import context, task


@task
def lint(cx: context) -> None:
    cx.run("pysen run lint")


@task
def format(cx: context) -> None:
    cx.run("pysen run format")


@task
def test(cx: context) -> None:
    cx.run('pytest -m "not e2e"', pty=True)


@task
def nextversion(cx: context) -> None:
    stdout = io.StringIO()
    result = cx.run("GIT_TERMINAL_PROMPT=0 git tag -l", out_stream=stdout)
    if result.return_code != 0:
        raise RuntimeError("git tag didn't complete successfully.")
    tags = result.stdout.split("\n")

    version_pattern = re.compile(r"(\d+)\.(\d+)\.(\d+)")
    version_list = []
    for tag in tags:
        m = version_pattern.match(tag)
        if m is None:
            continue
        v1 = int(m.group(1))
        v2 = int(m.group(2))
        v3 = int(m.group(3))
        version_list.append((v1, v2, v3))
    if len(version_list) == 0:
        raise RuntimeError("No valid tags.")
    latest_tag = sorted(version_list, reverse=True)[0]

    next_version = (latest_tag[0], latest_tag[1], latest_tag[2] + 1)
    next_version_str = ".".join([str(i) for i in next_version])
    print(next_version_str)


@task
def clean(cx: context) -> None:
    cx.run("rm -rf .mypy_cache")
    cx.run("rm -rf .pytest_cache")
    cx.run("rm -rf brownian_stock.egg-info")
    cx.run("rm -rf tmp")
    cx.run("rm -rf build")
    cx.run("rm -rf dist")
