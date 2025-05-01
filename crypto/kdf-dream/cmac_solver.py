from Crypto.Protocol.KDF import SP800_108_Counter
from primitives import CMAC_PRF
import os
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from pwnlib.util.iters import bruteforce

HEX_ALPHABET = [i.to_bytes(1, 'big').hex()[-1] for i in range(16)]
DESIRED_XOR_OUTPUT = b'allgoodprintflag'

### General Methods
def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def AES_K(k, m):
    assert len(m) == 16 and len(k) == 16
    return AES.new(k, AES.MODE_ECB).encrypt(m)

def INV_AES_K(k, c):
    assert len(c) == 16 and len(k) == 16
    return AES.new(k, AES.MODE_ECB).decrypt(c)

### CMAC Methods
def CMAC_PAD(m):
    padding_length = (16 - len(m))
    padding_bit_length = padding_length * 8
    padding_int = 1 << (padding_bit_length - 1)
    padding = padding_int.to_bytes(padding_length, 'big')
    return m + padding

MASK = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
MSB_MASK = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF & ~(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF >> 1)
CONST_RB = 0x00000000000000000000000000000087

def MSB(n):
    return (n & MSB_MASK) >> (16 * 8 - 1)

def GEN_K1(k):
    L = int.from_bytes(AES_K(k, b'\x00' * 16), 'big')

    if MSB(L) == 0:
        return ((L << 1) & MASK).to_bytes(16, 'big')
    else:
        return ((((L << 1) ^ CONST_RB)) & MASK).to_bytes(16, 'big')

def GEN_K2(k1):
    L = int.from_bytes(k1, 'big')

    if MSB(L) == 0:
        return ((L << 1) & MASK).to_bytes(16, 'big')
    else:
        return ((((L << 1) ^ CONST_RB)) & MASK).to_bytes(16, 'big')

### SP800-108 Methods
def get_info(context):
    key_len_enc = long_to_bytes(16 * 8, 4)
    return long_to_bytes(1, 4) + b'keygen_for_secure_bagdrop' + b'\x00' + context + key_len_enc

### Communication Methods
def get_message_blocks(context):
    initial_info = get_info(context)
    blocks = [initial_info[i:i+16] for i in range(0, len(initial_info), 16)]

    if len(blocks[-1]) < 16:
        blocks[-1] = CMAC_PAD(blocks[-1])
        
    return blocks

def get_new_ctx(first_part, RECIPIENT_CTX):
    return first_part + RECIPIENT_CTX

def find_custom_context(RECIPIENT_KEY, RECIPIENT_CTX, XOR_INPUT):
    init_blocks = get_message_blocks(get_new_ctx(b'\x00'*16, RECIPIENT_CTX))
    k2 = GEN_K2(GEN_K1(RECIPIENT_KEY))

    desired_mac = xor(XOR_INPUT, DESIRED_XOR_OUTPUT)

    desired_C4 = xor(INV_AES_K(RECIPIENT_KEY, desired_mac), xor(init_blocks[4], k2))
    desired_C3 = xor(INV_AES_K(RECIPIENT_KEY, desired_C4), init_blocks[3])
    desired_CT = INV_AES_K(RECIPIENT_KEY, desired_C3)
    C1 = AES_K(RECIPIENT_KEY, init_blocks[0])

    def calc_c2(context_part):
        return AES_K(RECIPIENT_KEY, xor(init_blocks[1][:14] + context_part[:2], C1))

    def is_c2_good(c2):
        return xor(init_blocks[2][-2:], c2[-2:]) == desired_CT[-2:]

    bruteforced_ctx_start = bruteforce(lambda x: is_c2_good(calc_c2(bytes.fromhex(x))), HEX_ALPHABET, 4, 'fixed')
    assert bruteforced_ctx_start is not None, "Couldn't bruteforce CTX, which could provide wanted output"
    bruteforced_ctx_start = bytes.fromhex(bruteforced_ctx_start)
    assert b'\x00' not in bruteforced_ctx_start, "Bruteforced CTX included illegal bytes"

    bruteforced_C2 = calc_c2(bruteforced_ctx_start)
    calculated_ctx_end = xor(bruteforced_C2[:14], desired_CT[:14])
    custom_ctx = bruteforced_ctx_start + calculated_ctx_end
    assert b'\x00' not in custom_ctx, "Calculated CTX included illegal bytes"

    assert xor(SP800_108_Counter(RECIPIENT_KEY, 16, CMAC_PRF, 1, b'keygen_for_secure_bagdrop', get_new_ctx(custom_ctx, RECIPIENT_CTX)), XOR_INPUT) == DESIRED_XOR_OUTPUT, "CTX doesn't give desired output"
    print('SUCCESS')
    return custom_ctx