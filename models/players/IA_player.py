import copy

class IAPlayer:

  import random
  
  def __init__(self, color):
    self.color = color  
  
  def play(self, board):
    moves = board.valid_moves(self.color)

    global emptySquares
	
    global initialDepth
    global lastV
    initialDepth = 3
    self.getDiscCount(board)
    if(emptySquares<=20):      
      initialDepth = 4            #brute force the tree
    lastV = -999999
    self.alphabeta(board, initialDepth, -999999, 999999, True)
    global chosenMove
    return chosenMove    
	
  def heuristic(self, board):
    return self.legalMovesCount(board) + self.cornerSquares(board) + (self.getDiscCount(board)/100) - self.enemyMovesCount(board)
	
  def cornerSquares(self, board):   #corner squares have a weight of 1000 (1 from legalMovesCount + 999) 
    result = 0
    if board.board[1][1] == self.color:
	  result+=999
    if (board.board[1][1] != self.color) and (board.board[1][1] != board.EMPTY):
	  result-=900
    if board.board[8][1] == self.color:
	  result+=999
    if (board.board[8][1] != self.color) and (board.board[8][1] != board.EMPTY):
	  result-=900
    if board.board[1][8] == self.color:
	  result+=999
    if (board.board[1][8] != self.color) and (board.board[1][8] != board.EMPTY):
	  result-=900
    if board.board[8][8] == self.color:
	  result+=999
    if (board.board[8][8] != self.color) and (board.board[8][8] != board.EMPTY):
	  result-=900
    return result
	
  def legalMovesCount(self, board):
    return len(board.valid_moves(self.color))

  def enemyMovesCount(self, board):
    if (self.color==board.WHITE):
      return len(board.valid_moves(board.BLACK))
    else:
      return len(board.valid_moves(board.WHITE))

  def getDiscCount(self, board):	#returns float
    global emptySquares
    emptySquares = 0
    count = 0.0
    for i in range(1, 9):
        for j in range(1, 9):
          if board.board[i][j] == self.color:
            count+=1.0
          if board.board[i][j] == board.EMPTY:
            emptySquares+=1
    return count
	
  def alphabeta(self, board, depth, alpha, beta, maximizingPlayer):
    global chosenMove
    global lastV
    enemyColor = board.WHITE
    if (self.color == board.WHITE):
      enemyColor = board.BLACK
    if (depth==0) or (self.legalMovesCount(board)==0):
      return self.heuristic(board)
    if maximizingPlayer:                            #maximizing player
      moves = board.valid_moves(self.color)           #every possible legal move
      v = -999999
      for move in moves:        
        newboard = copy.deepcopy(board)  
        newboard.play(move, self.color)
        v = max(v, self.alphabeta(newboard, depth-1, alpha, beta, False))
        alpha = max(alpha, v)
        if (depth==initialDepth) and (v>lastV):
          lastV=v
          chosenMove = copy.copy(move)
        if (beta <= alpha):
          break                                     #(* beta cut-off *)        
      return v
    else:                                           #minimizing player
      moves = board.valid_moves(enemyColor)           #every possible legal move
      v = 999999
      for move in moves:        
        newboard = copy.deepcopy(board)  
        newboard.play(move, enemyColor)
        v = min(v, self.alphabeta(newboard, depth-1, alpha, beta, True))
        beta = min(beta, v)
        if (beta <= alpha):
          break                                     #(* alpha cut-off *)
      return v
#initial call for maximizing player alphabeta(board, depth, -999999, 999999, True)
	
'''
  def minimax(self, board, depth, maximizingPlayer):
    global chosenMove
    if (depth==0) or (self.legalMovesCount(board)==0):
      return self.heuristic(board)
    moves = board.valid_moves(self.color)           #every possible legal move
    if maximizingPlayer:                            #maximizing player
      bestValue = -999999
      for move in moves:        
        newboard = copy.deepcopy(board)  
        newboard.play(move, self.color)		
        val = self.minimax(newboard, depth - 1, False)		
        bestValue = max(bestValue, val)
        if(bestValue>=val):
          chosenMove = copy.copy(move)
      return bestValue
    else:                                           #minimizing player
      bestValue = 999999
      for move in moves:
        newboard = copy.deepcopy(board)
        newboard.play(move, self.color)	  
        val = self.minimax(newboard, depth - 1, True)
        bestValue = min(bestValue, val)
      return bestValue
#initial call for maximizing player minimax(board, depth, True)
'''