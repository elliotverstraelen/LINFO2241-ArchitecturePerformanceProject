#ifndef __UTILS_H_
#define __UTILS_H_

#include <stddef.h> /* size_t */
#include <stdint.h> /* uintx_t */
#include <unistd.h>
#include <stdio.h>  /* ssize_t */
#include <stdlib.h>
#include <time.h>
#include <errno.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <math.h>
#include <pthread.h>

#include "packet_implem.h"

typedef struct {
  struct addrinfo *serverinfo;
  uint64_t key_payload_length;
  uint32_t key_size;
} client_thread_args;

/* Fill the pkt_response structure from the given parameters */
void create_pkt_response(pkt_response_t* pkt, pkt_error_code code, uint32_t fsize, char* file);

/* Read from sockfd to create a response packet */
void recv_request_packet(pkt_request_t* pkt, int sockfd);

/* Fill the pkt_request structure from the given parameters */
void create_pkt_request(pkt_request_t* pkt, uint32_t findex, uint32_t ksize, char *key);

/* Read from sockfd to create a response_packet */
void recv_response_packet(pkt_response_t* pkt, int sockfd);

/* Fill the timeval structure with the current clock time */
void get_current_clock(struct timeval *timestamp);

/* Return ms from timeval structure */
uint64_t get_ms(struct timeval *timestamp);

void* start_client(void* args);

/* Get random number following a normal distribution from paramter's mean and std. 
 * Uses the Box-Muller algorithm 
 * @pre: rand should be initialised, e.g. using: srand(time(NULL)); */
uint32_t get_gaussian_number(uint32_t mean, uint32_t std);

#endif  /* __UTILS_H_ */