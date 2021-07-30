from dotenv import load_dotenv
load_dotenv()

from brownie import accounts, chain
from brownie.utils import color
from brownie.network.gas.strategies import GasNowStrategy
from datetime import datetime, timedelta
from time import sleep

# this imports utils.py inside scripts :)
from .utils import *

# let's load the tokens I need
DAI = interface.ERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
MIC = interface.ERC20("0x368B3a58B5f49392e5C9E4C998cb0bB966752E51")
MIS = interface.ERC20("0x4b4D2e899658FB59b1D518b68fe836B100ee8958")
USDT = interface.ERC20("0xdAC17F958D2ee523a2206206994597C13D831ec7")

# and also the pools where I stake 
MIC_DAI = interface.MICPOOL("0xcE0058827e6c89E625e524D2fE6E3EF3d9BB6A0c")
MIC_LINK = interface.MICPOOL("0x0555EEa5f419e18CFc338dEa66aE84Fa7A2fD2BA")

# an array to loop through
pools = [MIC_DAI, MIC_LINK]

# check gas now and get fast gas price
gas_strategy = GasNowStrategy('fast')

# just in case I need to exit fast, I use this to multiply gas price from above
gas_ratio = 1

# I don't want to always sell, at least I need this amount
min_rewards = 10


# the fun part starts here
def main():
    
    # which wallet am I going to use?
    owner = the_wallet()

    # this is the status of my wallet
    print(f"The Wallet: {owner}")
    print(f"Balance of USDT: {USDT.balanceOf(owner).to('ether')}")
    print(f"Balance of DAI: {DAI.balanceOf(owner).to('ether')}")
    print(f"Balance of MIC: {MIC.balanceOf(owner).to('ether')}")
    print(f"Balance of MIS: {MIS.balanceOf(owner).to('ether')}")
    print("")

    # how much do we want to pay for gas?
    gas_price = gas_strategy.get_gas_price() * gas_ratio 

    # approve the stake contract to spend DAI
    DAI.approve(MIC_DAI, 2**256-1, {'from': owner, 'gas_price': gas_price}) 

    # stake
    MIC_DAI.stake("10_000 ether", {'from': owner, 'gas_limit': 150_000, 'gas_price': gas_price})

    # loop forever and ever... or until CTRL+C whatever happens first
    while(1):
        
        # let's check all the pool where I might have staked funds (DAI and LINK)
        for MIC_POOL in pools: 
            # ask for pending rewards
            pending_reward = MIC_POOL.earned(owner)
            print(f"Pending rewards {pending_reward.to('ether')}, min: {min_rewards}")

            # are rewards more than then min I consider profitable?
            if (pending_reward < (min_rewards * 1e18)):
                print(f"It's not enough. Less than {min_rewards}. I wait.")
            else:
                print("Let's claim and sell!")
                gas_price = gas_strategy.get_gas_price() * gas_ratio
                
                # claim the rewards
                MIC_POOL.getReward({'from': owner, 'gas_limit': 150_000, 'gas_price': gas_price})
                
                # I tried to claim, did I succeed?
                if (MIC.balanceOf(owner) > 0):
                    # This is my balance
                    print(f"Balance of MIC: {MIC.balanceOf(owner).to('ether')}")

                    # Swap it from USDT using Sushi
                    swapTokensSushi(owner, MIC.balanceOf(owner), MIC, USDT, gas_price)
                    
                    # clap! clap! and print balance
                    print("SOLD!")
                    print(f"Balance of USDT: {USDT.balanceOf(owner).to('ether')}")
                else :
                    print("Coudln't claim rewards")
                
                # what's my wallet status?
                print("")
                print(f"Balance of USDT: {USDT.balanceOf(owner)/1e6}")
                print(f"Balance of DAI: {DAI.balanceOf(owner).to('ether')}")
                print(f"Balance of MIC: {MIC.balanceOf(owner).to('ether')}")
                print(f"Balance of MIS: {MIS.balanceOf(owner).to('ether')}")
                print("")
                print("")

        #end for
        
        countdown(100) #1800 = 30 minutes