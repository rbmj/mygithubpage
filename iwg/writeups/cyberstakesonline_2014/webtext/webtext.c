#include <arpa/inet.h>
#include <errno.h>
#include <pwd.h>
#include <netdb.h>
#include <grp.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#ifndef BUFSIZE
#define BUFSIZE 1024
#endif

ssize_t sendlen(int fd, const char *buf, size_t n) {
  ssize_t rc;
  size_t nsent = 0;
  while (nsent < n) {
    rc = send(fd, buf + nsent, n - nsent, 0);
    if (rc == -1) {
      if (errno == EAGAIN || errno == EINTR) {
        continue;
      }
      return -1;
    }
    nsent += rc;
  }
  return nsent;
}

ssize_t sendstr(int fd, const char *str) {
  return sendlen(fd, str, strlen(str));
}

void strip_tags(char* buf) { 
  char stripped_buf[BUFSIZE];
  int write = 1;
  int d = 0;

  memset(stripped_buf, 0, BUFSIZE);
  for(size_t i = 0; i < strlen(buf); i++) {
    if(buf[i] == '<')
      write--;

    if(write != 0)
      stripped_buf[d] = buf[i];  

    if(buf[i] == '>') {
      write++;
      d--;
    }
    d += write;
  }
  stripped_buf[d] = '\0';
  strcpy(buf, stripped_buf);
}


void strip_script(char* buf) {
  char* bufcpy = buf;
  char stripped_buf[BUFSIZE];
  char* tag_start;
  memset(stripped_buf, 0, BUFSIZE);

  while((tag_start = strstr(bufcpy, "<script")) != NULL)
  {
    strncat(stripped_buf, bufcpy, tag_start - bufcpy);
    bufcpy = strstr(tag_start, "</script>");
    if(bufcpy == NULL)
      break;
    bufcpy += 9;
  }

  if(bufcpy != buf) {
    strcat(stripped_buf, bufcpy);
    strcpy(buf, stripped_buf);
  }

  bufcpy = buf;
  memset(stripped_buf, 0, BUFSIZE);

  while((tag_start = strstr(bufcpy, "<style")) != NULL) {
    strncat(stripped_buf, bufcpy, tag_start - bufcpy);
    bufcpy = strstr(tag_start, "</style>");
    if(bufcpy == NULL)
      break;
    bufcpy += 8;
  }

  if(buf != bufcpy) {
    strcat(stripped_buf, bufcpy);
    strcpy(buf, stripped_buf);
  }   
}


int main(int argc, char **argv) {
  char user_input[128];
  int nbRead;
  char hostname[128];
  struct hostent* host;
  char request[256];
  int urlsocket;
  struct sockaddr address;

  fprintf(stdout, "Please enter the URL you would like to retrieve: ");
  fflush(stdout);
  fgets(user_input, 127, stdin);
  nbRead = strlen(user_input);

  while(user_input[nbRead-1] == '\n') {
    nbRead -= 1;
    user_input[nbRead] = '\0';
  }

  char *hostname_start = strstr(user_input, "http://");
  if(hostname_start == NULL) {
    hostname_start = user_input;
  }
  char *hostname_end = strchr(hostname_start, '/');
  int hostname_len = 0;
  if(hostname_end == NULL) {
    hostname_len = strlen(hostname_start);
    hostname_end = hostname_start + hostname_len;
  } else {
    hostname_len = hostname_end - hostname_start;
  }
  memcpy(hostname, hostname_start, hostname_len);
  hostname[hostname_len] = '\0';

  if(strlen(hostname_end) > 0)
    strncpy(request, hostname_end, 256);
  else
    memcpy(request, "/", 2);

  char * host_addr = strtok(hostname, ":");
  char * host_port = strtok(NULL, ":");
  int port;
  if (host_port == NULL) {
    port = 80;
  } else {
    port = atoi(host_port);
  }

  host = gethostbyname(host_addr);
  if(host == NULL) {
    fprintf(stderr, "Could not lookup that URL\n");
    return 1;
  }

  urlsocket = socket(AF_INET, SOCK_STREAM, 0);
  if(urlsocket < 0 ) {
    fprintf(stderr, "Could not get a socket so you're out of luck\n");
    return 1;
  }

  memset((void *)&address, 0, 16);
  memcpy(address.sa_data + 2, host->h_addr_list[0], host->h_length);
  address.sa_family = host->h_addrtype;
  *(short*)address.sa_data = htons(port);
  if(connect(urlsocket, &address, 16) < 0) {
    fprintf(stderr, "Unable to connect to the server\n"); 
    return 1;
  }

  char req_buf[BUFSIZE];
  snprintf(req_buf, BUFSIZE - 1, "GET %s HTTP/1.0\x0d\nConnection: close\x0d\nHost : %s\x0d\nAccept: text/plain\x0d\n\x0d\n", request, user_input);
  sendstr(urlsocket, req_buf);

  char buf[BUFSIZE];
  memset(buf, 0, BUFSIZE);
  while(recv(urlsocket, buf, BUFSIZE - 1, 0) > 0)
  {
    strip_script(buf);
    strip_tags(buf);
    fprintf(stdout, "%s", buf);
    fflush(stdout);
  }
  return 0;
}
