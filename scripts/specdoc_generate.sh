#!/bin/bash

DPATH="${DOCS_PATH:="docs"}"

for f in plugins/modules/*.py
do
  MODULE_NAME="$(basename "$f" .py)"
  DOCPATH=$DPATH/modules/"$MODULE_NAME".md
  echo generating $DOCPATH
  PYTHONWARNINGS="ignore" ansible-specdoc -i "$f" -f jinja2 -t template/module.md.j2 -o $DOCPATH
done
