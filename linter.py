import re

from SublimeLinter.lint import Linter, ERROR, WARNING


class Preside(Linter):
    cmd = None
    line_col_base = (0, 0)
    regex = re.compile(r'^(?P<line>\d+):(?P<col>\d+):'
                       r' (warning \((?P<warning>.+?)\)|error \((?P<error>.+?)\)):'
                       r' (?P<message>.*)')
    re_flags = re.IGNORECASE

    # We use this to do the matching
    mark_regex_template = r'(?:(?P<warning>{warnings})|(?P<error>{errors})):?\s*(?P<message>.*)'

    # Words to look for
    defaults = {
        'selector': 'embedding.cfml, source.cfml, source.cfscript, text.html.cfm',
        # 'selector': '',
    }

    def run(self, cmd, code):
        output = []
        regions = self.view.find_all('for.*(.*).*{')

        for region in regions:
            line = self.view.substr( region )
            if line.find( 'var' ) > 0:
                continue

            row = self.view.rowcol( region.a )[0]
            col = self.view.rowcol( region.a )[1]

            error_type = WARNING
            word = 'Missing var'
            message = 'Potential race condition'

            output.append('{row}:{col}: {error_type} ({word}): {message}'.format(**locals()))

        return '\n'.join(output)
