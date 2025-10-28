import pygame as pg
import sys
from pygame.locals import *
from random import randint
import math

WIDTH = 1280
HEIGHT = 720
MARGIN = 18
BG = (18, 20, 30)
BOARD_BG = (22, 26, 40)
LINE_COLOR = (90, 100, 120)
HIGHLIGHT = (36, 160, 220)
SELECT_COLOR = (255, 200, 40)
X_COLOR = (220, 80, 80)
O_COLOR = (80, 220, 120)
INFO_BG = (12, 14, 20)
FPS = 30

PLAYER_MARK = 'o'
COMP_MARK = 'x'

pg.init()
FONT = pg.font.Font(None, 20)
BIG = pg.font.Font(None, 28)
LARGE = pg.font.Font(None, 34)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Jogo da Velha com MULTIVERSO")
clock = pg.time.Clock()

def empty_board():
    return [[None for _ in range(3)] for __ in range(3)]

def copy_board(b):
    return [row[:] for row in b]

def check_board_winner(board):
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] and board[r][0] is not None:
            return board[r][0]
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] and board[0][c] is not None:
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    if all(all(cell is not None for cell in row) for row in board):
        return 'draw'
    return None

def check_global_draw(multiverse):
    all_full = True
    any_winner = False

    for timeline in multiverse:
        for row in timeline["board"]:
            if None in row:
                all_full = False
                break
        if timeline["winner"] is not None:
            any_winner = True
            break

    if all_full and not any_winner:
        for timeline in multiverse:
            timeline["state"] = "draw"
        return True
    return False

timelines = []
def new_initial_timeline():
    return {'states': [empty_board()], 'winner': None, 'draw': False}
timelines.append(new_initial_timeline())

branches = []

current_timeline_idx = 0
time_travel_mode = False
selected_timeline_for_travel = None
selected_turn_index_for_travel = None
global_result = None

page = 0
TIMELINES_PER_PAGE = 6 

def layout_params(n_timelines):
    cols = 3
    rows = (min(n_timelines, TIMELINES_PER_PAGE) + cols - 1) // cols
    if rows == 0:
        rows = 1
    board_w = (WIDTH - (cols + 1) * MARGIN) // cols
    board_h = (HEIGHT - 180 - (rows + 1) * MARGIN) // rows
    size = min(board_w, board_h)
    return cols, rows, size

def page_range():
    total = len(timelines)
    pages = max(1, math.ceil(total / TIMELINES_PER_PAGE))
    start = page * TIMELINES_PER_PAGE
    end = min(total, start + TIMELINES_PER_PAGE)
    return start, end, pages

def get_board_rect_on_page(display_index):
    cols, rows, size = layout_params(TIMELINES_PER_PAGE)
    col = display_index % cols
    row = display_index // cols
    x = MARGIN + col * (size + MARGIN)
    y = MARGIN + row * (size + MARGIN)
    return pg.Rect(x, y + 40, size, size) 

def get_timeline_display_index(global_idx):
    start, end, pages = page_range()
    if not (start <= global_idx < end):
        return None
    return global_idx - start

def cell_rect_in_board(board_rect, r, c):
    w = board_rect.width / 3
    h = board_rect.height / 3
    x = board_rect.x + c * w
    y = board_rect.y + r * h
    return pg.Rect(x, y, w, h)

def mini_cell_rect(t_idx, turn_index, r, c):
    disp = get_timeline_display_index(t_idx)
    if disp is None:
        return None
    board_rect = get_board_rect_on_page(disp)
   
    mini_h = 28
    mini_x = board_rect.x
    mini_y = board_rect.y - mini_h - 6
    states = timelines[t_idx]['states']
    max_show = 8 
    n = len(states)
    show = min(n, max_show)
    start_i = max(0, n - show)
    if not (start_i <= turn_index < n):
        pos = turn_index - start_i
    else:
        pos = turn_index - start_i
    slot_w = board_rect.width / show
    thumb_w = slot_w * 0.94
    thumb_h = mini_h * 0.9
    x = mini_x + pos * slot_w + (slot_w - thumb_w)/2
    cell_w = thumb_w / 3
    cell_h = thumb_h / 3
    cell_x = x + (c * cell_w)
    cell_y = mini_y + (mini_h - thumb_h)/2 + (r * cell_h)
    return pg.Rect(cell_x, cell_y, cell_w, cell_h)

