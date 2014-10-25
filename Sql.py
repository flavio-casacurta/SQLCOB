from HOFs import *

dicval = {'CHAR'     : "' '"
         ,'DATE'     : "'01.01.0001'"
         ,'DECIMAL'  : '0'
         ,'SMALLINT' : '0'
         ,'INTEGER'  : '0'
         ,'TIME'     : "'00:00:00'"
         ,'TIMESTAMP': "'0001-01-01-01.01.01.000001'"
         ,'VARCHAR'  : "' '"}

dicpte = {'INCLUDE'  : '.'
         ,'DECLARE'  : '.'
         ,'OPEN'     : ''
         ,'FETCH'    : ''
         ,'CLOSE'    : ''
         ,'SELECT'   : ''
         ,'DELETE'   : ''
         ,'INSERT'   : ''
         ,'UPDATE'   : ''}

class Sql(object):

    def __init__(self):
        pass

    def sql(self, arq):
        lines = file(arq).readlines()
        ilines = iter(lines)
        for line in ilines:
             if issql(line):
                 print line
                 while sanitize(line).endswith('+'):
                     line = ilines.next()
                     print line
        return lines
