# Changelog

## 5.0.4

* add `cms git versions` printing the versions locally, from github and pypi
* add `cms git status` DIRS printing the status specified dirs
* used a function to implement both `cms git status pull/push`

## 5.0.3

* Update Readme
* Update pyproject.toml
* add `cms	git log`	which creates a very short log


## 5.0.2

* Add `cms git pull cloudmesh-*` to pull all matching directories
* Add `cms git pull .` to pull all matching directories
* Fix `--dryrun`
* remove the recursive `cms git all` method as it litarrly went in all subdirs and is not efficient

## 5.0.1

* Switch to src/
* Switch to pyproject.toml
* Version 4 is no longer supported, switch to version 5