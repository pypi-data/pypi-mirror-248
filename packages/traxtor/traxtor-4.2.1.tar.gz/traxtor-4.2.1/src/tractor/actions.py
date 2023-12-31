#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022

"""
real actions of tractor
"""

import os
import signal
import sys

from stem import Signal
from stem.control import Controller
from stem.process import launch_tor
from stem.util import term

from . import tractorrc
from . import checks


def print_bootstrap_lines(line):
    """
    prints bootstrap line in standard output
    """
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE), flush=True)


def start():
    """
    starts onion routing
    """
    if checks.running():
        print(
            term.format(
                "Tractor is already started", term.Attr.BOLD, term.Color.GREEN
            )
        )
        sys.exit(0)
    try:
        tmpdir, torrc = tractorrc.create()
    except ValueError:
        print(
            term.format(
                "Error Creating torrc. Check your configurations\n",
                term.Attr.BOLD,
                term.Color.RED,
            )
        )
    dconf = checks.dconf()
    print(
        term.format("Starting Tractor:\n", term.Attr.BOLD, term.Color.YELLOW)
    )
    try:
        tractor_process = launch_tor(
            torrc_path=torrc,
            init_msg_handler=print_bootstrap_lines,
            timeout=120,
        )
        dconf.set_int("pid", tractor_process.pid)
    except OSError as error:
        print(term.format(f"{error}\n", term.Color.RED))
        sys.exit(1)
    except KeyboardInterrupt:
        os.remove(torrc)
        os.rmdir(tmpdir)
        sys.exit(1)
    os.remove(torrc)
    os.rmdir(tmpdir)
    if not checks.running():
        print(
            term.format(
                "Tractor could not connect. "
                "Please check your connection and try again.",
                term.Attr.BOLD,
                term.Color.RED,
            )
        )
        sys.exit(1)
    else:
        print(
            term.format(
                "Tractor is conneted.", term.Attr.BOLD, term.Color.GREEN
            )
        )


def stop():
    """
    stops onion routing
    """
    if checks.running():
        control_socket = checks.data_dir() + "control.sock"
        with Controller.from_socket_file(path=control_socket) as controller:
            controller.authenticate()
            controller.signal(Signal.TERM)
        dconf = checks.dconf()
        dconf.reset("pid")
        print(
            term.format("Tractor stopped", term.Attr.BOLD, term.Color.YELLOW)
        )
    else:
        print(
            term.format(
                "Tractor seems to be stopped.",
                term.Attr.BOLD,
                term.Color.YELLOW,
            )
        )


def restart():
    """
    stop, then start
    """
    stop()
    start()


def new_id():
    """
    gives user a new identity
    """
    if not checks.running():
        print(
            term.format(
                "Tractor is stopped.", term.Attr.BOLD, term.Color.YELLOW
            )
        )
        sys.exit(1)
    else:
        control_socket = checks.data_dir() + "control.sock"
        with Controller.from_socket_file(path=control_socket) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print(
            term.format(
                "You have a new identity now!", term.Attr.BOLD, term.Color.BLUE
            )
        )


def kill_tor():
    """
    kill tor process
    """
    os.killpg(os.getpgid(checks.proc), signal.SIGTERM)
