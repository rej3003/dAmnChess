import fileinput, re, os

board = {}
thumbdict = {}

#hello opalMist its rej and i think you should use this line in your code
boardnumbers = list("12345678")
boardletters = list("abcdefgh")
turn = "w"

usagelite = """<sub>Usage:

BASIC MOVE:
!chess [coordinate one's letter][coordinate one's digit][coordinate two's letter][coordinate two's digit]
REGEX: [a-h][1-8][a-h][1-8]
e.g. !chess a2a4 (That is, Move piece at A2 to A4)

This bot does not use established algebraic chess notation to perform moves. (At least not yet!)

See \'!help chess\' for extended documentation."""

usage = """<sub>Usage:

BASIC MOVE:
!chess [coordinate one's letter][coordinate one's digit][coordinate two's letter][coordinate two's digit]
REGEX: [a-h][1-8][a-h][1-8]
e.g. !chess a2a4 (That is, Move piece at A2 to A4)

CREATE PIECE:
!chess +[b or w (colour of piece)][p(pawn), r(rook), n(knight), b(bishop), q(queen) or k(king)][coordinate letter][coordinate digit]
REGEX: \+[bw][prnbqk][a-h][1-8]
e.g. !chess +wqc8 (That is, Create(+) a White Queen at C8)

DESTROY PIECE:
!chess -[coordinate's letter][coordinate's digit]
REGEX: -[a-h][1-8]
e.g. !chess -h4 (That is, Destroy(-) the piece at H4)

SWAP PIECES:
!chess %[coordinate one's letter][coordinate one's digit][coordinate two's letter][coordinate two's digit]
REGEX: %[a-h][1-8][a-h][1-8]
e.g. !chess %a1d4 (That is, Swap(%) the pieces at A1 and D4)

COMMAND CHAINING:
Multiple command \"segments\" can be used in chain, delimited by a space. Useful for en passant, castling and promotion. Any sane number of segments may be chained.
e.g. !chess -a7 +wqa8

BOARD SIZE:
50x50px tile squares may be too big for some. Command segments \'setsmall\' and \'setlarge\' may be used to change the board display size. Chainable.
e.g. !chess setsmall

BOARD REFRESH:
Re-updates the topic. Useful for fixing failed thumbnail loading. Chainable.
e.g. !chess refresh

BOARD RESET:
Used to place the board in starting position condition. Chainable.
e.g. !chess reset

DUMP BOARD STATE:
Outputs a string of command segments which represent the current board state. Good for saving your games for later. Chainable.
e.g. !chess dumpstate

CLEAR ALL:
Destroys all the things. Want a blank board? This is what you use. Chainable.
e.g. !chess clearall

UNDO:
Returns the board to the state it was in prior to its last change.
e.g. !chess undo"""



