import sys
import logging


def add(input_list):
    result = 0
    for i in input_list:
        result = result + int(i)
    return result


def main():
    input_list = sys.argv[1:]
    logging.info("input: %s", input_list)
    result = add(input_list)
    logging.warning("result: %d", result)


if __name__ == "__main__":
    main()
