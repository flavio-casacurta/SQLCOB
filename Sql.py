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
         ,'DECLARE'  : ''
         ,'OPEN'     : ''
         ,'FETCH'    : ''
         ,'CLOSE'    : ''
         ,'SELECT'   : ''
         ,'DELETE'   : ''
         ,'INSERT'   : ''
         ,'UPDATE'   : ''}

class Sql(object):

    def __init__(self, diccnfg, include, tables, cmds):
        self.diccnfg = diccnfg
        self.include = include
        self.tables = tables
        self.cmds = cmds
        self.prereg = self.diccnfg['prereg']
        self.table = ''
        self.lnproc = 0
        self.possql = 0
        self.poscmd = 0
        self.ptsql = ''
        self.cmd = ''
        self.n = 0

    def sql(self, arq):
        lines = file(arq).readlines()
        self.n = 0
        line = lines[self.n]
        while True:
            try:
                if isProcedure(line):
                    self.lnproc = self.n
                    break
                else:
                    self.n += 1
                    line = lines[self.n]
            except IndexError:
                break

        self.homogenizaOF(lines)

        self.n = 0
        line = lines[self.n]
        while True:
            try:
                if issql(line):
                    line = self.procs(lines)
                else:
                    self.n += 1
                    line = lines[self.n]
            except IndexError:
                break
        return lines


    def procs(self, lines):
        line = lines[self.n]
        self.cmd = nextWord('SQL', line)
        eval('self.proc{}(lines)'.format(self.cmd))
        self.n += 1
        return lines[self.n]


    def procINCLUDE(self, lines):
        line = lines[self.n]
        if nextWord('INCLUDE', line) == 'FROM':
            self.table = nextWord('FROM', line)
            if '.' in self.table:
                self.table = self.table.split('.')[0]
            lines[self.n] = '{:11}EXEC SQL INCLUDE {:11}END-EXEC.\n'.format('', self.include[self.table].dclgen)
            odcl = self.prereg + self.table.replace('_', '-')

#      if self.table != 'SQLCA':
#          changeHosts(odcl, lines)


    def procDECLARE(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procOPEN(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procFETCH(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procCLOSE(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procSELECT(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procDELETE(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procINSERT(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def procUPDATE(self, lines):
        self.includeExec(lines)
        self.changePlus(lines)
        self.includeEndExec(lines)


    def includeExec(self, lines):
        line = lines[self.n]
        self.possql = line.index('SQL')
        lines[self.n] = unRemarks(line.replace('SQL', 'EXEC SQL'))
        self.ptsql = self.setptsql(lines)


    def includeEndExec(self, lines):
        self.n += 1
        lines.insert(self.n, '{:{}}END-EXEC{}\n'.format('', self.poscmd, self.ptsql))
        line = lines[self.n]


    def changePlus(self, lines):
        line = lines[self.n]
        while sanitize(line).endswith('+'):
            lines[self.n] = unRemarks(CHANGEPLUS(line))
            self.align(lines)
            self.n += 1
            line = lines[self.n]
        lines[self.n] = unRemarks(line)
        self.align(lines)


    def setptsql(self, lines):
        pt = dicpte[self.cmd]
        self.poscmd = 12
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
                    self.poscmd = lines[n].index(wrd)
                    if wrd in 'IF AND OR ELSE':
                        self.poscmd += 5
                    elif wrd == 'PERFORM' and 'UNTIL' in lines[n]:
                        self.poscmd += 5
                    break
                n -= 1
        return pt

    def align(self, lines):
        if self.poscmd > self.possql:
            line = lines[self.n]
            lines[self.n] = '{}{}{}'.format(line[:7], ' ' * (self.poscmd - self.possql), line[7:])


    def homogenizaOF(self, lines):
        self.n += 1
        line = lines[self.n]
        while True:
            try:
                if sanitize(line).endswith('OF'):
                    wrd = words(lines[self.n + 1])[1][0].replace(self.prereg, '').replace('-', '_')
                    if wrd in self.tables:
                        wrds = words(line)
                        fieldof = line[line.index(wrds[1][wrds[0]-2]):].strip()
                        lines[self.n] = line[:line.index(wrds[1][wrds[0]-2])] + '\n'
                        self.n += 1
                        line = lines[self.n]
                        lines[self.n] = line.replace(line.strip(), fieldof + ' ' + line.strip())
                    else:
                        self.n += 1
                        line = lines[self.n]
                else:
                    self.n += 1
                    line = lines[self.n]
            except IndexError:
                break

