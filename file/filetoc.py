#!/usr/bin/python

##                                                                              
## filetoc is a utility for converting plain files into C-language static byte
## array declarations.       
## Copyright (C) 2016  Kevin Balke  (kbalke@ucla.edu)                           
##                                                                              
## This program is free software; you can redistribute it and/or modify         
## it under the terms of the GNU General Public License as published by         
## the Free Software Foundation; either version 3 of the License, or            
## (at your option) any later version.                                          
##                                                                              
## This program is distributed in the hope that it will be useful,              
## but WITHOUT ANY WARRANTY; without even the implied warranty of               
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                
## GNU General Public License for more details.                                 
##                                                                              
## You should have received a copy of the GNU General Public License            
## along with this program; if not, write to the Free Software Foundation,      
## Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA            
##

import argparse, sys, os

parser = argparse.ArgumentParser(description='Convert any plain file into a C '
                                 'constant byte array declaration.')
parser.add_argument('-f', '--file', help='The file to convert.')
parser.add_argument('-n', '--name', help='The name to use for the output.')
parser.add_argument('-o', '--ofile', help='The name to use for the output file.')

parsed_args = parser.parse_args(sys.argv[1:])

HEADER_TEMPLATE = lambda guard, name : '''
#ifndef %s
#define %s

#include <stdint.h>

extern const uint8_t %s[];

#endif // %s
''' % (guard, guard, name, guard)

SOURCE_TEMPLATE = lambda name, declname, data : '''
#include "%s.h"

#pragma DATA_SECTION(%s, ".EXT_RAM")
const uint8_t %s[] = { %s };
''' % (name, declname, declname, ', '.join([str(x) for x in data]))


def write_header(filename, declname):
    ofile = open(filename + '.h', 'w')

    ofile.write(HEADER_TEMPLATE('_%s_H_' % declname.upper(), declname))

    ofile.close()

def write_source(filename, declname, data_bytes):
    ofile = open(filename + '.c', 'w')

    ofile.write(SOURCE_TEMPLATE(os.path.basename(filename), declname, data_bytes))

def write_files(filename, declname, data_bytes):
    write_header(filename, declname)
    write_source(filename, declname, data_bytes)


if parsed_args.file and parsed_args.name:
    filedata = open(parsed_args.file, 'r').read()

    write_files(parsed_args.ofile, parsed_args.name, [ord(c) for c in filedata])
