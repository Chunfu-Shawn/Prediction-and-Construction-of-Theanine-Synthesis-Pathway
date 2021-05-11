import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='Xiao13975431861',
                       db='igem')
cur = conn.cursor()


def load_csv(csv_file_path, table_name,  database):
    file = open(csv_file_path, 'r', encoding='utf-8')
    # 读取csv文件第一行字段名，创建表
    reader = file.readline()
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),'
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8mb4;'
    data_sql = """LOAD DATA LOCAL INFILE '%s' INTO TABLE '%s' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;""" % (csv_file_path, table_name)
    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 执行语句，导入数据
    cur.execute(create_sql)
    cur.execute(data_sql)
    conn.commit()
    # 关闭连接
    conn.close()
    cur.close()


def main():

    load_csv("F:\python\compound_end.csv", "compounds", "igem")


if __name__ == "__main__":
    main()
