# Statistic from git log

## Dependencies

- Install pdm (instruction at https://pdm.fming.dev/)

## Setup Development Environment

1. edit `.pdm.toml` to reference your preferred _Python_ interpreter.
1. edit `python.autoComplete.extraPaths` and `python.analysis.extraPaths` in `.vscode/settings.json` to have to correct _Python_ version (currently, it is `3.8`)
1. ```pdm install```


## Package wheel

```sh
python3 -m pip install --upgrade build
python3 -m build
```

## How to generate the statistic

git log > \<a file>

```python
"""main program."""

from gitlog_stat.statistic import Statistic

Statistic.build(
    "Title of my project",
    [
        "<the file path>",
    ],
)
```

you can include as many file paths as you wish.