def place_mark_on_timeline(t_idx, turn_index, r, c, mark):
    global timelines, branches
    tl = timelines[t_idx]
    states = tl['states']
    if turn_index < 0 or turn_index >= len(states):
        return None
    base = copy_board(states[turn_index])
    if base[r][c] is not None:
        return None
    base[r][c] = mark
    new_t = {'states': states[:turn_index+1] + [base], 'winner': None, 'draw': False}
    res = check_board_winner(base)
    if res == 'draw':
        new_t['draw'] = True
    elif res in ('x','o'):
        new_t['winner'] = res
    timelines.append(new_t)
    to_idx = len(timelines)-1
    branches.append({'from_t': t_idx, 'turn': turn_index, 'r': r, 'c': c, 'to_t': to_idx})
    return to_idx

def normal_move_on_current_timeline(r, c, mark):
    global timelines, current_timeline_idx
    tl = timelines[current_timeline_idx]
    last = copy_board(tl['states'][-1])
    if last[r][c] is not None or tl['winner'] or tl['draw']:
        return False
    last[r][c] = mark
    tl['states'].append(last)
    res = check_board_winner(last)
    if res == 'draw':
        tl['draw'] = True
    elif res in ('x','o'):
        tl['winner'] = res
    return True

def computer_move_on_timeline(t_idx):
    tl = timelines[t_idx]
    if tl['winner'] or tl['draw']:
        return
    last = copy_board(tl['states'][-1])
    empties = [(r,c) for r in range(3) for c in range(3) if last[r][c] is None]
    if not empties:
        return
    r,c = empties[randint(0,len(empties)-1)]
    last[r][c] = COMP_MARK
    tl['states'].append(last)
    res = check_board_winner(last)
    if res == 'draw':
        tl['draw'] = True
    elif res in ('x','o'):
        tl['winner'] = res

def evaluate_global_result():
    global global_result
    comp_win = any(tl.get('winner') == COMP_MARK for tl in timelines)
    player_win = any(tl.get('winner') == PLAYER_MARK for tl in timelines)
    if comp_win:
        global_result = COMP_MARK
    elif player_win:
        global_result = PLAYER_MARK
    else:
        all_done = all((tl.get('winner') is not None) or (tl.get('draw')) for tl in timelines)
        if all_done:
            global_result = 'draw'
        else:
            global_result = None

def reset_all():
    global timelines, branches, current_timeline_idx, time_travel_mode, selected_timeline_for_travel, selected_turn_index_for_travel, global_result, page
    timelines = [new_initial_timeline()]
    branches = []
    current_timeline_idx = 0
    time_travel_mode = False
    selected_timeline_for_travel = None
    selected_turn_index_for_travel = None
    global_result = None
    page = 0

reset_all()

def draw_x(surface, rect):
    pad = min(rect.width, rect.height) * 0.18
    pg.draw.line(surface, X_COLOR, (rect.x+pad, rect.y+pad), (rect.right-pad, rect.bottom-pad), 3)
    pg.draw.line(surface, X_COLOR, (rect.right-pad, rect.y+pad), (rect.x+pad, rect.bottom-pad), 3)

def draw_o(surface, rect):
    center = (rect.x + rect.width/2, rect.y + rect.height/2)
    radius = int(min(rect.width, rect.height)*0.36)
    pg.draw.circle(surface, O_COLOR, center, radius, 3)

