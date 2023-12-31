#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022

"""
actions for tractor internals
"""

import os
import sys

from gi.repository import Gio, GLib
from requests import get
from stem.util import system


def proc() -> int:
    """
    return the pid of tor process
    """
    _, port = ip_port()
    return system.pid_by_port(port)


def running() -> bool:
    """
    checks if Tractor is running or not
    """
    if proc():
        return system.is_running(proc())
    return False


def connected() -> bool:
    """
    checks if Tractor is connected or not
    """
    if running():
        _, port = ip_port()
        host = "https://check.torproject.org/"
        proxy = f"socks5h://127.0.0.1:{port}"
        expectation = "Congratulations."
        try:
            request = get(
                host, proxies={"http": proxy, "https": proxy}, timeout=10
            )
            if request.status_code == 200 and expectation in request.text:
                return True
            return False
        except Exception:
            return False
    return False


def proxy_set() -> bool:
    """
    checks if proxy is set or not
    """
    schema = "org.gnome.system.proxy"
    conf = Gio.Settings.new(schema)
    if conf.get_string("mode") != "manual":
        return False
    x_ip, x_port = ip_port()
    schema = "org.gnome.system.proxy.socks"
    conf = Gio.Settings.new(schema)
    my_ip = conf.get_string("host")
    my_port = conf.get_int("port")
    if my_ip == x_ip and my_port == x_port:
        return True
    return False


def ip_port() -> (str, int):
    """
    returns ip ans socks port
    """
    conf = dconf()
    accept_connection = conf.get_boolean("accept-connection")
    if accept_connection:
        myip = "0.0.0.0"
    else:
        myip = "127.0.0.1"
    socks_port = conf.get_int("socks-port")
    return myip, socks_port


def dconf():
    """
    returns dconf object
    """
    schema = "org.tractor"
    schemas = Gio.SettingsSchemaSource.get_default()
    if not Gio.SettingsSchemaSource.lookup(schemas, schema, False):
        print(
            f"""
        Please compile the "tractor.gschema.xml" file.
        In GNU/Linux you can copy it to "/usr/share/glib-2.0/schemas/"
        and run "sudo glib-compile-schemas /usr/share/glib-2.0/schemas/".
        The file is located at {os.path.dirname(os.path.abspath(__file__))}.
        """
        )
        sys.exit(404)
    mydconf = Gio.Settings.new(schema)
    return mydconf


def data_dir() -> str:
    """
    return the data directory of tractor
    """
    return GLib.get_user_config_dir() + "/tractor/"
