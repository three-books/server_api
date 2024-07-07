import sqlite3

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
    result = {'DOMAIN_NAME': domain_name,
              'NAME_SERVER': name_server
              }
    return result


def put_dhcp_config(domain_name, name_server):
    db = get_db()
    curs = db.cursor()
    curs.execute(
        f'UPDATE DHCP_CONFIG SET DOMAIN_NAME = "{domain_name}", NAME_SERVER = "{name_server}";'
    )
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

    result = {'SUBNET': subnet,
              'NETMASK': netmask,
              'DEFAULT_GATEWAY': default_gateway,
              'RANGE_START': range_start,
              'RANGE_END': range_end,
              'RANGE_NETMASK': range_netmask
              }

    return result


def put_dhcp_range(subnet, netmask, default_gateway, range_start, range_end, range_netmask):
    db = get_db()
    curs = db.cursor()
    curs.execute(
        f'UPDATE DHCP_RANGE SET '
        f'SUBNET = "{subnet}", '
        f'NETMASK = "{netmask}", '
        f'DEFAULT_GATEWAY = "{default_gateway}", '
        f'RANGE_START = "{range_start}", '
        f'RANGE_END = "{range_end}", '
        f'RANGE_NETMASK = "{range_netmask}"; '
    )
    db.commit()

    result = get_dhcp_range()
    return result


def get_fixed_ip():
    db = get_db()
    curs = db.cursor()
    curs.execute(
        'SELECT * FROM FIXED_IP;'
    )
    result = {}
    for item in curs.fetchall():
        no, ip, mac = item
        temp = {ip: mac}
        result[no] = temp

    return result
