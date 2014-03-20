# Headache
If you were suffering below boring issues, I recommend you using "gawk and shell", no excuse.

1. I got a 2G text file
2. I am warried about the memory leak or overflow
3. I need extract several column of text file
4. If the line match something, actually I don't need put in column result
5. I need transform the structured text to CSV
6. I need fast sort
7. I need sort by specific columns
8. I need get the differences of 2 files
9. I want split
10. I want combination

# Compare

        # diff -y --suppress-common-lines foo1.txt foo2.txt
        line3 line3 value2       | line2 line2 value
                                 > line3 line3 value3
                                 > line4 line4 value4
                                 > line5 line5 value5
    

# Extract `lines`

## Extract ISDN
    
        # cat huabiao.txt | grep -oP "MSISDN=[0-9]{10,13}" | sed 's/MSISDN=//g' > isdn
    
## Extract ISDN，IMSI and PDP
    
        # cat huawei_01.txt | awk '{
            if($0 ~ /MSISDN=/) {
                isdn=$0
            }
            if($0 ~ /PDPCNTX=/) {
                pdp=$0
            }
            if($0 ~ /SUBEND/) {
                print isdn,pdp
            }
            isdn=""
            pdp=""
        }' > isdn.pdp.txt
    

## Multiple PDP
    
    
        # cat huawei_01.txt | awk '{
            if($0 ~ /MSISDN=/) {
                isdn=$0
            }
        
            if($0 ~ /PDPCNTX=/) {
                if(len(pdp)==0) ｛
                    pdp=$0
                }
                else {
                    pdp=pdp" "$0
                }
            }
        
            if($0 ~ /SUBEND/) {
                print isdn,pdp
            }
            isdn=""
            pdp=""
        }' > isdn.pdp.txt
    

__Note: gawk use implicit varible, and the pattern is gonna applied on **each line**, remember initialize the **reused** varible at end of pattern, such as isdn, imsi, pdp in above sample__

# Sort

        # sort -u foo.txt > foo.new
        # sort foo.txt |uniq > foo.new
        # sort -t "," -k2 -u foo.txt

# KI Transform
The source: `e.txt`,

        123120123456789 abcdef0123456789abcdef0123456789 1 2 3
    
The target: `h.txt`,
    
        123120123456789 abcdef0123456789abcdef0123456789 3 2 1 0 @ 0
    
The transformer,

        # cat e.txt | awk '{print $1,$2,$5,$4,$3,0 @ 0}' > h.txt
    
---
Last Update: Sep 6, 2013 23:22 @Manila



Text File Comparison and Selection
Compare with diff
Single Column Compare

Single Column v.s. Double Columns or More

Dual Columns v.s. More Columns

Selection with diff
Single Column Selection from Multiple Columns

Multiple Columns selections from Multiple Columns


Selection with SQLITE3
tip: [todo]a flask app tool to easily implement this fast and flexible.


AWK
Get MSISDN and PDPCNTX from huabiao File
#cat huawei_01.txt | awk '{
    if($0 ~ /MSISDN=/) {
        isdn=$0
    }
    if($0 ~ /PDPCNTX=/) {
        pdp=$0
    }
    if($0 ~ /SUBEND/) {
        print isdn,pdp
    }
    isdn=""
    pdp=""
}' > isdn.pdp.txt

Q1: Multiple PDP
Question1: if you have multiple pdp lines, only last pdp would be output, since it is overwritten by pdp=$0
Solution1: judge the pdp varible, so it would be 

#cat huawei_01.txt | awk '{
    if($0 ~ /MSISDN=/) {
        isdn=$0
    }

    if($0 ~ /PDPCNTX=/) {
        if(len(pdp)==0) ｛
            pdp=$0
        }
        else {
            pdp=pdp" "$0
        }
    }

    if($0 ~ /SUBEND/) {
        print isdn,pdp
    }
    isdn=""
    pdp=""
}' > isdn.pdp.txt

Q2: Forget isdn="" or pdp=""
Question1: if you didn't put the isdn="", pdp="", what will happen
Solution1: Since the awk is kind a stream, exactly line stream editor, so the code segment will be applied on each every LINES, if we didn't restore the value to default ""/none, the NONE-matched lines would use the last "MATCHED" line's value to print out there


Remove Duplicated Lines

1. if your file is non-sequence-sensitive, just a sort

suppose your file name is foo.txt
te…@sexy.com$ sort -u foo.txt > foo.uniq

equal to
te…@sexy.com$ sort foo.txt | uniq > foo.uniq


2. if your file requires keeping the sequence after deleting the duplicated line

suppose the file name is foo.txt, and its format is csv, like

name,passwd,mail,home,tel1,tel2,tel3

“number it first, then sort it with -u, then sort it with the number”

get the numbered file

cat foo.txt | awk ‘{

    printf(“%s,%s\n”,NR,$0)

}’ > foo.tmp

sort the specific content (n column)
sort -t “,” -k2 -u foo.tmp > foo.tmp2

according to your number, sort it again
sort -t “,” -n -k1 foo.tmp2 > foo.tmp3

cut the number, if you don’t wanna keep it, :>
cut -f2- -d”,” foo.tmp3 > foo.uniq

done


Transform the KI

In the migration process, we need transform the E// KI file to the H// formatted,

The source format, e.txt

123120123456789 abcdef0123456789abcdef0123456789 1 2 3

the target format, h.txt

123120123456789 abcdef0123456789abcdef0123456789 3 2 1 0 @ 0


the transformation via the AWK
cat e.txt | awk ‘{print $1,$2,$5,$4,$3,”0 @ 0″}’ > h.txt &

Conclusion: the awk is really good at the structured lines data parsing and re-construction. Later I will show a complex one



Shell
Rename it

I used a lot Bash to handling the text file, as simple as better, usually I would add the prefix before the original file. Suppose the file is foo.txt, finally it would be more like final.sort.tmp.foo.txt. Ugly, isn't it? But easy to use with sort.$fp
There is a way you can change the files' name at the end when your work is totally finished. See you have a file list like this,
final.sort.tmp.foo1.txt
final.sort.tmp.foo2.txt
final.sort.tmp.foo3.txt
final.sort.tmp.foo4.txt
...
And we wanna them to foo1.mkv, foo2.mkv, foo3.mkv ...

    find . -name *.txt | awk '{FS=".";printf("%s.mkv\n",$4)}' | sh

or you love 'seed' <sed>

    find . -name *.txt | sed 's/.*\.\(foo.*\.\).*/mv "&" \1.mkv/g' | sh

As you always feels, "AWK" looks more meaningful.

There is a alternative solution


for fp in `ls`
do
    NEWNAME=`echo $fp| sed 's/\.new//'`
    mv $fp $NEWNAME`
done

OR you can

expr substr $name 1 8
Get MSISDN
$ cat huabiao*.txt | grep -oP “MSISDN=[0-9]{13}” | sed ‘s/MSISDN=//g’ > isdn.txt

cat huabiao*.txt, will display all of the files with “huabiao” prefix
grep -oP, will use the “perl” syntax to __ONLY__ find out the matched ones
sed ‘s/pattern/repl/g’ will find the “MSISDN”, replace it with “nothing” for all matches

Tip: sometimes it is difficult to get it done by a shell line, but you can use the PIPE "|" to make it happening in several steps. 



