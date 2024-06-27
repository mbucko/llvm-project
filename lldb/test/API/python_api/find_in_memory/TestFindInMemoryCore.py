"""
Test Process::FindInMemory.
"""

import lldb
from lldbsuite.test.lldbtest import *
from lldbsuite.test.decorators import *
from lldbsuite.test import lldbutil
from address_ranges_helper import *


class FindInMemoryTestCase(TestBase):
    NO_DEBUG_INFO_TESTCASE = True

    @skipUnlessArch("x86_64")
    @skipUnlessPlatform(["linux"])
    def test_find_in_memory_core_heap_ok(self):
        """
        Make sure a match exists in the core's heap memory and the right address ranges are provided.
        """
        self.build()
        (
            self.target,
            self.process,
            self.thread,
            self.bp,
        ) = lldbutil.run_to_source_breakpoint(
            self, "break here", lldb.SBFileSpec("main.cpp")
        )
        self.assertTrue(self.bp.IsValid())

        core_path = self.getBuildArtifact("find_in_memory.core")
        save_core_command = (
            "process save-core --plugin-name=minidump --style=full '%s'" % (core_path)
        )

        self.runCmd(save_core_command)
        self.assertTrue(os.path.isfile(core_path))

        self.target = self.dbg.CreateTarget(None)
        self.process = self.target.LoadCore(core_path)
        self.thread = self.process.GetSelectedThread()

        self.assertTrue(self.process, PROCESS_IS_VALID)
        self.assertTrue(self.process.GetProcessInfo().IsValid())

        error = lldb.SBError()
        addr = self.process.FindInMemory(
            DOUBLE_INSTANCE_PATTERN_HEAP,
            GetHeapRanges(self)[0],
            1,
            error,
        )
        self.assertSuccess(error)
        self.assertNotEqual(addr, lldb.LLDB_INVALID_ADDRESS)

    @skipUnlessArch("x86_64")
    @skipUnlessPlatform(["linux"])
    def test_find_in_memory_core_stack_ok(self):
        """
        Make sure a match exists in the core's heap memory and the right address ranges are provided.
        """
        self.build()
        (
            self.target,
            self.process,
            self.thread,
            self.bp,
        ) = lldbutil.run_to_source_breakpoint(
            self, "break here", lldb.SBFileSpec("main.cpp")
        )
        self.assertTrue(self.bp.IsValid())

        # saved_core_path = "/home/mbucko/local/find_in_memory_small.core"
        # saved_a_out = "/home/mbucko/local/a.out"
        core_path = self.getBuildArtifact("find_in_memory.core")
        exe_path = self.getBuildArtifact("a.out")
        save_core_command = (
            "process save-core --plugin-name=minidump --style=full '%s'" % (core_path)
        )

        self.runCmd(save_core_command)
        self.assertTrue(os.path.isfile(core_path))
        # import shutil
        # shutil.copyfile(core_path, saved_core_path)
        # shutil.copyfile(exe_path, saved_a_out)

        self.target = self.dbg.CreateTarget(exe_path)
        self.process = self.target.LoadCore(core_path)
        self.thread = self.process.GetSelectedThread()

        self.assertTrue(self.process, PROCESS_IS_VALID)
        self.assertTrue(self.process.GetProcessInfo().IsValid())

        error = lldb.SBError()
        addr = self.process.FindInMemory(
            SINGLE_INSTANCE_PATTERN_STACK,
            GetStackRange(self),
            1,
            error,
        )
        self.assertSuccess(error)
        self.assertNotEqual(addr, lldb.LLDB_INVALID_ADDRESS)

    @skipUnlessArch("x86_64")
    @skipUnlessPlatform(["linux"])
    def test_find_ranges_in_memory_core_heap_ok(self):
        """
        Make sure a match exists in the core's heap memory and the right address ranges are provided.
        """
        self.build()
        (
            self.target,
            self.process,
            self.thread,
            self.bp,
        ) = lldbutil.run_to_source_breakpoint(
            self, "break here", lldb.SBFileSpec("main.cpp")
        )
        self.assertTrue(self.bp.IsValid())

        core_path = self.getBuildArtifact("find_in_memory.core")
        save_core_command = (
            "process save-core --plugin-name=minidump --style=full '%s'" % (core_path)
        )

        self.runCmd(save_core_command)
        self.assertTrue(os.path.isfile(core_path))

        self.target = self.dbg.CreateTarget(None)
        self.process = self.target.LoadCore(core_path)
        self.thread = self.process.GetSelectedThread()

        self.assertTrue(self.process, PROCESS_IS_VALID)
        self.assertTrue(self.process.GetProcessInfo().IsValid())

        error = lldb.SBError()
        matches = self.process.FindRangesInMemory(
            DOUBLE_INSTANCE_PATTERN_HEAP,
            GetHeapRanges(self),
            1,
            10,
            error,
        )

        self.assertSuccess(error)
        self.assertEqual(matches.GetSize(), 2)

    @skipUnlessArch("x86_64")
    @skipUnlessPlatform(["linux"])
    def test_find_ranges_in_memory_core_stack_ok(self):
        """
        Make sure a match exists in the core's heap memory and the right address ranges are provided.
        """
        self.build()
        (
            self.target,
            self.process,
            self.thread,
            self.bp,
        ) = lldbutil.run_to_source_breakpoint(
            self, "break here", lldb.SBFileSpec("main.cpp")
        )
        self.assertTrue(self.bp.IsValid())

        core_path = self.getBuildArtifact("find_in_memory.core")
        save_core_command = (
            "process save-core --plugin-name=minidump --style=full '%s'" % (core_path)
        )

        self.runCmd(save_core_command)
        self.assertTrue(os.path.isfile(core_path))

        self.target = self.dbg.CreateTarget(None)
        self.process = self.target.LoadCore(core_path)
        self.thread = self.process.GetSelectedThread()

        self.assertTrue(self.process, PROCESS_IS_VALID)
        self.assertTrue(self.process.GetProcessInfo().IsValid())

        error = lldb.SBError()
        matches = self.process.FindRangesInMemory(
            SINGLE_INSTANCE_PATTERN_STACK,
            GetStackRanges(self),
            1,
            10,
            error,
        )

        self.assertSuccess(error)
        self.assertEqual(matches.GetSize(), 1)
