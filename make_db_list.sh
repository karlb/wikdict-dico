#!/bin/bash
# Generate a list of dbs for inclusion via dico's `#include` command
#
# Example dicod.conf:
#
# load-module python {
#   command "python"
#         " init-script=wikdict-dico"
#         " load-path=/home/karl/wikdict-dico"
#         " root-class=DicoModule";
# }
#
# #include /home/karl/wikdict-dico/dico-dbs.list
#

sqlite3 ~/wikdict-prod/data/dict/wikdict.sqlite3 << EOF > dico-dbs.list
.headers off
.mode list
SELECT 'database { name "' || from_lang || '-' || to_lang || '"; handler "python ' || from_lang || ' ' || to_lang || ' /home/karl/wikdict-prod/data/dict/' || from_lang || '-' || to_lang || '.sqlite3"; }' FROM lang_pair WHERE translations >= 1000
EOF

