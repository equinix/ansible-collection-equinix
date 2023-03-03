#!/bin/bash

DPATH="${DOCS_PATH:="docs"}"

for f in plugins/modules/*.py
do
  echo $f
  MODULE_NAME="$(basename "$f" .py)"
  PYTHONWARNINGS="ignore" ansible-specdoc -i "$f" -f jinja2 -t template/module.md.j2 -o $DPATH/modules/"$MODULE_NAME".md;
done

for f in plugins/inventory/*.py
do
  echo $f
  MODULE_NAME="$(basename "$f" .py)"
  PYTHONWARNINGS="ignore" ansible-specdoc -i "$f" -f jinja2 -t template/module.md.j2 -o $DPATH/inventory/"$MODULE_NAME".md;
done
