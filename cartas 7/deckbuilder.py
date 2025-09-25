import random
import cartas
import evolucoes
import efeitos
from valores import MAX_DECK, MAX_COPIES

def build_deck():
    """
    Cria um deck com exatamente MAX_DECK cartas.
    Cada criatura pode ter no máximo MAX_COPIES cópias.
    Os efeitos são atribuídos às cartas.
    """
    deck = []
    all_creatures = evolucoes.get_all_creatures()

    # Dicionário para mapear nomes para efeitos
    effects_map = {
        "sapo": {"effect": efeitos.heal_hero},
        "raia elétrica": {"effect": efeitos.deal_damage},
        "escorpião": {"on_death": efeitos.damage_all_on_death},
        "raptor": {"on_attack": efeitos.double_attack_on_attack},
        "capivara": {"activable": efeitos.heal_self_activable},
        "peixe": {"effect": efeitos.draw_card_effect}
    }

    # Adicionar as cartas base
    for name, cost, atk, hp in all_creatures:
        # Pega os efeitos do mapa, se existirem
        card_effects = effects_map.get(name.lower(), {})

        # Cria a carta com os efeitos atribuídos
        new_card = cartas.Card(
            name, cost, atk, hp,
            effect=card_effects.get("effect"),
            on_death=card_effects.get("on_death"),
            on_attack=card_effects.get("on_attack"),
            activable=card_effects.get("activable")
        )

        # Adiciona a carta até o número máximo de cópias
        for _ in range(MAX_COPIES):
            deck.append(new_card.copy())

    # Embaralha o deck antes de preencher com slimes
    random.shuffle(deck)

    # Se faltar, completa com slime
    while len(deck) < MAX_DECK:
        print("[INFO] Deck incompleto, adicionando Slime extra.")
        # O Slime não tem limite de cópias, ele é o "filler"
        deck.append(cartas.Card("Slime", 1, 1, 1, effect=efeitos.heal_hero))

    # Corta o deck se exceder o limite (não deveria acontecer se as regras forem seguidas)
    if len(deck) > MAX_DECK:
        print("[AVISO] Deck excedeu o limite, cortando cartas extras.")
        deck = deck[:MAX_DECK]

    # Validação final (opcional, mas boa prática)
    validate_deck(deck)

    return deck


def validate_deck(deck):
    """
    Valida se o deck segue as regras:
    - Deve ter exatamente MAX_DECK cartas
    - Nenhuma carta (exceto Slime) pode ter mais que MAX_COPIES cópias
    """
    if len(deck) != MAX_DECK:
        print(f"[ERRO] Deck inválido: tem {len(deck)} cartas (esperado {MAX_DECK}).")
        return

    counts = {}
    for c in deck:
        counts[c.name.lower()] = counts.get(c.name.lower(), 0) + 1

    for name, count in counts.items():
        if name != "slime" and count > MAX_COPIES:
            print(f"[ERRO] Carta '{name}' tem {count} cópias (máx {MAX_COPIES}).")