class main:
	
	
	def __init__(self, system):
		"""init"""
		self.name = "Chess"
		self.version = "0.4"
		self.author = "OpalMist"
		system.add_command("chess", self.chess, True, usage)
	
	
	
	def chess(self, ns, user, args, system): # chess()' own code at bottom
		
		def processcommandstring(self, n):
			"""Processes the give command string"""
			print ("Hi! I'm processcommandstring")
			if isvalidcommandstring(self, n) is True:
				for i in range (0, len(n)):
					processsegment(self, n[i])
			else: return
			return
		
		def isvalidcommandstring(self, n):
			"""Is input a valid command string? Returns True or False"""
			print ("Hi! I'm isvalidcommandstring()")
			failure = False
			# Iterate through each segment in the string, trip failure flag if isvalidsegment() rejects any.
			for i in range (0, len(n)):
				if isvalidsegment(self, n[i]) is False: failure = True
			if failure is False: return True
			else:
				print ("isvalidcommandstring() returned false for ", n)
				return False
		
		def isvalidsegment(self, n):
			"""Does input meet segment grammar requirements? Returns True or False"""
			print ("Hi! I'm isvalidsegment()")

			if n == "reset": return True
		
			if n == "dumpstate": return True
		
			if n == "clearall": return True
			
			if n == "refresh": return True

			if n == "setsmall": return True

			if n == "setlarge": return True
			
			if n == "undo": return True
			
			pattern = re.compile("[a-h][1-8][a-h][1-8]")
			if len(n) == 4:
				if pattern.match(n) is not None: return True # Fullmatch not in used version of python?
		
			pattern = re.compile("\+[bw][prnbqk][a-h][1-8]")
			if len(n) == 5:
				if pattern.match(n) is not None: return True
		
			pattern = re.compile("-[a-h][1-8]")
			if len(n) == 3:
				if pattern.match(n) is not None: return True
		
			pattern = re.compile("%[a-h][1-8][a-h][1-8]")
			if len(n) == 5:
				if pattern.match(n) is not None: return True
			else:
				print ("isvalidsegment() returned false for ", n)
				return False
		
		def processsegment(self, n):
			"""Segment in, forward to appropriate move function."""
			print ("Hi! I'm processsegment()")
			
			r = ""

			if n == "reset": boardreset(self)
			
			if n == "dumpstate": dumpstate(self)
			
			if n == "clearall": clearall(self)

			if n == "setsmall": setsize(self, "small")

			if n == "setlarge": setsize(self, "large")
			
			if n == "undo": undo(self)
			
			if n == "refresh": refreshboard(self)
			
			pattern = re.compile("[a-h][1-8][a-h][1-8]")
			if pattern.match(n) is not None: movemove(self, n)
			
			pattern = re.compile("\+[bw][prnbqk][a-h][1-8]")
			if pattern.match(n) is not None: moveadd(self, n)
			
			pattern = re.compile("-[a-h][1-8]")
			if pattern.match(n) is not None: movedestroy(self, n)
			
			pattern = re.compile("%[a-h][1-8][a-h][1-8]")
			if pattern.match(n) is not None: moveswap(self, n)
			
			return
		
		def clearall(self):
			"""Clears the board"""
			print ("Hi! I'm clearall()")
			processcommandstring(self, "-f1 -h8 -f3 -f4 -f5 -f6 -f7 -f8 -h3 -b3 -h6 -h7 -h4 -h5 -b4 -b5 -b6 -b7 -b1 -d8 -e4 -d6 -d7 -d4 -d5 -b8 -d3 -d1 -e1 -d2 -h2 -f2 -e3 -e2 -g7 -g6 -g5 -g4 -g3 -g2 -g1 -h1 -b2 -g8 -a1 -a3 -c8 -a5 -e8 -a7 -a6 -e5 -a8 -e7 -e6 -c7 -c6 -c5 -c4 -c3 -a2 -c1 -c2 -a4".split(" "))
			readboardtofile(self, "board.dat")
		
					
		def movemove(self, n):
			"""Valid move segment in, manipulate the array grid accordingly"""
			print ("Hi! I'm movemove()" ,n )
			coordinate1 = n[0]+n[1]
			coordinate2 = n[2]+n[3]
			if coordinate1 is not coordinate2:
				if board[coordinate1] != "xx":
					board[coordinate2] = board[coordinate1]
					board[coordinate1] = "xx"
			return
		
		def moveswap(self, n):
			"""Valid swap segment in, manipulate the array grid accordingly"""
			print ("Hi! I'm moveswap()")
			coordinate1 = n[1]+n[2]
			coordinate2 = n[3]+n[4]
			board[coordinate1], board[coordinate2] = board[coordinate2], board[coordinate1]
			return
		
		def moveadd(self, n):
			"""Valid add segment in, manipulate the array grid accordingly."""
			print ("Hi! I'm moveadd()")
			piecetype = n[1]+n[2]
			coordinate = n[3]+n[4]
			board[coordinate] = piecetype
			return
		
		def movedestroy(self, n):
			"""Valid destroy segment in, manipulate the array grid accordingly"""
			print ("Hi! I'm movedestroy()")
			coordinate = n[1]+n[2]
			board[coordinate] = "xx"
			return
		
		def boardreset(self):
			"""Resets the board"""
			print ("Hi! I'm boardreset()")
			processcommandstring(self, "+wbf1 +brh8 -f3 -f4 -f5 -f6 +bpf7 +bbf8 -h3 -b3 -h6 +bph7 -h4 -h5 -b4 -b5 -b6 +bpb7 +wnb1 +bqd8 -e4 -d6 +bpd7 -d4 -d5 +bnb8 -d3 +wqd1 +wke1 +wpd2 +wph2 +wpf2 -e3 +wpe2 +bpg7 -g6 -g5 -g4 -g3 +wpg2 +wng1 +wrh1 +wpb2 +bng8 +wra1 -a3 +bbc8 -a5 +bke8 +bpa7 -a6 -e5 +bra8 +bpe7 -e6 +bpc7 -c6 -c5 -c4 -c3 +wpa2 +wbc1 +wpc2 -a4".split(" "))
			readboardtofile(self, "board.dat")
			return

		def currentexpression(self):
			"""Returns the current board state as a command string"""
			expression = ""
			for index, entry in board.items():
				expression = expression + "+" + entry + index + " "
				expression = expression.replace("+xx", "-")
			expression = expression + "EOF"
			expression = expression.replace(" EOF", "")
			return expression
		
		def readboardtofile(self, bfile):
			"""Reads the board array to file"""
			print ("Hi! I'm readboardtofile()")
			if os.path.isfile("Storage/chess/"+ bfile) is False:
				system.bot.say (ns, "+++ OUT OF CHEESE ERROR (Missing boardfile. Botmaster intervention required. +++")
			boardhandle = open("Storage/chess/" + bfile, "w+")
			boardhandle.write(currentexpression(self))
			boardhandle.close()
			return

		def dumpstate(self):
			"""Outputs the current board state as a command string"""
			system.bot.say (ns, "<b></b>!chess " + currentexpression(self))
			return
		
		def readfiletoboard(self, bfile):
			"""Reads the file and feeds it into the command string interpreter"""
			print ("Hi! I'm readfiletoboard()")
			if os.path.isfile("Storage/chess/"+bfile) is True:
				boardhandle = open("Storage/chess/" + bfile, "r")
				n = boardhandle.read()
				n = n.split(" ")
				boardhandle.close()
				error = False
				if isvalidcommandstring(self, n) is True:
					processcommandstring(self, n)
					return
				else: error = True
			else: error = True
			if error is True:
				system.bot.say (ns, "+++ BAD BOARDFILE. RESETTING... +++")			
				boardreset(self)
			return

		def setsmall(self):

			"""Reads small thumbs into dictionary"""
			thumbdict['borderx']= ':thumb549998092:' ; thumbdict['border1'] = ':thumb549999927:' ; thumbdict['border2'] = ':thumb549999985:' ; thumbdict['border3'] = ':thumb550000027:'
			thumbdict['border4']= ':thumb550000095:' ; thumbdict['border5'] = ':thumb550000131:' ; thumbdict['border6'] = ':thumb550000172:' ; thumbdict['border7'] = ':thumb550000219:'
			thumbdict['border8']= ':thumb550000266:' ; thumbdict['bordera'] = ':thumb550006183:' ; thumbdict['borderb'] = ':thumb550006221:' ; thumbdict['borderc'] = ':thumb550006706:'
			thumbdict['borderd']= ':thumb550006284:' ; thumbdict['bordere'] = ':thumb550006324:' ; thumbdict['borderf'] = ':thumb550006351:' ; thumbdict['borderg'] = ':thumb550006393:'
			thumbdict['borderh']= ':thumb550006438:'

			thumbdict['xxb'] = ':thumb550008130:' ; thumbdict['bpb'] = ':thumb550007819:' ; thumbdict['wpb'] = ':thumb550008521:' ; thumbdict['brb'] = ':thumb550008626:'
			thumbdict['wrb'] = ':thumb550009022:' ; thumbdict['bnb'] = ':thumb550008784:' ; thumbdict['wnb'] = ':thumb550008940:' ; thumbdict['bbb'] = ':thumb550008716:'
			thumbdict['wbb'] = ':thumb550008866:' ; thumbdict['bqb'] = ':thumb550008821:' ; thumbdict['wqb'] = ':thumb550008988:' ; thumbdict['bkb'] = ':thumb550008747:'
			thumbdict['wkb'] = ':thumb550008900:' ; thumbdict['xxw'] = ':thumb550010354:' ; thumbdict['bpw'] = ':thumb550010247:' ; thumbdict['wpw'] = ':thumb550010480:'
			thumbdict['brw'] = ':thumb550010315:' ; thumbdict['wrw'] = ':thumb550010559:' ; thumbdict['bnw'] = ':thumb550010203:' ; thumbdict['wnw'] = ':thumb550010450:'
			thumbdict['bbw'] = ':thumb550010125:' ; thumbdict['wbw'] = ':thumb550010379:' ; thumbdict['bqw'] = ':thumb550010283:' ; thumbdict['wqw'] = ':thumb550010516:'
			thumbdict['bkw'] = ':thumb550010157:' ; thumbdict['wkw'] = ':thumb550010415:'
			return

		def setlarge(self):
			"""Reads big thumbs into dictionary"""
			thumbdict['borderx'] = ':thumb547646766:' ; thumbdict['border1'] = ':thumb547646779:' ; thumbdict['border2'] = ':thumb547646789:' ; thumbdict['border3'] = ':thumb547646795:'
			thumbdict['border4'] = ':thumb547646806:' ; thumbdict['border5'] = ':thumb547646817:' ; thumbdict['border6'] = ':thumb547646825:' ; thumbdict['border7'] = ':thumb547646833:'
			thumbdict['border8'] = ':thumb547646843:' ; thumbdict['bordera'] = ':thumb547646851:' ; thumbdict['borderb'] = ':thumb547646859:' ; thumbdict['borderc'] = ':thumb547646864:'
			thumbdict['borderd'] = ':thumb547646869:' ; thumbdict['bordere'] = ':thumb547646877:' ; thumbdict['borderf'] = ':thumb547646883:' ; thumbdict['borderg'] = ':thumb547646891:'
			thumbdict['borderh'] = ':thumb547646902:'
			
			thumbdict['xxb'] = ':thumb547649730:' ; thumbdict['bpb'] = ':thumb547646910:' ; thumbdict['wpb'] = ':thumb547647007:' ; thumbdict['brb'] = ':thumb547646942:'
			thumbdict['wrb'] = ':thumb547647039:' ; thumbdict['bnb'] = ':thumb547646751:' ; thumbdict['wnb'] = ':thumb547646994:' ; thumbdict['bbb'] = ':thumb547646713:'
			thumbdict['wbb'] = ':thumb547646962:' ; thumbdict['bqb'] = ':thumb547646925:' ; thumbdict['wqb'] = ':thumb547647022:' ; thumbdict['bkb'] = ':thumb547646725:'
			thumbdict['wkb'] = ':thumb547646978:' ; thumbdict['xxw'] = ':thumb547646955:' ; thumbdict['bpw'] = ':thumb547646918:' ; thumbdict['wpw'] = ':thumb547647014:'
			thumbdict['brw'] = ':thumb547646946:' ; thumbdict['wrw'] = ':thumb547647048:' ; thumbdict['bnw'] = ':thumb547646759:' ; thumbdict['wnw'] = ':thumb547647003:'
			thumbdict['bbw'] = ':thumb547646720:' ; thumbdict['wbw'] = ':thumb547646971:' ; thumbdict['bqw'] = ':thumb547646934:' ; thumbdict['wqw'] = ':thumb547647029:'
			thumbdict['bkw'] = ':thumb547646730:' ; thumbdict['wkw'] = ':thumb547646988:'
			return

		def setsize(self, n):
			""""writes to the size file"""
			sizehandle = open ("Storage/chess/size.dat", "w+")
			sizehandle.write(n)
			sizehandle.close()
			readsize(self)
			system.bot.set(ns, "topic", currentthumbstring(self))
			return

		def readsize(self):
			"""reads the sizefile and calls the appropriate function"""
			sizehandle = open ("Storage/chess/size.dat", "r")
			if sizehandle.read() == "small": setsmall(self)
			else: setlarge(self)
			sizehandle.close()
			return
			
		def readtofile(self, nfile, ndata):
			filehandle = open ("Storage/chess/" + nfile, "w+")
			filehandle.write(ndata)
			filehandle.close()
			
		def readfromfile(self, nfile):
			filehandle = open ("Storage/chess/" + nfile, "r")
			ndata = filehandle.read()
			filehandle.close()
			return ndata
		
		def currentthumbstring(self):
			"""Reads values from grid array and returns the outgoing topic string"""
			print ("Hi! I'm currentthumbstring()")
			
			n=""
			n = n + (":borderx::bordera::borderb::borderc::borderd::bordere::borderf::borderg::borderh::borderx:<br/>")
			n = n + (":border8:"+":"+board["a8"]+"w::"+board["b8"]+"b::"+board["c8"]+"w::"+board["d8"]+"b::"+board["e8"]+"w::"+board["f8"]+"b::"+board["g8"]+"w::"+board["h8"]+"b:"+":border8:"+"<br/>")
			n = n + (":border7:"+":"+board["a7"]+"b::"+board["b7"]+"w::"+board["c7"]+"b::"+board["d7"]+"w::"+board["e7"]+"b::"+board["f7"]+"w::"+board["g7"]+"b::"+board["h7"]+"w:"+":border7:"+"<br/>")
			n = n + (":border6:"+":"+board["a6"]+"w::"+board["b6"]+"b::"+board["c6"]+"w::"+board["d6"]+"b::"+board["e6"]+"w::"+board["f6"]+"b::"+board["g6"]+"w::"+board["h6"]+"b:"+":border6:"+"<br/>")
			n = n + (":border5:"+":"+board["a5"]+"b::"+board["b5"]+"w::"+board["c5"]+"b::"+board["d5"]+"w::"+board["e5"]+"b::"+board["f5"]+"w::"+board["g5"]+"b::"+board["h5"]+"w:"+":border5:"+"<br/>")
			n = n + (":border4:"+":"+board["a4"]+"w::"+board["b4"]+"b::"+board["c4"]+"w::"+board["d4"]+"b::"+board["e4"]+"w::"+board["f4"]+"b::"+board["g4"]+"w::"+board["h4"]+"b:"+":border4:"+"<br/>")
			n = n + (":border3:"+":"+board["a3"]+"b::"+board["b3"]+"w::"+board["c3"]+"b::"+board["d3"]+"w::"+board["e3"]+"b::"+board["f3"]+"w::"+board["g3"]+"b::"+board["h3"]+"w:"+":border3:"+"<br/>")
			n = n + (":border2:"+":"+board["a2"]+"w::"+board["b2"]+"b::"+board["c2"]+"w::"+board["d2"]+"b::"+board["e2"]+"w::"+board["f2"]+"b::"+board["g2"]+"w::"+board["h2"]+"b:"+":border2:"+"<br/>")
			n = n + (":border1:"+":"+board["a1"]+"b::"+board["b1"]+"w::"+board["c1"]+"b::"+board["d1"]+"w::"+board["e1"]+"b::"+board["f1"]+"w::"+board["g1"]+"b::"+board["h1"]+"w:"+":border1:"+"<br/>")
			n = n + (":borderx::bordera::borderb::borderc::borderd::bordere::borderf::borderg::borderh::borderx:")
			
			n = n.replace(':borderx:', thumbdict['borderx']); n = n.replace(':bordera:', thumbdict['bordera']); n = n.replace(':borderb:', thumbdict['borderb']) ; n = n.replace(':borderc:', thumbdict['borderc'])
			n = n.replace(':borderd:', thumbdict['borderd']); n = n.replace(':bordere:', thumbdict['bordere']); n = n.replace(':borderf:', thumbdict['borderf']); n = n.replace(':borderg:', thumbdict['borderg'])
			n = n.replace(':borderh:', thumbdict['borderh']); n = n.replace(':border1:', thumbdict['border1']); n = n.replace(':border2:', thumbdict['border2']); n = n.replace(':border3:', thumbdict['border3'])
			n = n.replace(':border4:', thumbdict['border4']); n = n.replace(':border5:', thumbdict['border5']); n = n.replace(':border6:', thumbdict['border6']); n = n.replace(':border7:', thumbdict['border7'])
			n = n.replace(':border8:', thumbdict['border8'])

			n = n.replace(":xxb:", thumbdict["xxb"]); n = n.replace(":bpb:", thumbdict["bpb"]); n = n.replace(":wpb:", thumbdict["wpb"]); n = n.replace(":brb:", thumbdict["brb"])
			n = n.replace(":wrb:", thumbdict["wrb"]); n = n.replace(":bnb:", thumbdict["bnb"]); n = n.replace(":wnb:", thumbdict["wnb"]); n = n.replace(":bbb:", thumbdict["bbb"])
			n = n.replace(":wbb:", thumbdict["wbb"]); n = n.replace(":bqb:", thumbdict["bqb"]); n = n.replace(":wqb:", thumbdict["wqb"]); n = n.replace(":bkb:", thumbdict["bkb"])
			n = n.replace(":wkb:", thumbdict["wkb"]); n = n.replace(":xxw:", thumbdict["xxw"]); n = n.replace(":bpw:", thumbdict["bpw"]); n = n.replace(":wpw:", thumbdict["wpw"])
			n = n.replace(":brw:", thumbdict["brw"]); n = n.replace(":wrw:", thumbdict["wrw"]); n = n.replace(":bnw:", thumbdict["bnw"]); n = n.replace(":wnw:", thumbdict["wnw"])
			n = n.replace(":bbw:", thumbdict["bbw"]); n = n.replace(":wbw:", thumbdict["wbw"]); n = n.replace(":bqw:", thumbdict["bqw"]); n = n.replace(":wqw:", thumbdict["wqw"])
			n = n.replace(":bkw:", thumbdict["bkw"]); n = n.replace(":wkw:", thumbdict["wkw"])
			
			return n
			
			
		def coordmod(self, coord, modbyx, modbyy):
			"""WIP Accepts coordinate and its intended modifiers. Returns new coordinate or 'ERR' if out of range"""
			print ("Hi! I'm coordmod()")
			try:	
				coord = coord[0] + " " + coord[1]
				coord = coord.split(" ")
				currentx = boardletters.index(coord[0]) +1
				currenty = boardnumbers.index(coord[1]) +1 
				currentx = currentx + modbyx
				currenty = currenty + modbyy
				if currentx < 1: return "ERR"
				if currenty < 1: return "ERR"
				if currentx > len(boardletters): return "ERR"
				if currenty > len(boardnumbers): return "ERR"
				coord[0]=boardletters[currentx - 1]
				coord[1]=boardnumbers[currenty - 1]
				coord = "".join(coord)
			except(IndexError):
				return "ERR"
				
			return coord
			
		
		
		def scan(self, fromcoord, NSEW, maxsteps):
			"""Accepts a coordinate, direction and maximum steps (<1 for until bump.)"""
						
			

			if NSEW == "N":
				xmod = 0
				ymod = 1
			if NSEW == "NE":
				xmod = 1
				ymod = 1
			if NSEW == "E":
				xmod = 1
				ymod = 0
			if NSEW == "SE":
				xmod = 1
				ymod = -1
			if NSEW == "S":
				xmod = 0
				ymod = -1
			if NSEW == "SW":
				xmod = -1
				ymod = -1
			if NSEW == "W":
				xmod = -1
				ymod = 0
			if NSEW == "NW":
				xmod = -1
				ymod = 1 			
			
			bump = False
			steps = 0
			whatdidibumpinto = ""
			threatenedtiles = ""
			threatening = ""
			while bump is False:
				try:
					steps = steps + 1
					if steps == maxsteps: bump = True
					n = board[coordmod(self, fromcoord, steps * xmod, steps * ymod)]
					if n != "xx":
						whatdidibumpinto = n
						bump = True
					
				except(KeyError):
					bump = True
					whatdidibumpinto = "wall"
					
			threatening = threatening.replace("fromcoord" + " ", "")
			return threatening
			
		def queenthreatens(self, coord):
			"""Accepts a tile coordinate. Returns a list of threatened coordinates assuming a queen is on that tile."""
			threatens=""
			threatens = threatens + scan (self, coord, "N", 0)
			threatens = threatens + scan (self, coord, "NE", 0)
			threatens = threatens + scan (self, coord, "E", 0)
			threatens = threatens + scan (self, coord, "SE", 0)
			threatens = threatens + scan (self, coord, "S", 0)
			threatens = threatens + scan (self, coord, "SW", 0)
			threatens = threatens + scan (self, coord, "W", 0)
			threatens = threatens + scan (self, coord, "NW", 0)
			threatens = threatens  + "EOL"
			threatens = threatens.replace (" EOL", "")
			return threatens
			
		def rookthreatens(self, coord):
			"""Accepts a tile coordinate. Returns a list of threatened coordinates assuming a rook is on that tile."""
			threatens=""
			threatens = threatens + scan (self, coord, "N", 0)
			threatens = threatens + scan (self, coord, "E", 0)
			threatens = threatens + scan (self, coord, "S", 0)
			threatens = threatens + scan (self, coord, "W", 0)
			threatens = threatens + "EOL"
			threatens = threatens.replace (" EOL", "")
			return threatens
			
		def bishopthreatens(self, coord):
			"""Accepts a tile coordinate. Returns a list of threatened coordinates assuming a bishop is on that tile."""
			threatens=""
			threatens = threatens + scan (self, coord, "NE", 0)
			threatens = threatens + scan (self, coord, "SE", 0)
			threatens = threatens + scan (self, coord, "SW", 0)
			threatens = threatens + scan (self, coord, "NW", 0)
			threatens = threatens  + "EOL"
			threatens = threatens.replace (" EOL", "")
			return threatens
			
		def kingthreatens(self, coord):
			"""Accepts a tile coordinate. Returns a list of threatened coordinates assuming a rook is on that tile."""
			threatens=""
			threatens = threatens + scan (self, coord, "N", 1)
			threatens = threatens + scan (self, coord, "NE", 1)
			threatens = threatens + scan (self, coord, "E", 1)
			threatens = threatens + scan (self, coord, "SE", 1)
			threatens = threatens + scan (self, coord, "S", 1)
			threatens = threatens + scan (self, coord, "SW", 1)
			threatens = threatens + scan (self, coord, "W", 1)
			threatens = threatens + scan (self, coord, "NW", 1)
			threatens = threatens + "EOL"
			threatens = threatens.replace (" EOL", "")
			return threatens
			
			
		def knightthreatens(self, coord):
			"""Accepts a coordinate. Returns a list of threatened coordinates assuming a knight is on that tile"""
			threatens=""
			threatens = threatens + coordmod(self, coord, 1, 2) + " "
			threatens = threatens + coordmod(self, coord, 2, 1) + " "
			threatens = threatens + coordmod(self, coord, 2, -1) + " "
			threatens = threatens + coordmod(self, coord, 1, -2)+ " "
			threatens = threatens + coordmod(self, coord, -1, -2) + " "
			threatens = threatens + coordmod(self, coord, -2, -1) + " "
			threatens = threatens + coordmod(self, coord, -2, 1) + " "
			threatens = threatens + coordmod(self, coord, -1, 2) + " "
			threatens = threatens.replace("ERR ", "")
			threatens = threatens + "EOL"
			threatens = threatens.replace(" EOL", "")
			return threatens

		def whitepawnthreatens(self, coord):
			"""Accepts a coordinate. Returns a list of threatened coordinates assuming a white pawn is on that tile"""
			threatens = ""
			threatens = threatens + coordmod(self, coord, 1, 1) + " "
			threatens = threatens + coordmod(self, coord, -1, 1) + " "
			threatens = threatens.replace("ERR ", "")
			threatens = threatens + "EOL"
			threatens = threatens.replace(" EOL", "")
			return threatens

		def blackpawnthreatens(self, coord):
			"""Accepts a coordinate. Returns a list of threatened coordinates assuming a black pawn is on that tile"""
			threatens = ""
			threatens = threatens + coordmod(self, coord, 1, -1) + " "
			threatens = threatens + coordmod(self, coord, -1, -1) + " "
			threatens = threatens.replace("ERR ", "")
			threatens = threatens + "EOL"
			threatens = threatens.replace(" EOL", "")
			return threatens
			
		def threatenedby(self, colour):
			"""Accepts a colour. (b or w) Returns a list of all coordinates currently threatened by that colour's pieces"""
			threatenslist = ""
			for coord,piece in board.items():
				if piece != "xx":
					if piece [0] == colour:
						if piece == "wp" and colour == "w": threatenslist = threatenslist + whitepawnthreatens(self, coord) + " "
						if piece == "bp" and colour == "b": threatenslist = threatenslist + blackpawnthreatens(self, coord) + " "
						if piece[1] == "r": threatenslist = threatenslist + rookthreatens(self, coord) + " "
						if piece[1] == "n": threatenslist = threatenslist + knightthreatens(self, coord) + " "
						if piece[1] == "b": threatenslist = threatenslist + bishopthreatens(self, coord) + " "
						if piece[1] == "k": threatenslist = threatenslist + kingthreatens(self, coord) + " "
						if piece[1] == "q": threatenslist = threatenslist + queenthreatens(self, coord) + " "
			threatenslist = threatenslist + "EOL"
			threatenslist = threatenslist.replace(" EOL", "")
			return threatenslist
			
		def isincheck(self, colour, threatening):
			"""Accepts a colour to be threatened and a list of coordinates to be considered threatening. Returns True or False."""
			threatening = threatening.split(" ")
			for index, entry in board.items():
				if entry == colour + "k":
					for i in range (0, len(threatening)-1):
						if threatening[i] == index: return True
			return False
			
		def alertifcheck(self):		
			if isincheck(self, "b", threatenedby(self, "w")) is True: system.bot.say (ns, "<b>Black is in check!</b>")
			if isincheck (self, "w", threatenedby(self, "b")) is True: system.bot.say (ns, "<b>White is in check!</b>")
			
		def nextturn(self):
			if turn == "w":
				turn == "b"
				system.bot.say (ns, "<b>Black's Turn</b>")
			if turn == "b":
				turn == "w"
				system.bot.say (ns, "<b>White's Turn</b>")
			return
			
		def undo(self):
			readfiletoboard(self, "undo.dat")
			return
			
		def settopic(self):
			system.bot.set(ns, "topic", currentthumbstring(self))
			return
			
		def refreshboard(self):
			return
			

		readfiletoboard(self, "board.dat")
		boardold = currentexpression(self)
		inputfromdamn = args ### INPUTFROMdAMN
		if len(inputfromdamn) == 1:
			print ("Command string blank")
			system.bot.say (ns, usagelite)
			return
		else:
			del inputfromdamn[0]
			if isvalidcommandstring(self, inputfromdamn) is True:
				processcommandstring(self, inputfromdamn)
				readboardtofile(self, "board.dat")
			else:
				system.bot.say (ns, "+++ MELON MELON MELON [BAD INPUT] See \'!help chess\' +++")
				return
		readsize(self)
		alertifcheck(self)
		#if boardold != currentexpression(self):
		system.bot.set(ns, "topic", currentthumbstring(self))
		readtofile(self, "undo.dat", boardold)
		return


