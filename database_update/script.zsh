#按照TPIA数据上的map中的K序号，从kegg上下载K，
cat /Users/chunfu/Desktop/Li\ lab/茶氨酸/KEGG/KOMap/map*.txt | while read id; 
do wget -c -nc http://rest.kegg.jp/get/$id; 
done

#提取K文件中的DELINK的酶相关序号，并整理成list
cat /Users/chunfu/Desktop/Li\ lab/茶氨酸/K_files/K* \
|grep DBLINKS | cut -d ' ' -f 7- | tr ' ' '\n' >RN.txt

#利用正则表达式去杂和去重
cat /Users/chunfu/Desktop/Li lab/茶氨酸/RN.txt | grep ^R RN.txt > RN2.txt
sort RN2.txt | uniq > RN3.txt

#按照TPIA数据上的K中的R序号，从kegg上下载R，
cat /Users/chunfu/Desktop/Li\ lab/茶氨酸/R_files/RN3.txt | while read id; 
do wget -c -nc http://rest.kegg.jp/get/$id; 
done