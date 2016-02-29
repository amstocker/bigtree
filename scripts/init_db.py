from sys import argv
from os import path
from glob import glob
from subprocess import check_output, STDOUT


for script in glob(path.join(argv[1], "create_*.sql")):
    
    print(check_output(
        "psql -f {}".format(script),
        stderr=STDOUT,
        shell=True)
    .strip())
