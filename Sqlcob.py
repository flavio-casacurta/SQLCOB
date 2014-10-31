#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ajusta as isntru��es SQL dos programas COBOL convertido pelo EASY2COB

para todos os programs do diret�rio no properties ['DIRSOUPGM'] com a exten��o ['EXTSOU']

'pathProp.txt' default do diret�io do properties
'''

import os
from collections import namedtuple
from HOFs import *
from utilities import *
from DirFileList import *
from Sql import Sql


class Sqlcob(object):
    def __init__(self, properties='pathProp.txt'):
        self.properties = properties
        path = ''.join(open(self.properties).readline().replace("'", "").split())
        config = file(os.path.join(path, 'config.properties')).readlines()
        self.diccnfg = {line.split()[0]: line.split()[1] for line in config}
        self.include = self.loadinclude()[0]
        self.dcltable = self.loadinclude()[1]
        self.tables = self.loadtables()
        self.cmds = file(r'CBLCMDS.TXT').read().splitlines()
        self.sql = Sql(self.diccnfg, self.include, self.tables, self.cmds)


    def sqlcob(self):
        ispgm = lambda pgm: pgm[-3:].upper() == self.diccnfg['EXTSOU']

        dirfilelist = DirFileList()
        dirfilelist.setDirFileList(self.diccnfg['DIRSOUPGM'])
        pgmlist = dirfilelist.getDirFileList()

        for pgm in filter(ispgm, pgmlist):
            basename = os.path.basename(pgm)
            print pgm
            pgmwrite = open('{}'.format(os.path.join(self.diccnfg['DIRCNVPGM'], basename)), 'w')
            pgmwrite.writelines(self.sql.sql(pgm))
            pgmwrite.close()


    def loadinclude(self):
        lines = file('{}'.format(os.path.join(self.diccnfg['DIRDATWOR'], 'include.txt'))).readlines()
        Attrs = namedtuple('Attrs', ['dclgen', 'prefixo', 'declare'])
        include = {}
        dcltable = {}
        for line in lines:
            lis = line.split()
            include[lis[0]] = Attrs(lis[1], '' if lis[2] == 'None' else lis[2], lis[3])
            dcltable[lis[1]] = lis[0]
        return include, dcltable


    def loadtables(self):
        isdcl = lambda dcl: dcl[-3:].upper() == self.diccnfg['EXTCPY']
        dirfilelist = DirFileList()
        dirfilelist.setDirFileList(self.diccnfg['DIRSOUDCL'])
        dcllist = dirfilelist.getDirFileList()
        Attrs = namedtuple('Attrs', ['datatype', 'isnull'])
        tables = {}
        for dcl in filter(isdcl, dcllist):
            basename = os.path.basename(dcl)
            fields = {}
            lines = file(dcl).readlines()
            lines = change({'(': ' ', ',': ' '}, lines)
            n = 0
            while 'EXEC SQL DECLARE' not in lines[n]:
                n += 1
            n += 1
            while 'END-EXEC' not in lines[n]:
                wrds = words(lines[n])[1]
                fields[wrds[0]] = Attrs(wrds[1], False if 'NOT NULL' in lines[n] else True)
                n += 1
            tables[self.dcltable[basename[:-(len(self.diccnfg['EXTCPY']) + 1)]]] = fields
        return tables

