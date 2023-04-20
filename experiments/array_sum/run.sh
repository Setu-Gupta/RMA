#!/bin/bash

# Perform warmup runs
for i in {1..5};
do
        echo "OPT Warmup $i"
        ./opt
done
echo "============================== OPT ========================" >> log
# Perform evaluation runs
for i in {1..25};
do
       echo "OPT Evaluation $i"
        ./opt >> log
done
echo "============================== END ========================" >> log

# Perform warmup runs
for i in {1..5};
do
       echo "UNOPT Warmup $i"
        ./unopt
done
echo "============================= UNOPT =======================" >> log
# Perform evaluation runs
for i in {1..25};
do
       echo "UNOPT Evaluation $i"
        ./unopt >> log
done
echo "============================= END =======================" >> log
