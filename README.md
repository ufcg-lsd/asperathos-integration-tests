# Asperathos Integration Tests
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Overview

This repository contains integration tests of internal and external components in the asperathos framework.

## Running

First, you need to have Docker and Docker Compose installed in your OS.
Next, if not already, you have to set the KUBECONFIG env var to the cluster you want to run tests on:

```bash
$ export KUBECONFIG=/path/to/your/.kube/config
```

Finally, run the integration tests with docker-compose:

```bash
$ docker-compose up
```
