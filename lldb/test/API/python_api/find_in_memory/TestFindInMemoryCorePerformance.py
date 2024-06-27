"""
Test Process::FindInMemory.
"""

import datetime
import lldb
from lldbsuite.test.lldbtest import *
from lldbsuite.test.decorators import *
from lldbsuite.test import lldbutil
from address_ranges_helper import *



class FindInMemoryTestCase(TestBase):
    NO_DEBUG_INFO_TESTCASE = True
    saved_core_path = "/Users/mbucko/repos/llvm/Debug/bin/aa.out.core"
    saved_exe_path = "/Users/mbucko/repos/llvm/Debug/bin/aa.out"

    def GetAllRanges(self):
        regions = self.process.GetMemoryRegions()
        address_ranges = lldb.SBAddressRangeList()
        total_size = 0
        for i in range(regions.GetSize()):
            region_info = lldb.SBMemoryRegionInfo()

            if not regions.GetMemoryRegionAtIndex(i, region_info):
                continue
            # if not region_info.IsWritable():
                # print(str(i))
                # continue
            # if region_info.IsExecutable():
                # continue
            # if not region_info.IsReadable():
                # continue
            if lldb.SBAddress(region_info.GetRegionBase(), self.target).GetSection():
                continue

            print("MIRO region: " + str(region_info)) 
            address_start = region_info.GetRegionBase()
            size = region_info.GetRegionEnd() - address_start
            if size < 100000000:
                continue
            total_size += size
            # print("MIRO adding region with size: " + str(size / 1024 / 1024) + "MiB")
            address_ranges.Append(lldb.SBAddressRange(
                lldb.SBAddress(address_start, self.target), size
            ))
        print("MIRO Total Regions size: " + str(total_size / 1024 / 1024) + "MiB")
        self.assertTrue(address_ranges.GetSize() > 0)
        return address_ranges

    # def test_find_ranges_in_memory_core_heap_ok(self):
    #     """
    #     Make sure a match exists in the core's heap memory and the right address ranges are provided.
    #     """
    #     print("START: " + str(datetime.datetime.now()))
    #     self.build()
    #     (
    #         self.target,
    #         self.process,
    #         self.thread,
    #         self.bp,
    #     ) = lldbutil.run_to_source_breakpoint(
    #         self, "break here", lldb.SBFileSpec("large_heap.cpp")
    #     )
        
    #     print("BUILD FINISHED: " + str(datetime.datetime.now()))
    #     self.assertTrue(self.bp.IsValid())

    #     core_path = self.getBuildArtifact("find_in_memory.core")
    #     exe_path = self.getBuildArtifact("a.out")
        
    #     save_core_command = (
    #         "process save-core --plugin-name=mach-o --style=full '%s'" % (core_path)
    #     )

    #     self.runCmd(save_core_command)
    #     self.assertTrue(os.path.isfile(core_path))
    #     import shutil
    #     shutil.copyfile(core_path, self.saved_core_path)
    #     shutil.copyfile(exe_path, self.saved_exe_path)
    #     import subprocess
    #     output = subprocess.check_output(["rm", "-rf", "/Users/mbucko/repos/llvm/Debug/bin/aa.out.dSYM"])
    #     print("MIRO output: " + output.decode())
    #     output = subprocess.check_output(["dsymutil", "/Users/mbucko/repos/llvm/Debug/bin/aa.out"])
    #     print("MIRO output: " + output.decode())

    #     # self.target = self.dbg.CreateTarget(None)
    #     self.target = self.dbg.CreateTarget(self.saved_exe_path)
    #     # self.process = self.target.LoadCore(self.saved_core_path)
    #     self.process = self.target.LoadCore(core_path)
    #     dsym_command = (
    #         "target symbols add /Users/mbucko/repos/llvm/Debug/bin/aa.out.dSYM/Contents/Resources/DWARF/aa.out"
    #     )
    #     self.runCmd(dsym_command)

    #     self.assertTrue(self.process, PROCESS_IS_VALID)
    #     self.thread = self.process.GetSelectedThread()
    #     self.assertTrue(self.process.IsValid())

    #     error = lldb.SBError()
    #     print("READY TO SEARCH: " + str(datetime.datetime.now()))
    #     start_time = datetime.datetime.now()

    #     ranges = GetHeapRanges(self)
    #     matches = self.process.FindRangesInMemory(
    #         DOUBLE_INSTANCE_PATTERN_HEAP,
    #         ranges,
    #         8,
    #         10,
    #         error,
    #     )

    #     end_time = datetime.datetime.now()
    #     duration = end_time - start_time
    #     print("MIRO Duration:", duration.total_seconds())
    #     print("DONE SEARCHING: " + str(datetime.datetime.now()))

    #     self.assertSuccess(error)
    #     self.assertEqual(matches.GetSize(), 22)

    def test_find_ranges_in_memory_core_heap_ok(self):
        """
        Make sure a match exists in the core's heap memory and the right address ranges are provided.
        """
        print("START: " + str(datetime.datetime.now()))
        self.target = self.dbg.CreateTarget(self.saved_exe_path)
        self.process = self.target.LoadCore(self.saved_core_path)
        dsym_command = (
            "target symbols add /Users/mbucko/repos/llvm/Debug/bin/aa.out.dSYM/Contents/Resources/DWARF/aa.out"
        )
        self.runCmd(dsym_command)
        self.assertTrue(self.process, PROCESS_IS_VALID)
        self.thread = self.process.GetSelectedThread()
        self.assertTrue(self.process.IsValid())

        error = lldb.SBError()
        print("READY TO SEARCH: " + str(datetime.datetime.now()))
        start_time = datetime.datetime.now()

        # ranges = GetHeapRanges(self)
        ranges = self.GetAllRanges()
        matches = self.process.FindRangesInMemory(
            DOUBLE_INSTANCE_PATTERN_HEAP,
            ranges,
            8,
            100,
            error,
        )
        print("MIRO matches: " + str(matches))
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        print("MIRO Duration:", duration.total_seconds())
        print("DONE SEARCHING: " + str(datetime.datetime.now()))

        self.assertSuccess(error)
        self.assertEqual(matches.GetSize(), 22)
