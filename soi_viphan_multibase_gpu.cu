/* SOI-VI-PHAN ∂̂ đa-base trên GPU — tính len_B(n), digitsum_B(n) cho 4 base SONG SONG.
 * 1 thread = 1 mã n; mỗi base một mảng. Sau đó Δ (sai phân) lộ mốc lũy thừa base.
 * nvcc -O3 -arch=sm_86 -o svmb soi_viphan_multibase_gpu.cu && ./svmb
 */
#include <cstdio>
#include <cuda_runtime.h>
__constant__ int BASES[4]={2,3,4,100};

/* moi thread: mot ma n, mot base -> len_B(n) va digitsum_B(n) */
__global__ void per_base(int* len,int* dsum,int N){
  int n=blockIdx.x*blockDim.x+threadIdx.x; int bi=blockIdx.y; if(n>=N) return;
  int B=BASES[bi]; long v=n; int L=0,S=0;
  if(v==0){L=1;} else { while(v){S+=v%B; v/=B; L++; } }
  len[bi*N+n]=L; dsum[bi*N+n]=S;
}
/* Δ sai phân: out[n]=f[n+1]-f[n] — soi "so be li ti" 1 LSB, song song */
__global__ void delta(const int* f,int* d,int N){
  int n=blockIdx.x*blockDim.x+threadIdx.x; int bi=blockIdx.y;
  if(n<N-1) d[bi*N+n]=f[bi*N+n+1]-f[bi*N+n];
}
int main(){
  cudaDeviceProp p;cudaGetDeviceProperties(&p,0);
  printf("SOI-VI-PHAN da-base GPU — %s\n",p.name);
  const int N=6561; int hbase[4]={2,3,4,100};
  int *dlen,*dsum,*ddlt; cudaMalloc(&dlen,4*N*sizeof(int));cudaMalloc(&dsum,4*N*sizeof(int));cudaMalloc(&ddlt,4*N*sizeof(int));
  dim3 blk(256), grd((N+255)/256,4);
  per_base<<<grd,blk>>>(dlen,dsum,N);
  delta<<<grd,blk>>>(dlen,ddlt,N);            /* Δlen_B song song */
  cudaDeviceSynchronize();
  int* hl=(int*)malloc(4*N*sizeof(int)); int* hd=(int*)malloc(4*N*sizeof(int));
  cudaMemcpy(hl,dlen,4*N*sizeof(int),cudaMemcpyDeviceToHost);
  cudaMemcpy(hd,ddlt,4*N*sizeof(int),cudaMemcpyDeviceToHost);
  for(int bi=0;bi<4;bi++){
    printf("base %3d: len(N-1)=%d | Δlen nhay tai: ",hbase[bi],hl[bi*N+N-1]);
    int cnt=0; for(int n=0;n<N-1&&cnt<6;n++) if(hd[bi*N+n]!=0){printf("%d ",n+1);cnt++;}
    printf(" (luy thua %d)\n",hbase[bi]);
  }
  printf("\n∂̂ GPU: 4 base × %d mã song song; Δ soi mốc lũy thừa từng base.\n",N);
  cudaFree(dlen);cudaFree(dsum);cudaFree(ddlt);free(hl);free(hd);return 0;
}
