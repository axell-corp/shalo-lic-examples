# coding: utf-8
#
# shalo_lic/__init__.py
#
# (C) 2023 AXELL CORPORATION
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
#

''' Python-binding for SHALO LICENSING '''

import ctypes
from . import core

def decrypt( inp, app_key = None ):
	inp = bytearray(inp)
	input_array = ctypes.c_char * len(inp)
	input_pointer = input_array.from_buffer(inp)

	if app_key is not None:
		app_key = bytearray(app_key)
		appkey_array = ctypes.c_char * len(app_key)
		appkey_pointer = appkey_array.from_buffer(app_key)
	else:
		appkey_pointer = None

	output = bytearray(len(inp))
	output_char_array = ctypes.c_char * len(output)
	output_pointer = output_char_array.from_buffer(output)

	count = ctypes.c_uint64(len(output))

	code = core.lib.shalodDecodeAssetWithAppKey(output_pointer, ctypes.byref(count), input_pointer, len(inp), appkey_pointer)
	core.check_error(code)

	return bytearray(output[0:count.value])
