from glob import glob
from subprocess import check_output, STDOUT


for script in glob("create_*.sql"):
    
    print(check_output(
        "psql -f {}".format(script),
        stderr=STDOUT,
        shell=True)
    .strip())
