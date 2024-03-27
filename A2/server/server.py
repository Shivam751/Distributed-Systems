from flask import Flask, jsonify, request
from mysql.connector.errors import Error
import os
import mysql.connector


class SQLHandler:
    def __init__(self, host='localhost', user='root', password='abc'):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        connected = False
        while not connected:
            try:
                self.mydb = mysql.connector.connect(
                    host=self.host, user=self.user, password=self.password)
                connected = True
            except Exception:
                pass

    def query(self, sql, value=None):
        if not hasattr(self, 'mydb') or self.mydb is None:
            self.connect()
        cursor = self.mydb.cursor()
        if value is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, value)
        res = cursor.fetchall()
        cursor.close()
        self.mydb.commit()
        return res

    def querymany(self, sql, values):
        if not hasattr(self, 'mydb') or self.mydb is None:
            self.connect()
        cursor = self.mydb.cursor()
        cursor.executemany(sql, values)
        res = cursor.fetchall()
        cursor.close()
        self.mydb.commit()
        return res

    def hasDB(self, dbname):
        res = self.query("SHOW DATABASES")
        return dbname in [r[0] for r in res]

    def UseDB(self, dbname):
        if not self.hasDB(dbname):
            self.query(f"CREATE DATABASE {dbname}")
        self.query(f"USE {dbname}")

    def DropDB(self, dbname):
        res = self.query("SHOW DATABASES")
        if dbname in [r[0] for r in res]:
            self.query(f"DROP DATABASE {dbname}")

    def CreateTable(self, tabname, columns, dtypes, prikeys):
        res = self.query("SHOW TABLES")
        if tabname not in [r[0] for r in res]:
            dmap = {'number': 'INT', 'string': 'VARCHAR(255)', 'float': 'FLOAT', 'double': 'DOUBLE',
                    'date': 'DATE', 'datetime': 'DATETIME', 'boolean': 'BOOLEAN', 'char': 'CHAR(1)', }
            col_config = ''
            for col, dtype in zip(columns, dtypes):
                constraint = 'PRIMARY KEY' if col in prikeys else ''
                col_config += f"{col} {dmap[dtype.lower()]} {constraint}, "
            col_config = col_config.rstrip(', ')
            self.query(f"CREATE TABLE {tabname} ({col_config})")

    def Exists(self, table_name, col, val):
        res = self.query(f"SELECT * FROM {table_name} where {col}={val}")
        return len(res) > 0

    def Select(self, table_name, col=None, low=None, high=None):
        schema = self.query(f"DESCRIBE {table_name}")
        schema = [col[0] for col in schema]
        if col == None:
            rows = self.query(f"SELECT * FROM {table_name}")
        elif high == None:
            rows = self.query(f"SELECT * FROM {table_name} where {col}={low}")
        else:
            rows = self.query(
                f"SELECT * FROM {table_name} where {col} BETWEEN {low} AND {high}")

        res = [dict(zip(schema, row)) for row in rows]
        return res

    def Update(self, table_name, col, val, data):
        format = ', '.join([f'{col}=%s' for col, val in data.items()])
        values = tuple(data.values())
        self.query(
            f"UPDATE {table_name} SET {format} WHERE {col}={val}", values)

    def Insert(self, table_name, rows):
        schema = self.query(f"DESCRIBE {table_name}")
        schema = [col[0] for col in schema]

        if not all(set(row.keys()) == set(schema) for row in rows):
            raise mysql.connector.Error(
                msg="Invalid row: Does not match table schema")

        format = ", ".join(["%s"]*len(schema))
        schema = ", ".join(schema)
        values = [tuple(row.values()) for row in rows]
        self.querymany(
            f"INSERT INTO {table_name} ({schema}) VALUES ({format})", values)

    def Delete(self, table_name, col, val):
        self.query(f"DELETE FROM {table_name} WHERE {col}={val}")


app = Flask(__name__)
sql = SQLHandler()
server_name = os.environ['SERVER_NAME']


