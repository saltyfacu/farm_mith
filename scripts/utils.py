import os
from functools import lru_cache
from pathlib import Path
from time import sleep

from brownie import accounts, interface, project, config

#DEBUG = os.environ["DEBUG"] == "1"

DAI = interface.ERC20("0x6b175474e89094c44da98b954eedeac495271d0f")
MIC = interface.ERC20("0x368B3a58B5f49392e5C9E4C998cb0bB966752E51")
MIS = interface.ERC20("0x4b4D2e899658FB59b1D518b68fe836B100ee8958")
USDT = interface.ERC20("0xdAC17F958D2ee523a2206206994597C13D831ec7")

MIC_DAI = interface.MICPOOL("0xcE0058827e6c89E625e524D2fE6E3EF3d9BB6A0c")
MIC_LINK = interface.MICPOOL("0x0555EEa5f419e18CFc338dEa66aE84Fa7A2fD2BA")

ROUTER = interface.IUniswapV2Router02("0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F") #Sushi

@lru_cache(maxsize=None)
def all_wallets():
  wallets = accounts

  return wallets

def the_wallet():
  #return accounts[0]
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
      token_in.approve(ROUTER, 2**256-1, {'from': owner, 'gas_price': gas_price})

  path = [token_in, token_out]

  # Market buy sell
  return ROUTER.swapExactTokensForTokensSupportingFeeOnTransferTokens( #Sushi
      amount,
      0,
      path,
      owner,
      2607999400, #2052
      {'from': owner, 'gas_price': gas_price, 'gas_limit': 300_000}
  )
