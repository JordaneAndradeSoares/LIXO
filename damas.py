import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 720, 720
SQUARE = WIDTH // 8
FPS = 60

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (255, 255, 0)
SELECT = (0, 200, 255)
RED = (220, 20, 20)
BLACK = (30, 30, 30)
CROWN = (255, 215, 0)
MANDATORY = (255, 50, 50) # vermelho forte para capturas obrigatórias

FONT = pygame.font.SysFont("arial", SQUARE // 2)
SMALL = pygame.font.SysFont("arial", 18)

ROWS, COLS = 8, 8

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

class Damas:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Damas em Pygame")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        # peças pretas (b) no topo, vermelho (r) embaixo
        for r in range(3):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    self.board[r][c] = 'b'
        for r in range(5, 8):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    self.board[r][c] = 'r'

        self.turn_red = True
        self.selected = None
        self.valid_moves = {}
        self.must_capture = False
        self.game_over = False
        self.winner = None
        self.find_all_moves()

    def draw(self):
        # tabuleiro e peças
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * SQUARE, r * SQUARE, SQUARE, SQUARE)
                color = LIGHT if (r + c) % 2 == 0 else DARK

                pygame.draw.rect(self.screen, color, rect)

                # iluminar peças obrigadas a capturar
                if self.must_capture and (r, c) in self.valid_moves:
                    pygame.draw.rect(self.screen, MANDATORY, rect, 4)

                # seleção e highlights
                if self.selected == (r, c):
                    pygame.draw.rect(self.screen, SELECT, rect, 3)
                if self.selected and (r, c) in self.valid_moves.get(self.selected, []):
                    pygame.draw.rect(self.screen, HIGHLIGHT, rect, 3)

                piece = self.board[r][c]
                if piece:
                    self.draw_piece(r, c, piece)

        # texto de turno / instruções
        turn_text = 'VERMELHO' if self.turn_red else 'PRETO'
        txt = SMALL.render(f"Vez: {turn_text}  —  R para reset", True, (0, 0, 0))
        self.screen.blit(txt, (10, HEIGHT - 20))

        # se acabou, desenha overlay simples
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # semitransparente
            self.screen.blit(overlay, (0, 0))
            msg = f"Fim de jogo! Vencedor: {self.winner}" if self.winner else "Fim de jogo! Empate."
            label = FONT.render(msg, True, (255, 255, 255))
            rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(label, rect)
            hint = SMALL.render("Pressione R para reiniciar", True, (255, 255, 255))
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(hint, hint_rect)

    def draw_piece(self, r, c, piece):
        center = (c * SQUARE + SQUARE // 2, r * SQUARE + SQUARE // 2)
        color = RED if piece.lower() == 'r' else BLACK
        pygame.draw.circle(self.screen, color, center, SQUARE // 3)
        if piece.isupper():
            pygame.draw.circle(self.screen, CROWN, center, SQUARE // 6)

    def click(self, pos):
        if self.game_over:
            return

        r, c = pos[1] // SQUARE, pos[0] // SQUARE
        if not in_bounds(r, c):
            return

        # se já havia uma seleção, tenta mover
        if self.selected:
            dests = self.valid_moves.get(self.selected, [])
            if (r, c) in dests:
                self.make_move(self.selected, (r, c))
                return
            # clique fora de um destino cancela seleção (ou seleciona outra peça se válida)
            self.selected = None

        piece = self.board[r][c]
        if not piece:
            return

        # se é a vez da cor da peça
        if (self.turn_red and piece.lower() == 'r') or (not self.turn_red and piece.lower() == 'b'):
            # só permite selecionar se essa peça tiver movimentos válidos
            if (r, c) in self.valid_moves and self.valid_moves[(r, c)]:
                self.selected = (r, c)

    def find_all_moves(self):
        self.valid_moves = {}
        self.must_capture = False

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.board[r][c]
                if not piece:
                    continue
                # apenas peças do jogador atual
                if (self.turn_red and piece.lower() == 'r') or (not self.turn_red and piece.lower() == 'b'):
                    moves, captures = self.get_piece_moves(r, c)
                    if captures:
                        self.valid_moves[(r, c)] = captures
                        self.must_capture = True
                    elif moves:
                        self.valid_moves[(r, c)] = moves

        # se existe captura obrigatória, filtra movimentos simples
        if self.must_capture:
            for k in list(self.valid_moves.keys()):
                caps = [m for m in self.valid_moves[k] if abs(m[0] - k[0]) == 2]
                if caps:
                    self.valid_moves[k] = caps
                else:
                    # remove peças que não capturam
                    del self.valid_moves[k]

        # CORREÇÃO CRÍTICA: se não houver movimentos, o jogo acabou para o jogador atual
        if not self.valid_moves:
            self.selected = None
            self.game_over = True
            # vencedor é o adversário
            self.winner = 'PRETO' if self.turn_red else 'VERMELHO'
            return

        # se há movimentos, garante que game_over esteja falso
        self.game_over = False
        self.winner = None

    def get_piece_moves(self, r, c):
        piece = self.board[r][c]
        if not piece:
            return [], []

        # direções: peças simples and reis
        if piece.lower() == 'r' and not piece.isupper():
            directions = [(-1, -1), (-1, 1)]
        elif piece.lower() == 'b' and not piece.isupper():
            directions = [(1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        moves = []
        captures = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # movimento simples
            if in_bounds(nr, nc) and self.board[nr][nc] is None:
                moves.append((nr, nc))
            # captura
            elif in_bounds(nr, nc) and self.board[nr][nc] is not None:
                if self.board[nr][nc].lower() != piece.lower():
                    jr, jc = nr + dr, nc + dc
                    if in_bounds(jr, jc) and self.board[jr][jc] is None:
                        captures.append((jr, jc))
        return moves, captures

    def make_move(self, fr, to):
        fr_r, fr_c = fr
        to_r, to_c = to
        piece = self.board[fr_r][fr_c]
        if not piece:
            return

        was_capture = False
        # detectar captura (salto de 2)
        if abs(to_r - fr_r) == 2 and abs(to_c - fr_c) == 2:
            mr = (fr_r + to_r) // 2
            mc = (fr_c + to_c) // 2
            # remove a peça capturada
            self.board[mr][mc] = None
            was_capture = True

        # mover peça
        self.board[fr_r][fr_c] = None
        self.board[to_r][to_c] = piece

        # promoção a rei
        if piece == 'r' and to_r == 0:
            self.board[to_r][to_c] = 'R'
            piece = 'R'
        if piece == 'b' and to_r == 7:
            self.board[to_r][to_c] = 'B'
            piece = 'B'

        # se foi captura, verificar se há captura sequencial obrigatória
        if was_capture:
            _, more_caps = self.get_piece_moves(to_r, to_c)
            # manter apenas saltos (capturas)
            more_caps = [m for m in more_caps if abs(m[0] - to_r) == 2]
            if more_caps:
                # jogador continua com a mesma peça (captura múltipla)
                self.valid_moves = {(to_r, to_c): more_caps}
                self.selected = (to_r, to_c)
                self.must_capture = True
                return

        # troca de vez
        self.selected = None
        self.turn_red = not self.turn_red
        # recalcula movimentos do próximo jogador
        self.find_all_moves()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click(event.pos)

            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    Damas().run()