def draw_branches():
    for b in branches:
        src_rect = mini_cell_rect(b['from_t'], b['turn'], b['r'], b['c'])
        to_disp = get_timeline_display_index(b['to_t'])
        dst_rect = None
        if to_disp is not None:
            board_rect = get_board_rect_on_page(to_disp)
            dst_rect = cell_rect_in_board(board_rect, b['r'], b['c'])
      
        if src_rect is None or dst_rect is None:
            continue
        src = (src_rect.x + src_rect.width/2, src_rect.y + src_rect.height/2)
        dst = (dst_rect.x + dst_rect.width/2, dst_rect.y + dst_rect.height/2)
     
        mid = ((src[0]+dst[0])/2, min(src[1], dst[1]) - 60)
        points = [src]
        steps = 20
        for t in range(1, steps+1):
            tt = t/steps
           
            x = (1-tt)**2*src[0] + 2*(1-tt)*tt*mid[0] + tt**2*dst[0]
            y = (1-tt)**2*src[1] + 2*(1-tt)*tt*mid[1] + tt**2*dst[1]
            points.append((x,y))
        pg.draw.lines(screen, (200,180,80), False, points, 2)
       
        angle = math.atan2(dst[1]-points[-2][1], dst[0]-points[-2][0])
        ah = 8
        p1 = (dst[0] - ah*math.cos(angle - 0.4), dst[1] - ah*math.sin(angle - 0.4))
        p2 = (dst[0] - ah*math.cos(angle + 0.4), dst[1] - ah*math.sin(angle + 0.4))
        pg.draw.polygon(screen, (200,180,80), [dst, p1, p2])

