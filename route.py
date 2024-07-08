from flask import Flask
from flask import request

from models import dhcp

app = Flask(__name__)


@app.route('/dhcp/config', methods=['GET', 'PUT'])
def dhcp_config():
    if request.method == 'GET':
        result = dhcp.get_dhcp_config()
        return result

    if request.method == 'PUT':
        domain_name = request.values.get('domain_name')
        server_name = request.values.get('server_name')
        result = dhcp.put_dhcp_config(domain_name, server_name)
        return result


@app.route('/dhcp/range', methods=['GET', 'PUT'])
def dhcp_range():

    if request.method == 'GET':
        result = dhcp.get_dhcp_range()
        return result

    if request.method == 'PUT':
        subnet = request.values.get('subnet')
        netmask = request.values.get('netmask')
        default_gateway = request.values.get('default_gateway')
        range_start = request.values.get('range_start')
        range_end = request.values.get('range_end')
        range_netmask = request.values.get('range_netmask')
        result = dhcp.put_dhcp_range(subnet, netmask, default_gateway, range_start, range_end, range_netmask)
        return result


@app.route('/dhcp/fixed-ip', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dhcp_fixed_ip():
    if request.method == 'GET':
        result = dhcp.get_fixed_ip()
        return result

    if request.method == 'POST':
        ip = request.values.get('ip')
        mac = request.values.get('mac')
        result = dhcp.post_fixed_ip(ip, mac)
        return result

    if request.method == 'PUT':
        key_id = request.values.get('id')
        ip = request.values.get('ip')
        mac = request.values.get('mac')
        result = dhcp.put_fixed_ip(key_id, ip, mac)
        return result

    if request.method == 'DELETE':
        key_id = request.values.get('id')
        result = dhcp.delete_fixed_ip(key_id)
        return result

def main():
    app.run()


if __name__ == '__main__':
    main()
