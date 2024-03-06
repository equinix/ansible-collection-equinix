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
  MODULE_NAME=`basename $f`
  ANSIBLEDOC_CMD="ansible-doc -M plugins/modules -t module $MODULE_NAME"
  if $ANSIBLEDOC_CMD &> /dev/null; then
      echo "ansible-doc accepts docstrings injected to $MODULE_NAME"
  else
      echo "ansible-doc can't parse docstrings injected to $MODULE_NAME"
      echo "you might need to adjust specdoc values in the module script"
      echo "try:"
      echo "  $ANSIBLEDOC_CMD" 
      exit 1
  fi
done
