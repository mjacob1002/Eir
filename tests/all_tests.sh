echo "Running all tests available";

# run the tests
for d in */; do
    echo $d
    cd $d
    for e in *.sh; do
	echo $e;
	./$e;
    done
    cd ..
done
