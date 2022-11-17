#!bin/bash

ITERATOR=30
while [ ${ITERATOR} -ne 0 ]
do
    # START=${SECONDS}
    # python3 app.py
    python3 aws_test_script.py
    ((ITERATOR--))
    # DURATION=$(( SECONDS - START))
    # echo "${DURATION} seconds..."
done

