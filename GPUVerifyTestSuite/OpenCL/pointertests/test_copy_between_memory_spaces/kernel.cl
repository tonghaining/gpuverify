//pass
//--local_size=64 --num_groups=64


__kernel void foo(__global float* A)
{
  __local float B[10];
  int x;

  if(B[0] > 0)
  {
    x = 1;
  }

  barrier(CLK_LOCAL_MEM_FENCE);

  if(A[0] > 0)
  {
    B[0] = A[0];
  }
}

