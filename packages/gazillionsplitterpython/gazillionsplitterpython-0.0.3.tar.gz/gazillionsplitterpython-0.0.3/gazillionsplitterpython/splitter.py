import sys
from urllib.parse import urlsplit

mylist = []
wordlist = ''
outputFile = 'output.txt'

def printHelp():
	tool_name = "Gazillion endpoint splitter"
	box_width = len(tool_name) + 4  
	
	print(f"\033[1;33m{'*' * box_width}")
	print(f"* \033[1;32m{tool_name.upper()}\033[1;33m *")
	print(f"{'*' * box_width}\033[0m")
	
	print("\n\033[1;36mUSAGE:")
	print(f"  python splitter.py -l <url-list> -o <outputFile>")
	
	print("\n\033[1;36mOPTIONS:")
	print("  -l <worlist>: Specify the path to the URL list.")
	print("  -o <outputFile>: Specify the output file name.")
	print("  -h: Display this help message.\033[0m")
	
	print("\n\033[1;93mEXAMPLE:")
	print(f" \033[1;93mgazillionsplitterpython -l wordlist.txt -o output.txt\033[0m")
	print(f" \033[1;93mgazillionsplitterpython -l list.txt -o output.txt\033[0m")

def printUsage():
	tool_name = "Gazillion endpoint splitter"
	box_width = len(tool_name) + 4  
	
	print(f"\033[1;33m{'*' * box_width}")
	print(f"* \033[1;32m{tool_name.upper()}\033[1;33m *")
	print(f"{'*' * box_width}\033[0m")
	
	print(f" \033[1;93mUse -h to check the help window\033[0m")

def split_url(url):
	global mylist
	splittedUrl = urlsplit(url)
	base = splittedUrl.scheme + '://' + splittedUrl.netloc + '/' 
	paths = splittedUrl.path.split('/')
	mylist.append("Break")
	for i in range(len(paths)):
		if i != 0:
			base = base + paths[i] + "/"
			mylist.append(base)
	
def readUrl(filePath):
	global mylist
	global outputFile
	with open(filePath,'r') as file:
		lines = [line.strip() for line in file]
		for line in lines:
			split_url(line)
		sortedList = []
		splittedList = (',').join(mylist).split('Break')
		with open('report.txt','w') as output:
			for j in splittedList:
				urlToWrite = j.split(',')
				urlToWrite.pop(0)
				for k in range(len(urlToWrite)):
					if k == 0:
						output.write("Original URL ==> " + urlToWrite[k] + '\n')
						output.write("Splitted URLs :- \n")
					else:
						output.write(urlToWrite[k] + '\n')
		[sortedList.append(x) for x in mylist if x not in sortedList and x != 'Break']
		mylist = list(set(mylist))
		with open('report.txt','a') as file:
			file.write('\n\nSplitted URLs in ' + outputFile + ' :-\n')
			for i in sortedList:
				file.write(i+'\n')
		with open(outputFile,'w') as outputF:
			for i in sortedList:
				outputF.write(i+'\n')
				print(i)
		print(f"\nSuccessfully the URL is splitted and saved in output file",outputFile)

def main():
	if len(sys.argv) <= 1:
		printUsage()
		sys.exit(1)
	for i in range(1,len(sys.argv),2):
		if sys.argv[i] == '-l' or sys.argv[i] == '--list':
			wordlist = sys.argv[i+1]
		elif sys.argv[i] == '-o' or sys.argv[i] == '--output':
			outputFile = sys.argv[i+1]
		elif sys.argv[i] == '-h' or sys.argv[i] == '--help':
			printHelp()
			sys.exit(1)
		else:
			printUsage()
			sys.exit(1)
	readUrl(wordlist)

if __name__ == "__main__":
	main()