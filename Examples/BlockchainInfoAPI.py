# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 12:37:05 2018

@author: Gareth

Validate an imported block against Blockchain.info's api
https://blockchain.info/api

Respects apis request limting queries to 1 every 10s

Queries for blocks are done using block hash, and are returned in json format
"""

# %% Imports

import requests
import time
from Blocks import Dat


# %% Get genesis block from Blockchain.info api

# api url
url = "https://blockchain.info/rawblock/"
# Query by blockhash
blockHash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
# Query
resp = requests.get(url + blockHash)

# Check reponse 200
if resp.status_code == 200:
    print "Good response"
else:
    print "Bad response code {}".format(resp.status_code)


# %% Look at response

# Print block info
print resp.json()

# Print individual fields, eg
print "\n"
print resp.json()['bits']
print resp.json()['mrkl_root']


# %% Function version

def ext_validate(block,
                 lastTime=0,
                 url="https://blockchain.info/rawblock/",
                 pr=True):
    """
    Query a block hash from Blockchain.info's api. Check it matches the block
    on size, merkle root, number of transactions, previous block hash

    Respects apis request limting queries to 1 every 10s.
    """

    # Wait if last query was less than 10s ago
    dTime = (time.time() - lastTime)
    if dTime < 11:
        sleep_time = 11 - dTime
        if pr:
            print "Sleeping for {0}".format(sleep_time)
        time.sleep(sleep_time)

    # Query
    resp = requests.get(url + block.hash)
    # Record the last time
    lastTime = time.time()

    # Get the json
    jr = resp.json()

    # Check size
    t1 = jr['size'] == block.blockSize
    if pr:
        print t1

    # Check merkle root
    t2 = jr['mrkl_root'] == block.merkleRootHash
    if pr:
        print t2

    # Check number of transactions
    t3 = jr['n_tx'] == block.nTransactions
    if pr:
        print t3

    # Check previous block hash
    t4 = jr['prev_block'] == block.prevHash
    if pr:
        print t4

    # The the overall result
    result = t1 & t2 & t3 & t4

    # Report
    if pr:
        if result:
            print "Pass"
        else:
            print "Fail"

    return lastTime, result


# Load a block
f = 'Blocks/blk00000.dat'
dat = Dat(f,
          verb=5)

dat.read_next_block()
block = dat.blocks[0]

# Reset timer
lastTime = 0
# Query using this block hash
lastTime, result = ext_validate(block)

# Run same query again to test wait timer
print "\n"
lastTime, result = ext_validate(block, lastTime)