import program as prog
import experiment as exp
import sys
from pathlib import Path

def main():
    sys.path.insert(0, str(Path(__file__).parent / "libpointing/bindings/Python/cython"))

    program = prog.Program()
    program.run()

if __name__ == "__main__":
    main()