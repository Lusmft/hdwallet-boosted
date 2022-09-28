# Boosted HDWallet

Speeds up [HDWallet](https://github.com/meherett/python-hdwallet) work by replacing the elliptic curve math from pure python to the heavily optimized C library [libsecp256k1](https://github.com/bitcoin-core/secp256k1) used by [Bitcoin Core](https://github.com/bitcoin/bitcoin) for operations on the elliptic curve [secp256k1](https://en.bitcoin.it/wiki/Secp256k1).

[coincurve](https://github.com/ofek/coincurve) is used as python binding to the libsecp256k1.


## Installation

The easiest way to install `hdwallet_boosted` is via pip:

```
pip install git+https://github.com/baffolobill/python-hdwallet-boosted.git
```

## Quick Usage

Absolutely the same, as for [HDWallet](https://github.com/meherett/python-hdwallet/blob/master/README.md#quick-usage), but import `HDWallet` from `hdwallet_boosted`:

```python
#!/usr/bin/env python3

# from hdwallet import HDWallet
from hdwallet_boosted import HDWallet

from hdwallet.symbols import BTC


hdwallet = HDWallet(symbol=BTC)
hdwallet.from_xpublic_key(xpublic_key="xpub661MyMwAqRbcGGUtsoFw2d6ARvD2ABd7z327zxt2XiBBwMx9GAuNrrE7tbRuWF5MjjZ1BzDsRdaSHc9nVKAgHzQrv6pwYW3Hd7LSzbh8sWS")
hdwallet.from_path(path="m/44/0/0/0/0")

print(hdwallet.p2pkh_address())
```


## Donations

If You found this tool helpful consider making a donation:

| Coins                         | Addresses                                  |
| ----------------------------- | :----------------------------------------: |
| Bitcoin `BTC`                 | bc1q4lk0ahv5f0shc3wjkc78tc3cme6mtngclhsa0f |
| Tether `USDT TRC20`           | TWaHeuBM99vG7NvpkmmezNgEh1UsjKC2GY         |
| Ethereum `ETH`                | 0xb5288c37100b38f116A9aA70DBBe387F343f76cD |
