# a Database Wrapper for Redis and MySQL

## from DBService import MysqlService

### 
        mysql_server = MysqlService(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT)
        # query
        mysql_server.query("SELECT * FROM TABLE")
        # execute
        mysql_server.execute("UPDATE from TABLES SET a = 55 WHERE id = 1")
        # transaction
        mysql_server.query(["UPDATE from TABLES SET a = 55 WHERE id = 1","UPDATE from TABLES SET a = 545 WHERE id = 2"])

## from DBService import RedisService

        redis_server = RedisService("redis://:user@host:port/db")