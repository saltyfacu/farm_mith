import os
from functools import lru_cache
from pathlib import Path
from time import sleep

from brownie import accounts, interface, project, config

# this is what I will use to swap
ROUTER = interface.IUniswapV2Router02("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F") #Sushi

@lru_cache(maxsize=None)
def all_wallets():
  wallets = accounts

  return wallets

def the_wallet():
  # "force=True" is to take control of a wallet you don't own. It only owkr on mainnet fork
  return accounts.at("0xb527a981e1d415af696936b3174f2d7ac8d11369", force=True)


def countdown(secs):
    width = len(str(secs))
    
    for i in range(0,secs):
        current_secs = secs - i
        print(f"Sleeping... {secs-i:>10}",end="\r")
        sleep(1)

def swapTokensUni(owner, amount, token_in, token_out, gas_price):
  if token_in.allowance(owner, ROUTER) < amount:
      print("APPROVING...")
      token_in.approve(ROUTER, 2**256-1, {'from': owner, 'gas_price': gas_price})

  path = [token_in, token_out]

  # Market buy sell
  return ROUTER.swapExactTokensForTokens(
      amount,
      0,
      path,
      owner,
      2607999400, #2052
      {'from': owner, 'gas_price': gas_price, 'gas_limit': 300_000}
  )

def swapTokensSushi(owner, amount, token_in, token_out, gas_price):
  if token_in.allowance(owner, ROUTER) < amount:
      print("APPROVING...")
      # allow the contrat to spend my tokens
      token_in.approve(ROUTER, 2**256-1, {'from': owner, 'gas_price': gas_price})

  # usually, the path is TOKEN_A --> WETH --> TOKEN_B
  # but in this case, I know that the direct path exists
  path = [token_in, token_out]

  # SWAP!
  return ROUTER.swapExactTokensForTokensSupportingFeeOnTransferTokens( #Sushi
      amount, # amount I send
      0, # minimum aount I want to receive. I put 0 becasue I'm farming shitcoins and I want to get out of them no matter what
      path, # the path I set above
      owner, # who? which wallet?
      2607999400, #expiration: year 2052, I just don't want it to expire.... maybe it's not the best decision here.
      {'from': owner, 'gas_price': gas_price, 'gas_limit': 300_000} # for gas_limit, try and set very high in this cases
  )
