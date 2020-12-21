import os
import subprocess
import tempfile
import uuid

from IPython.core.magic import Magics, cell_magic, magics_class
from common import helper

DEFAULT_COMPILER = '/usr/local/cuda/bin/nvcc'
ext = '.cu'


@magics_class
class NVCCPlugin(Magics):

    def __init__(self, shell):
        super(NVCCPlugin, self).__init__(shell)

        self.argparser = helper.get_argparser()

    @staticmethod
    def compile(file_path, compiler=DEFAULT_COMPILER):
        print('Using compiler', compiler)
        subprocess.check_output(
            [compiler, file_path + ext, "-o", file_path + ".out", '-O3', '-Wno-deprecated-gpu-targets', '-std=c++14'], stderr=subprocess.STDOUT)

    def run(self, file_path, timeit=False):
        if timeit:
            stmt = f"subprocess.check_output(['{file_path}.out'], stderr=subprocess.STDOUT)"
            output = self.shell.run_cell_magic(
                magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output(
                [file_path + ".out"], stderr=subprocess.STDOUT)
            output = output.decode('utf8')
            
        helper.print_out(output)
        return None

    @cell_magic
    def cu(self, line, cell):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
            with open(file_path + ext, "w") as f:
                f.write(cell)
            try:
                self.compile(file_path, compiler=(args.compiler if args.compiler else DEFAULT_COMPILER))
                output = self.run(file_path, timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                helper.print_out(e.output.decode("utf8"))
                output = None
        return output
