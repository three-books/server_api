import json
import string
import subprocess

from models import dhcp

# dhcpdConf = './test/dhcpd.conf'
dhcpdConf = '/etc/dhcp/dhcpd.conf'


def create_dhcpd_conf():
    with open(dhcpdConf, 'w') as f:
        f.write(shaping_dhcpd_conf())

    result = subprocess.run(['systemctl', 'restart', 'isc-dhcp-server'])

    return result.returncode


def shaping_dhcpd_conf():
    domain_name, name_server = dhcp.get_dhcp_config().values()
    subnet, netmask, default_gateway, range_start, range_end, range_netmask = dhcp.get_dhcp_range().values()

    fixed_ip_list = []
    fixed_ip_dict = json.loads(dhcp.get_fixed_ip())
    for item in fixed_ip_dict:
        index, ip, mac, note = item.values()
        fixed_ip_list.append(fixed_ip_template(ip, mac, index))
    fixed_ip = ''.join(fixed_ip_list)

    return template(domain_name, name_server, subnet, netmask, default_gateway,
                    range_start, range_end, range_netmask, fixed_ip)


def template(domain_name, name_server, subnet, netmask, default_gateway,
             range_start, range_end, range_netmask, fixed_ip):
    result = string.Template("""
# dhcpd.conf
option domain-name "$domainName";
option domain-name-servers $nameServer;
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
authoritative;
subnet $subnet netmask $netmask {
    option routers $defaultGateway;
    option subnet-mask $rangeNetmask;
    range dynamic-bootp $rangeStart $rangeEnd;
    $fixedIp
}
""")
    return result.substitute(domainName=domain_name,
                             nameServer=name_server,
                             subnet=subnet,
                             netmask=netmask,
                             defaultGateway=default_gateway,
                             rangeStart=range_start,
                             rangeEnd=range_end,
                             rangeNetmask=range_netmask,
                             fixedIp=fixed_ip)


def fixed_ip_template(ip, mac,index):
    result = string.Template("""
    host host$index {
        hardware ethernet $mac;
        fixed-address $ip;
    }""")
    return result.substitute(index=index, mac=mac, ip=ip)


if __name__ == '__main__':
    shaping_dhcpd_conf()
