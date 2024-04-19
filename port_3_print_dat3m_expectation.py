import os
import subprocess

SPV_DISASSEMBLY_FOLDER = "./testsuite/spv-dis/"
FILE_MAP_TXT = "./file_map.txt"
VERIFY_RESULT_TXT = "./verify_result.txt"


PASS = "PASS"
FAIL = "FAIL"
RACE = "RACE"
ABORT = "ABORT"


UN_SUPPORTED_TOKEN = ["|"]


def check_support(test):
    with open(test, "r") as f:
        for line in f:
            if any(token in line for token in UN_SUPPORTED_TOKEN):
                return False
    return True


def read_verify_result():
    verify_result = {}
    with open(VERIFY_RESULT_TXT, "r") as f:
        for line in f:
            test, result = line.split()
            verify_result[test] = result
    return verify_result


def dat3m_print(test_path, result, support):
    test_path = test_path.replace(SPV_DISASSEMBLY_FOLDER, "")
    if support:
        print(f"{{\"gpu-verify-auto/{test_path}\", 1, {result}}},")
    else:
        print(f"// {{\"gpu-verify-auto/{test_path}\", 1, {result}}},")


def print_safety_result(verify_result):
    for test in verify_result:
        support = check_support(test)
        if verify_result[test] == PASS:
            dat3m_print(test, PASS, support)
        if verify_result[test] == FAIL:
            dat3m_print(test, FAIL, support)


def print_race_result(verify_result):
    for test in verify_result:
        support = check_support(test)
        if verify_result[test] == PASS:
            dat3m_print(test, PASS, support)
        if verify_result[test] == RACE:
            dat3m_print(test, FAIL, support)


def main():
    verify_result = read_verify_result()
    print_safety_result(verify_result)
    print_race_result(verify_result)


if __name__ == "__main__":
    main()
