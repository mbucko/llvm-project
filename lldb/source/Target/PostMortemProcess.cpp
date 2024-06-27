//===-- PostMortemProcess.cpp -----------------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#include "lldb/Target/PostMortemProcess.h"

#include "lldb/Utility/LLDBLog.h"

#include <iostream>

using namespace lldb;
using namespace lldb_private;

lldb::addr_t PostMortemProcess::FindInMemory(lldb::addr_t low,
                                             lldb::addr_t high,
                                             const uint8_t *buf, size_t size) {
  const size_t region_size = high - low;
  if (region_size < size)
    return LLDB_INVALID_ADDRESS;
  static uint64_t total_search_space = 0;

  // PeekMemory
  size_t mem_size = 0;
  const uint8_t *data = PeekMemory(low, high, mem_size);
  if (data == nullptr || mem_size != region_size) {
    LLDB_LOG(GetLog(LLDBLog::Process),
             "Failed to get contiguous memory region for search. low: 0x{}, "
             "high: 0x{}. Failling back to Process::FindInMemory",
             low, high);
    // In an edge case when the search has to happen across non-contiguous
    // memory, we will have to fall back on the Process::FindInMemory.
    // return this->Process::FindInMemory(low, high, buf, size);
    std::cout << ">>>>> MIRO Failed to get contiguous memory region for search. "
                 "Failling back on Process::FindInMemory "
              << std::hex << low << "-" << high << std::endl;
  total_search_space += region_size;

  std::cout
      << "MIRO actual total search space: " << std::dec
      << (total_search_space / 1024 / 1024) << "MiB" << std::endl;
    return Process::FindInMemory(low, high, buf, size);
    // return LLDB_INVALID_ADDRESS;
  }

  total_search_space += region_size;

  std::cout
      << "MIRO actual total search space: " << std::dec
      << (total_search_space / 1024 / 1024) << "MiB" << std::endl;

  // std::cout
  //     << "MIRO running optimized FindInMemory search on postmortem process"
  //     << std::endl;
  return Process::FindInMemoryGeneric(data, low, high, buf, size);
}
