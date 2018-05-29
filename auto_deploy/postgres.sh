echo "
---> Switched to postgres user shell. Initiating database.
"

if [ ! -d "/var/lib/postgres/data" ]; then
    initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data'
fi