@app.route('/config', methods=['POST'])
def configure_server():
    payload = request.get_json()
    schema = payload.get('schema')
    shards = payload.get('shards')

    if not schema or not shards:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    if 'columns' not in schema or 'dtypes' not in schema or len(schema['columns']) != len(schema['dtypes']) or len(schema['columns']) == 0:
        return jsonify({"message": "Invalid schema", "status": "error"}), 400

    for shard in shards:
        sql.UseDB(dbname=shard)
        sql.CreateTable(
            tabname='studT', columns=schema['columns'], dtypes=schema['dtypes'], prikeys=['Stud_id'])

    response_message = f"{', '.join(f'{server_name}:{shard}' for shard in shards)} configured"
    response_data = {"message": response_message, "status": "success"}

    return jsonify(response_data), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


@app.route('/copy', methods=['GET'])
def copy_data():

    payload = request.get_json()

    shards = payload.get('shards')

    if not shards:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    response_data = {}
    for shard in shards:
        if not sql.hasDB(dbname=shard):
            return jsonify({"message": f"{server_name}:{shard} not found", "status": "error"}), 404
        sql.UseDB(dbname=shard)
        response_data[shard] = sql.Select(table_name='studT')
    response_data["status"] = "success"

    return jsonify(response_data), 200


@app.route('/read', methods=['POST'])
def read_data():

    payload = request.get_json()

    shard = payload.get('shard')
    Stud_id = payload.get('Stud_id')

    if not shard or not Stud_id or 'low' not in Stud_id or 'high' not in Stud_id:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    if not sql.hasDB(dbname=shard):
        return jsonify({"message": f"{server_name}:{shard} not found", "status": "error"}), 404

    sql.UseDB(dbname=shard)
    data = sql.Select(table_name="studT", col="Stud_id",
                      low=Stud_id['low'], high=Stud_id['high'])

    response_data = {"data": data, "status": "success"}

    return jsonify(response_data), 200


@app.route('/write', methods=['POST'])
def write_data():

    payload = request.get_json()

    shard = payload.get('shard')
    curr_idx = payload.get('curr_idx')
    data = payload.get('data')

    if not shard or curr_idx is None or not data:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    if not sql.hasDB(dbname=shard):
        return jsonify({"message": f"{server_name}:{shard} not found", "status": "error"}), 404

    sql.UseDB(dbname=shard)
    sql.Insert(table_name='studT', rows=data)

    curr_idx += len(data)

    response_data = {"message": "Data entries added",
                     "curr_idx": curr_idx, "status": "success"}

    return jsonify(response_data), 200


@app.route('/update', methods=['PUT'])
def update_data():

    payload = request.get_json()

    shard = payload.get('shard')
    Stud_id = payload.get('Stud_id')
    data = payload.get('data')

    if not shard or Stud_id is None or not data:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    if not sql.hasDB(dbname=shard):
        return jsonify({"message": f"{server_name}:{shard} not found", "status": "error"}), 404

    sql.UseDB(dbname=shard)
    if not sql.Exists(table_name='studT', col="Stud_id", val=Stud_id):
        return jsonify({"message": f"Data entry for Stud_id:{Stud_id} not found", "status": "error"}), 404
    sql.Update(table_name='studT', col="Stud_id", val=Stud_id, data=data)

    response_data = {
        "message": f"Data entry for Stud_id:{Stud_id} updated", "status": "success"}

    return jsonify(response_data), 200


@app.route('/del', methods=['DELETE'])
def delete_data():
    payload = request.get_json()

    shard = payload.get('shard')
    Stud_id = payload.get('Stud_id')

    if not shard or Stud_id is None:
        return jsonify({"message": "Invalid payload", "status": "error"}), 400

    if not sql.hasDB(dbname=shard):
        return jsonify({"message": f"{server_name}:{shard} not found", "status": "error"}), 404

    sql.UseDB(dbname=shard)
    if not sql.Exists(table_name='studT', col="Stud_id", val=Stud_id):
        return jsonify({"message": f"Data entry for Stud_id:{Stud_id} not found", "status": "error"}), 404
    sql.Delete(table_name='studT', col="Stud_id", val=Stud_id)

    response_data = {
        "message": f"Data entry with Stud_id:{Stud_id} removed", "status": "success"}

    return jsonify(response_data), 200


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Exception: {e}")
    if isinstance(e, Error):
        return jsonify({"message": e.msg, "status": "error"}), 400
    else:
        return jsonify({"message": "Internal server Error: check params", "status": "error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)