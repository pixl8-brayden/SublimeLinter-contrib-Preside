from SublimeLinter.lint import Linter  # or NodeLinter, PythonLinter, ComposerLinter, RubyLinter


class __class__(Linter):
	cmd = '__cmd__'
	regex = r''
	multiline = False
	defaults = {
		'selector': 'embedding.cfml'
	}
