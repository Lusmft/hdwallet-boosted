import hashlib
import hmac
import struct
from binascii import unhexlify
from typing import Optional

import ecdsa
from coincurve import PublicKey
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa import int_to_string, string_to_int
from hdwallet import (
    BIP32HDWallet,
    BIP44HDWallet,
    BIP49HDWallet,
    BIP84HDWallet,
    BIP141HDWallet,
    HDWallet,
)
from hdwallet.exceptions import DerivationError
from hdwallet.hdwallet import BIP32KEY_HARDEN, CURVE_ORDER
from hdwallet.libs.ecc import N

# Values for `x` and `y` are taken from `hdwallet.libs.ecc.G(...)`.
GENERATOR_POINT_PUBLIC_POINT = PublicKey.from_point(
    x=0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    y=0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,
)


class BoostedHDWallet(HDWallet):
    """
    Boosted Hierarchical Deterministic Wallet

    Please note, that this optimization is necessary only for public keys.

    On my machine original call of `.from_index()` takes ~0.061 seconds. After
    optimization: 0.0006 seconds.

    >>> from hdwallet_boosted import BoostedHDWallet
    >>> from hdwallet.symbols import BTC
    >>> boosted_hdwallet: BoostedHDWallet = BoostedHDWallet(symbol=BTC)
    >>> boosted_hdwallet.from_public_key(public_key="02f93f58b97c3bb616645c3dda256ec946d87c45baf531984c022dd0fd1503b0a8")
    >>> boosted_hdwallet.from_index(index=0)
    """

    def _derive_key_by_index(self, index) -> Optional["BoostedHDWallet"]:
        """
        Optimization needed only for HDWallet, created from Public Key.
        Other code left as is.
        """
        if not self._root_private_key and not self._root_public_key:
            raise ValueError("You can't drive this master key.")

        i_str = struct.pack(">L", index)
        if index & BIP32KEY_HARDEN:
            if self._key is None:
                raise DerivationError("Hardened derivation path is invalid for xpublic key.")
            data = b"\0" + self._key.to_string() + i_str
        else:
            data = unhexlify(self.public_key()) + i_str

        if not self._chain_code:
            raise ValueError("You can't drive xprivate_key and private_key.")

        i = hmac.new(self._chain_code, data, hashlib.sha512).digest()
        il, ir = i[:32], i[32:]

        il_int = string_to_int(il)
        if il_int > CURVE_ORDER:
            return None

        if self._key:
            pvt_int = string_to_int(self._key.to_string())
            k_int = (il_int + pvt_int) % CURVE_ORDER
            if k_int == 0:
                return None
            secret = (b"\0" * 32 + int_to_string(k_int))[-32:]

            self._private_key, self._chain_code, self._depth, self._index, self._parent_fingerprint = (
                secret, ir, (self._depth + 1), index, unhexlify(self.finger_print())
            )
            self._key = ecdsa.SigningKey.from_string(self._private_key, curve=SECP256k1)
            self._verified_key = self._key.get_verifying_key()
        else:
            # Original code specially left to show the difference.
            #
            # key_point = S256Point.parse(unhexlify(self.public_key()))
            #
            # This is the slowest part in original code. Let's optimize it.
            # left_point = il_int * G
            #
            # total = key_point + left_point

            # This operation happens in `hdwallet.libc.ecc.S256Point.__rmul__(...)`,
            # just before multiplication.
            coefficient = il_int % N
            boosted_left_point: PublicKey = GENERATOR_POINT_PUBLIC_POINT.multiply(
                scalar=coefficient.to_bytes(32, byteorder='big'), 
                update=False,
            )

            boosted_key_point: PublicKey = PublicKey(data=unhexlify(self.public_key()))
            boosted_total: PublicKey = boosted_key_point.combine(public_keys=[boosted_left_point])
            boosted_address: bytes = boosted_total.format(compressed=True)

            self._chain_code, self._depth, self._index, self._parent_fingerprint = (
                ir, (self._depth + 1), index, unhexlify(self.finger_print())
            )
            self._verified_key = ecdsa.VerifyingKey.from_string(
                boosted_address, curve=SECP256k1
            )
        return self


class BoostedBIP32HDWallet(BoostedHDWallet, BIP32HDWallet): pass
class BoostedBIP44HDWallet(BoostedHDWallet, BIP44HDWallet): pass
class BoostedBIP49HDWallet(BoostedHDWallet, BIP49HDWallet): pass
class BoostedBIP84HDWallet(BoostedHDWallet, BIP84HDWallet): pass
class BoostedBIP141HDWallet(BoostedHDWallet, BIP141HDWallet): pass
