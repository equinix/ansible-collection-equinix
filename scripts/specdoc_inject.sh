#!/bin/bash

DPATH="${DOCS_PATH:="docs"}"

for f in plugins/modules/*.py
do
  echo $f
  PYTHONWARNINGS="ignore" ansible-specdoc -j -i "$f";
done

for f in plugins/inventory/*.py
do
  echo $f
  PYTHONWARNINGS="ignore" ansible-specdoc -j -i "$f";
done
