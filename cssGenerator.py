import re
import pyperclip

def generateCSS(filename):
	keywords = ['for', 'in', 'and', 'list', 'while', 'if', 'else', 'elif', 'import', 'return']
	output = ''
	with open(filename, 'r') as f:
		for line in f:
			# add spans around strings
			line = re.sub(r'(".*?")', r'<span class="string">\1</span>', line)
			line = re.sub(r'(\'.*?\')', r'<span class="string">\1</span>', line)
			# add spans around keywords
			for keyword in keywords:
				line = re.sub(r'\b{}\b'.format(keyword), '<span class="keyword">{}</span>'.format(keyword), line)
			# add spans around functions
			line = re.sub(r'\b(\w+)\(', r'<span class="function">\1</span>(', line)
			# add spans around comments
			line = re.sub(r'(\#.*$)', r'<span class="comment">\1</span>', line)
			# replace tabs with &nbsp;
			line = re.sub(r'\t', '&nbsp;'*4, line)
			if line == '\n' or line == '':
				line = '&nbsp;'
			output += '<p>' + line.strip() + '</p>\n'
		pyperclip.copy(output)
		return output

if __name__ == "__main__":
	generatedCSS = generateCSS('exampleInput.py')
	print(generatedCSS)