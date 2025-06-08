import asyncio
import pygame
import ui

async def main():

    pygame.init()
    screen = pygame.display.set_mode((ui.SCREEN_WIDTH, ui.SCREEN_HEIGHT))
    pygame.display.set_caption("Nordle")
    clock = pygame.time.Clock()

    # Create the UI object
    wordle = ui.WordleUI()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass all events to the UI handler
            wordle.handle_input(event)

        # Drawing calls
        screen.fill(ui.DEFAULT_BG)
        ui.draw_header_and_messages(screen, wordle)
        ui.draw_grid(screen, wordle)
        ui.draw_keyboard(screen, wordle)
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())