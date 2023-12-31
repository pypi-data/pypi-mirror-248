cmake_minimum_required(VERSION 3.18)
set(PROJECT_NAME _prips)
project(${PROJECT_NAME} LANGUAGES CXX CUDA)

set(SOURCES "")
set(INCLUDES "")
set(LIBRARIES "cuda")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE  ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

list(APPEND SOURCES src/main.cu
    src/jit.cuh
    src/common.cu
    src/common.cuh
    src/control.cu
    src/control.cuh
    src/MD_core/MD_core.cu
    src/MD_core/MD_core.cuh
    src/neighbor_list/neighbor_list.cu
    src/neighbor_list/neighbor_list.cuh
    src/collective_variable/collective_variable.cu
    src/collective_variable/collective_variable.cuh)

find_package(CUDAToolkit REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

add_definitions(-DNO_GLOBAL_CONTROLLER)
if (CUDAToolkit_VERSION VERSION_GREATER "11.0")
set(CMAKE_CUDA_ARCHITECTURES 70)
add_definitions(-DCUDA_ARCH_BIN=70)
else()
set(CMAKE_CUDA_ARCHITECTURES 50)
add_definitions(-DCUDA_ARCH_BIN=50)
endif()

add_library(${PROJECT_NAME} SHARED ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME ${PROJECT_NAME} PREFIX "" SUFFIX ".so")
set_target_properties(${PROJECT_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
list(APPEND INCLUDES ${CUDA_INCLUDE_DIRS})
list(APPEND LIBRARIES ${CUDA_LIBRARIES})

list(APPEND INCLUDES ${Python3_INCLUDE_DIRS})
list(APPEND LIBRARIES ${Python3_LIBRARIES})

include_directories(${INCLUDES})
link_directories(${CUDA_TARGET_DIR})
target_link_libraries(${PROJECT_NAME} PUBLIC ${LIBRARIES} CUDA::nvrtc)

install(TARGETS ${PROJECT_NAME}
EXCLUDE_FROM_ALL
COMPONENT python_modules
DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME})
