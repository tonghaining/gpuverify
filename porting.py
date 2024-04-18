import os
import sys
import subprocess

OPENCL_TESTSUITE_FOLDER = "./testsuite/OpenCL/"
SPV_DISASSEMBLY_FOLDER = "./testsuite/spv-dis/"
CLSPV_PATH = "/home/haintong/Documents/Library/clspv/build/bin/clspv"
SPIRV_DIS_PATH = "/home/haintong/Documents/Library/spirv-tools/bin/spirv-dis"


def get_opencl_tests(directory):
    tests = {}
    for (dirpath, dirnames, filenames) in os.walk(directory):
        if len(filenames) > 0:
            for file in filenames:
                if file.endswith(".cl"):
                    test_name = dirpath.replace(OPENCL_TESTSUITE_FOLDER, "").split("/")[-1]
                    test_path = os.path.join(dirpath, file)
                    test_dir = dirpath.replace(OPENCL_TESTSUITE_FOLDER, "")
                    if test_name in tests:
                        raise ValueError(f"Duplicate test name: {test_name}")
                    tests[test_path] = (test_name, test_dir)
    return tests


def delete_empty_folders(directory):
    for (dirpath, dirnames, filenames) in os.walk(directory, topdown=False):
        if len(filenames) == 0 and len(dirnames) == 0:
            os.rmdir(dirpath)


def compile_with_clspv(input_file, output_file):
    try:
        command = [CLSPV_PATH, input_file, "--cl-std=CL2.0", "--inline-entry-points", "--spv-version=1.6", "-o",
                   output_file]
        print(f"Running {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Failed to compile {input_file}: {result.stdout}")
            return 1
        return 0
    except Exception as e:
        print(f"Met error while compiling {input_file}: {e}")
        return 1


def disassemble_with_spirv_dis(input_file, output_file):
    try:
        command = [SPIRV_DIS_PATH, input_file, "-o", output_file]
        print(f"Running: {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Failed to disassemble {input_file}: {result.stdout}")
            return 1
        return 0
    except Exception as e:
        print(f"Met error while disassembling {input_file}: {e}")
        return 1


def main():
    tests = get_opencl_tests(OPENCL_TESTSUITE_FOLDER)
    fail_count = 0
    for test in tests:
        test_name, test_dir = tests[test]
        base_dir = os.path.join(SPV_DISASSEMBLY_FOLDER, test_dir)
        os.makedirs(base_dir, exist_ok=True)
        spv_file = os.path.join(base_dir, test_name + ".spv")
        dis_assembly_file = os.path.join(base_dir, test_name + ".spv.dis")
        compile_res = compile_with_clspv(test, spv_file)
        fail_count += compile_res
        if compile_res != 0:
            continue
        print(f"Compiled {test} to {spv_file}")
        fail_count += disassemble_with_spirv_dis(spv_file, dis_assembly_file)
        print(f"Disassembled {spv_file} to {dis_assembly_file}")
        subprocess.run(["rm", spv_file])
    # delete_empty_folders(SPV_DISASSEMBLY_FOLDER)
    print(f"Failed porting {fail_count} tests out of {len(tests)} tests")


if __name__ == "__main__":
    main()
