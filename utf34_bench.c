/* UTF-34 BENCHMARK — chay THAT encode/decode moi bien the base-B/N tren may.
 * Kiem round-trip + do toc do (Mchar/s, ns/char) + byte/ma.
 * cc -O2 -o utf34_bench utf34_bench.c -lm && ./utf34_bench
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

/* encode value -> N digit base-B, moi digit w bit -> bitbuf (packed). tra ve so byte. */
static int enc(uint64_t v,int B,int N,int w,uint8_t*out){
    uint8_t dig[64];
    for(int i=0;i<N;i++){ dig[i]=(uint8_t)(v% (uint64_t)B); v/= (uint64_t)B; } /* LSB first */
    int nbits=N*w, nbytes=(nbits+7)/8;
    memset(out,0,nbytes);
    /* MSB-first digit -> bit stream */
    int bit=0;
    for(int i=N-1;i>=0;i--){
        for(int b=w-1;b>=0;b--){
            int val=(dig[i]>>b)&1;
            if(val) out[bit>>3] |= (uint8_t)(0x80>>(bit&7));
            bit++;
        }
    }
    return nbytes;
}
/* decode bitbuf -> value */
static uint64_t dec(const uint8_t*in,int B,int N,int w){
    uint64_t v=0; int bit=0;
    for(int i=0;i<N;i++){
        uint32_t d=0;
        for(int b=0;b<w;b++){
            int val=(in[bit>>3]>>(7-(bit&7)))&1;
            d=(d<<1)|val; bit++;
        }
        v=v*(uint64_t)B + d;   /* MSB-first */
    }
    return v;
}

typedef struct{const char*name;int B,N;} Variant;

static void run(Variant vv,uint64_t lo,uint64_t hi,int rep){
    int w=(int)ceil(log2((double)vv.B));
    int nbytes=(vv.N*w+7)/8;
    double waste = w - log2((double)vv.B);
    uint8_t buf[64];
    /* round-trip correctness */
    uint64_t bad=0,checked=0;
    for(uint64_t v=lo; v<hi; v++){
        enc(v,vv.B,vv.N,w,buf);
        if(dec(buf,vv.B,vv.N,w)!=v) bad++;
        checked++;
    }
    /* perf: encode+decode rep lan tren dai */
    volatile uint64_t sink=0;
    double t=now();
    for(int r=0;r<rep;r++)
        for(uint64_t v=lo; v<hi; v++){
            enc(v,vv.B,vv.N,w,buf);
            sink += dec(buf,vv.B,vv.N,w);
        }
    double dt=now()-t;
    double ops=(double)(hi-lo)*rep;
    double mcps=ops/dt/1e6;
    printf("  %-16s B=%-3d N=%d w=%d | %2dB/ma | RT %s (%llu/%llu) | %6.1f Mchar/s | %.2f ns/char | waste %.2f%%\n",
        vv.name,vv.B,vv.N,w,nbytes, bad==0?"KHOP":"SAI",(unsigned long long)(checked-bad),(unsigned long long)checked,
        mcps, 1e9/(mcps*1e6), waste/w*100.0);
    (void)sink;
}

int main(void){
    printf("=== UTF-34 BENCHMARK (encode+decode THAT bang C) ===\n");
    struct timespec ts; clock_gettime(CLOCK_REALTIME,&ts);
    printf("Dai test: 0..200.000 | rep=5 | encode roi decode, kiem round-trip\n\n");
    Variant vs[]={
        {"UTF-34 base-2",2,34},
        {"UTF-34 base-3",3,34},
        {"UTF-34 base-4",4,34},
        {"UTF-34 base-100",100,34},
        {"UTF-34 base-128",128,34},
        {"UTF-32 base-3",3,32},
        {"UTF-36 base-3",3,36},
        {"UTF-38 base-3",3,38},
    };
    for(int i=0;i<(int)(sizeof(vs)/sizeof(vs[0]));i++)
        run(vs[i], 0, 200000ULL, 5);
    printf("\nHET. Tat ca chay THAT tren may nay, khong mo phong.\n");
    return 0;
}
