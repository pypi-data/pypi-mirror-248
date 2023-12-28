from Crypto.Hash import keccak
from web3 import Web3, Account

def inputBytes(func):
    
    def wrapper(cont):
        if isinstance(cont,str):
            cont = cont.encode()
        assert isinstance(cont,bytes)
        return func(cont)
    
    return wrapper

@inputBytes
def keccak_256(cont: bytes) -> str:
    hash_obj = keccak.new(digest_bits=256)
    hash_obj.update(cont)
    return hash_obj.hexdigest()

sha3 = SHA3 = keccak_256
@inputBytes
def funcSign(cont: bytes) -> str:
    keccak256Hash = keccak_256(cont)
    return '0x' + keccak256Hash[:8]


def W3(chain: Union[int, str]) -> Web3:
    if isinstance(chain, int): # ChainId
        if chain == 5: # Goerli
            return GoerliWeb3()
        elif chain == 11155111: # Sepolia
            return SepoliaWeb3()
        else:
            raise ValueError("Unknown Chain ID, please update")
    elif isinstance(chain, str): # Chain name
        if chain.lower() == 'Goerli'.lower() or 'Goerli'.lower().startswith(chain.lower()):
            return GoerliWeb3()
        if chain.lower() == 'Sepolia'.lower() or 'Sepolia'.lower().startswith(chain.lower()):
            return SepoliaWeb3()
        else:
            raise ValueError("Unknown Chain ID, please update")
    else:
        raise ValueError("Unsupported input type")

def SepoliaWeb3(rpc='https://ethereum-sepolia.publicnode.com'):
    # Sepolia
    sepolia_rpc = rpc
    SepoliaWeb3 = Web3(Web3.HTTPProvider(sepolia_rpc))
    assert SepoliaWeb3.is_connected(), "Unable to connect to chain"
    return SepoliaWeb3

def GoerliWeb3(rpc='https://ethereum-goerli.publicnode.com'):
    # Goerli
    goerli_rpc = rpc
    GoerliWeb3 = Web3(Web3.HTTPProvider(goerli_rpc))
    assert GoerliWeb3.is_connected(), "Unable to connect to chain"
    return GoerliWeb3


if __name__ == '__main__':
    print(funcSign('balanceOf(address)'))