def draw_all():
    screen.fill(BG)
    
    start, end, pages = page_range()
    display_count = end - start
   
    for global_idx in range(start, end):
        disp = get_timeline_display_index(global_idx)
        board_rect = get_board_rect_on_page(disp)
    
        pg.draw.rect(screen, BOARD_BG, board_rect, border_radius=6)
       
        if global_idx == current_timeline_idx:
            pg.draw.rect(screen, HIGHLIGHT, board_rect, 4, border_radius=6)
        if time_travel_mode and global_idx == selected_timeline_for_travel:
            pg.draw.rect(screen, SELECT_COLOR, board_rect, 4, border_radius=6)

        mini_h = 28
        mini_area = pg.Rect(board_rect.x, board_rect.y - mini_h - 6, board_rect.width, mini_h)
       
        pg.draw.rect(screen, (28,28,34), mini_area, border_radius=4)
        states = timelines[global_idx]['states']
        n = len(states)
        max_show = 8
        show = min(max_show, n)
        start_i = max(0, n - show)
        slot_w = board_rect.width / show
        for i in range(show):
            si = start_i + i
            thumb_x = mini_area.x + i * slot_w + slot_w*0.03
            thumb_w = slot_w*0.94
            thumb_h = mini_h*0.9
            thumb_rect = pg.Rect(thumb_x, mini_area.y + (mini_h - thumb_h)/2, thumb_w, thumb_h)
            pg.draw.rect(screen, (12,16,20), thumb_rect, border_radius=3)
          
            small_cell_w = thumb_w / 3
            small_cell_h = thumb_h / 3
            st = states[si]
            for r in range(3):
                for c in range(3):
                    cr = pg.Rect(thumb_rect.x + c*small_cell_w, thumb_rect.y + r*small_cell_h, small_cell_w, small_cell_h)
                    if st[r][c] == 'x':
                        draw_x(screen, cr.inflate(-small_cell_w*0.18, -small_cell_h*0.18))
                    elif st[r][c] == 'o':
                        draw_o(screen, cr.inflate(-small_cell_w*0.18, -small_cell_h*0.18))
           
            if time_travel_mode and global_idx == selected_timeline_for_travel and si == selected_turn_index_for_travel:
                pg.draw.rect(screen, SELECT_COLOR, thumb_rect, 2, border_radius=3)
          
            txt = FONT.render(str(si), True, (180,180,180))
            screen.blit(txt, (thumb_rect.x + 2, thumb_rect.y - 14))

        for i in range(1,3):
            x = board_rect.x + i * board_rect.width/3
            pg.draw.line(screen, LINE_COLOR, (x, board_rect.y), (x, board_rect.y+board_rect.height), 2)
            y = board_rect.y + i * board_rect.height/3
            pg.draw.line(screen, LINE_COLOR, (board_rect.x, y), (board_rect.x+board_rect.width, y), 2)

        last = timelines[global_idx]['states'][-1]
        for r in range(3):
            for c in range(3):
                mark = last[r][c]
                if mark:
                    cr = cell_rect_in_board(board_rect, r, c).inflate(-board_rect.width*0.08, -board_rect.width*0.08)
                    if mark == 'x':
                        draw_x(screen, cr)
                    else:
                        draw_o(screen, cr)

        label = f"T{global_idx}  (len={len(states)-1})"
        t = FONT.render(label, True, (210,210,210))
        screen.blit(t, (board_rect.x+4, board_rect.y+4))
        if timelines[global_idx]['winner']:
            s = f"WIN:{timelines[global_idx]['winner']}"
            tt = FONT.render(s, True, (220,100,100))
            screen.blit(tt, (board_rect.right-78, board_rect.y+4))
        elif timelines[global_idx]['draw']:
            tt = FONT.render("DRAW", True, (200,200,120))
            screen.blit(tt, (board_rect.right-56, board_rect.y+4))

    draw_branches()

    info_rect = pg.Rect(0, HEIGHT-120, WIDTH, 120)
    pg.draw.rect(screen, INFO_BG, info_rect)
    mode_text = "VIAGEM: ON" if time_travel_mode else "VIAGEM: OFF"
    mode_surf = LARGE.render(mode_text, True, (230,230,230))
    screen.blit(mode_surf, (MARGIN, HEIGHT-108))

    ctrl_txt = "Controles: Clique timeline | T: alternar viagem | números 0..9: escolher turno (quando em viagem) | ← → trocar página | R: reset"
    screen.blit(FONT.render(ctrl_txt, True, (200,200,200)), (MARGIN, HEIGHT-72))

    if time_travel_mode:
        hint = "Modo Viagem: clique numa timeline para selecionar. Escolha turno (0..9) ou clique na mini (acima do board). Depois clique em uma célula do novo board para criar ramificação."
        screen.blit(FONT.render(hint, True, (220,220,180)), (MARGIN, HEIGHT-50))
    else:
        hint2 = "Modo Normal: clique na ponta de um timeline e jogue. Você é O (verde). Computador joga X (vermelho)."
        screen.blit(FONT.render(hint2, True, (200,200,200)), (MARGIN, HEIGHT-50))

    pg_count = BIG.render(f"Page {page+1}/{pages}", True, (200,200,200))
    screen.blit(pg_count, (WIDTH - MARGIN - pg_count.get_width(), HEIGHT-108))

    if global_result:
        if global_result == COMP_MARK:
            msg = "DERROTA GLOBAL: o computador venceu em alguma linha temporal! (clique para reset)"
            clr = (250,120,120)
        elif global_result == PLAYER_MARK:
            msg = "VITÓRIA GLOBAL: você venceu em alguma linha temporal! (clique para reset)"
            clr = (120,250,140)
        else:
            msg = "EMPATE GLOBAL. (clique para reset)"
            clr = (200,200,200)
        big = LARGE.render(msg, True, clr)
        screen.blit(big, (WIDTH//2 - big.get_width()//2, HEIGHT-90))

    pg.display.update()

def timeline_and_cell_from_pos(pos):
    start, end, pages = page_range()
    for gidx in range(start, end):
        disp = get_timeline_display_index(gidx)
        board_rect = get_board_rect_on_page(disp)
      
        mini_h = 28
        mini_area = pg.Rect(board_rect.x, board_rect.y - mini_h - 6, board_rect.width, mini_h)
        if mini_area.collidepoint(pos):
           
            states = timelines[gidx]['states']
            n = len(states)
            max_show = 8
            show = min(max_show, n)
            start_i = max(0, n - show)
            slot_w = board_rect.width / show
            relx = pos[0] - mini_area.x
            idx = int(relx // slot_w)
            idx = max(0, min(show-1, idx))
            turn = start_i + idx
          
            thumb_x = mini_area.x + idx * slot_w + slot_w*0.03
            thumb_w = slot_w*0.94
            thumb_h = mini_h*0.9
            relxx = pos[0] - thumb_x
            relyy = pos[1] - (mini_area.y + (mini_h - thumb_h)/2)
            c = int(relxx // (thumb_w/3))
            r = int(relyy // (thumb_h/3))
            c = max(0,min(2,c))
            r = max(0,min(2,r))
            return gidx, 'mini', turn, r, c
    
        if board_rect.collidepoint(pos):
            relx = pos[0] - board_rect.x
            rely = pos[1] - board_rect.y
            c = int(relx // (board_rect.width/3))
            r = int(rely // (board_rect.height/3))
            c = max(0,min(2,c))
            r = max(0,min(2,r))
            return gidx, 'board', len(timelines[gidx]['states'])-1, r, c
    return None, None, None, None, None

running = True
while running:
    for ev in pg.event.get():
        if ev.type == QUIT:
            running = False
            break
        if ev.type == KEYDOWN:
            if ev.key == K_t:
                time_travel_mode = not time_travel_mode
                selected_timeline_for_travel = None
                selected_turn_index_for_travel = None
            elif ev.key == K_r:
                reset_all()
            elif ev.key == K_LEFT:
                if page > 0:
                    page -= 1
            elif ev.key == K_RIGHT:
                _, _, pages = page_range()
                if page < pages-1:
                    page += 1
            elif time_travel_mode and selected_timeline_for_travel is not None:
                if ev.unicode.isdigit():
                    digit = int(ev.unicode)
                    max_turn = len(timelines[selected_timeline_for_travel]['states']) - 1
                    if digit <= max_turn:
                        selected_turn_index_for_travel = digit

        if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
            if global_result:
                reset_all()
                continue
            pos = pg.mouse.get_pos()
            gidx, area, turn, r, c = timeline_and_cell_from_pos(pos)
            if gidx is None:
                continue
            if not time_travel_mode:
                
                if gidx != current_timeline_idx:
                    current_timeline_idx = gidx
                else:
                    tl = timelines[current_timeline_idx]
                    last = tl['states'][-1]
                    if last[r][c] is None and not tl.get('winner') and not tl.get('draw'):
                        ok = normal_move_on_current_timeline(r, c, PLAYER_MARK)
                        if ok:
                            evaluate_global_result()
                            if not global_result:
                                computer_move_on_timeline(current_timeline_idx)
                                evaluate_global_result()
            else:
                if selected_timeline_for_travel is None:
                    selected_timeline_for_travel = gidx
                    selected_turn_index_for_travel = len(timelines[selected_timeline_for_travel]['states']) - 1

                    if area == 'mini':
                        selected_turn_index_for_travel = turn
                else:
                    if gidx != selected_timeline_for_travel:
                        selected_timeline_for_travel = gidx
                        selected_turn_index_for_travel = len(timelines[selected_timeline_for_travel]['states']) - 1
                        if area == 'mini':
                            selected_turn_index_for_travel = turn
                    else:
                        if area == 'mini':
                            selected_turn_index_for_travel = turn
                        elif area == 'board':
                            if selected_turn_index_for_travel is None:
                                selected_turn_index_for_travel = len(timelines[selected_timeline_for_travel]['states']) - 1
                            branch_idx = place_mark_on_timeline(selected_timeline_for_travel, selected_turn_index_for_travel, r, c, PLAYER_MARK)
                            if branch_idx is not None:
                                computer_move_on_timeline(branch_idx)
                                current_timeline_idx = branch_idx
                                selected_timeline_for_travel = None
                                selected_turn_index_for_travel = None
                                evaluate_global_result()
                            else:
                                selected_timeline_for_travel = None
                                selected_turn_index_for_travel = None

    draw_all()
    clock.tick(FPS)

pg.quit()
sys.exit()