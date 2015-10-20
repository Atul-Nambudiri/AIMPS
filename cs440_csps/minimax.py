import sys 

def main():
	if len(sys.argv) < 2:
		print("Must Enter in a Map")
	else:
		board = []
		with open(sys.argv[1], 'r') as board_file:
			for line in board_file:
				linelist = line.strip('\t').strip('\r\n').split(" ")
				linelist = [int(x) for x in linelist]
				board.append(linelist)
		print(board)

if __name__ == "__main__":
	main()


