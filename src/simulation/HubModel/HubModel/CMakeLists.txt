# CMakeList.txt : CMake project for HubModel, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)

# Add source to this project's executable.
add_executable (HubModel "RadialMain.cpp"  "GenRand.h" "GenRand.cpp" "Person.h" "Person.cpp" "Hub.h" "Hub.cpp" "StrongInfect.h" "StrongInfect.cpp")

# TODO: Add tests and install targets if needed.
