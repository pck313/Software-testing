import pygame
from algorithm import lru_page_replacement

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)

PINK = (255, 179, 198)
DARK_PINK = (251, 111, 146)

GREEN = (40, 180, 99)
RED = (231, 76, 60)

BLUE = (52, 152, 219)

ROUGE = (169, 80, 100)
HOT_PINK = (255, 105, 180)

WIDTH, HEIGHT = 1400, 650

COLUMN_SPACING = 45
START_X = 50


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(
        "Mô phỏng LRU Page Replacement"
    )


    font = pygame.font.SysFont("Segoe UI", 20)

    bold_font = pygame.font.SysFont(
        "Segoe UI",
        24,
        bold=True
    )

    italic_font = pygame.font.SysFont(
        "Segoe UI",
        20,
        italic=True
    )

    right_font = pygame.font.SysFont("Segoe UI", 48, bold=True)


    input_box = pygame.Rect(420, 25, 500, 40)

    input_text = (
        "7 0 1 2 0 3 0 4 2 3 0 3 "
        "0 3 2 1 2 0 1 7 0 1"
    )

    active = False


    frame_box = pygame.Rect(1080, 25, 80, 40)

    frame_text = "3"

    frame_active = False


    num_frames = int(frame_text)

    reference_string = [
        int(x)
        for x in input_text.split()
    ]

    history, total_faults = lru_page_replacement(
        reference_string,
        num_frames
    )


    current_step = 0

    running = True

    clock = pygame.time.Clock()

    space_hold_time = 0

    sakura_img = pygame.image.load("sakura.png").convert_alpha()
    sakura_img = pygame.transform.scale(sakura_img, (220, 220))


    while running:

        screen.fill(WHITE)

        screen.blit(sakura_img, (WIDTH - 300, HEIGHT - 220))

        right_text = right_font.render("THUẬT TOÁN LRU", True, ROUGE)

        right_text = pygame.transform.rotate(right_text, -90)

        screen.blit(
            right_text,
            (WIDTH - 140, HEIGHT // 2 - right_text.get_height() // 2)
        )

        label_txt = bold_font.render(
            "Nhập chuỗi:",
            True,
            ROUGE
        )

        screen.blit(label_txt, (70, 30))

        pygame.draw.rect(
            screen,
            HOT_PINK if active else ROUGE,
            input_box,
            2
        )

        input_surface = font.render(
            input_text,
            True,
            BLACK
        )

        screen.blit(
            input_surface,
            (input_box.x + 10, input_box.y + 8)
        )

        frame_label = bold_font.render(
            "Số frame:",
            True,
            ROUGE
        )

        screen.blit(frame_label, (950, 30))

        pygame.draw.rect(
            screen,
            HOT_PINK if frame_active else ROUGE,
            frame_box,
            2
        )

        frame_surface = font.render(
            frame_text,
            True,
            BLACK
        )

        screen.blit(
            frame_surface,
            (frame_box.x + 20, frame_box.y + 8)
        )


        title_txt = bold_font.render(
            "Chuỗi số hiệu các trang:",
            True,
            ROUGE
        )

        screen.blit(title_txt, (30, 100))


        for i, val in enumerate(reference_string):

            color = BLUE if i == current_step - 1 else BLACK

            txt = font.render(
                str(val),
                True,
                color
            )

            x_pos = START_X + i * COLUMN_SPACING

            text_rect = txt.get_rect(
                center=(x_pos, 145)
            )

            screen.blit(txt, text_rect)


        y_offset = 180

        for i in range(current_step):

            data = history[i]

            x_pos = START_X + i * COLUMN_SPACING

            for j in range(num_frames):

                rect = pygame.Rect(
                    x_pos - 15,
                    y_offset + j * 55,
                    35,
                    50
                )

                frame_color = PINK

                if j == data["replaced_index"]:
                    frame_color = DARK_PINK

                pygame.draw.rect(
                    screen,
                    frame_color,
                    rect,
                    0
                )

                if data["frames"][j] != -1:

                    page_num = data["frames"][j]

                    p_txt = font.render(
                        str(page_num),
                        True,
                        BLACK
                    )

                    screen.blit(
                        p_txt,
                        (rect.centerx - 5,
                         rect.centery - 10)
                    )



            res_txt = font.render(
                data["status"],
                True,
                GREEN
                if data["status"] == "Ko lỗi"
                else RED
            )

            res_rect = res_txt.get_rect(
                center=(
                    x_pos,
                    y_offset + num_frames * 60 + 5
                )
            )

            screen.blit(res_txt, res_rect)

        if current_step == len(reference_string):

            summary_txt = bold_font.render(
                f"Tổng số Page Fault: {total_faults}",
                True,
                ROUGE
            )

            screen.blit(
                summary_txt,
                (30, HEIGHT - 110)
            )


        instr_txt = italic_font.render(
            "SPACE: chạy từng bước | "
            "DELETE: xóa ký tự | "
            "R: làm mới | "
            "ENTER: cập nhật dữ liệu",
            True,
            HOT_PINK
        )

        screen.blit(
            instr_txt,
            (WIDTH // 2 - 360, HEIGHT - 40)
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False


            if event.type == pygame.MOUSEBUTTONDOWN:

                if input_box.collidepoint(event.pos):

                    active = True
                    frame_active = False

                elif frame_box.collidepoint(event.pos):

                    frame_active = True
                    active = False

                else:

                    active = False
                    frame_active = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    try:
                        reference_string = [
                            int(x)
                            for x in input_text.split()
                        ]

                        num_frames = int(frame_text)

                        history, total_faults = lru_page_replacement(
                            reference_string,
                            num_frames
                        )

                        current_step = 0

                    except:
                        pass

                elif active:

                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

                elif frame_active:

                    if event.key == pygame.K_BACKSPACE:
                        frame_text = frame_text[:-1]
                    elif event.unicode.isdigit():
                        frame_text += event.unicode

                else:

                    if event.key == pygame.K_SPACE:
                        if current_step < len(history):
                            current_step += 1

                    elif event.key == pygame.K_r:
                        current_step = 0


        keys = pygame.key.get_pressed()


        if (
            keys[pygame.K_SPACE]
            and not active
            and not frame_active
        ):

            space_hold_time += clock.get_time()

            if space_hold_time > 300:

                if current_step < len(history):

                    current_step += 1

                    pygame.time.delay(100)

        else:

            space_hold_time = 0

        if keys[pygame.K_BACKSPACE]:

            if active:

                if len(input_text) > 0:

                    input_text = input_text[:-1]

                    pygame.time.delay(40)

            elif frame_active:

                if len(frame_text) > 0:

                    frame_text = frame_text[:-1]

                    pygame.time.delay(40)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()