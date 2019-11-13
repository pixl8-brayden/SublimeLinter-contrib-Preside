import re

from SublimeLinter.lint import Linter, ERROR


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

        def missingVarInForLoopError(line):
            if len(re.findall(r'for.*\(.* in .*\)*{', line)) > 0 or len(re.findall(r'for.*\(.*;.*;.*\)*{', line)) > 0:
                if line.find('var') < 0:
                    return True, 'Missing var', 'Potential race condition', line.find('for')
            return False, '', '', 0

        # Process
        output = []
        regions = self.view.find_all('.*')

        # For debugging
        print('Process running...')

        for region in regions:
            line = self.view.substr(region)

            # check missing var in for loop
            missingVarStatus, missingVarWord, missingVarMessage, missingVarPos = missingVarInForLoopError(line=line)
            if missingVarStatus:
                row = self.view.rowcol(region.a)[0]
                col = missingVarPos

                error_type = ERROR
                word = missingVarWord
                message = missingVarMessage

                output.append('{row}:{col}: {error_type} ({word}): {message}'.format(**locals()))

        # For debugging
        print('Process finished!')

        return '\n'.join(output)
