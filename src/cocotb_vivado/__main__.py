#!/usr/bin/env python3

import sys
import importlib
import traceback
import os

sys.modules["cocotb.simulator"] = importlib.import_module("cocotb_vivado.stub.simulator")

import cocotb

from .stub.mgr import Mgr

from sys import argv

def _initialize_simulator(argv_,xsim_design):
    mgr = Mgr.init(xsim_design)

    cocotb._initialise_testbench([])

    mgr.run()

    mgr.close()

    if cocotb.regression_manager.failures:
        exit(1)
    

def run(module, xsim_design, top_level_lang):
    if top_level_lang != "verilog":
        raise Exception("Only verilog supported as top level languge")

    os.environ["MODULE"] = module
    _initialize_simulator([],xsim_design)
    


if __name__ == "__main__":
    snapshot_name = os.getenv("VIVADO_SNAPSHOT_NAME")
    
    design_so_file = "xsim.dir/{snapshot_name}/xsimk.so".format(snapshot_name=snapshot_name)
    
    _initialize_simulator(argv,design_so_file)
