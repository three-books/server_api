from flask import Flask
from flask import request
from flask_cors import CORS

from method import CreateConfig
from models import dhcp
from models import auth

app = Flask(__name__)
CORS(app)


@app.route('/dhcp/config', methods=['GET', 'PUT'])
def dhcp_config():
    if request.method == 'GET':
        result = dhcp.get_dhcp_config()
        return result

    if request.method == 'PUT':
        domain_name = request.values.get('domain_name') or request.json['domain_name']
        server_name = request.values.get('server_name') or request.json['server_name']
        result = dhcp.put_dhcp_config(domain_name, server_name)
        return result


@app.route('/dhcp/range', methods=['GET', 'PUT'])
def dhcp_range():
    if request.method == 'GET':
        result = dhcp.get_dhcp_range()
        return result

    if request.method == 'PUT':
        subnet = request.values.get('subnet') or request.json['subnet']
        netmask = request.values.get('netmask') or request.json['netmask']
        default_gateway = request.values.get('default_gateway') or request.json['default_gateway']
        range_start = request.values.get('range_start') or request.json['range_start']
        range_end = request.values.get('range_end') or request.json['range_end']
        range_netmask = request.values.get('range_netmask') or request.json['range_netmask']
        result = dhcp.put_dhcp_range(subnet, netmask, default_gateway, range_start, range_end, range_netmask)
        return result


@app.route('/dhcp/fixed-ip', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dhcp_fixed_ip():
    if request.method == 'GET':
        result = dhcp.get_fixed_ip()
        return result

    if request.method == 'POST':
        ip = request.values.get('ip') or request.json['ip']
        mac = request.values.get('mac') or request.json['mac']
        note = request.values.get('note') or request.json['note']
        result = dhcp.post_fixed_ip(ip, mac, note)
        return result

    if request.method == 'PUT':
        key_id = request.values.get('id') or request.json['id']
        ip = request.values.get('ip') or request.json['ip']
        mac = request.values.get('mac') or request.json['mac']
        note = request.values.get('note') or request.json['note']
        result = dhcp.put_fixed_ip(key_id, ip, mac, note)
        return result

    if request.method == 'DELETE':
        key_id = request.values.get('id') or request.json['id']
        result = dhcp.delete_fixed_ip(key_id)
        return result


@app.route('/dhcp/leases', methods=['GET'])
def dhcp_leases():
    if request.method == 'GET':
        result = dhcp.get_leases()
        return result


@app.route('/auth', methods=['POST'])
def auth_login():
    if request.method == 'POST':
        account = request.values.get('id') or request.json['id']
        password = request.values.get('password') or request.json['password']
        result = auth.login(account, password)
        return result

@app.route('/test', methods=['GET'])
def test():
    if request.method == 'GET':
        CreateConfig.create_dhcpd_conf()
        return 'OK'



def main():
    app.run()


if __name__ == '__main__':
    main()
