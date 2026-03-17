import cocotb_vivado
import subprocess
import os
import pathlib
import shutil

import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock

from cocotbext.axi import AxiLiteBus, AxiLiteMaster, AxiLiteRam

from cocotb_vivado.runner import get_runner
import pytest

@cocotb.test()
async def cocotb_axil_test(dut):

    clk = Clock(dut.clk, 200, units="ns")
    cocotb.start_soon(clk.start())

    dut.rst.value = 1
    await Timer(500, "ns")
    dut.rst.value = 0

    axil_master = AxiLiteMaster(AxiLiteBus.from_prefix(dut, "axil"), dut.clk, dut.rst)
    axil_ram = AxiLiteRam(AxiLiteBus.from_prefix(dut, "axil"), dut.clk, dut.rst, size=2**16)

    data_in = list(range(16))

    await axil_master.write(0, data_in)

    data_out = []
    data_out = list((await axil_master.read(12, 4)).data) + data_out
    data_out = list((await axil_master.read(8, 4)).data) + data_out
    data_out = list((await axil_master.read(4, 4)).data) + data_out
    data_out = list((await axil_master.read(0, 4)).data) + data_out

    assert data_in == data_out


def test_axil():
    src_path = pathlib.Path(__file__).parent.absolute()

    sources = [ src_path / "test_axil.v" ]
    
    hdl_toplevel_lang = "verilog"
    sim = os.getenv("SIM","vivado")
    toplevel = "test_axil"
    runner = get_runner(sim)
    tb_name = "test_axil"

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

@pytest.mark.skipif(
    not os.getenv("COCOTB_VIVADO_TEST_DIRECT"),
    reason="Deprecated launching method. Specify COCOTB_VIVADO_TEST_DIRECT=1 to run test anyway."
    "Additionally, make sure you first update the LD_LIBRARY_PATH; see README.md for details"
)
def test_axil_directlaunch():
    src_path = pathlib.Path(__file__).parent.absolute()
    if not os.path.exists("xsim.dir/work.test_axil/xsimk.so"):
        subprocess.run(["xvlog", src_path / "test_axil.v"])
        subprocess.run(["xelab", "work.test_axil", "-dll"])

    cocotb_vivado.run(module="test_axil", xsim_design="xsim.dir/work.test_axil/xsimk.so", top_level_lang="verilog")

    
if __name__ == "__main__":
    test_axil()
