//pass
//--blockDim=64 --gridDim=64

#include "cuda.h"

__device__ void f(int x) {

}

__global__ void foo() {

  f(2);

}
