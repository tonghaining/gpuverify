//pass
//--blockDim=64 --gridDim=64

#include "cuda.h"

__global__ void foo() {

  int x = 1;

  x = !x;

}
