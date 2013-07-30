#!/bin/bash
dropdb learning_greek
set -e
createdb learning_greek
gondor sqldump primary | python manage.py dbshell
python manage.py upgradedb --execute
set +e
