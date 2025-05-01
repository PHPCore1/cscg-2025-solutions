from Crypto.Protocol.KDF import SP800_108_Counter
from primitives import HMAC_PRF, CMAC_PRF, KMAC_PRF, SHA256
import random


def mitm(msg, ctx, sender, receiver):
    print(f'you have intercepted {sender} sending the following message to {receiver}')
    print(f'context: {ctx}')
    print(f'msg: {msg}')
    modified_message = input(f"what would you like {receiver} to receive?").strip()
    # empty input to not modify message
    if modified_message == "":
        return msg
    return modified_message

def xor(a, b):
    assert len(a) == len(b)
    return bytes([x^y for x,y in zip(a,b)])

# 2048 bit DH group: https://www.ietf.org/rfc/rfc3526.txt
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
G = 2


## Online Ephemeral DH Key exchange
# Parameter generation
alice_x = random.randint(2,P-1)
bob_x = random.randint(2,P-1)
alice_a = pow(G,alice_x, P)
bob_b = pow(G,bob_x, P)

# broadcast DH
alice_b = mitm(str(bob_b), "DH", "Bob", "Alice")
bob_a = mitm(str(alice_a), "DH", "Alice", "Bob")

alice_b = int(alice_b)
assert alice_b > 1 and alice_b < P, "Alice is sus about the key they received"
bob_a = int(bob_a)
assert bob_a > 1 and bob_a < P, "Bob is sus about the key they received"

# shared key computation
alice_shared_key = SHA256.new(str(pow(alice_b, alice_x, P)).encode()).digest()[:16]
bob_shared_key = SHA256.new(str(pow(bob_a, bob_x, P)).encode()).digest()[:16]



## Online KDF protocol agreement
alice_acceptable = mitm("HMAC/CMAC/KMAC", "protocol", "Bob", "Alice")
bob_acceptable = mitm("HMAC/CMAC/KMAC", "protocol", "Alice", "Bob")

# Handshake setup, using NIST certified PRF's
if "HMAC" in bob_acceptable:
    bob_prf = HMAC_PRF
elif "CMAC" in bob_acceptable:
    bob_prf = CMAC_PRF
elif "KMAC" in bob_acceptable:
    bob_prf = KMAC_PRF
else:
    exit("Bob had no useable PRF's")
if "HMAC" in alice_acceptable:
    alice_prf = HMAC_PRF
elif "CMAC" in alice_acceptable:
    alice_prf = CMAC_PRF
elif "KMAC" in alice_acceptable:
    alice_prf = KMAC_PRF
else:
    exit("Alice had no useable PRF's")


# Generate ephemeral KDF material
alice_ctx1 = random.randbytes(16)
while b'\x00' in alice_ctx1:
    alice_ctx1 = random.randbytes(16)
bob_ctx2 = random.randbytes(16)
while b'\x00' in bob_ctx2:
    bob_ctx2 = random.randbytes(16)

# Exchange inputs to KDF
alice_ctx2 = mitm(bob_ctx2.hex(), "KDF nonce", "Bob", "Alice")
bob_ctx1 = mitm(alice_ctx1.hex(), "KDF nonce", "Alice", "Bob")
assert len(alice_ctx2) == 32 and len(bob_ctx1) == 32, "Alice or Bob are suspicious of their KDF inputs"

# build_context
alice_ctx = alice_ctx1 + bytes.fromhex(alice_ctx2)
bob_ctx = bytes.fromhex(bob_ctx1) + bob_ctx2

# NIST SP 800-108, Recommendation for Key Derivation Using Pseudorandom Functions
alice_OTP = SP800_108_Counter(alice_shared_key, 16, alice_prf, 1, b'keygen_for_secure_bagdrop', alice_ctx)
bob_OTP = SP800_108_Counter(bob_shared_key, 16, bob_prf, 1, b'keygen_for_secure_bagdrop', bob_ctx)

### Alice uses the OTP from the KDF to encrypt a message to bob, which is left at physical bag drop site we can't MITM
alice_msg = b'wearecompromised'
bagdrop = xor(alice_msg, alice_OTP)

print("Alice has made the bag drop, waiting for Bob to pick up and decode the message")

bob_msg = xor(bagdrop, bob_OTP)

with open('./test.txt', 'w') as f:
    f.writelines(map(lambda x: x + '\n', [
        str(alice_a),
        str(bob_b),
        alice_shared_key.hex(),
        bob_shared_key.hex(),
        alice_acceptable,
        bob_acceptable,
        alice_ctx1.hex(),
        bob_ctx2.hex(),
        alice_ctx.hex(),
        bob_ctx.hex(),
        alice_OTP.hex(),
        bob_OTP.hex(),
        bagdrop.hex(),
        bob_msg.hex()
    ]))

if bob_msg == b'wearecompromised':
    print("Bob received alice's warning and disappears into the night with the flag")
    exit()

elif bob_msg == b'allgoodprintflag':
    with open("flag.txt", "r") as f:
        print(f.read())
    exit()

else:
    print("Bob reads the message, but luckily KDF's are very secure so its just nonsense.")
    print("He can tell someone tried to influence the key exchange, so he disappears into the night with the flag")
