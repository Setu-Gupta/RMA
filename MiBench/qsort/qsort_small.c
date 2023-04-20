#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <marker.h>

#define UNLIMIT
#define MAXARRAY 60000 /* this number, if too large, will cause a seg. fault!! */

struct myStringStruct {
        char qstring[128];
};

int compare(const void *elem1, const void *elem2)
{
        add_marker(3);
        int result;

        result = strcmp((*((struct myStringStruct *)elem1)).qstring, (*((struct myStringStruct *)elem2)).qstring);

        return (result < 0) ? 1 : ((result == 0) ? 0 : -1);
}


int
main(int argc, char *argv[]) {
        add_marker(START);
        struct myStringStruct array[MAXARRAY];
        FILE *fp;
        int i,count=0;

        if (argc<2) {
                fprintf(stderr,"Usage: qsort_small <file>\n");
                add_marker(END);
                exit(-1);
        }
        else {
                fp = fopen(argv[1],"r");

                while((fscanf(fp, "%s", &array[count].qstring) == 1) && (count < MAXARRAY)) {
                        add_marker(1);
                        count++;
                }
        }
        printf("\nSorting %d elements.\n\n",count);
        qsort(array,count,sizeof(struct myStringStruct),compare);

        for(i=0;i<count;i++)
        {
                printf("%s\n", array[i].qstring);
                add_marker(2);
        }
        add_marker(END);
        return 0;
}
