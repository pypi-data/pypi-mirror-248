#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022

"""
this module creates tractorrc file
"""

import os
import tempfile

from . import bridges
from . import checks


def create():
    """
    main function of the module
    # TODO: refactor to more little functions
    """
    dconf = checks.dconf()
    my_ip, socks_port = checks.ip_port()
    data_dir = checks.data_dir()
    exit_node = dconf.get_string("exit-node")
    with open(bridges.get_file(), encoding="utf-8") as file:
        mybridges = file.read()
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "tractorrc")
    with open(path, "w", encoding="utf-8") as file:
        file.write(f"SocksPort {my_ip}:{str(socks_port)}\n")
        if dconf.get_boolean("accept-connection"):
            file.write("SocksPolicy accept *\n")
        dns_port_lines = (
            f"DNSPort {my_ip}:{str(dconf.get_int('dns-port'))}\n"
            "AutomapHostsOnResolve 1\n"
            "AutomapHostsSuffixes .exit,.onion\n"
        )
        file.write(dns_port_lines)
        http_port = str(dconf.get_int("http-port"))
        file.write(f"HTTPTunnelPort {my_ip}:{http_port}\n")
        file.write(f"DataDirectory {data_dir}\n")
        file.write(f"ControlSocket {data_dir}/control.sock\n")
        if exit_node != "ww":
            exit_node_policy = (
                f"ExitNodes {'{'}{exit_node}{'}'}\n" "StrictNodes 1\n"
            )
            file.write(exit_node_policy)
        bridge_type = dconf.get_int("bridge-type")
        if bridge_type == 1:
            file.write("UseBridges 1\n")
            file.write(mybridges)
        elif bridge_type == 2:
            file.write("UseBridges 1\n")
            transport = dconf.get_string("plugable-transport")
            file.write(f"ClientTransportPlugin obfs4 exec {transport}\n")
            file.write(mybridges)
        elif bridge_type != 0:
            raise ValueError("Bridge type is not supported")
    return tmpdir, path
