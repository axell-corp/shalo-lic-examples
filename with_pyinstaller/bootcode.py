#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# with_pyinstaller/bootcode.py
#
# (C) 2023 AXELL CORPORATION
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
#

import sys
from io import BytesIO
from os import path
from zipfile import *
import importlib
import shalo_lic

class ShaloFinder( importlib.abc.MetaPathFinder ):
	def __init__( self, loader ):
		self.loader = loader

	def find_spec( self, fname, path, target = None ):
		if self.loader.has( fname ):
			ispkg = self.loader.is_pkg( fname )
			return importlib.machinery.ModuleSpec(
				fname, self.loader,
				is_package = ispkg
			)
		return None

class ShaloLoader( importlib.abc.Loader ):
	def __init__( self, stream ):
		strm = shalo_lic.decrypt( stream )
		self.strm = BytesIO(strm)
		self.blob = ZipFile(self.strm)
		self.files = set( self.blob.namelist() )
		self.dirs = set( [path.dirname(i) for i in self.blob.namelist() if '/' in i] )

	def fname_to_path( self, fname, ext = ".py" ):
		return fname.replace(".", "/") + ext

	def has( self, fname ):
		return self.fname_to_path(fname) in self.files or self.is_pkg(fname)

	def is_pkg( self, fname ):
		return self.fname_to_path( fname, '' ) in self.dirs

	def create_module( self, spec ):
		return None

	def exec_module( self, module ):
		path = self.fname_to_path(module.__name__)

		if module.__package__ == module.__name__:
			path = f"{module.__package__}/__init__.py"
			if path not in self.files:
				return
		if path not in self.files:
			raise ImportError(f"{path} is not found on zip file.")
		with self.blob.open(path) as f:
			exec( f.read(), module.__dict__ )

	def exec( self, path ):
		with self.blob.open( path ) as f:
			exec( f.read() )

if hasattr( sys, '_MEIPASS' ):
	p = sys._MEIPASS
else:
	p = path.dirname(path.abspath(__file__))

with open( path.join( p, '__main__.bin' ), 'rb' ) as f:
	loader = ShaloLoader( f.read() )

sys.meta_path.append( ShaloFinder(loader) )

loader.exec( '__main__.py' )
