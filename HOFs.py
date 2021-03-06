from HOFsGenericas import *


isCopy = lambda line: 'COPY' in words(line)[1]
isInclude = lambda line: ('INCLUDE' in words(line)[1] and 'SQLCA' not in words(line)[1])
isLink = lambda line: 'LINK' in words(line)[1]
isXctl = lambda line: 'XCTL' in words(line)[1]
isCall = lambda line: 'CALL' in words(line)[1]
isPic = lambda line: 'PIC' in words(line)[1]
procRe = re.compile(r'PROCEDURE[\s]+DIVISION', re.UNICODE)
isProcedure = lambda line: truth(procRe.findall(line))
l672 = lambda line: line[6:72].rstrip()
isNotBlank = lambda line: len(l672(line).strip()) > 0
issql = lambda line: truth(line[6:7] == '*' and (' SQL ' in line or '*SQL ' in line))
unRemarks = lambda line: line[:6]+' '+line[7:]
CHANGEPLUS = lambda line: re.sub('(\+\s*\n)', '\n', line)
isOFOLDDCL = lambda line, arg: re.findall(r'OF\s+'+arg, line)
CHANGEHOST = lambda line, arg1, arg2, arg3: re.sub(arg1+'\s+OF\s+'+arg2, arg3, line)
