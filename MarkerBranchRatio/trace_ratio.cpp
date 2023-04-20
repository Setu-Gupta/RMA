/*
 * Copyright (C) 2004-2021 Intel Corporation.
 * SPDX-License-Identifier: MIT
 */

#include <iostream>
#include <fstream>
#include "pin.H"
#include <map>

using std::cerr;
using std::cout;
using std::endl;
using std::ios;
using std::ofstream;
using std::string;

// Only trace branches if this variable is marked true
BOOL enable_branch_tracing = false;

// Counts of branches and other instructions
UINT64 branches = 0;
UINT64 total = 0;

KNOB<INT64> KnobMagic(KNOB_MODE_WRITEONCE, "pintool", "m", "7788", "specify the magic marker number");

// This function is called for every marker
VOID handleMarker(UINT64 rcx, INT64 arg, UINT64 expected)
{
        // Only print if RCX has the magic value
        if(rcx != expected)
                return;

        // -1 marks the start of trace
        if(arg == -1)
                enable_branch_tracing = true;
        // -2 marks the end of trace
        else if(arg == -2)
                enable_branch_tracing = false;

}

VOID countBranch()
{
        if(enable_branch_tracing)
                branches += 1;
}

VOID countAll()
{
        if(enable_branch_tracing)
                total += 1;
}

// Instrument the code to insert print instructions whenever a branch or a marker is observed
VOID Instruction(INS ins, VOID* v)
{
        // Insert a call to track branches
        if(INS_IsBranch(ins) && INS_HasFallThrough(ins))
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)countBranch, IARG_END);
        else
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)countAll, IARG_END);
        
        // Insert a call to track markers
        if(INS_IsXchg(ins) && INS_OperandReg(ins, 0) == REG_BX && INS_OperandReg(ins, 1) == REG_BX)
        {
                INS_InsertCall(ins, IPOINT_BEFORE, (AFUNPTR)handleMarker,
                                IARG_REG_VALUE, REG_GCX,        /* RCX value */
                                IARG_REG_VALUE, REG_GDX,        /* argument */
                                IARG_UINT64, (UINT64)v,         /* expected value in RCX */
                                IARG_END);
        }
}

// Close the output file
VOID Fini(INT32 code, VOID* v)
{
        cout << ((float)branches)/((float)total) << endl;
}

// Print Help Message
INT32 Usage()
{
        cerr << "This tool tracks the markers and prints the ratio of branches in the code" << endl;
        cerr << endl << KNOB_BASE::StringKnobSummary() << endl;
        return -1;
}

int main(int argc, char* argv[])
{
        // Initialize pin
        if (PIN_Init(argc, argv)) return Usage();
        
        // Register the function to be called to instrument instructions
        INT64 magic = KnobMagic.Value();
        INS_AddInstrumentFunction(Instruction, (VOID*)magic);

        // Register Fini to be called when the application exits
        PIN_AddFiniFunction(Fini, 0);

        // Start the program, never returns
        PIN_StartProgram();

        return 0;
}
