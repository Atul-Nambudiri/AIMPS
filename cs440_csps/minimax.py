import sys 

def main():
	if len(sys.argv) < 2:
		print("Must Enter in a Map")
	else:
		board = []
		with open(sys.argv[1], 'r') as board_file:
			for line in board_file:
				linelist = line.split(" ")
				

