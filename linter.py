import re

from SublimeLinter.lint import Linter, ERROR, WARNING


class Preside(Linter):
    cmd = None
    line_col_base = (0, 0)
    regex = re.compile(r'^(?P<line>\d+):(?P<col>\d+):'
                       r' (warning \((?P<warning>.+?)\)|error \((?P<error>.+?)\)):'
                       r' (?P<message>.*)')
    re_flags = re.IGNORECASE
    mark_regex_template = r'(?:(?P<warning>{warnings})|(?P<error>{errors})):?\s*(?P<message>.*)'
    defaults = {
        'selector': 'embedding.cfml, source.cfml, source.cfscript, text.html.cfm',
    }

    def run(self, cmd, code):
        # Temp variable
        tempList = []
        start = False

        # Functions
        def missingVarInForLoopError(line):
            if len(re.findall(r'for.*\(.* in .*\)*{', line)) > 0 or len(re.findall(r'for.*\(.*;.*;.*\)*{', line)) > 0:
                if line.find('var') < 0:
                    return True, 'Missing var in loop', \
                        'Potential race condition', line.find('for')
            return False, '', '', 0

        def variableDeclareError(line):
            global start
            global tempList

            backetStart = re.findall(r'function.*\).*\{', line)
            if len(backetStart):
                start = True
                return False, '', '', 0

            backetStop = re.findall(r'.*\}', line)
            if len(backetStop):
                start = False
                tempList = []
                return False, '', '', 0

            if start:
                if len(re.findall(r'\/\/', line)):
                    return False, '', '', 0

                potentialVariable = re.findall(r'\s(\w.*)\s\= .*', line)
                if len(potentialVariable) and not re.findall(r'\.', potentialVariable[0]):
                    if re.findall(r'var', potentialVariable[0]):
                        tempList.append(re.findall(r'var\s(\w.*)\s\= .*', line)[0])

                    if potentialVariable[0].replace('var ', '') not in tempList:
                        return True, 'Variable missing declaration', \
                            'Please confirm your variable is declared probably.', line.find(potentialVariable[0])

            return False, '', '', 0

        # Process
        output = []
        regions = self.view.find_all('.*')

        # For debugging
        print('Process running...')

        for region in regions:
            line = self.view.substr(region)

            # check missing var in for loop
            missingVarStatus, missingVarWord, \
                missingVarMessage, missingVarPos = missingVarInForLoopError(line=line)

            if missingVarStatus:
                row = self.view.rowcol(region.a)[0]
                col = missingVarPos

                error_type = ERROR
                word = missingVarWord
                message = missingVarMessage

                output.append('{row}:{col}: {error_type} ({word}): {message}'.format(**locals()))

            # check missing var in for loop
            variableDeclareStatus, variableDeclareWord, \
                variableDeclareMessage, variableDeclarePos = variableDeclareError(line=line)

            if variableDeclareStatus:
                row = self.view.rowcol(region.a)[0]
                col = variableDeclarePos

                error_type = WARNING
                word = variableDeclareWord
                message = variableDeclareMessage

                output.append('{row}:{col}: {error_type} ({word}): {message}'.format(**locals()))

        # For debugging
        print('Process finished!')

        return '\n'.join(output)
