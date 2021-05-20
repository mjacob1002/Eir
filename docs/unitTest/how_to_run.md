In order to run each test, after forking the repository, go to each of the python file for each of the tests and run the following in the shell:

```shell

python3 <NAME_OF_FILE>
```

For example, if I wanted to run the test for the HubSEIRSV model, the following command would be run:

```shell

python3 test_HubSEIR.py

```
Additionally, the shell files in each subdirectory(Deterministic, Hub, Periodic). For example, to run all of the periodic model tests from the tests/Periodic/ directory:

```shell

./test_Periodic.sh
```

In order to test every test for every model type, run the following from the tests/ directory:
```shell
./all_tests.sh
```
