#define MAGIC_NUMBER            7788
#if defined(__i386)
   #define MAGIC_REG_A "ecx"
   #define MAGIC_REG_B "edx"
#else
   #define MAGIC_REG_A "rcx"
   #define MAGIC_REG_B "rdx"
#endif

#define myMarker(magic, arg) ({                 \
   unsigned long _magic = magic, _arg = arg;    \
   __asm__ __volatile__ (                       \
   "mov %0, %%" MAGIC_REG_A "\n"                \
   "\tmov %1, %%" MAGIC_REG_B "\n"              \
   "\txchg %%bx, %%bx\n"                        \
   :                    /* no outputs*/         \
   : "g"(_magic),       /* inputs    */         \
     "g"(_arg)                                  \
   : "%" MAGIC_REG_A,   /* clobbered */         \
     "%" MAGIC_REG_B );                         \
})

#define add_marker(arg) myMarker(MAGIC_NUMBER, arg)
#define START   -1
#define END     -2
