import sys
import requests
import os

# 屏蔽warning信息，因为下面verify=False会报警告信息
requests.packages.urllib3.disable_warnings()


def download(url, file_path):
    # verify=False 这一句是为了有的网站证书问题，为True会报错
    r = requests.get(url, stream=True, verify=False)

    # 既然要实现下载进度，那就要知道你文件大小啊，下面这句就是得到总大小
    total_size = int(r.headers['Content-Length'])
    temp_size = 0

    with open(file_path, "w") as f:
        # iter_content()函数就是得到文件的内容，
        # 有些人下载文件很大怎么办，内存都装不下怎么办？
        # 那就要指定chunk_size=1024，大小自己设置，
        # 意思是下载一点写一点到磁盘。
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                #############花哨的下载进度部分###############
                done = int(50 * temp_size / total_size)
                # 调用标准输出刷新命令行，看到\r回车符了吧
                # 相当于把每一行重新刷新一遍
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符，执行完后需要换行了，不然都在一行显示


if __name__ == '__main__':

    num = 0
    while True:
        link = r'http://rest.kegg.jp/get/'
        UUID = r'2a4a3044-0b1a-4722-83ed-43ba5d6d25b0'
        # path是下载文件保存的路径
        path = r'F:\IGEM\PATHub\database\KEGG\enzyme_info'
        # url是文件网址链接
        url = os.path.join(link, UUID)
        f1 = open(r'F:\IGEM\PATHub\database\KEGG\all_enzyme_ecnum', 'r')
        for line in f1:
            if num == 0:
                link += line
            else:
                link += '+' + line
            num += 1
            while num == 10:
                # 调用上面下载函数即可
                download(url, path)
