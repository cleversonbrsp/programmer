#!/bin/bash
# Execução dos scripts DDL
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f /path/to/extracted/data/ddl_script.sql

# Execução dos scripts DML
psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f /path/to/extracted/data/dml_script.sql
