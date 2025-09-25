#TODO: conferir os efeitos

import pygame
import random
import sys

# importando arquivos auxiliares
import evolucoes
import valores
import cartas
import deckbuilder

# -------- PYGAME UI & LÓGICA --------
class Game:
    def __init__(self):
        self.pending_card = None   # carta aguardando decisão de descarte

        pygame.init()
        self.screen = pygame.display.set_mode((cartas.valores.WIDTH, cartas.valores.HEIGHT))
        pygame.display.set_caption("Mini TCG - Multiplayer Local")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(cartas.valores.FONT_NAME, 18)
        self.bigfont = pygame.font.Font(cartas.valores.FONT_NAME, 28)

        deck1 = deckbuilder.build_deck()
        deck2 = deckbuilder.build_deck()  # pode mudar para outro deck manual depois

        self.player1 = cartas.Player("Player 1", deck1)
        self.player2 = cartas.Player("Player 2", deck2)

        self.player1.game_ref = self
        self.player2.game_ref = self

        self.current = self.player1
        self.other = self.player2
        self.turn = 1
        self.selected_card_idx = None
        self.selected_field_idx = None
        self.winner = None

        self.init_game()

    def init_game(self):
        for p in (self.player1, self.player2):
            p.hand = []
            p.field = []
            p.deck = p.deck[:]
            random.shuffle(p.deck)
            p.draw(3)
            p.max_mana = 2 # começando com 3 de mana
            p.mana = 0
            p.life = 20
        self.current = self.player1
        self.other = self.player2
        self.turn = 1
        self.selected_card_idx = None
        self.selected_field_idx = None
        self.winner = None
        self.start_turn(self.current)

    def start_turn(self, player):
        player.max_mana = min(cartas.valores.MAX_MANA, player.max_mana + 1)
        player.mana = player.max_mana 
        player.draw(1)
        for c in player.field:
            c.summoned_turn = False
            c.has_attacked = False

    def end_turn(self):
        self.selected_card_idx = None
        self.selected_field_idx = None
        self.current, self.other = self.other, self.current
        self.turn += 1
        self.start_turn(self.current)

    # --- Layout helpers ---
    def get_avatar_rect(self, player):
        if player is self.player1:
            return pygame.Rect(20, cartas.valores.HEIGHT - 220, 180, 180)
        else:
            return pygame.Rect(20, 40, 180, 180)

    def get_opponent_avatar_rect(self):
        return self.get_avatar_rect(self.other)

    def get_field_area(self, player):
        if player is self.player1:
            top = cartas.valores.HEIGHT - 360
        else:
            top = 220
        left = cartas.valores.BOARD_LEFT
        width = cartas.valores.WIDTH - left - cartas.valores.BOARD_RIGHT_PADDING
        height = cartas.valores.BOARD_HEIGHT
        return pygame.Rect(left, top, width, height)

    def get_hand_area(self, player):
        if player is self.player1:
            top = cartas.valores.HEIGHT - 150
        else:
            top = 40
        left = cartas.valores.BOARD_LEFT
        width = cartas.valores.WIDTH - left - cartas.valores.BOARD_RIGHT_PADDING
        height = 140
        return pygame.Rect(left, top, width, height)

    def get_hand_rects(self, player):
        area = self.get_hand_area(player)
        n = max(1, len(player.hand))
        card_w = max(60, min(110, area.width // n - 8))
        card_h = min(140, area.height - 8)
        spacing = min(140, max(20, (area.width - card_w) // max(1, n - 1)))
        rects = []
        start_x = area.x + (area.width - (card_w + spacing * (n - 1))) // 2
        y = area.y + (area.height - card_h) // 2
        for i in range(n):
            rects.append(pygame.Rect(start_x + i * spacing, y, card_w, card_h))
        return rects

    def get_field_slot_rects(self, player, slots=cartas.valores.BOARD_SLOTS):
        area = self.get_field_area(player)
        n = slots
        spacing = 16
        card_w = (area.width - spacing * (n - 1)) // n
        card_w = max(70, min(140, card_w))
        card_h = min(140, area.height - 8)
        total_width = card_w * n + spacing * (n - 1)
        start_x = area.x + (area.width - total_width) // 2
        y = area.y + (area.height - card_h) // 2
        rects = []
        for i in range(n):
            rects.append(pygame.Rect(start_x + i * (card_w + spacing), y, card_w, card_h))
        return rects

    # --- Interações ---
    def play_card_by_mouse(self, mouse_pos):
        hand_rects = self.get_hand_rects(self.current)
        for i, rect in enumerate(hand_rects):
            if rect.collidepoint(mouse_pos) and i < len(self.current.hand):
                played = self.current.play_from_hand(i)
                if played:
                    return True
        return False

    def select_field_card(self, mouse_pos, player):
        slot_rects = self.get_field_slot_rects(player)
        for i, rect in enumerate(slot_rects):
            if rect.collidepoint(mouse_pos):
                return i
        return None

    def attack_with_selected(self, target_pos):
        if self.selected_field_idx is None:
            idx = self.select_field_card(target_pos, self.current)
            if idx is not None and idx < len(self.current.field):
                c = self.current.field[idx]
                if not getattr(c, "summoned_turn", False) and not c.has_attacked:
                    self.selected_field_idx = idx
            return

        if self.selected_field_idx >= len(self.current.field):
            self.selected_field_idx = None
            return
        attacker = self.current.field[self.selected_field_idx]

        if attacker.has_attacked:
            self.selected_field_idx = None
            return

        opp_slot_idx = self.select_field_card(target_pos, self.other)
        if opp_slot_idx is not None and opp_slot_idx < len(self.other.field):
            defender = self.other.field[opp_slot_idx]
            defender.health -= attacker.attack
            attacker.health -= defender.attack
            # dispara on_attack se houver
            if getattr(attacker, "on_attack", None):
                attacker.trigger_on_attack(self, self.current, defender)
            attacker.has_attacked = True
            self.current.remove_dead()
            self.other.remove_dead()
            self.selected_field_idx = None
            return

        if self.get_opponent_avatar_rect().collidepoint(target_pos):
            self.other.life -= attacker.attack
            if getattr(attacker, "on_attack", None):
                attacker.trigger_on_attack(self, self.current, None)
            attacker.has_attacked = True
            self.check_winner()
            self.selected_field_idx = None
            return

        self.selected_field_idx = None

    def check_winner(self):
        if self.player1.life <= 0:
            self.winner = self.player2.name
        elif self.player2.life <= 0:
            self.winner = self.player1.name

    # --- Desenho ---
    def draw_card(self, surf, card, rect, selected=False, hide_details=False):
        color = cartas.valores.LIGHT_GREY if selected else cartas.valores.CARD_BG
        pygame.draw.rect(surf, color, rect, border_radius=6)
        pygame.draw.rect(surf, cartas.valores.DARK, rect, 2, border_radius=6)
        cost_rect = pygame.Rect(rect.x + 6, rect.y + 6, 36, 26)
        pygame.draw.rect(surf, cartas.valores.BLUE, cost_rect, border_radius=6)

        self.draw_text(surf, str(card.cost), cost_rect.center, 18, cartas.valores.WHITE, center=True)
        self.draw_text(surf, card.name, (rect.x + 10, rect.y + 40), 14)

        if card.effect:
            self.draw_text(surf, "Efeito!", (rect.x + 10, rect.y + rect.height - 70), 14, cartas.valores.RED)

        self.draw_text(surf, f"ATK: {card.attack}", (rect.x + 10, rect.y + rect.height - 46), 14)
        self.draw_text(surf, f"HP: {card.health}/{card.max_health}", (rect.x + 10, rect.y + rect.height - 26), 14)

        if card.has_attacked:
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            s.fill((120, 0, 0, 80))
            surf.blit(s, rect.topleft)
            self.draw_text(surf, "X", (rect.right - 18, rect.y + 8), 20, cartas.valores.WHITE, center=False)
        if card.summoned_turn:
            self.draw_text(surf, "Summ", (rect.x + rect.width - 44, rect.y + 8), 12, cartas.valores.DARK)

    def draw_text(self, surf, text, pos, size=18, color=cartas.valores.BLACK, center=False):
        font = pygame.font.Font(cartas.valores.FONT_NAME, size)
        rend = font.render(text, True, color)
        r = rend.get_rect()
        if center:
            r.center = pos
        else:
            r.topleft = pos
        surf.blit(rend, r)

    def render(self):
        s = self.screen
        s.fill((50, 55, 65))

        mouse_pos = pygame.mouse.get_pos()

        for p in (self.player1, self.player2):
            rect = self.get_avatar_rect(p)
            pygame.draw.rect(s, cartas.valores.GREY, rect)
            pygame.draw.rect(s, cartas.valores.DARK, rect, 2)
            self.draw_text(s, p.name, (rect.x + 10, rect.y + 8), 20)
            self.draw_text(s, f"Life: {p.life}", (rect.x + 10, rect.y + 40), 18)
            self.draw_text(s, f"Deck: {len(p.deck)}", (rect.x + 10, rect.y + 66), 16)
            self.draw_text(s, f"Field: {len(p.field)}", (rect.x + 10, rect.y + 88), 14)
            self.draw_text(s, f"Cemitério: {len(p.cemetery)}", (rect.x + 10, rect.y + 110), 14)

        self.draw_text(
            s,
            f"Turno: {self.turn}   Vez: {self.current.name}   Mana: {self.current.mana}/{self.current.max_mana}",
            (cartas.valores.WIDTH//2 - 320, 10), 20, cartas.valores.WHITE
        )

        for p in (self.other, self.current):
            slot_rects = self.get_field_slot_rects(p)
            for i, rect in enumerate(slot_rects):
                if i < len(p.field):
                    card = p.field[i]
                    selected = (p is self.current and self.selected_field_idx == i)
                    hide = (p is not self.current)
                    self.draw_card(s, card, rect, selected=selected, hide_details=hide)
                else:
                    pygame.draw.rect(s, (80, 80, 80), rect, 2, border_radius=6)
                    if self.selected_field_idx is not None and p is self.other and rect.collidepoint(mouse_pos):
                        txt = self.bigfont.render("?", True, cartas.valores.YELLOW)
                        tr = txt.get_rect(center=rect.center)
                        s.blit(txt, tr)

        for p in (self.other, self.current):
            hand_rects = self.get_hand_rects(p)
            for i, rect in enumerate(hand_rects):
                if i >= len(p.hand):
                    continue
                card = p.hand[i]
                hide = (p is not self.current)
                selected = (p is self.current and self.selected_card_idx == i)
                self.draw_card(s, card, rect, selected=selected, hide_details=hide)

        if self.selected_field_idx is not None:
            slot_rects = self.get_field_slot_rects(self.current)
            if self.selected_field_idx < len(slot_rects):
                r = slot_rects[self.selected_field_idx]
                pygame.draw.rect(s, cartas.valores.YELLOW, r, 4, border_radius=6)

        if self.winner:
            over_rect = pygame.Rect(cartas.valores.WIDTH//2 - 220, cartas.valores.HEIGHT//2 - 80, 440, 160)
            pygame.draw.rect(s, cartas.valores.YELLOW, over_rect)
            pygame.draw.rect(s, cartas.valores.DARK, over_rect, 3)
            self.draw_text(s, f"{self.winner} VENCEU!", (over_rect.x + 60, over_rect.y + 50), 48, cartas.valores.BLACK)

        # Se há uma carta aguardando escolha de descarte
        if self.pending_card:
            rect = pygame.Rect(cartas.valores.WIDTH//2 - 60, cartas.valores.HEIGHT//2 - 90, 120, 180)
            self.draw_card(self.screen, self.pending_card, rect, selected=True)
            self.draw_text(
                self.screen,
                "Escolha uma carta para descartar",
                (rect.x - 80, rect.y - 40),
                20,
                cartas.valores.YELLOW
            )

        pygame.display.flip()

    def update(self):
        self.check_winner()

    def run(self):
        running = True
        while running:
            self.clock.tick(cartas.valores.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Bloqueia turno se tiver descarte pendente
                        if not self.winner and not self.pending_card:
                            self.end_turn()
                    if event.key == pygame.K_r:
                        self.init_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.winner:
                        continue
                    pos = pygame.mouse.get_pos()

                    # --- Caso especial: escolher descarte ---
                    if self.pending_card:
                        # clique em uma carta da mão para descartar
                        hand_rects = self.get_hand_rects(self.current)
                        chosen = False
                        for i, rect in enumerate(hand_rects):
                            if rect.collidepoint(pos) and i < len(self.current.hand):
                                # descarta carta da mão
                                self.current.cemetery.add(self.current.hand.pop(i))
                                self.current.hand.append(self.pending_card)
                                self.pending_card = None
                                chosen = True
                                break

                        # clique na pending_card para descartar ela mesma
                        pending_rect = pygame.Rect(cartas.valores.WIDTH//2 - 60, cartas.valores.HEIGHT//2 - 90, 120, 180)
                        if not chosen and pending_rect.collidepoint(pos):
                            self.current.cemetery.add(self.pending_card)
                            self.pending_card = None

                        # bloqueia ações até o descarte ser resolvido
                        continue  # não faz outras jogadas até resolver o descarte

                    # --- fluxo normal se não há pending_card ---
                    played = self.play_card_by_mouse(pos)
                    if not played:
                        if self.selected_field_idx is not None:
                            self.attack_with_selected(pos)
                        else:
                            idx = self.select_field_card(pos, self.current)
                            if idx is not None and idx < len(self.current.field):
                                c = self.current.field[idx]
                                if not getattr(c, "summoned_turn", False) and not c.has_attacked:
                                    self.selected_field_idx = idx
                                else:
                                    self.selected_field_idx = None

            self.update()
            self.render()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run()