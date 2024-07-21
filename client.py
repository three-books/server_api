import requests

# print('get---start---------------')
# g_c = requests.get('http://127.0.0.1:5000/dhcp/config')
# print(g_c.text)
# g_r = requests.get('http://127.0.0.1:5000/dhcp/range')
# print(g_r.text)
# g_f = requests.get('http://127.0.0.1:5000/dhcp/fixed-ip')
# print(g_f.text)
# g_l = requests.get('http://127.0.0.1:5000/dhcp/leases')
# print(g_l.text)
# print('get---end-----------------')
#
# print('put---start---------------')
# p_c = requests.put('http://127.0.0.1:5000/dhcp/config', {'domain_name': 'qwer', 'server_name': 'yuio'})
# print(p_c.text)
# p_r = requests.put('http://127.0.0.1:5000/dhcp/range', {'subnet': '10.0.0.0', 'netmask': '255.0.0.0',
#                                                         'default_gateway': '10.0.0.1', 'range_start': '10.1.0.100',
#                                                         'range_end': '10.1.0.200', 'range_netmask': '255.255.255.0'})
# print(p_r.text)
# p_f = requests.put('http://127.0.0.1:5000/dhcp/fixed-ip', {'id': '2', 'ip': '192.168.99.99',
#                                                            'mac': 'AB:CD:EF:GH:IJ:KL',
#                                                            'note': 'test'})
# print(p_f.text)
# print('put---end----------------')
#
# print('post---start---------------')
# post_f = requests.post('http://127.0.0.1:5000/dhcp/fixed-ip', {'ip': '192.168.99.88',
#                                                                'mac': 'AB:CD:EF:GH:IJ:88',
#                                                                'note': 'testNote'})
# print(post_f.text)
# print('post---end----------------')
# print('delete---start---------------')
# d_f = requests.delete('http://127.0.0.1:5000/dhcp/fixed-ip', data={'id': 1})
# print(d_f.text)
# print('delete---end----------------')
#
# print('-------------------------------------------------------------------------------------------')
# post_a = requests.post('http://127.0.0.1:5000/auth', {'id': 'admin', 'password': 'admin'})
# print(post_a.text)
# print('-------------------------------------------------------------------------------------------')
#
requests.get('http://127.0.0.1:5000/test')