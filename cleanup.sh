#!/bin/bash

docker stop asperathos-integration-tests_tests_1
docker rm -v asperathos-integration-tests_tests_1
docker rm -v asperathos-integration-tests_docker_1
docker network rm asperathos-integration-tests_default
docker volume rm d54-data
docker volume rm organon-data
docker image rm asperathos-integration-tests_tests

