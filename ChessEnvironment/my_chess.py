pieces_number_FEN = {
    0:  'P',
    1:  'R',
    2:  'N',
    3:  'B',
    4:  'Q',
    5:  'K',
    6:  'p',
    7:  'r',
    8:  'n',
    9:  'b',
    10: 'q',
    11: 'k',
}

class ChessDict():
    def empty_board(self) -> None:
        self.chess_dict = {}
        for i in range(8):
            self.chess_dict[i] = {}
            for j in range(8):
                    self.chess_dict[i][j] = None

    def start_board(self):
        self.chess_dict = {}
        for i in range(8):
            if i == 0:
                self.chess_dict[i] = {0: 'R', 1: 'N', 2: 'B', 3: 'Q', 4: 'K', 5: 'B', 6: 'N', 7: 'R'}

            elif i == 1:
                self.chess_dict[i] = {}
                for j in range(8):
                    self.chess_dict[i][j] = 'P'

            elif i == 6:
                self.chess_dict[i] = {}
                for j in range(8):
                    self.chess_dict[i][j] = 'p'

            elif i == 7:
                self.chess_dict[i] = {0: 'r', 1: 'n', 2: 'b', 3: 'q', 4: 'k', 5: 'b', 6: 'n', 7: 'r'}

            else:
                self.chess_dict[i] = {}
                for j in range(8):
                        self.chess_dict[i][j] = None

    def __init__(self, mod='start') -> None:
        if mod == 'start':
            self.start_board()
        elif mod == 'empty':
            self.empty_board()
        else:
            self.empty_board()
    
    def _read_uci_position(self, uci:str):
        uci = uci.lower()
        return int(uci[1])-1, ord(uci[0])-97

    def __getitem__(self, key):
        if type(key) is int:
            if key < 10:
                return self.chess_dict[key]
        
        if type(key) is str:
            key = self._read_uci_position(key)

        return self.chess_dict[key[0]][key[1]]
    
    def __setitem__(self, key, value):
        if type(key) is int:
            if key < 10:
                self.chess_dict[key] = value
        
        if type(key) is str:
            key = self._read_uci_position(key)

        self.chess_dict[key[0]][key[1]] = value

    def __str__(self) -> str:
        out_str = ''
        for key_1 in range(7,-1,-1):
            for key_a in self[key_1]:
                if self[key_1, key_a] is None:
                    out_str += '_'
                else:
                    out_str += self[key_1, key_a]
            out_str += '\n'

        return out_str
    
    def __sub__(self, other):
        ans = []
        for i in range(8):
            for j in range(8):
                if self[i, j] != other[i, j]:
                    ans.append([i, j])
        return ans
    
    def move(self, uci_move:str):
        uci_from, uci_to = uci_move.lower().split(' ')
        self[uci_to] = self[uci_from]
        self[uci_from] = None

    def coord_cls_to_board(self, xyc_list):
        self.empty_board()
        for x, y, c in xyc_list:
            self[int(y*8), int(x*8)] = pieces_number_FEN[c]

def _key_to_uci(key):
    return chr(key[1]+97)+str(key[0]+1)

def find_move(difference:list, board_next):
    if board_next[difference[0]] == None:
        key_from, key_to = difference[0], difference[1]
    else:
        key_from, key_to = difference[1], difference[0]

    return _key_to_uci(key_from) + ' ' + _key_to_uci(key_to)

chess = ChessDict()
chess1 = ChessDict()
chess3 = ChessDict('empty')
chess3.coord_cls_to_board([[0.1, 0.1, 0],[0.2, 0.2, 6]])

# chess['e2'] = 'K'

chess.move('e2 e4')
chess1.move('e2 e4')

chess.move('d7 d5')
chess1.move('d7 d5')

# chess.move('e2 e4')
chess1.move('e4 d5')

print(chess)
print(find_move(chess-chess1, chess1))
print(chess[1])
print(chess3)