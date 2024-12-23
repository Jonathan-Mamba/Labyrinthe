import pgtext as ptext
import pygame


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

    # Game loop.
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit(0)

        # Update.
        ptext.draw("Font name and size", (20, 100), fontsize=60)
        ptext.draw("Font decoration", (300, 180), sysfontname="freesans", italic=True, underline=True)
        ptext.draw("Positioned text", topright=(840, 20))
        ptext.draw("Here's some neatly-wrapped text.", (90, 210), width=120, lineheight=1.5)
        ptext.draw("Outlined text", (400, 70), owidth=1.5, ocolor=(255, 255, 0), color=(0, 0, 0))
        ptext.draw("Drop shadow", (640, 110), shadow=(2, 2), scolor="#202020")
        ptext.draw("Color gradient", (540, 170), color="red", gcolor="purple")
        ptext.draw("Transparency", (700, 240), alpha=0.1)
        ptext.draw("Vertical text", midleft=(40, 440), angle=90)
        ptext.draw("_Inline_ [styles]!", (630, 320), underlinetag="_", colortag={"[": "yellow", "]": None})
        ptext.draw("All together now:\nCombining the above options",
                   midbottom=(427, 460), width=360, fontsize=48, underline=True,
                   color="#AAFF00", gcolor="#66AA00", owidth=1.5, ocolor="black", alpha=0.8, angle=5)
        # Draw.
        pygame.display.flip()
