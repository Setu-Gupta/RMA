/* +++Date last modified: 05-Jul-1997 */

/*
 **  BITFILES.C - reading/writing bit files
 **
 **  Public domain by Aare Tali
 */

#include <stdlib.h>
#include "bitops.h"
#include <marker.h>

bfile *bfopen(char *name, char *mode)
{
        add_marker(1);
        bfile * bf;

        bf = malloc(sizeof(bfile));
        if (NULL == bf)
        {
                add_marker(2);
                return NULL;
        }
        bf->file = fopen(name, mode);
        if (NULL == bf->file)
        {
                add_marker(3);
                free(bf);
                return NULL;
        }
        bf->rcnt = 0;
        bf->wcnt = 0;
        add_marker(4);
        return bf;
}

int bfread(bfile *bf)
{
        add_marker(5);
        if (0 == bf->rcnt)          /* read new byte */
        {
                add_marker(6);
                bf->rbuf = (char)fgetc(bf->file);
                bf->rcnt = 8;
        }
        bf->rcnt--;
        add_marker(7);
        return (bf->rbuf & (1 << bf->rcnt)) != 0;
}

void bfwrite(int bit, bfile *bf)
{
        add_marker(8);
        if (8 == bf->wcnt)          /* write full byte */
        {
                add_marker(9);
                fputc(bf->wbuf, bf->file);
                bf->wcnt = 0;
        }
        bf->wcnt++;
        bf->wbuf <<= 1;
        bf->wbuf |= bit & 1;
        add_marker(10);
}

void bfclose(bfile *bf)
{
        add_marker(11);
        fclose(bf->file);
        free(bf);
}

#ifdef TEST

void test1(void)
{
        add_marker(12);
        bfile *out;
        bfile *in;
        FILE  *in1;
        FILE  *in2;

        in = bfopen("bitfiles.c", "rb");
        out = bfopen("bitfiles.cc", "wb");
        if ((NULL == in) || (NULL == out))
        {
                add_marker(13);
                printf("Can't open/create test files\n");
                exit(1);
        }
        while (!feof(in->file))
        {
                add_marker(14);
                bfwrite(bfread(in), out);
        }
        bfclose(in);
        bfclose(out);
        in1 = fopen("bitfiles.c", "rb");
        in2 = fopen("bitfiles.cc", "rb");
        if ((NULL == in1) || (NULL == in2))
        {
                add_marker(15);
                printf("Can't open test files for verifying\n");
                exit(1);
        }
        while (!feof(in1) && !feof(in2))
        {
                add_marker(16);
                if (fgetc(in1) != fgetc(in2))
                {
                        add_marker(17);
                        printf("Files not identical, copy failed!\n");
                        exit(1);
                }
        }
        if (!feof(in1) || !feof(in2))
        {
                add_marker(18);
                printf("Not same size, copy failed!\n");
                exit(1);
        }
        fclose(in1);
        fclose(in2);
}

void test2(void)
{
        FILE  *in1;
        bfile *in2;
        int    ch;
        
        add_marker(19);
        in1 = fopen("bitfiles.c", "rb");
        in2 = bfopen("bitfiles.cc", "rb");
        if ((NULL == in1) || (NULL == in2))
        {
                add_marker(20);
                printf("Can't open test files\n");
                exit(1);
        }
        while (!feof(in1) && !feof(in2->file))
        {
                add_marker(21);
                ch = fgetc(in1);
                if (ch < ' ')
                {
                        add_marker(22);
                        ch = '.';
                }
                printf(" '%c' ", ch);
                for (ch = 0; ch < 8; ch++)
                {
                        add_marker(23);
                        printf("%c", "01"[bfread(in2)]);
                }
                printf("   ");
        }
        fclose(in1);
        bfclose(in2);
        add_marker(24);
}

main()
{
        add_marker(START);
        test1();
        test2();
        add_marker(END);
        return 0;
}

#endif /* TEST */
