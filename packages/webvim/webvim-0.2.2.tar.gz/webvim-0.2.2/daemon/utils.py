# -*- coding: utf-8 -*-
import platform


def is_mac():
    """
    is Mac
    :return:
    """
    return platform.system() == "Darwin"


def is_linux():
    """
    is linux
    """
    return platform.system() == "Linux"


def is_termux():
    """
    is termux
    """
    return is_linux()