#!/usr/bin/env python3

from .__main__ import run

# monkey-patch the clock & trigger layer
import cocotb.clock
import cocotb.triggers
from .clock_scheduler import ScheduledClock, RisingEdge, FallingEdge, Edge
cocotb.clock.Clock = ScheduledClock
cocotb.triggers.RisingEdge = clock_scheduler.RisingEdge
cocotb.triggers.FallingEdge = clock_scheduler.FallingEdge
cocotb.triggers.Edge = clock_scheduler.Edge

