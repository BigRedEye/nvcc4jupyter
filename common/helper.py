import argparse


def get_argparser():
    parser = argparse.ArgumentParser(description='NVCCPlugin params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    parser.add_argument("-c", "--compiler", type=str, default=None,
                        help='path to the nvcc compiler')
    return parser


def print_out(out: str):
    for l in out.split('\n'):
        print(l)
