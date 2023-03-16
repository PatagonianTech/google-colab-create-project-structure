#!/usr/bin/env bash

(
  _err() {
    echo "$@" 1>&2
    exit 1
  }

  if [ -f mod_cfs.py ]; then
    # Already installed?
    if [ ! -d google-colab-create-project-structure ]; then
      # Source folder not found
      _err "'google-colab-create-project-structure' not found"
    fi
  else
    # Not installed
    if [ -d google-colab-create-project-structure ]; then
      # Go to source folder
      cd google-colab-create-project-structure
    else
      # Source folder not found
      _err "'google-colab-create-project-structure' not found"
    fi
  fi

  cd ..
  ln -vfs google-colab-create-project-structure/src src
  ln -vfs google-colab-create-project-structure/mod_cfs.py mod_cfs.py
)
