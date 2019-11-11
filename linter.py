from SublimeLinter.lint import Linter, WARNING


class Preside(Linter):
    cmd = 'presidelint'
    regex = r''
    multiline = False
    default_type = WARNING
    defaults = {
        'selector': 'embedding.cfml'
    }
