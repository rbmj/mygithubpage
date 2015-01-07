#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/engine.h>
#include <openssl/err.h>

const char* cmd = "cat key\n";
const char* sh = "SHELL\x00\n";
const char* token = "828C2EE84B\n";
const char* n = "e607c3c83d87cfe248156854478d6d68f6ededc0a3f0a318506424617993d623da8f282af6ac38eee692ede54a1277019bc6e70bc085c90d5105acb425b6aeb18c858bbce0648643dc5ca8269e1c4ac61ac7c4be8d5b22a020374bb83436159b863c7d12633db3d9d867ddf31dcefcb6940c68842d293c23395106f6bd5faf2d";
const char* e = "65537";
const char* d = "3e2032bc4e01f41f4520a300c0226e3e3f129b77bfcf29fd5318f8ca6aaf86d2402111d428b2f2dd72e093e7ad4db75e73d81066982489dc52d9997f3e004cc59bf988fc4266de81fd12aab043a76f4db9a6f5d32b3c295bc3884b99d7ff42fff2f37caacf812d1fad4f5f4ab16628ed25814f353ef17f1eebc76bdc39ebbaf1";


int main(int argc, char **argv) {
  RSA* rsa = RSA_new();
  BN_hex2bn(&(rsa->n), n);
  BN_dec2bn(&(rsa->e), e);
  BN_hex2bn(&(rsa->d), d);

  char *buf = (char *)malloc(1024);
  if(buf == NULL) {
    perror("mem alloc failed");
    exit(1);
  }

  /* read challenge */
  fread(buf, 1024, 1, stdin);
  int encrypted_size = *(int*)buf;
  char * encrypted_challenge = buf + sizeof(int);
  unsigned long long challenge;

  if (RSA_private_decrypt(encrypted_size, encrypted_challenge, (unsigned char*)&challenge, rsa, RSA_PKCS1_OAEP_PADDING) == -1) {
    fprintf(stderr, "%s\n", ERR_error_string(ERR_get_error(), NULL));
  }

  /* write challenge */
  fwrite((char*)&challenge, sizeof(challenge), 1, stdout);
  char n = '\n';
  fwrite(&n, 1, 1, stdout);
  free(buf);

  return 0;
}

