import testinit
endersutils = testinit.endersutils

game = endersutils.game(1280, 720)
game.initEngine()

# Initialize screen
game.engine.display.set_caption("Better F**king Robot")

def gameF():
    ball_obj = game.engine.draw.circle(surface=game.s, color=(72, 0, 255), center=[100, 100], radius=40)

game.run(gameF, 60)
game.engine.quit()