# Keccak (SHA-3) hashing algorithm

Keccak (SHA-3) is a variable-bit hashing algorithm. The hash function is based on the construction of a cryptographic sponge, in which data is first "absorbed" into the sponge, while the original message M is subjected to multi-round permutations f, and then the result Z is "squeezed" out of the sponge. At the “absorption” phase, the blocks of the message are summed modulo 2 with a subset of the state, after which the entire state is transformed using the permutation function f. During the "squeezing" phase, the output blocks are read from the same subset of the state modified by the permutation function f.

## Installation

To see the result of algorithms simple just run keccak.py file in python runtime environment. To see different result edit bob_message.txt file to change the message for Alice