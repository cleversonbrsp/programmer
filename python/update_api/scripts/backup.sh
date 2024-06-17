#!/bin/bash
# Backup do banco de dados
pg_dump -U $DB_USER -h $DB_HOST -d $DB_NAME -F c -b -v -f backup.bak

# Backup dos arquivos binários
tar -czvf backup_arquivos_website.tar.gz /path/to/website/files/
