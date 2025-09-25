import random

# importando arquivos auxiliares
import valores 
import efeitos

# importando o arquivo evolucoes inteiro
from evolucoes import *

# -------- CLASSES DO JOGO --------
class Card:
    def __init__(self, name, cost, attack, health, effect=None, on_death=None, on_attack=None, activable=None):
        self.name = name
        self.cost = cost
        self.attack = attack
        self.health = health
        self.max_health = health
        self.summoned_turn = False
        self.has_attacked = False

        self.effect = effect
        self.on_death = on_death
        self.on_attack = on_attack
        self.activable = activable

    def is_creature(self):
        return True

    def copy(self):
        return Card(
            self.name, self.cost, self.attack, self.max_health,
            self.effect, self.on_death, self.on_attack, self.activable
        )

    def trigger_effect(self, game, owner, target=None):
        if callable(self.effect):
            self.effect(game, owner, target)

    def trigger_on_death(self, game, owner):
        if callable(self.on_death):
            self.on_death(game, owner, self)

    def trigger_on_attack(self, game, owner, target):
        if callable(self.on_attack):
            self.on_attack(game, owner, target)

    def trigger_activable(self, game, owner):
        if callable(self.activable):
            self.activable(game, owner)

class Cemetery:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def last(self):
        return self.cards[-1] if self.cards else None

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

class Player:
    def __init__(self, name, deck_cards):
        self.name = name
        self.deck = deck_cards[:]
        random.shuffle(self.deck)
        self.hand = []
        self.field = []
        self.life = 20
        self.max_mana = 0
        self.mana = 0
        self.game_ref = None
        self.cemetery = Cemetery()

    def draw(self, n=1):
        drawn = []
        for _ in range(n):
            if not self.deck:
                self.life -= 1
                continue
            c = self.deck.pop(0)

            if len(self.hand) < valores.MAX_HAND:
                self.hand.append(c)
                drawn.append(c)
            else:
                # Se a mão está cheia -> salvar como pending_card para escolha
                if self.game_ref:  
                    self.game_ref.pending_card = c
                else:
                    # fallback se não tiver referência do jogo
                    self.cemetery.add(c)
        return drawn

    def play_from_hand(self, card_index):
        if card_index < 0 or card_index >= len(self.hand):
            return None
        card = self.hand[card_index]
        if card.cost > self.mana:
            return None

        # --- evolução ---
        evolved = False
        for i, field_card in enumerate(self.field):
            evolutions = get_evolution(field_card.name)
            if card.name.strip().lower() in [e.lower().strip() for e in evolutions]:
                if getattr(field_card, "on_death", None):
                    field_card.trigger_on_death(self.game_ref, self)
                self.cemetery.add(field_card)
                self.field[i] = card
                self.hand.pop(card_index)
                self.mana -= card.cost
                card.summoned_turn = True
                card.has_attacked = False
                if card.effect:
                    card.trigger_effect(self.game_ref, self)
                evolved = True
                break

        if evolved:
            return card

        # --- jogando normalmente ---
        if len(self.field) >= valores.BOARD_SLOTS:  # campo cheio
            return None

        self.mana -= card.cost
        self.field.append(card)
        card.summoned_turn = True
        card.has_attacked = False
        self.hand.pop(card_index)
        if card.effect:
            card.trigger_effect(self.game_ref, self)
        return card


    def remove_dead(self):
        survivors = []
        for c in self.field:
            if c.health > 0:
                survivors.append(c)
            else:
                if c.on_death:
                    c.trigger_on_death(self.game_ref, self)
                self.cemetery.add(c)
        self.field = survivors

    def activate_card_effect(self, card_index):
        if 0 <= card_index < len(self.field):
            card = self.field[card_index]
            if card.activable and self.mana >= card.cost:
                self.mana -= card.cost
                card.trigger_activable(self.game_ref, self)
                return True
        return False

# -------- UTILITÁRIOS --------
def make_sample_deck():
    cards = []
    from evolucoes import get_all_creatures
    bases = get_all_creatures()
    for name, cost, atk, hp in bases:
        for _ in range(4):
            effect = None
            on_death = None
            on_attack = None
            activable = None

            # --- Exemplos de associação ---
            if name == "sapo":
                effect = efeitos.heal_hero
            elif name == "raia elétrica":
                effect = efeitos.deal_damage
            elif name == "escorpiao":
                on_death = efeitos.damage_all_on_death
            elif name == "raptor":
                on_attack = efeitos.double_attack_on_attack
            elif name == "capivara":
                activable = efeitos.heal_self_activable

            cards.append(
                Card(name, cost, atk, hp,
                     effect=effect,
                     on_death=on_death,
                     on_attack=on_attack,
                     activable=activable)
            )
    random.shuffle(cards)
    return cards