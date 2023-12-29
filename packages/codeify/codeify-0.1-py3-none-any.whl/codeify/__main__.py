from .codegen import run_generation
from .types import CodeGeneration
from argparse import ArgumentParser
import sys
import traceback

def _parse_args() -> CodeGeneration:
    parser = ArgumentParser(description='Codeify (code generator)')
    parser.add_argument('-i', '--input', help='input directory', metavar='<dir>', required=True)
    parser.add_argument('-o', '--output', help='output directory', metavar='<dir>', required=True)
    parser.add_argument('-s', '--spec', help='specification file (yaml)', metavar='<spec.yaml>', required=True)

    args = parser.parse_args()
    return CodeGeneration(args.input, args.output, args.spec)

def main() -> int:
    try:
        run_generation(_parse_args())
        return 0
    except Exception as ex:
        print(f"error: {ex}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1
