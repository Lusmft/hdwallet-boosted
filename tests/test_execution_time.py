#!/usr/bin/env python3

import json
import os
import random
import time

from hdwallet import HDWallet
from hdwallet_boosted import BoostedHDWallet

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "./values.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def _generate_xpublic_key():
    hdwallet: HDWallet = HDWallet(
        symbol=_["bitcoin"]["mainnet"]["symbol"]
    )
    
    hdwallet.from_mnemonic(
        mnemonic=_["bitcoin"]["mainnet"]["mnemonic"],
        passphrase=_["bitcoin"]["mainnet"]["passphrase"],
        language=_["bitcoin"]["mainnet"]["language"]
    )
    hdwallet.clean_derivation()
    hdwallet.from_path(path="m/44'/0/0'/0")
    return hdwallet.xpublic_key()


def _create_wallet_instance(cls, xpublic_key):
    wallet = cls(symbol=_["bitcoin"]["mainnet"]["symbol"])
    wallet.from_xpublic_key(xpublic_key)
    wallet.clean_derivation()
    return wallet


def _get_address_for_index(wallet_instance, index):
    wallet_instance.clean_derivation()
    wallet_instance.from_index(index)
    return wallet_instance.p2pkh_address()


def _timeit(wallet_cls, xpublic_key, index):
    started = time.time()
    wallet = _create_wallet_instance(wallet_cls, xpublic_key)
    address = _get_address_for_index(wallet, index)
    duration = time.time() - started
    return wallet, address, duration


def test_execution_time_became_better():
    """
    Test if execution time is became better.
    """
    xpublic_key = _generate_xpublic_key()
    max_derivation_path_element_value = 2**31 - 1
    index = random.randint(0, max_derivation_path_element_value)
    _orig_wallet, orig_address, orig_time = _timeit(HDWallet, xpublic_key, index)
    _boosted_wallet, boosted_address, boosted_time = _timeit(BoostedHDWallet, xpublic_key, index) 
    
    assert orig_address == boosted_address
    assert boosted_time < orig_time
    # On my desktop it takes "0.002 seconds". Ensure the execution time is 
    # pretty low value.
    assert boosted_time < 0.01
