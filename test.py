import pymysql

def get_conn():
    """ Get a connection to the RDS database

    Returns:
        pymysql.connect: Connection to the RDS database
    """
    return pymysql.connect(
        host='predimodbinstance.cbiog1ld7y5x.eu-west-1.rds.amazonaws.com',
        db='predimmo',
        user='admin',
        password='N8XR3u#m9[5Mk6UK',
        port=3306)

conn = get_conn()

sql = """
UPDATE data_django
SET latitude = 48.862121
WHERE latitude = 48.845"""

# sql = "SELECT * from data_django where longitude = 2.3752 and latitude = 48.845"
with conn.cursor() as cursor:
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    print(result)

