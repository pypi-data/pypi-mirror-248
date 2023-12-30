---
title: Installation
---
# Installing Docop

- do a pip install
- set up a few directories for tasks, docs and  and pipes
- copy config.yaml.in to config.yaml and specify the directories there
- read the docs on how to [configure docop](config.md), use the [command-line tool](cmdline.md), create [tasks](tasks.md) and [pipes](pipes.md) etc.

There's also a Makefile to automate some tasks.

To create simple directory layout and set up a default `config.yaml` configuration (recommended):

```bash
make setup
```

If you need to build and use the documentation locally:

```bash
make docs
```
