/* UTF-34 BENCHMARK TOI UU byte-level — codec dung duoc that.
 * base-2/4/128 (luy thua 2): copy digit thang, khong vong bit.
 * base-3: pack 5-trit/byte base-243 (MIN-WASTE).  base-100: 2 digit/... byte-level.
 * cc -O3 -march=native -o utf34_bench_fast utf34_bench_fast.c -lm && ./utf34_bench_fast
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

/* ---------- base luy thua 2 (w bit/digit, dong khit) : encode = ghi digit theo w bit, byte-level ----------
   Voi w=1(base2),2(base4),7(base128): value <-> N digit base-2^w == chinh la value nhi phan N*w bit.
   Nen encode = viet value ra buffer little-endian; decode = doc lai. O(1) theo may. */
static inline int enc_pow2(uint64_t v,int N,int w,uint8_t*out){
    int nbytes=(N*w+7)/8; for(int i=0;i<nbytes;i++){out[i]=(uint8_t)v; v>>=8;} return nbytes;
}
static inline uint64_t dec_pow2(const uint8_t*in,int N,int w){
    int nbytes=(N*w+7)/8; uint64_t v=0; for(int i=nbytes-1;i>=0;i--) v=(v<<8)|in[i]; return v;
}
/* ---------- base-3 MIN-WASTE: 5 trit/byte base-243 ---------- */
static inline int enc_b3(uint64_t v,int N,uint8_t*out){
    uint8_t t[64]; for(int i=0;i<N;i++){t[i]=v%3;v/=3;}
    int nb=(N+4)/5; for(int i=0;i<nb;i++){int b=0;for(int j=4;j>=0;j--){int idx=i*5+j;b=b*3+(idx<N?t[idx]:0);}out[i]=(uint8_t)b;}
    return nb;
}
static inline uint64_t dec_b3(const uint8_t*in,int N){
    uint8_t t[64]; int nb=(N+4)/5;
    for(int i=0;i<nb;i++){int b=in[i];for(int j=0;j<5;j++){int idx=i*5+j;if(idx<N)t[idx]=b%3;b/=3;}}
    uint64_t v=0; for(int i=N-1;i>=0;i--) v=v*3+t[i]; return v;
}
/* ---------- base-100: 2 digit base-100 -> 1 byte? khong (100^2=10000>256). Dung 7bit/digit byte-level pack ---------- */
static inline int enc_b100(uint64_t v,int N,uint8_t*out){
    uint8_t d[64]; for(int i=0;i<N;i++){d[i]=(uint8_t)(v%100);v/=100;}
    /* pack 7-bit/digit LSB-first vao byte stream */
    int nbits=N*7,nbytes=(nbits+7)/8; memset(out,0,nbytes); int bit=0;
    for(int i=0;i<N;i++){uint8_t x=d[i];for(int b=0;b<7;b++){if((x>>b)&1)out[bit>>3]|=1<<(bit&7);bit++;}}
    return nbytes;
}
static inline uint64_t dec_b100(const uint8_t*in,int N){
    uint8_t d[64]; int bit=0;
    for(int i=0;i<N;i++){uint8_t x=0;for(int b=0;b<7;b++){if((in[bit>>3]>>(bit&7))&1)x|=1<<b;bit++;}d[i]=x;}
    uint64_t v=0; for(int i=N-1;i>=0;i--) v=v*100+d[i]; return v;
}

typedef enum{POW2,B3,B100} Kind;
typedef struct{const char*name;int B,N,w;Kind k;} V;

static void run(V vv,uint64_t hi,int rep){
    uint8_t buf[64]; uint64_t bad=0;
    /* correctness */
    for(uint64_t v=0;v<hi;v++){
        int nb; uint64_t back;
        if(vv.k==POW2){nb=enc_pow2(v,vv.N,vv.w,buf);back=dec_pow2(buf,vv.N,vv.w);}
        else if(vv.k==B3){nb=enc_b3(v,vv.N,buf);back=dec_b3(buf,vv.N);}
        else{nb=enc_b100(v,vv.N,buf);back=dec_b100(buf,vv.N);}
        (void)nb; if(back!=v)bad++;
    }
    /* perf */
    volatile uint64_t sink=0; double t=now();
    for(int r=0;r<rep;r++)for(uint64_t v=0;v<hi;v++){
        if(vv.k==POW2){enc_pow2(v,vv.N,vv.w,buf);sink+=dec_pow2(buf,vv.N,vv.w);}
        else if(vv.k==B3){enc_b3(v,vv.N,buf);sink+=dec_b3(buf,vv.N);}
        else{enc_b100(v,vv.N,buf);sink+=dec_b100(buf,vv.N);}
    }
    double dt=now()-t; double ops=(double)hi*rep; double mcps=ops/dt/1e6;
    int nbytes = vv.k==B3?(vv.N+4)/5 : (vv.N*vv.w+7)/8;
    printf("  %-16s | %2dB/ma | RT %s | %8.1f Mchar/s | %6.2f ns/char\n",
        vv.name,nbytes,bad==0?"KHOP":"SAI",mcps,1e9/(mcps*1e6));
    (void)sink;
}
int main(void){
    printf("=== UTF-34 BENCHMARK TOI UU byte-level (codec dung duoc) ===\n");
    printf("Dai 0..1.000.000 | rep=30 | encode+decode\n\n");
    V vs[]={
        {"UTF-34 base-2",2,34,1,POW2},
        {"UTF-34 base-4",4,34,2,POW2},
        {"UTF-34 base-128",128,34,7,POW2},
        {"UTF-34 base-3",3,34,2,B3},
        {"UTF-34 base-100",100,34,7,B100},
        {"UTF-32 base-3",3,32,2,B3},
        {"UTF-36 base-3",3,36,2,B3},
        {"UTF-38 base-3",3,38,2,B3},
    };
    for(int i=0;i<(int)(sizeof(vs)/sizeof(vs[0]));i++) run(vs[i],1000000ULL,30);
    printf("\nHET. Chay THAT tren may nay.\n");
    return 0;
}
