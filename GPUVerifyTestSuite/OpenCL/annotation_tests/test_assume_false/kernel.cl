//pass
//--local_size=64 --num_groups=64


__kernel void foo()
{
  __assume(false);
  __assert(false);
}