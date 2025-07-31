import argparse
import sys

from openfhe import *

class CKKSParser:
    def __init__(self):
        self.context = CryptoContext()
        self.public_key = None
        self.input = None


    def load(self, args):
        self.init_context(args.cc)
        self.init_public_key(args.key_pub)
        self.init_eval_mult_key(args.key_mult)
        self.init_rotation_key(args.key_rot)
        self.init_ciphertext(args.sample)


    def init_context(self, context_path):
        self.context, ok = DeserializeCryptoContext(context_path, BINARY)
        if not ok:
            raise Exception('load crypto context')


    def init_public_key(self, public_key_path):
        self.public_key, ok = DeserializePublicKey(public_key_path, BINARY)
        if not ok:
            raise Exception('load public key')


    def init_eval_mult_key(self, eval_key_path):
        if not self.context.DeserializeEvalMultKey(eval_key_path, BINARY):
            raise Exception('load mult key')


    def init_rotation_key(self, rotation_key_path):
        if not self.context.DeserializeEvalAutomorphismKey(rotation_key_path, BINARY):
            raise Exception('load rotation key')
        

    def init_ciphertext(self, ciphertext_path):
        self.input, ok = DeserializeCiphertext(ciphertext_path, BINARY)
        if not ok:
            raise Exception('load ciphertext')
 
def solve(input, context, pub_key):
    # put your solution here
    plaintext = context.MakeCKKSPackedPlaintext([...])
    ciphertext = context.Encrypt(pub_key, plaintext)
    return ciphertext


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--key_pub')
        parser.add_argument('--key_mult')
        parser.add_argument('--key_rot')
        parser.add_argument('--cc')
        parser.add_argument('--sample')
        parser.add_argument('--output')
        args = parser.parse_args()

        a = CKKSParser()
        a.load(args)
        
        a.context.Enable(PKESchemeFeature.PKE)
        a.context.Enable(PKESchemeFeature.KEYSWITCH)
        a.context.Enable(PKESchemeFeature.LEVELEDSHE)
        a.context.Enable(PKESchemeFeature.ADVANCEDSHE)

        answer = solve(a.input, a.context, a.public_key)

        if not SerializeToFile(args.output, answer, BINARY):
            raise Exception('output serialization failed')

    except Exception as err:
        print(f'execution error: {err}')
        sys.exit(1)