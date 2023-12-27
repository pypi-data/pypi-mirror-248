#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
THIS FILE IS PART OF NETWORK FOR MWAFU LIBRARY LOVE BOOK STORE BY MATT BELFAST BROWN
__init__.py - The core part of the Foreign Name Translator.

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
# import list
import ForeNameTranslator.mode.mode_FNM_Tra as mode_FNM_Tra
import ForeNameTranslator.mode.mode_TRA_Api as mode_TRA_Api

# information list
__title__ = "ForeNameTranslator"
__version__ = "0.0.1"
__author__ = "Matt Belfast Brown"
__license__ = "GPL-3.0"
__copyright__ = "Copyright (c) 2023 Matt Belfast Brown \nCopyright (C) 2023 Love Book Store Volunteer Association of NWAFU"
__all__ = ["mode", "mode_FNM_Tra", "mode_TRA_Api"]

# function list
fun_gain_potn = mode_FNM_Tra.fun_gain_potn
fun_encp_code = mode_TRA_Api.fun_encp_code
fun_trca_info = mode_TRA_Api.fun_trca_info
fun_gain_tran = mode_TRA_Api.fun_gain_tran
fun_gain_pron = mode_TRA_Api.fun_gain_pron
