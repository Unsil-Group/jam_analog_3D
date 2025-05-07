import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from models.base_tower import draw_base_tower
from models.bench import draw_bench
from models.clock import draw_clock_face
from models.tree import draw_tree


# Initialize 3D object
def init_objects():
    global base_tower_list, tree_list
    global base_tower_list, bench_list
    base_tower_list = glGenLists(1)
    bench_list = glGenLists(1)
    tree_list = glGenLists(1)

    # Compile Clock Tower base
    glNewList(base_tower_list, GL_COMPILE)
    draw_base_tower()
    glEndList()

    # Compile Trees
    glNewList(tree_list, GL_COMPILE)
    draw_tree()
    glEndList()

    # Compile Benches
    glNewList(bench_list, GL_COMPILE)
    draw_bench()
    glEndList()


def main():
    pygame.init()
    display = (1280, 720)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Clock Tower in City Environment")

    # 3D Camera Configuration
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, -1.0, -10.0)
    glEnable(GL_DEPTH_TEST)

    init_objects()

    # Control Mouse Variable
    clock = pygame.time.Clock()
    mouse_drag = False
    last_mouse_pos = (0, 0)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse Controlling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_drag = True
                    last_mouse_pos = event.pos
                elif event.button == 4:
                    glTranslatef(0, 0, 1.0)
                elif event.button == 5:
                    glTranslatef(0, 0, -1.0)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_drag = False

            if event.type == pygame.MOUSEMOTION and mouse_drag:
                dx, dy = (
                    event.pos[0] - last_mouse_pos[0],
                    event.pos[1] - last_mouse_pos[1],
                )
                last_mouse_pos = event.pos
                glRotatef(dx, 0, 1, 0)
                glRotatef(dy, 1, 0, 0)

            # Input Keyboard Detection
            keys = pygame.key.get_pressed()

            # (WASD)
            if keys[pygame.K_w]:
                glTranslatef(0, 0, 0.1)
            if keys[pygame.K_s]:
                glTranslatef(0, 0, -0.1)
            if keys[pygame.K_a]:
                glTranslatef(0.1, 0, 0)
            if keys[pygame.K_d]:
                glTranslatef(-0.1, 0, 0)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw object ground
        glColor3f(0.3, 0.6, 0.3)  # Green ground
        glBegin(GL_QUADS)
        glVertex3f(-10, -0.5, -10)
        glVertex3f(10, -0.5, -10)
        glVertex3f(10, -0.5, 10)
        glVertex3f(-10, -0.5, 10)
        glEnd()

        glCallList(base_tower_list)

        # Draw clock faces on all 4 sides of the tower
        for i in range(4):
            glPushMatrix()
            glRotatef(90 * i, 0, 1, 0)
            glTranslatef(0, 1.5, 0.35)
            draw_clock_face()
            glPopMatrix()

        # Place trees around the scene
        for angle in range(0, 360, 45):
            glPushMatrix()
            glRotatef(angle, 0, 1, 0)
            glTranslatef(3.0, -0.5, 0)
            glCallList(tree_list)
            glPopMatrix()

        # Place benches around the scene
        for angle in range(0, 360, 90):
            glPushMatrix()
            glRotatef(angle + 45, 0, 1, 0)
            glTranslatef(1.5, 0, 0)
            glCallList(bench_list)
            glPopMatrix()

        # Update display
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
