cmake_minimum_required(VERSION 3.10)
project(HPCParser)

set(CMAKE_CXX_STANDARD 17)

# Find OpenMP
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    link_libraries(OpenMP::OpenMP_CXX)
endif()

# Find HDF5 (Optional for this scaffold, but good to have)
# find_package(HDF5 COMPONENTS CXX)
# if(HDF5_FOUND)
#     include_directories(${HDF5_INCLUDE_DIRS})
#     link_libraries(${HDF5_LIBRARIES})
# endif()

include_directories(include)

add_executable(hpc_parser src/engine.cpp)
