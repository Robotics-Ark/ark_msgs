import sys
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop

PKG_PROTO_ROOT = Path("proto")


def compile_protos() -> None:
    protos = sorted(PKG_PROTO_ROOT.rglob("*.proto"))
    if not protos:
        return

    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        # IMPORTANT:
        # Use src as python_out so generated modules keep correct package imports,
        # e.g. `from ark_msgs._generated import translation_pb2 ...`
        f"-I{PKG_PROTO_ROOT}",
        f"--python_out=src",
        # If this fails on your machine with protoc-gen-pyi missing, delete this line.
        f"--pyi_out=src",
        *[str(p) for p in protos],
    ]
    subprocess.check_call(cmd)


class build_py(_build_py):
    def run(self):
        compile_protos()
        super().run()


class develop(_develop):
    def run(self):
        compile_protos()
        super().run()


setup(
    cmdclass={"build_py": build_py, "develop": develop},
)
