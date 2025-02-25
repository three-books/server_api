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
            MAC_ADDRESS VARCHAR(20),
            NOTE VARCHAR(200)
        );
    """
    exec_db(fixed_ip)

    account = """
        CREATE TABLE ACCOUNT (
            ID VARCHAR(35),
            PASSWORD VARCHAR(35)
        );
    """
    exec_db(account)


def insert_data():
    dhcp_config = """
        INSERT INTO DHCP_CONFIG 
        VALUES("alt.com", "202.224.32.1, 202.224.32.2");
    """
    exec_db(dhcp_config)

    dhcp_range = """
        INSERT INTO DHCP_RANGE
        VALUES("192.168.2.0", "255.255.255.0", "192.168.2.1", "192.168.2.100", "192.168.2.200", "255.255.255.0")
    """
    exec_db(dhcp_range)

    fixed_ip = """
        INSERT INTO FIXED_IP 
        VALUES("1", "192.168.2.8", "BC:6E:E2:37:3F:61", "302-PC013-wifi"),
        ("2", "192.168.2.9", "68:E1:DC:13:41:8C", "302-PC013-eth")
        
    """
    exec_db(fixed_ip)

    account = """
        INSERT INTO ACCOUNT 
        VALUES("admin", "admin")
    """
    exec_db(account)


def test():
    db = sqlite3.connect(
        'server_api.db',
        isolation_level=None,
    )
    sql = 'select * from ACCOUNT WHERE ID=? AND PASSWORD=?;'
    result = db.execute(sql, ('admin', 'admin'))
    print(result.fetchone())
    db.close()


def main():
    create_db()
    create_table()
    insert_data()
    test()


if __name__ == '__main__':
    main()
