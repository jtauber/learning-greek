dropdb -h localhost learning_greek; createdb -h localhost learning_greek && gondor sqldump primary | ./manage.py dbshell && ./manage.py syncdb --noinput
