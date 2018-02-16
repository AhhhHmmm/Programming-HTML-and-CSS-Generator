import re
import pyperclip

def generateCSS(filename):
	dataTypes = ['True', 'False', 'None',]
	keywords = ['and', 'as', 'assert', 'break', 'continue',
		'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
		'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
		'try', 'while', 'with', 'yield',]
	operations = [' = ', ' \+ ', ' - ', ' [*]+? ', ' / ', ' % ', ' // ',]
	output = ''
	with open(filename, 'r') as f:
		for line in f:
			# matching class keyword is special because that appears in added html tags, must go first
			line = re.sub(r'\bclass\b', '<span class="keyword">class</span>', line)
			# add spans around strings
			if '#' not in line:
				line = re.sub(r'("[^keyword].*?")', r'<span class="string">\1</span>', line)
				line = re.sub(r'(\'[^keyword].*?\')', r'<span class="string">\1</span>', line)
			# add spans around dataTypes
			for dataType in dataTypes:
				if '#' not in line:
					line = re.sub(r'\b({})\b'.format(dataType), r'<span class="dataType">\1</span>', line)
			# add spans around keywords
			for keyword in keywords:
				if '#' not in line:
					line = re.sub(r'\b({})\b'.format(keyword), r'<span class="keyword">\1</span>', line)
			# add spans around operations
			for operation in operations:
				if '#' not in line:
					line = re.sub(r'({})'.format(operation), r'<span class="keyword">\1</span>', line)
			# add spans around functions
			if '#' not in line:
				line = re.sub(r'\b(\w+)\(', r'<span class="function">\1</span>(', line)
			# add spans around comments
			line = re.sub(r'(\#.*$)', r'<span class="comment">\1</span>', line)
			# replace tabs with &nbsp;
			line = re.sub(r'\t', '&nbsp;'*4, line)
			if line == '\n' or line == '':
				line = '&nbsp;'
			output += '<p>' + line.strip() + '</p>\n'
		output = output[:-1]
		pyperclip.copy(output)
		return output

if __name__ == "__main__":
	generatedCSS = generateCSS('bigExample.py')
	print(generatedCSS)