from dotenv import load_dotenv
load_dotenv()

from brownie import accounts, chain
from brownie.utils import color
from brownie.network.gas.strategies import GasNowStrategy
from datetime import datetime, timedelta
from time import sleep

from .utils import *

gas_strategy = GasNowStrategy('fast')
gas_ratio = 1
min_rewards = 0.2

pools = [MIC_DAI, MIC_LINK]

def main():
    
    owner = the_wallet()

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

    while(1):
        for MIC_POOL in pools: 
            pending_reward = MIC_POOL.earned(owner)
            print(f"Pending rewards {pending_reward.to('ether')}, min: {min_rewards}")

            if (pending_reward < (min_rewards * 1e18)):
                print(f"It's not enough. Less than {min_rewards}. I wait.")
            else:
                print("Let's claim and sell!")
                gas_price = gas_strategy.get_gas_price() * gas_ratio
                
                MIC_POOL.getReward({'from': owner, 'gas_limit': 150_000, 'gas_price': gas_price})
                
                if (MIC.balanceOf(owner) > 0):
                    print(f"Balance of MIC: {MIC.balanceOf(owner).to('ether')}")
                    swapTokensSushi(owner, MIC.balanceOf(owner), MIC, USDT, gas_price)
                    print("SOLD!")
                    print(f"Balance of USDT: {USDT.balanceOf(owner).to('ether')}")
                else :
                    print("Coudln't claim rewards")
                
                print("")
                print(f"Balance of USDT: {USDT.balanceOf(owner)/1e6}")
                print(f"Balance of DAI: {DAI.balanceOf(owner).to('ether')}")
                print(f"Balance of MIC: {MIC.balanceOf(owner).to('ether')}")
                print(f"Balance of MIS: {MIS.balanceOf(owner).to('ether')}")
                print("")
                print("")

        #end for
        
        countdown(100) #1800 = 30 minutes