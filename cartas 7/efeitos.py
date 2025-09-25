import cartas

# sapo
def heal_hero(game, owner, target=None):
    owner.life = min(20, owner.life + 3)

# raia eletrica
def deal_damage(game, owner, target=None):
    other = game.player1 if owner is game.player2 else game.player2
    other.life -= 2
    game.check_winner()

# escorpião
def damage_all_on_death(game, owner, card):
    other = game.player1 if owner is game.player2 else game.player2
    for c in other.field:
        c.health -= 1
    other.remove_dead()

# raptor
def double_attack_on_attack(game, owner, target):
    if isinstance(target, cartas.Card):
        target.health -= owner.field[-1].attack  # dano extra

# capivara
def heal_self_activable(game, owner, target=None):
    owner.life = min(20, owner.life + 5)

# peixe
def draw_card_effect(game, owner, target=None):
    owner.draw_card()