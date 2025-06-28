import random

import numpy as np
import pygame
import sys
import math

from source import main
from source.logic.AI import get_ai_move
from source.main import scroll_state
from source.menus import main_menu
from source.utils import size, DragDebugger, DebugSprite, get_owner, SM, SpriteSheetAtlas, Sprite
from source.logic.piece import Piece, PieceType

from source.shaders.CA import Abber

# test_atlas = SpriteSheetAtlas(
#     assets["images/BOYFRIEND.png"],
#     assets["images/BOYFRIEND.xml"]
# )

# test_sprite = utils.Sprite(
#     test_atlas,
#     pos=(550, 300),
#     animations=["BF idle dance"],
#     scale=0.6,
#     frame_rate=24
# )

# test_sprite.update(dt)
# test_sprite.draw(scene_surface)
def run_connect_four(screen, assets, difficulty, draw_fps):
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    SQUARESIZE = 80

    w, h = screen.get_size()
    scene_surface = pygame.Surface((w, h))

    boardSprite = size(assets[f"images/board{difficulty}.png"], 1)

    player_piece = size(assets["images/blue.png"], 1)
    enemy_piece = size(assets["images/red.png"], 1)

    bomb_piece = size(assets["images/bomb.png"], 1)

    win_image = size(assets["images/win.png"], 1)
    lose_image = size(assets["images/lose.png"], 1)

    explosion_atlas = SpriteSheetAtlas(
        assets["images/explosion.png"],
        assets["images/explosion.xml"]
    )

    fire_atlas = SpriteSheetAtlas(
        assets["images/fire.png"],
        assets["images/fire.xml"]
    )

    explosions = []
    all_pieces = pygame.sprite.Group()

    #drag_debugger = DragDebugger()

    gameMusic = SM(assets[f"music/{difficulty}.wav"], "music")
    gameMusic.set_volume(main.volumes["music"])
    gameMusic.play(loops=-1)

    explosionsound = SM(assets["sfx/explosion.wav"], "sfx")
    win_sound = SM(assets["sfx/win.wav"], "sfx")
    lose_sound = SM(assets["sfx/lose.wav"], "sfx")
    explosionsound.set_volume(main.volumes["sfx"])
    win_sound.set_volume(main.volumes["sfx"])
    lose_sound.set_volume(main.volumes["sfx"])

    dither = assets["images/dither.png"]
    grid_img = assets[f"images/grid{difficulty}.png"]

    clock = main.clock

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    flash_duration = 750
    flash_start_time = pygame.time.get_ticks()

    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    font = pygame.font.Font("../assets/fonts/undertalesans.ttf", 75)
    pygame.display.set_caption(f"Strike Four | {difficulty.capitalize()}")

    x_offset = (800 - width) // 2
    y_offset = (765 - height) // 2

    tile_size = 128

    offset_x = scroll_state["offset_x"]
    offset_y = scroll_state["offset_y"]

    scroll_x = scroll_state["scroll_x"]
    scroll_y = scroll_state["scroll_y"]

    fire = None
    if difficulty == "medium":
        scroll_x *= 1.35
        scroll_y *= 1.15
    elif difficulty == "hard":
        fire = Sprite(
            fire_atlas,
            pos=(w // 2, h + 125),
            animations=["fire"],
            scale=1.5,
            frame_rate=48
        )
        fire.play("fire")
        scroll_x *= 4
        scroll_y *= 2

    if difficulty == "hard":
        shader_offset = main.shaderVal * 1.5
    else:
        shader_offset = main.shaderVal

    chroma = Abber(offset=shader_offset)

    scroll_state["offset_x"] = offset_x
    scroll_state["offset_y"] = offset_y

    # to make hard mode a little fairer
    def should_use_bomb():
        if difficulty == "hard":
            return random.random() < 0.3  #30%
        else:
            return random.random() < 0.1  #10%

    use_bomb_next = should_use_bomb

    def create_board():
        board = [[None for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        return np.array(board, dtype=object)

    def drop_piece(board, row, col, piece_type):
        x = x_offset + col * SQUARESIZE + (SQUARESIZE - player_piece.get_width()) // 2
        y = y_offset + row * SQUARESIZE + (SQUARESIZE - player_piece.get_height()) // 2

        if piece_type == PieceType.BOMB:
            img = bomb_piece
            piece = Piece(piece_type, (x, y), img)
            board[row][col] = piece

            exp = Sprite(
                explosion_atlas,
                pos=(x, y + 200),
                animations=["explode bitch"],
                scale=1.25,
                frame_rate=24
            )
            explosionsound.play()
            exp.play("explode")
            explosions.append(exp)

            all_pieces.add(piece)
            detonate_bomb(board, row, col)
            apply_gravity(board) # accounting for pieces that might defy gravity for some fuckin reason

            if winning_move(board, PieceType.PLAYER):
                return PieceType.PLAYER
            if winning_move(board, PieceType.ENEMY):
                return PieceType.ENEMY
            return None

        else:
            img = player_piece if piece_type == PieceType.PLAYER else enemy_piece
            piece = Piece(piece_type, (x, y), img)
            board[row][col] = piece
            all_pieces.add(piece)

            if winning_move(board, piece_type):
                return piece_type
            return None

    def detonate_bomb(board, row, col): # i fucking hate math
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < ROW_COUNT and 0 <= c < COLUMN_COUNT:
                    piece = board[r][c]
                    if piece:
                        all_pieces.remove(piece)
                    board[r][c] = None

    # GOD BLESS STACKOVERFLOW AND REDDIT
    # COULDN'T HAVE MADE THIS WITHOUT IT
    # I STILL HATE MATH BTW
    def apply_gravity(board):
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT - 1, -1, -1):
                if board[row][col] is None:
                    for above_row in range(row - 1, -1, -1):
                        if board[above_row][col] is not None:
                            piece = board[above_row][col]
                            board[row][col] = piece
                            board[above_row][col] = None

                            x = x_offset + col * SQUARESIZE + (SQUARESIZE - player_piece.get_width()) // 2
                            y = y_offset + row * SQUARESIZE + (SQUARESIZE - player_piece.get_height()) // 2
                            piece.rect.topleft = (x, y)

                            break

    def is_valid_location(board, col):
        return get_next_open_row(board, col) != -1

    def get_next_open_row(board, col):
        for r in range(ROW_COUNT - 1, -1, -1):
            if board[r][col] is None:
                return r
        return -1

    def winning_move(board, piece):
        # Horizontal
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(get_owner(board[r][c + i]) == piece for i in range(4)):
                    return True

        # Vertical
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT):
                if all(get_owner(board[r + i][c]) == piece for i in range(4)):
                    return True

        # Diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if all(get_owner(board[r + i][c + i]) == piece for i in range(4)):
                    return True

        # Diagonal 2
        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(get_owner(board[r - i][c + i]) == piece for i in range(4)):
                    return True

        return False

    def draw_board(board):
        all_pieces.draw(scene_surface)
        scene_surface.blit(boardSprite, (120, 100))

    board = create_board()
    game_over = False
    result_image = None
    turn = 0  # 0 = player, 1 = AI

    draw_board(board)
    draw_fps(screen, clock)

    time_since_flash = pygame.time.get_ticks() - flash_start_time
    if time_since_flash < flash_duration:
        alpha = 255 - int((time_since_flash / flash_duration) * 255)
        flash_overlay = pygame.Surface((w, h)).convert_alpha()
        flash_overlay.fill((255, 255, 255, alpha))
        scene_surface.blit(flash_overlay, (0, 0))

    hover_col = -1
    ai_move_delay = 500
    ai_move_start_time = None
    ai_moved = False

    while not game_over:
        dt = clock.tick(main.fps)

        offset_x += scroll_x
        offset_y += scroll_y

        if offset_x <= -tile_size:
            offset_x += tile_size
        elif offset_x >= tile_size:
            offset_x -= tile_size

        if offset_y <= -tile_size:
            offset_y += tile_size
        elif offset_y >= tile_size:
            offset_y -= tile_size

        scroll_state["offset_x"] = offset_x
        scroll_state["offset_y"] = offset_y

        scene_surface.fill((0, 0, 0))
        cols = w // tile_size + 8
        rows = h // tile_size + 8

        for row in range(rows):
            for col in range(cols):
                x = col * tile_size + offset_x
                y = row * tile_size + offset_y
                scene_surface.blit(grid_img, (x, y))

        scene_surface.blit(dither,(0,0))
        mouse_x = pygame.mouse.get_pos()[0]
        hover_col = int((mouse_x - x_offset) / SQUARESIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if turn == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor((posx - x_offset) / SQUARESIZE))
                    col = max(0, min(COLUMN_COUNT - 1, col))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)

                        winner = None
                        if use_bomb_next:
                            winner = drop_piece(board, row, col, PieceType.BOMB)
                        else:
                            winner = drop_piece(board, row, col, PieceType.PLAYER)

                        use_bomb_next = should_use_bomb()

                        if winner == PieceType.PLAYER:
                            result_image = win_image
                            game_over = True
                            gameMusic.stop()
                            win_sound.play()
                        elif winner == PieceType.ENEMY:
                            result_image = lose_image
                            game_over = True
                            gameMusic.stop()
                            lose_sound.play()

                        if not game_over:
                            turn = 1

        # AI TURN
        if turn == 1 and not game_over:
            if ai_move_start_time is None:
                ai_move_start_time = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            if current_time - ai_move_start_time >= ai_move_delay and not ai_moved:
                col = get_ai_move(board, is_valid_location, get_next_open_row, drop_piece, winning_move, difficulty)
                if col == -1:
                    game_over = True
                elif is_valid_location(board, col):
                    row = get_next_open_row(board, col)

                    winner = None
                    if random.random() < 0.1:
                        winner = drop_piece(board, row, col, PieceType.BOMB)
                    else:
                        winner = drop_piece(board, row, col, PieceType.ENEMY)

                    if winner == PieceType.PLAYER:
                        result_image = win_image
                        game_over = True
                        gameMusic.stop()
                        win_sound.play()
                    elif winner == PieceType.ENEMY:
                        result_image = lose_image
                        game_over = True
                        gameMusic.stop()
                        lose_sound.play()

                    if not game_over:
                        turn = 0
                ai_moved = True

            if ai_moved:
                ai_move_start_time = None
                ai_moved = False

        draw_board(board)

        if fire:
            #swag shader stuff
            fire.update(dt)
            frame_name = fire.animations[fire.current_anim][fire.frame_idx]
            img = fire.atlas.get(frame_name)
            if img:
                if fire.scale != 1.0:
                    img = pygame.transform.smoothscale(
                        img,
                        (
                            int(img.get_width() * fire.scale),
                            int(img.get_height() * fire.scale)
                        )
                    )

                rect = img.get_rect()
                rect.midbottom = fire.pos

                scene_surface.blit(img, rect, special_flags=pygame.BLEND_ADD)

        if 0 <= hover_col < COLUMN_COUNT and is_valid_location(board, hover_col):
            hover_x = x_offset + hover_col * SQUARESIZE + (SQUARESIZE - player_piece.get_width()) // 2
            hover_y = y_offset // 2 - player_piece.get_height() // 2

            hover_img = bomb_piece if use_bomb_next else player_piece
            scene_surface.blit(hover_img, (hover_x, hover_y))

        time_since_flash = pygame.time.get_ticks() - flash_start_time
        if time_since_flash < flash_duration:
            alpha = 255 - int((time_since_flash / flash_duration) * 255)
            flash_overlay = pygame.Surface((w, h)).convert_alpha()
            flash_overlay.fill((255, 255, 255, alpha))
            scene_surface.blit(flash_overlay, (0, 0))

        for exp in explosions[:]:
            exp.update(dt)
            exp.draw(scene_surface)
            if exp.frame_idx == len(exp.animations[exp.current_anim]) - 1:
                explosions.remove(exp)

        if result_image:
            rect = result_image.get_rect(center=(w // 2, h // 2))
            scene_surface.blit(result_image, rect)

        if main.shader:
            chroma.apply(screen, scene_surface)
        else:
            screen.blit(scene_surface, (0, 0))

        draw_fps(screen, clock)
        pygame.display.flip()

        if game_over:
            pygame.time.wait(3000)
            gameMusic.stop()
            main_menu.run(screen, assets, clock, draw_fps)
            return
