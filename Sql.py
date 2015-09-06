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
        self.lnstart = 0
        self.lnstop = 0
        self.possql = 0
        self.poscmd = 0
        self.ptsql = ''
        self.cmd = ''
        self.n = 0

    def sql(self, arq):
        lines = file(arq).readlines()
        self.n = 0
        line = lines[self.n]

# define a linha da PROCEDURE DIVISION.
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

# Trata comandos SQL
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
            debug = True

        if self.table != 'SQLCA':
            self.changeHosts(odcl, lines)


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
        self.lnstart = self.n
        self.possql = line.index('SQL')
        lines[self.n] = unRemarks(line.replace('SQL', 'EXEC SQL'))
        self.ptsql = self.setptsql(lines)


    def includeEndExec(self, lines):
        self.n += 1
        lines.insert(self.n, '{:{}}END-EXEC{}\n'.format('', self.poscmd, self.ptsql))
        line = lines[self.n]
        self.lnstop = self.n


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
                        ns = 0
                        for s in xrange(len(line.rstrip())-1, 0, -1):
                            if line[s] == ' ':
                                ns += 1
                            if ns == 2:
                                break
                        fieldof = line[s:].strip()
                        line = line[:s] + '\n'
                        lines[self.n] = line
                        self.n += 1
                        line = lines[self.n]
                        line = line.replace(line.strip(), fieldof + ' ' + line.strip())
                        lines[self.n] = line
                    else:
                        self.n += 1
                        line = lines[self.n]
                else:
                    self.n += 1
                    line = lines[self.n]
            except IndexError:
                break


    def changeHosts(self, odcl, lines):
        n = self.lnproc + 1
        line = lines[n]
        while True:
            try:
                if isOFOLDDCL(line, odcl):
                    lsp = line.split()
                    wpo = lsp.index(odcl)
                    if wpo < 2:
                        upn = n - 1
                        line = lines[upn]
                        wrds = words(line)
                        fld = wrds[1][wrds[0]-1]
                        for s in xrange(len(line.rstrip())-1, 0, -1):
                            if line[s] == ' ':
                                break
                        line = line[:s] + '\n'
                        lines[upn] = line
                        line = lines[n]
                        lines[n] = line.replace(line.strip(), fld + ' ' + line.strip())
                        line = lines[n]
                        lsp = line.split()
                        wpo = lsp.index(odcl)
                    host = lsp[wpo-2]
                    newhost = self.include[self.table].prefix + host + ' OF ' + self.include[self.table].declare
                    line = CHANGEHOST(line, host, odcl, newhost)
                    lines[n] = line
                    if len(line.rstrip()) > 72:
                        for s in xrange(72, 0, -1):
                            if line[s] == ' ':
                                break
                        f = line[s:]
                        line = line[:s] + '\n'
                        lines[n] = line
                        n += 1
                        lines.insert(n, '{:>73}'.format(f))
                        line = lines[n]
                else:
                    n += 1
                    line = lines[n]
            except IndexError:
                break

