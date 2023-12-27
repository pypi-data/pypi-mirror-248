#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
mode_TRA_Api.py - The core part of the Foreign Name Translator.

Author: Matt Belfast Brown
Creat Date: 2023-12-25
Version Date: 2023-12-27
Version: 0.0.1

THIS PROGRAM IS FREE FOR EVERYONE,IS LICENSED UNDER GPL-3.0
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0 LICENSE.

Copyright (C) 2023 Matt Belfast Brown
Copyright (C) 2023 Love Book Store Volunteer Association of NWAFU

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.  If not,
see <http://www.gnu.org/licenses/>.
"""

# define import lib list
import time
import uuid
import requests
from hashlib import sha256


def fun_encp_code(stri_sign):
    hash_algo = sha256()
    hash_algo.update(stri_sign.encode('utf-8'))
    return hash_algo.hexdigest()


def fun_trca_info(word_need):
    if word_need is None:
        return None
    word_size = len(word_need)
    return word_need if word_size <= 20 else word_need[0:10] + str(word_size) + word_need[word_size - 10:word_size]


def fun_gain_tran(word_need, appl_iden, appl_keys):
    stri_salt = str(uuid.uuid1())
    vari_cuti = str(int(time.time()))
    vari_sign = fun_encp_code(appl_iden + fun_trca_info(word_need) + stri_salt + vari_cuti + appl_keys)
    dic_head_used = {'Content-Type': 'application/x-www-form-urlencoded'}
    dic_data_used = {
        'appKey': appl_iden, 'q': word_need, 'curtime': vari_cuti, 'salt': stri_salt, 'sign': vari_sign, 'signType': 'v3',
        'from': 'en', 'to': 'zh-CHS',
        }
    vari_rslt = requests.post(yapi_link, data=dic_data_used, headers=dic_head_used)
    stri_rslt = vari_rslt.json()
    return stri_rslt


def fun_gain_pron(word_need, appl_iden, appl_keys):
    stri_rest = fun_gain_tran(word_need, appl_iden, appl_keys)
    vari_pron = "/" + stri_rest["basic"]["uk-phonetic"] + "/"
    return vari_pron


# define string list
yapi_link = 'https://openapi.youdao.com/api'
