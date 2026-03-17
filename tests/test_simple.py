import subprocess
import os
import pathlib
import shutil

import cocotb_vivado
import cocotb
from cocotb.triggers import Timer

import pytest

from pathlib import Path
from cocotb_vivado.runner import get_runner
    
@cocotb.test()
async def simple_test(dut):
    dut.clk.value = 0
    await Timer(10, units="ns")
    assert dut.out.value == 0
    dut.clk.value = 1
    await Timer(10, units="ns")
    assert dut.out.value == 1

@pytest.mark.skipif(
    not os.getenv("COCOTB_VIVADO_TEST_DIRECT"),
    reason="Deprecated launching method. Specify COCOTB_VIVADO_TEST_DIRECT=1 to run test anyway."
    "Additionally, make sure you first update the LD_LIBRARY_PATH; see README.md for details"
)
def test_simple_directlaunch():
    src_path = pathlib.Path(__file__).parent.absolute()

    shutil.rmtree("xsim.dir", ignore_errors=True)

    if not os.path.exists("xsim.dir/work.tb/xsimk.so"):
        subprocess.run(["xvlog", src_path / "tb.v"])
        subprocess.run(["xelab", "work.tb", "-dll"])

    cocotb_vivado.run(module="test_simple", xsim_design="xsim.dir/work.tb/xsimk.so", top_level_lang="verilog")

def test_simple():
    """
    Launch test using the Python runner format.
    """
    tb_name = "test_simple"

    proj_path = Path(__file__).resolve().parent
    sources = [proj_path / "tb.v"]

    sim = os.getenv("SIM","vivado")
    hdl_toplevel_lang = "verilog"
    toplevel = "tb"

    runner = get_runner(sim)

    runner.build(
        sources=sources,
        hdl_toplevel=toplevel,
        always=True,
        timescale = ('1ns','1ps'),
        parameters={},
        waves=False)
    runner.test(
        hdl_toplevel=toplevel,
        test_module=tb_name,
        hdl_toplevel_lang=hdl_toplevel_lang,
        waves=False)


if __name__ == "__main__":
    test_simple()
