import requests

print('get---start---------------')
g_c = requests.get('http://127.0.0.1:5000/dhcp/config')
print(g_c.text)
g_r = requests.get('http://127.0.0.1:5000/dhcp/range')
print(g_r.text)
g_f = requests.get('http://127.0.0.1:5000/dhcp/fixed-ip')
print(g_f.text)
print('get---end-----------------')

print('put---start---------------')
p_c = requests.put('http://127.0.0.1:5000/dhcp/config', {'domain_name': 'qwer', 'server_name': 'yuio'})
print(p_c.text)
p_r = requests.put('http://127.0.0.1:5000/dhcp/range', {'subnet': '10.0.0.0', 'netmask': '255.0.0.0',
                                                        'default_gateway': '10.0.0.1', 'range_start': '10.1.0.100',
                                                        'range_end': '10.1.0.200', 'range_netmask': '255.255.255.0'})
print(p_r.text)
print('put---end----------------')