import sqlite3
import subprocess

from flask import Flask
from flask import g

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('./db/server_api.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_dhcp_config():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'SELECT * FROM DHCP_CONFIG;'
    )
    domain_name, name_server = curs.fetchone()
    result = {'domainName': domain_name,
              'nameServer': name_server
              }
    curs.close()
    return result


def put_dhcp_config(domain_name, name_server):
    db = get_db()
    curs = db.cursor()
    sql = 'UPDATE DHCP_CONFIG SET DOMAIN_NAME = ?, NAME_SERVER = ?;'
    curs.execute(sql, (domain_name, name_server))
    db.commit()
    result = get_dhcp_config()

    return result


def get_dhcp_range():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'SELECT * FROM DHCP_RANGE;'
    )
    subnet, netmask, default_gateway, range_start, range_end, range_netmask = curs.fetchone()

    result = {'subnet': subnet,
              'netmask': netmask,
              'defaultGateway': default_gateway,
              'rangeStart': range_start,
              'rangeEnd': range_end,
              'rangeNetmask': range_netmask
              }
    curs.close()
    return result


def put_dhcp_range(subnet, netmask, default_gateway, range_start, range_end, range_netmask):
    db = get_db()
    curs = db.cursor()
    sql = """
        UPDATE DHCP_RANGE SET
        SUBNET = ?,
        NETMASK = ?,
        DEFAULT_GATEWAY = ?,
        RANGE_START = ?,
        RANGE_END = ?,
        RANGE_NETMASK = ?;
    """
    curs.execute(sql, (subnet, netmask, default_gateway, range_start, range_end, range_netmask))
    db.commit()

    result = get_dhcp_range()
    return result


def get_fixed_ip():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'SELECT * FROM FIXED_IP;'
    )
    result = []
    for i, item in enumerate(curs.fetchall()):
        no, ip, mac, note = item
        result.append({'no': no,
                       'ip': ip,
                       'mac': mac,
                       'note': note})

    curs.close()
    return result


def post_fixed_ip(ip, mac, note):
    db = get_db()
    curs = db.cursor()
    curs.execute('SELECT MAX(ID) FROM FIXED_IP;')
    key = int(curs.fetchone()[0]) + 1
    sql = 'INSERT INTO FIXED_IP VALUES (?,?,?,?);'
    curs.execute(sql, (key, ip, mac, note))
    db.commit()

    result = get_fixed_ip()
    return result


def put_fixed_ip(key, ip, mac, note):
    db = get_db()
    curs = db.cursor()
    sql = """
        UPDATE FIXED_IP SET
        IP = ?,
        MAC_ADDRESS = ?,
        NOTE = ?
        WHERE ID = ?;
    """
    curs.execute(sql, (ip, mac, note, key))
    db.commit()
    result = get_fixed_ip()
    return result


def delete_fixed_ip(key):
    db = get_db()
    curs = db.cursor()
    # curs.execute(f'DELETE FROM FIXED_IP WHERE ID = "{key}";')
    sql = 'DELETE FROM FIXED_IP WHERE ID = ?;'
    curs.execute(sql, (key,))
    db.commit()
    result = get_fixed_ip()
    return result


def get_leases():
    output_str = subprocess.run('dhcp-lease-list', capture_output=True, text=True).stdout

    isNeedData = False
    needDataList = []

    for row in output_str.splitlines():

        if isNeedData:
            needDataList.append(row)

        if row.startswith('================='):
            isNeedData = True

    result = []
    for row in needDataList:
        rowList = row.split()

        result.append({
            'mac': rowList.pop(0),
            'ip': rowList.pop(0),
            'manufacturer': rowList.pop(-1),
            'time': rowList.pop(-1),
            'date': rowList.pop(-1),
            'hostname': ' '.join(rowList)})

    # result = [{'mac': '68:e1:dc:13:41:8c', 'ip': '10.0.0.100', 'manufacturer': '-NA-', 'time': '09:12:05',
    #            'date': '2024-06-26', 'hostname': 'DESKTOP-FPE8SQ'},
    #           {'mac': 'b8:27:eb:50:93:53', 'ip': '10.0.0.103', 'manufacturer': '-NA-', 'time': '15:01:17',
    #            'date': '2024-06-26', 'hostname': '-NA-'},
    #           {'mac': 'd8:3a:dd:54:1c:9a', 'ip': '10.0.0.104', 'manufacturer': '-NA-', 'time': '09:38:45',
    #            'date': '2024-06-26', 'hostname': '-NA-'}]
    return result
