#!/bin/bash

SWITCH="-j"

CALLED_NAME=`basename $0`
VERB="injecting generated docs to"

if [ $CALLED_NAME == "specdoc_remove.sh" ]; then
    SWITCH="-jc"
    VERB="removing generated docs from"
fi

DPATH="${DOCS_PATH:="docs"}"

for f in plugins/modules/*.py
do
  echo $VERB $f
  PYTHONWARNINGS="ignore" ansible-specdoc $SWITCH -i "$f";
done
