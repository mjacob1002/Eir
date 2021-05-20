echo "Running test for Deterministic Models:";
for FILE in `ls *.py`; do echo -e $FILE; python3 $FILE; done

