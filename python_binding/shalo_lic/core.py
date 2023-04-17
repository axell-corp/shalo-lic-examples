# coding: utf-8
#
# shalo_lic/core.py
#
# (C) 2023 AXELL CORPORATION
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
#

''' Python-binding for SHALO LICENSING: core implementation '''

import os
import sys
import ctypes

#### load shaloX.{dll,dylib,so}  ####
if sys.platform == "win32":
	fnamed = "shalod.dll"
	fnamem = "shalom.dll"
	loader = ctypes.WinDLL
elif sys.platform == "darwin":
	fnamed = "libshalod.dylib"
	fnamem = "libshalom.dylib"
	loader = ctypes.CDLL
else:
	fnamed = "libshalod.so"
	fnamem = "libshalom.so"
	loader = ctypes.CDLL

succeeded = False
candidate = ["", str(os.path.dirname(os.path.abspath(__file__))) + str(os.sep)]
for e in candidate:
	try:
		loader(e + fnamem)
		lib = loader(e + fnamed)
		succeeded = True
	except:
		pass

if not succeeded:
	msg = "'%s' and '%s' are not found" % (fnamed, fnamem)
	raise ImportError(msg)

#### public API declaration ####
lib.shalodDecodeAssetWithAppKey.restype = ctypes.c_int
lib.shalodDecodeAssetWithAppKey.argtypes = (
	ctypes.c_char_p,                 # outp
	ctypes.POINTER(ctypes.c_uint64), # o_length (byte)
	ctypes.c_char_p,                 # inp
	ctypes.c_uint,                   # i_length (byte)
	ctypes.c_char_p,                 # app_key
)

#### Exception class ####
class ShaloLicException(Exception) : pass
class ShaloLicIoException(ShaloLicException) : pass
class ShaloLicInvalidLicenseException(ShaloLicException) : pass
class ShaloLicInvalidArgumentException(ShaloLicException) : pass
class ShaloLicOutOfResourcesException(ShaloLicException) : pass
class ShaloLicPlainBinaryException(ShaloLicException) : pass
class ShaloLicNotFoundException(ShaloLicException) : pass
class ShaloLicAppKeyException(ShaloLicException) : pass
class ShaloLicUsbDeviceException(ShaloLicException) : pass
class ShaloLicLibUsbMissingException(ShaloLicException) : pass
class ShaloLicInvalidBinaryException(ShaloLicException) : pass
class ShaloLicInternalErrorException(ShaloLicException) : pass

#### utility functions ####
def check_error( code ):
	SUCCESS = 0
	err_list = {
		-1 : ShaloLicIoException,
		-2 : ShaloLicInvalidLicenseException,
		-3 : ShaloLicInvalidArgumentException,
		-4 : ShaloLicOutOfResourcesException,
		-5 : ShaloLicPlainBinaryException,
		-6 : ShaloLicNotFoundException,
		-7 : ShaloLicAppKeyException,
		-8 : ShaloLicUsbDeviceException,
		-9 : ShaloLicLibUsbMissingException,
		-10 : ShaloLicInvalidBinaryException,
		-128 : ShaloLicInternalErrorException
	}
	if code == SUCCESS:
		return

	detail = "result_code: " + str(code)
	if code in err_list:
	    e = err_list[code]
	    raise e
	else:
	    raise ShaloException(detail)
