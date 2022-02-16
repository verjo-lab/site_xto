#/usr/bin/awk -f
{
    copy=0;

    for (i=1;i<=NF;i++)
    {
        j=index($i,",");
        if (j>0)
        {
            fields[i]=substr($i,j+1);
            $i=substr($i,1,j-1);
            copy=1
        }
        else fields[i]=$i;
    }
    print;

    if (copy==1)
    {
        for (i=1;i<NF;i++) printf("%s%s",fields[i],OFS);
        printf("%s%s",fields[NF],ORS)
    }
}