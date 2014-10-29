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

    def __init__(self, diccnfg, include, cmds):
        self.diccnfg = diccnfg
        self.include = include
        self.cmds = cmds
        self.possql = 0
        self.ptsql = ''
        self.cmd = ''
        self.n = 0

    def sql(self, arq):
        lines = file(arq).readlines()
        ilines = iter(lines)
        self.n = 0
        line = ilines.next()
        while True:
            try:
                if issql(line):
                    self.cmd = nextWord('SQL', line)
                    line = eval('self.proc{}(lines, ilines)'.format(self.cmd))
                else:
                    self.n += 1
                    line = ilines.next()
            except StopIteration:
                break
        return lines


    def procINCLUDE(self, lines, ilines):
        line = lines[self.n]
        if nextWord('INCLUDE', line) == 'FROM':
            self.table =  nextWord('FROM', line)
            if '.' in self.table:
                self.table = self.table.split('.')[0]
        lines[self.n] = '{:11}EXEC SQL  INCLUDE {:10}END-EXEC.\n'.format('', self.include[self.table].DCLGEN)
        odcl = self.diccnfg['PREREG'] + self.table.replace('_', '-')
        self.n += 1
        line = ilines.next()
        return line

#    if @table \= 'SQLCA' then
#       call loadDcl
#    'x '@fid()' (profile utl_settings'
#     call changeHosts
# return



    def procDECLARE(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procOPEN(self, lines, ilines):
        self.includeExec(lines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procFETCH(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procCLOSE(self, lines, ilines):
        self.includeExec(lines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procSELECT(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procDELETE(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procINSERT(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line

    def procUPDATE(self, lines, ilines):
        self.includeExec(lines)
        self.changePlus(lines, ilines)
        self.includeEndExec(lines, ilines)

        self.n += 1
        line = ilines.next()
        return line


    def includeExec(self, lines):
        line = lines[self.n]
        self.possql = line.index('SQL')
        lines[self.n] = unRemarks(line.replace('SQL', 'EXEC SQL'))
        self.ptsql = self.setptsql(lines)


    def includeEndExec(self, lines, ilines):
        self.n += 1
        lines.insert(self.n, '{:{}}END-EXEC{}\n'.format('', self.possql, self.ptsql))
        line = ilines.next()


    def changePlus(self, lines, ilines):
        line = lines[self.n]
        while sanitize(line).endswith('+'):
            lines[self.n] = unRemarks(line.replace('+\n', '\n'))
            self.n += 1
            line = ilines.next()
        lines[self.n] = unRemarks(line)


    def setptsql(self, lines):
        pt = dicpte[self.cmd]
        if pt == '':
            n = self.n - 1
            while isRem(lines[n]):
                n -= 1
            if sanitize(lines[n]).endswith('.'):
                pt = '.'
            while True:
                if lines[n][7:11].strip() != '':
                    break
                wrd = words(lines[n])[1][0]
                if wrd in self.cmds:
                    self.possql = lines[n].index(wrd)
                    if wrd in 'IF AND OR ELSE':
                        self.possql += 5
                    elif wrd == 'PERFORM' and 'UNTIL' in lines[n]:
                        self.possql += 5
                    break
                n -= 1
        return pt

