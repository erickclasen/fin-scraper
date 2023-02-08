#!/bin/bash
./run.py btc-usd i
./run.py eth-usd i
./run.py xmr-usd i

./run.py eth-btc i
#./run.py xmr-btc i

#./run.py xmr-eth i

./dbl-run.py gc=f si=f i
./run.py si=f i
./run.py dx-y.nyb i


./dbl-run.py eth-usd paxg-usd i
#./dbl-run.py xmr-usd paxg-usd i

