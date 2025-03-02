import sys
import time
import numpy as np
sys.path.insert(0, '../make/bin/python')

import pyhelayers
from copy import copy, deepcopy

print(pyhelayers)

### setting the inputs
text = "hello world"
strings = ["hell", "worl"]

# for simplicity, this code assumes all strings are of the same size
text_length = len(text)
string_length = len(strings[0])
if any(len(s) != string_length for s in strings):
    raise ValueError("All strings must be of the same size")

# also for simplicity, this code assumes lengths of strings are a power of 2
if (string_length & (string_length - 1)) != 0:
    raise ValueError("Strings lengths must be a power of 2")


### setting up the FHE context
mockup = True

NUM_SLOTS = 32*1024
# NUM_SLOTS = 16

# FHE Context requirements 
requirement = pyhelayers.HeConfigRequirement(
        num_slots = NUM_SLOTS,
        multiplication_depth = 12,
        fractional_part_precision = 42,
        integer_part_precision = 18,
        security_level = 128)

# Init the context and generates the keys.
if not mockup:
    requirement.bootstrappable = True
    he_context = pyhelayers.HeaanContext()
else:
    requirement.multiplication_depth = 1000
    requirement.security_level = 0
    he_context = pyhelayers.MockupContext()

print("Initializing context . . .")
he_context.init(requirement)
encoder = pyhelayers.TTEncoder(he_context)

if not mockup:
    he_context.set_automatic_bootstrapping(True)


# packing decisions

TEXT_TILESIZE = 2
BATCH_TILESIZE = NUM_SLOTS // TEXT_TILESIZE

# set TEXT_DIM as 0 or 1 to set the order of the dimensions
TEXT_DIM = 0
BATCH_DIM = 1 - TEXT_DIM


if TEXT_DIM == 0:
    text_shape = pyhelayers.TTShape([TEXT_TILESIZE, BATCH_TILESIZE])
else:
    text_shape = pyhelayers.TTShape([BATCH_TILESIZE, TEXT_TILESIZE])

if TEXT_TILESIZE > 1:
    text_shape.get_dim(TEXT_DIM).set_interleaved(True)
string_shape = deepcopy(text_shape)

text_shape.get_dim(BATCH_DIM).set_original_size(1)
text_shape.get_dim(BATCH_DIM).set_num_duplicated(BATCH_TILESIZE)


# helper function to encode a text
def encode_text(text, shape):
    global encoder
    if TEXT_DIM == 0:
        cleartext = [[ord(c)] for c in text]
    else:
        cleartext = [[ord(c) for c in text]]
    ptext = encoder.encode(shape, cleartext)
    return ptext

# helper function to encrypt a batch of strings
def encrypt_strings(strings, shape):
    global encoder
    cleartext = [[ord(c) for c in s] for s in strings]
    if TEXT_DIM == 0:
        cleartext = list(map(list, zip(*cleartext)))
    print(cleartext)
    ctext = encoder.encode_encrypt(shape, cleartext)
    return ctext

strings = encrypt_strings(strings, string_shape)

output = None

fe = pyhelayers.TTFunctionEvaluator(he_context)


# check if the strings are at location i
for i in range(text_length - string_length):
    print("==================== comparing strings at location", i)
    ptext = encode_text(text[i:i+string_length], text_shape)

    print('comparing to: {}'.format(encoder.decode_double(ptext).flatten().astype(int).tolist()))
    strs = fe.compare(strings, ptext, 3, 3, 256)
    print('comparison result is:')
    print(encoder.decrypt_decode_double(strs))

    # now:
    # strs[i,j] = 0     if strings[j,i] < text[i] 
    # strs[i,j] = 0.5   if strings[j,i] == text[i] 
    # strs[i,j] = 1     if strings[j,i] > text[i] 
    strs.add_scalar(-0.5)
    strs.multiply_scalar(2)
    strs.square()
    strs.multiply_scalar(-1)
    strs.add_scalar(1)
    # now:
    # strs[i,j] = 0     if strings[j,i] != text[i] 
    # strs[i,j] = 1     if strings[j,i] == text[i] 
    print('after adjusting to indicators:')
    print(encoder.decrypt_decode_double(strs))

    # multiply string_length consecutive slots
    strs.multiply_over_dim(TEXT_DIM)
    print('after folding the indicators:')
    print(encoder.decrypt_decode_double(strs))

    strs.multiply_scalar(i+1)

    if output == None:
        output = strs
    else:
        output.add(strs)

output.add_scalar(-1)
print('final output:')
print(encoder.decrypt_decode_double(output))

