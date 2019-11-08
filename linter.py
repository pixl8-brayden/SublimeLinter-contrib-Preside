from SublimeLinter.lint import Linter  # or NodeLinter, PythonLinter, ComposerLinter, RubyLinter

class Preside(Linter):
	cmd = '__cmd__'
	regex = r''
	multiline = False
	defaults = {
		'selector': 'embedding.cfml'
	}
