import re
import pyperclip

def generateCSS(filename):
	dataTypes = ['True', 'False', 'None',]
	keywords = ['and', 'as', 'assert', 'break', 'continue',
		'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if',
		'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
		'try', 'while', 'with', 'yield',]
	operations = [' = ', ' \+ ', ' - ', ' [*]+? ', ' / ', ' % ', ' // ', ' > ', ' < ',]
	output = ''
	with open(filename, 'r') as f:
		for line in f:
			# Split at the hashtags to block comments parts from being syntax highlighted
			# lineparts[0] is the part before the # after splitting
			lineparts = line.split('#')
			# matching class keyword must go first
			lineparts[0] = re.sub(r'\bclass\b', '<span class="keyword">class</span>', lineparts[0])
			
			# add spans around strings
			lineparts[0] = re.sub(r'("[^keyword].*?")', r'<span class="string">\1</span>', lineparts[0])
			lineparts[0] = re.sub(r'(\'.*?\')', r'<span class="string">\1</span>', lineparts[0])
			
			# add spans around dataTypes
			for dataType in dataTypes:
				lineparts[0] = re.sub(r'\b({})\b'.format(dataType), r'<span class="dataType">\1</span>', lineparts[0])
			
			# add spans around keywords
			for keyword in keywords:
				lineparts[0] = re.sub(r'\b({})\b'.format(keyword), r'<span class="keyword">\1</span>', lineparts[0])
			
			# add spans around operations
			for operation in operations:
				lineparts[0] = re.sub(r'({})'.format(operation), r'<span class="keyword">\1</span>', lineparts[0])

			# add spans around functions
			lineparts[0]= re.sub(r'(\b[^#>].\w+)\(', r'<span class="function">\1</span>(', lineparts[0])
			# # add spans around functionKeywords
			# if '#' not in line:
			# 	line = re.sub(r'\b(\w+)=', r'<span class="functionKeywords">\1</span>=', line)
			
			# add spans around comments
			line = '#'.join(lineparts)
			line = re.sub(r'(\#.*$)', r'<span class="comment">\1</span>', line)
			# replace tabs with &nbsp;
			line = re.sub(r'\t', '&nbsp;'*4, line)
			if line == '\n' or line == '':
				line = '&nbsp;'
			output += '<p class="code-line">' + line.strip() + '</p>\n'
		output = output[:-1]
		pyperclip.copy(output)
		return output

if __name__ == "__main__":
	generatedCSS = generateCSS('bigExample.py')
	print(generatedCSS)