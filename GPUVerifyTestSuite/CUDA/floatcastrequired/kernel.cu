//pass
//--blockDim=64 --gridDim=64

#include "cuda.h"

__global__ void foo() {

  float x = __exp10f(2);

}
