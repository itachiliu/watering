import pymysql

def insert_environmental_data(
    humidity, temperature, light_intensity, soil_type, timestamp, device_id
):
    connection = pymysql.connect(
        host='shuttle.proxy.rlwy.net',
        user='root',
        password='ThFOXYGhUpOUJISvyvEeEcHmrcHXYANv',
        database='railway',
        port=57904,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO humidity
            (humidity, temperature, light_intensity, soil_type, timestamp, device_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                humidity, temperature, light_intensity, soil_type, timestamp, device_id
            ))
        connection.commit()
        print("数据写入成功！")
    finally:
        connection.close()

if __name__ == "__main__":
    # 示例数据
    insert_environmental_data(
        humidity=45,
        temperature=22,
        light_intensity=300,
        soil_type=1,
        timestamp="2025-05-30 10:00:00",
        device_id="sensor_001"
    )