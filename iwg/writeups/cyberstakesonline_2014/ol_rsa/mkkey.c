#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/engine.h>


void readBN(char* s, BIGNUM** bn) {
  if (!s || !bn) return;
  if (s[0] == '0' && s[1] == 'x') BN_hex2bn(bn, s+2);
  else BN_dec2bn(bn, s);
}

int main(int argc, char **argv) {
  if (argc != 9) {
    fprintf(stderr, "USAGE: %s [n] [e] [d] [p] [q] [dmp1] [dmq1] [iqmp]\n", argv[0]);
    return 1;
  }
  RSA* rsa = RSA_new();
  readBN(argv[1], &(rsa->n));
  readBN(argv[2], &(rsa->e));
  readBN(argv[3], &(rsa->d));
  readBN(argv[4], &(rsa->p));
  readBN(argv[5], &(rsa->q));
  readBN(argv[6], &(rsa->dmp1));
  readBN(argv[7], &(rsa->dmq1));
  readBN(argv[8], &(rsa->iqmp));
  PEM_write_RSAPrivateKey(stdout, rsa, NULL, NULL, 0, NULL, NULL);
  RSA_free(rsa);

  return 0;
}
