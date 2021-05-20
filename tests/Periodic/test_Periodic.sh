echo "Running test for Periodic Models:";
for FILE in `ls *.py`; do echo -e $FILE; python3 $FILE; done

