//xfail:BOOGIE_ERROR
//--local_size=1024 --num_groups=1024
//[\s]*kernel.cl:[\s]+error:[\s]+possible read-write race on \(\(char\*\)a\)\[32]
//kernel.cl:13:5:[\s]+write by thread[\s]+\(8, 0, 0\)[\s]+group[\s]+\([\d]+, 0, 0\)[\s]+a\[get_local_id\(0\)] = get_local_id\(0\);
//kernel.cl:11:3:[\s]+read by thread[\s]+\([\d]+, 0, 0\)[\s]+group[\s]+\([\d]+, 0, 0\)[\s]+b\[get_local_id\(0\)] = a\[8];



__kernel void foo(__local int* a, __local int* b) {

  b[get_local_id(0)] = a[8];
  
  a[get_local_id(0)] = get_local_id(0);
  
}