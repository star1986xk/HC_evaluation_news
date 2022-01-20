#!/usr/bin/python3
# -*- coding: utf-8 -*-
import hashlib


def get_md5(text: str):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

