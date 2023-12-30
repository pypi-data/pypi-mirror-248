---
title: Configuration settings
---
# Docop configuration

Configuration is given in the `config.yaml` file. Alternatively, another file may be given by using the `docop --config` option.

## Directories

The directories section specifies where docop will look up for pipelines (specified as `.yaml` files), Python task modules (`.py`) and documents that have been created by tasks.

Directories are relative to the current directory where docop is being run from.

``` yaml
--8<-- "./docs/example-config.yaml:dirs"
```

## Sources to fetch

``` yaml
--8<-- "./docs/example-config.yaml:sources"
```

## Export targets

Beyond mandating a `targets` section containing names of export targets, docop does not have any conventions for specifying target information. Any extra content can be given, including data used for authentication.

``` yaml
--8<-- "./docs/example-config.yaml:targets"
```

## Authentication

Often, when retrieving, processing or exporting content, some third party system needs to be authenticated with.

Authentication account information to be used can be given in the configuration or pipe definition in the `accounts` section. If not given and the `--account` command-line option is given, account information present in any sources and targets having the same name are used. 

This behavior can be disabled; see below.

## Additional options

Additional options are given in their own `options` section in the config file.

``` yaml
--8<-- "./docs/example-config.yaml:options"
```

The available options are:

- `no implicit account` - when given, accounts are not looked up in sources and targets, just explicitly in the accounts section only
