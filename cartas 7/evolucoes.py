from typing import List, Dict, Tuple, Optional
from collections import deque
import unicodedata

# --- Grafo de evoluções baseado no PDF reduzido ---
EVOLUTIONS: Dict[str, List[str]] = {
    "slime": ["slime 2", "peixe"],
    "slime 2": ["trilobita", "slime 3"],
    "trilobita": ["trilobita 2", "aranha do mar"],
    "trilobita 2": ["camarão", "inseto alado"],
    "aranha do mar": ["aranha do mar 2", "aranha"],
    "camarão": ["camarão pistola", "caranguejo"],
    "inseto alado": ["abelha", "besouro cortador"],
    "aranha": ["aranha 2", "escorpião"],
    "aranha do mar 2": ["aranha do mar 3", "carrapato"],

    "slime 3": ["lapa", "slime 4"],
    "lapa": ["amonite", "caracol"],
    "amonite": ["amonite 2", "polvo"],
    "caracol": ["caracol 2", "lesma"],
    "slime 4": ["estrela do mar", "água viva"],
    "estrela do mar": ["estrela do mar 2", "ouriço do mar"],
    "água viva": ["água viva 2", "água viva pólipo"],

    "peixe": ["peixe 2", "salamandra"],
    "peixe 2": ["peixe 3", "tubarão"],
    "peixe 3": ["peixe 4", "cavalo marinho"],
    "peixe 4": ["piranha", "salmão"],
    "cavalo marinho": ["cavalo marinho 2", "cavalo marinho dragão"],
    "tubarão": ["tubarão 2", "raia"],
    "tubarão 2": ["tubarão 3", "tubarão martelo"],
    "raia": ["raia elétrica", "raia manta"],

    "salamandra": ["salamandra 2", "lagarto"],
    "salamandra 2": ["sapo", "salamandra 3"],
    "lagarto": ["raptor", "mamífero"],
    "sapo": ["sapo transparente", "sapo peludo e com garras"],
    "salamandra 3": ["cobra cega", "salamandra 4"],
    "raptor": ["águia", "pterossauro", "crocodilo mosassauro"],
    "mamífero": ["capivara", "baleia"],
}

# --- Normalização de nomes (remove acentos / case-insensitive) ---
def _normalize(name: str) -> str:
    s = name.strip().lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")

# Mapeia nomes normalizados -> nome oficial
_name_map: Dict[str, str] = {}
for k in EVOLUTIONS.keys():
    _name_map[_normalize(k)] = k
for outs in EVOLUTIONS.values():
    for v in outs:
        _name_map[_normalize(v)] = v

def _resolve(name: str) -> Optional[str]:
    return _name_map.get(_normalize(name))

# --- Funções básicas ---
def can_evolve(creature: str) -> bool:
    real = _resolve(creature)
    return real in EVOLUTIONS and len(EVOLUTIONS.get(real, [])) > 0

def get_evolution(creature: str) -> List[str]:
    """Retorna lista de evoluções possíveis da criatura"""
    real = _resolve(creature)
    if real is None:
        return []
    return EVOLUTIONS.get(real, [])

def full_chain(start: str) -> List[List[str]]:
    real = _resolve(start)
    if real is None:
        return [[start]]
    evols = EVOLUTIONS.get(real, [])
    if not evols:
        return [[real]]
    chains = []
    for evo in evols:
        for path in full_chain(evo):
            chains.append([real] + path)
    return chains

# --- Distâncias (multi-root BFS) ---
def compute_distances_all_roots(evos: Dict[str, List[str]]) -> Dict[str, int]:
    nodes = set(evos.keys())
    for outs in evos.values():
        for v in outs:
            nodes.add(v)
    indeg = {n: 0 for n in nodes}
    for u, outs in evos.items():
        for v in outs:
            indeg[v] = indeg.get(v, 0) + 1
    roots = [n for n, d in indeg.items() if d == 0]
    dist = {}
    q = deque()
    for r in roots:
        dist[r] = 0
        q.append(r)
    while q:
        u = q.popleft()
        for v in evos.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist

DISTANCES = compute_distances_all_roots(EVOLUTIONS)

def get_stats(creature: str) -> Tuple[int, int, int]:
    """Retorna (custo, ataque, vida) baseados na distância ao root"""
    real = _resolve(creature)
    if real is None:
        raise ValueError(f"Criatura desconhecida: {creature}")
    d = DISTANCES.get(real, 0)
    return (d, 1 + d, 1 + d)

def get_all_creatures():
    """Retorna lista [(nome, custo, atk, vida)] de todas as criaturas"""
    result = []
    seen = set()
    for name in list(EVOLUTIONS.keys()) + [v for outs in EVOLUTIONS.values() for v in outs]:
        if name not in seen:
            c, a, h = get_stats(name)
            result.append((name, c, a, h))
            seen.add(name)
    return result

# --- Custos de invocação / evolução ---
def get_summon_cost(creature: str, used_material: bool = False) -> int:
    cost, _, _ = get_stats(creature)
    return max(1, cost - 1) if used_material else cost

def evolve_cost_direct(base: str, target: str) -> int:
    """Custo de evoluir diretamente base -> target (desconto -1 se for filho direto)"""
    b = _resolve(base)
    t = _resolve(target)
    if b and t and t in EVOLUTIONS.get(b, []):
        return get_summon_cost(t, used_material=True)
    return get_summon_cost(target, used_material=False)

def evolve_cost_any(base: str, target: str) -> int:
    """Custo de evoluir base em qualquer descendente target (desconto -1)"""
    if is_reachable(base, target):
        return get_summon_cost(target, used_material=True)
    return get_summon_cost(target, used_material=False)

# --- Utilitários de caminho ---
def is_reachable(base: str, target: str) -> bool:
    b = _resolve(base)
    t = _resolve(target)
    if b is None or t is None:
        return False
    seen = set()
    q = deque([b])
    while q:
        u = q.popleft()
        if u in seen: 
            continue
        seen.add(u)
        for v in EVOLUTIONS.get(u, []):
            if v == t:
                return True
            if v not in seen:
                q.append(v)
    return False

def find_path(base: str, target: str) -> Optional[List[str]]:
    b = _resolve(base)
    t = _resolve(target)
    if b is None or t is None:
        return None
    q = deque([b])
    parent = {b: None}
    while q:
        u = q.popleft()
        for v in EVOLUTIONS.get(u, []):
            if v not in parent:
                parent[v] = u
                q.append(v)
                if v == t:
                    path = []
                    cur = v
                    while cur is not None:
                        path.append(cur)
                        cur = parent[cur]
                    return list(reversed(path))
    return None

# --- Teste rápido ---
if __name__ == "__main__":
    print("Evoluções do peixe 4:", get_evolution("peixe 4"))
    print("Cadeia do slime:")
    for chain in full_chain("slime"):
        print(" -> ".join(chain))
    print("\nExemplo de custo:")
    print("Invocar piranha direto:", get_summon_cost("piranha"))
    print("Evoluir peixe 4 -> piranha:", evolve_cost_direct("peixe 4", "piranha"))