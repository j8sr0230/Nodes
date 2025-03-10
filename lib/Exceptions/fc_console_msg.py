#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	This module is used to expose native FreeCAD console printing system to establish user information template.
	
	It will use Console.Print{some functionality} to establish `def __init__` way of informing user about various issues that may arise.
	
	Respected exceptions should be shown in 'Report View' of FreeCAD as well as Python Console so it can be debugged or tracked easily.

"""

from FreeCAD import Console as FCC

__author__ = 'Danilo Mitrovic'

# 4 main message types, and levels (the rest is for ease of access)
MSG_TYPES = 4;
MSG_LEVEL = {
	0 : "MESSAGE",
	1 : "LOGGING",
	2 : "WARNING",
	3 : "ERROR",
	"MESSAGE": 0,
	"LOGGING": 1,
	"WARNING": 2,
	"ERROR":3
};

class nodesMessage:
	
	"""
		Nodes::Message base object to allow Nodes to inform users about their use, warn them if they try something unusual and
		raise an error if error occures in such way that user can be informed properly. 
		
		lib	: Library that it is using it : In this case Nodes
		module	: Module that is calling it, in this case Exceptions 
		obj	: Object that is calling it, whatever Qt, FC or Nodes class that is a caller 
		caller  : specific functionality, function or system that message is sent from 
	"""
	
	level = 0;
	lib = None;
	module = None;
	obj = None;
	caller = None;
	
	def __init__(self, level = 3, lib = "Nodes", module = "Exceptions", obj = "nodesMessage", caller = "none"):
		
		"""
			Initialises itself with next arguments (level : int, lib :str, module:str, obj:str, caller:str)
				all of them can be none in which case each is substituted with empty string
					: str(self) -> '->->->->'
			
			It then calls for FCC functions at __init__ (so it would allow raise X if requried) even for message.
		"""
	
		global MSG_TYPES;
		
		self.level 	= int(level)%MSG_TYPES;
		self.lib 	= '' if lib is None else str(lib);
		self.module 	= '' if module is None else str(module);
		self.obj 	= '' if obj is None else str(obj);
		self.caller 	= '' if caller is None else str(caller);
		
	
	def __repr__(self):
		"""
			used to show how this object is initialized for ease of use
		"""
		return f"nodesMessage({self.level},{self.lib},{self.module},{self.caller}";
	
	def build_signature(self):
		return f"NODES::{MSG_LEVEL[self.level]}: ";
	
	def build_origin(self):
		"""
			builds origin path (ie who called it)
		"""
		return '->'.join([self.lib,self.module,self.obj,self.caller])
	
	def __str__(self):
		global MSG_LEVEL;
		"""
			displays uncollored version for internal logging if required
		"""
		return f"NODES::{MSG_LEVEL[self.level]}: @ {self.build_origin()} : ";

class nodesError(Exception):
	
	def __init__(self,lib = "Nodes", module="Exceptions", obj= "Error", caller="none", error_msg = "Error Explanation Here"):
		msg = nodesMessage(3, lib,module,obj,caller);
		FCC.PrintCritical(str(msg) + error_msg+'\n');

class nodesWarning(Exception):
	def __init__(self,lib = "Nodes", module="Exceptions", obj= "Error", caller="none", error_msg = "Warning Explanation Here"):
		msg = nodesMessage(2, lib,module,obj,caller);
		FCC.PrintWarning(str(msg) + error_msg+'\n');

class nodesLog(Exception):
	def __init__(self,lib = "Nodes", module="Exceptions", obj= "Error", caller="none", error_msg = "Logging Information Here"):
		msg = nodesMessage(1, lib,module,obj,caller);
		FCC.PrintLog(str(msg) + error_msg+'\n');

class nodesInformation(Exception):
	def __init__(self,lib = "Nodes", module="Exceptions", obj= "Error", caller="none", error_msg = "User Message Here"):
		msg = nodesMessage(0, lib,module,obj,caller);
		FCC.PrintMessage(str(msg) + error_msg+'\n');


__all__ = ['nodesError','nodesWarning','nodesLog','nodesInformation'];


