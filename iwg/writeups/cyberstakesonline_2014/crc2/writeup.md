--this is only a sketch--

CRC2:  A Meet-in-the-Middle attack, similar to 2-DES, is possible.
The reduced keyspace of 2^24 (vice 2^48) is small enough to brute
force in a reasonable amount of time.  The process is two steps;
first to narrow the keyspace to a reasonable size using the meet in
the middle attack:

Given encryption function E(k, p) = c and a decryption function 
D(k) = E^-1(k) or equivalently D(k, c) = p
Compute the keyspace K = H^6 = B^24 where H is hex digits/B is 
binary digits
For one chosen plaintext p and encrypted ciphertext c,
compute all encryptions e = (E(k, p), k) for all k in K and all
decryptions d = (D(k, c), k) for all k in K
Find the intersection keyspace K0 = (k1, k2) such that for some m, 
(m, k1) in E and (m, k2) in D

Then, successively bruteforce the keyspace until you only have one key left:

While the keyspace Ki has more than one element:
Choose another p, c
Construct the set Ki = (k1, k2) for all (k1, k2) in Ki-1 such that
E(k1, p) == D(k2, p)
The key (k1', k2') is the only member of Ki
Compute flag = D(k1', D(k2', encryptedFlag))

