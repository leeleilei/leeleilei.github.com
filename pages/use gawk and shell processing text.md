# 烦恼
如果你的工作中有这样的场景，请义无反顾的使用 gawk 和 shell toolkit

1. 我有一个2G大小的文件要处理，
2. 我担心处理耗时过大，内存泄漏
3. 我想提取其中的几列
4. 如果所在行有bala-bala，我并不想提取
5. 其中有些行并不是CSV结构，我想格式化
6. 我想格式化这个类似XML结构的文本
7. 我想快速排序
8. 我想按第2,3列排序
9. 我想对比两个文件的不同
10. 我想分割文件
11. 我想合并文件

# 对比不同

        # diff -y --suppress-common-lines foo1.txt foo2.txt
        line3 line3 value2       | line2 line2 value
                                 > line3 line3 value3
                                 > line4 line4 value4
                                 > line5 line5 value5
    

# 提取某些`行值`

## 提取ISDN
    
        # cat huabiao.txt | grep -oP "MSISDN=[0-9]{10,13}" | sed 's/MSISDN=//g' > isdn
    
## 提取ISDN，IMSI和PDP
    
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
    

__Note: 由于gawk可以无声名的使用变量，并且是pattern重复处理stream，一定记得将关键变量初始话，否则上一条记录的变量带给下一条记录。__

# 排序并排除重复记录

        # sort -u foo.txt > foo.new
        # sort foo.txt |uniq > foo.new
        # sort -t "," -k2 -u foo.txt

# KI变换
The source,

        123120123456789 abcdef0123456789abcdef0123456789 1 2 3
    
The target,
    
        123120123456789 abcdef0123456789abcdef0123456789 3 2 1 0 @ 0
    
The transform,

        # cat e.txt | awk ‘{print $1,$2,$5,$4,$3,”0 @ 0″}’ > h.txt &
    
---
Last Update: Sep 6, 2013 23:22 @Manila
