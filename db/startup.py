import os
import sqlite3

from flask import Flask
from flask import g
from flask import request

app = Flask(__name__)


def create_db():
    os.remove('server_api.db')
    db = sqlite3.connect(
        'server_api.db',
        isolation_level=None,
    )
    db.close()


def exec_db(sql):
    db = sqlite3.connect(
        'server_api.db',
        isolation_level=None,
    )
    result = db.execute(sql)
    db.close()

    return result


def create_table():
    dhcp_config = """
        CREATE TABLE DHCP_CONFIG (
            DOMAIN_NAME VARCHAR(60),
            NAME_SERVER VARCHAR(60)
        );
    """
    exec_db(dhcp_config)

    dhcp_range = """
        CREATE TABLE DHCP_RANGE (
            SUBNET VARCHAR(35),
            NETMASK VARCHAR(35),
            DEFAULT_GATEWAY VARCHAR(35),
            RANGE_START VARCHAR(35),
            RANGE_END VARCHAR(35),
            RANGE_NETMASK VARCHAR(35)
        );
    """
    exec_db(dhcp_range)

    fixed_ip = """
        CREATE TABLE FIXED_IP (
            ID VARCHAR(4),
            IP VARCHAR(35),
            MAC_ADDRESS VARCHAR(20)
        );
    """
    exec_db(fixed_ip)


def insert_data():
    dhcp_config = """
        INSERT INTO DHCP_CONFIG 
        VALUES("test.com", "dns.test.com");
    """
    exec_db(dhcp_config)

    dhcp_range = """
        INSERT INTO DHCP_RANGE
        VALUES("192.168.3.0", "255.255.255.0", "192.168.3.1", "192.168.3.100", "192.168.3.200", "255.255.255.0")
    """
    exec_db(dhcp_range)

    fixed_ip = """
        INSERT INTO FIXED_IP 
        VALUES("1", "192.168.3.3", "12:34:56:ff:ff:aa"),
        ("2", "192.168.3.4", "12:34:56:ff:ff:ab"),
        ("3", "192.168.3.5", "12:34:56:ff:ff:ac")
    """
    exec_db(fixed_ip)


def test():
    sql = 'select * from DHCP_CONFIG'
    db = sqlite3.connect(
        'server_api.db',
        isolation_level=None,
    )
    result = db.execute(sql)
    print(result.fetchone())
    db.close()


def main():
    create_db()
    create_table()
    insert_data()


if __name__ == '__main__':
    main()
