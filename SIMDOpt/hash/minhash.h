/*
 * minhash.h
 *
 *  Created on: 2017Äê6ÔÂ3ÈÕ
 *      Author: LLL
 */

#ifndef MINHASH_H_
#define MINHASH_H_

#ifdef __cplusplus
extern "C"
{
#endif 

#include <stdint.h>

	typedef struct {
		uint32_t hash;
		uint32_t pos;
	} Min;

	Min minhash(char *s, int k, int seed);
	Min minhash_bitpack(char *s, int k, unsigned char reverse);

#ifdef __cplusplus
}
#endif 



#endif /* MINHASH_H_ */
