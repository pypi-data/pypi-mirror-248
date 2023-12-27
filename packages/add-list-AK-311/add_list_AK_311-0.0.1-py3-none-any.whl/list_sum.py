import sys
import logging


def add(input_list):
    result = 0
    for i in input_list:
        result = result + int(i)
    return result


def main():
    input = sys.argv
    input.pop(0)
    logging.info("input: ", input)
    result = add(input)
    logging.info("result:", result)
    print(result)


if __name__ == "__main__":
    main()

