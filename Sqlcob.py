#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Ajusta as isntru��es SQL dos programas COBOL convertido pelo EASY2COB

para todos os programs do diret�rio no properties ['DIRSOUPGM'] com a exten��o ['EXTSOU']

'pathProp.txt' default do diret�io do properties
'''

import os
from Sql import Sql
from DirFileList import *


class Sqlcob(object):


    def __init__(self, properties = 'pathProp.txt'):
        self.properties = properties
        self.sql = Sql()

    def sqlcob(self):
        path = ''.join(open(self.properties).readline().replace("'", "").split())
        config = open(os.path.join(path,'config.properties')).readlines()
        diccnfg = {line.split()[0]:line.split()[1] for line in config}
        ispgm = lambda pgm: pgm[-3:].upper() == diccnfg['EXTSOU']

        dirfilelist = DirFileList()
        dirfilelist.setDirFileList(diccnfg['DIRSOUPGM'])
        pgmlist = dirfilelist.getDirFileList()

        for pgm in filter(ispgm, pgmlist):
            basename = os.path.basename(pgm)
            print pgm
            pgmwrite = open('{}'.format(os.path.join(diccnfg['DIRCNVPGM'], basename)), 'w')
            pgmwrite.writelines(self.sql.sql(pgm))
            pgmwrite.close()
