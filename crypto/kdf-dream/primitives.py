from Crypto.Hash import CMAC, HMAC, KMAC128, SHA256
from Crypto.Cipher import AES



# https://www.rfc-editor.org/rfc/rfc4615.html
def CMAC_PRF(K, M):
    if len(K) == 16:
        K = K
    else:
        K = CMAC.new(bytes(bytearray(16)), K, AES).digest()
    PRV = CMAC.new(K, M, AES).digest()
    return PRV

# https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.198-1.pdf
def HMAC_PRF(K,M):
    PRV = HMAC.new(K,M,SHA256).digest()[:16]
    return PRV

# https://csrc.nist.gov/files/pubs/sp/800/185/ipd/docs/sp800_185_draft.pdf
def KMAC_PRF(K,M):
    PRV = KMAC128.new(key=K, data=M, mac_len=16).digest()
    return PRV

