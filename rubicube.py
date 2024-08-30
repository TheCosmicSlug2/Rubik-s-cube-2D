import pygame as pg
from copy import deepcopy
from random import randint, choice

""" Code pour décrire un rubik's cube et ses changements """

"""

               --- --- ---
              | 0 | 1 | 2 |
               --- --- ---
              | 3 | 4 | 5 |  => Bleu
               --- --- ---
              | 6 | 7 | 8 |
               --- --- ---
 --- --- ---   --- --- ---   --- --- ---   --- --- ---
| 0 | 1 | 2 | | 0 | 1 | 2 | | 0 | 1 | 2 | | 0 | 1 | 2 |
 --- --- ---   --- --- ---   --- --- ---   --- --- ---
| 3 | 4 | 5 | | 3 | 4 | 5 | | 3 | 4 | 5 | | 3 | 4 | 5 |  => Orange, Blanc, Rouge, Jaune
 --- --- ---   --- --- ---   --- --- ---   --- --- ---
| 6 | 7 | 8 | | 6 | 7 | 8 | | 6 | 7 | 8 | | 6 | 7 | 8 |
 --- --- ---   --- --- ---   --- --- ---   --- --- ---
               --- --- ---
              | 0 | 1 | 2 |
               --- --- ---
              | 3 | 4 | 5 |  => Vert
               --- --- ---
              | 6 | 7 | 8 |
               --- --- ---

"""

lookup_linked_faces = {
        0: [2, 1, 4, 3],
        1: [5, 4, 0, 2],
        2: [5, 1, 0, 3],
        3: [5, 2, 0, 4],
        4: [5, 3, 0, 1],
        5: [4, 1, 2, 3]
    }


lookup_rotation_reference = {
        # Bleu
        0: [(0, 1, 2), (0, 1, 2), (0, 1, 2,), (0, 1, 2)],
        # Orange
        1: [(0, 3, 6), (2, 5, 8), (0, 3, 6), (0, 3, 6)],

        # Si la face est blanche, on a pas besoin de changer les index
        2: [(0, 1, 2), (2, 5, 8), (8, 7, 6), (6, 3, 0)],

        # Rouge
        3: [(2, 5, 8), (2, 5, 8), (2, 5, 8), (6, 3, 0)],

        # jaune
        4: [(8, 7, 6), (2, 5, 8), (0, 1, 2), (6, 3, 0)],

        # Verte
        5: [(8, 7, 6), (8, 7, 6), (8, 7, 6), (8, 7, 6)]

    }

cube_data = [
    [
        'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'
    ],

    [
        'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'
    ],

    [
        'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'
    ],

    [
        'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'
    ],

    [
        'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y'
    ],

    [
        'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'
    ]
]




def draw_cube(cube_data):

    cube_start_of_faces = [
        (1, 0),
        (0, 1), (1, 1), (2, 1), (3, 1),
        (1, 2)
    ]

    dic_str_to_color = {
        "b": (0, 0, 255),
        "o": (255, 128, 0),
        "w": (255, 255, 255),
        "r": (255, 0, 0),
        "y": (255, 255, 0),
        "g": (0, 255, 0)
    }
    
    cell_dims = (33, 33)

    surface = pg.Surface((400, 300))

    for face_idx, face in enumerate(cube_data):
        for cell_idx, cell in enumerate(face):
            cell_x = cell_idx % 3
            cell_y = cell_idx // 3
            ecart_left = cube_start_of_faces[face_idx][0] * 100 + cell_x * cell_dims[0]
            ecart_top = cube_start_of_faces[face_idx][1] * 100 + cell_y * cell_dims[1]
            
            cell_rect = pg.Rect(ecart_left, ecart_top, cell_dims[0], cell_dims[1])

            cell_color = dic_str_to_color[cell]

            pg.draw.rect(surface, cell_color, cell_rect)
    
    return surface

"""

b : 0
o : 1
w : 2
r : 3
y : 4
g : 5

ordre des linked faces : devant, gauche, derrière, droite selon le patron

"""


def get_all_diffent_nb_from_liste(liste):

    lookup_liste = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    liste_returned = []

    for i in lookup_liste:
        if i not in liste:
            liste_returned.append(i)
    
    return liste_returned




def rotate_face(cube_data, face_idx, dir):



    # Rajouter index de changement de rotation en fonction de la face de référence mais si tu comprends



    # Trouver les Indices de chaque face

    current_face_idx = face_idx
    forward_face_idx = lookup_linked_faces[face_idx][0]
    left_face_idx = lookup_linked_faces[face_idx][1]
    backward_face_idx = lookup_linked_faces[face_idx][2]
    right_face_idx = lookup_linked_faces[face_idx][3]
    

    # Trouver les contenus de chaque face

    current_face_data = cube_data[current_face_idx]
    forward_face_data = cube_data[forward_face_idx]
    left_face_data = cube_data[left_face_idx]
    backward_face_data = cube_data[backward_face_idx]
    right_face_data = cube_data[right_face_idx]


    # Changer les faces

    # Current face :
    

    changed_current_face = []

    rotation_matrix = [6, 3, 0, 7, 4, 1, 8, 5, 2] # Comment les arrêtes et les sommets de la face principale changent pendant une rotation à droite
    if dir == "left":
        rotation_matrix = reversed(rotation_matrix)


    for new_cell_pos in rotation_matrix:
        changed_current_face.append(current_face_data[new_cell_pos])

    """
    changed_current_face.append(current_face_data[6]) # sommet bas gauche       => haut gauche
    changed_current_face.append(current_face_data[3]) # arrête gauche           => arrête haut
    changed_current_face.append(current_face_data[0]) # Sommet haut gauche      => haut droit
    changed_current_face.append(current_face_data[7]) # Arrête bas              => gauche
    changed_current_face.append(current_face_data[4]) # Mileu
    changed_current_face.append(current_face_data[1]) # arrête haut             => droite
    changed_current_face.append(current_face_data[8]) # sommet bas droit        => bas gauche
    changed_current_face.append(current_face_data[5]) # arrête droit            => bas
    changed_current_face.append(current_face_data[2]) # sommet haut droit       => bas droit 
    """
    
    # forward face :

    changed_forward_face = []
    changed_left_face = []
    changed_backward_face = []
    changed_right_face = []

    forward_pos = lookup_rotation_reference[current_face_idx][0]
    left_pos = lookup_rotation_reference[current_face_idx][1]
    backward_pos = lookup_rotation_reference[current_face_idx][2]
    right_pos = lookup_rotation_reference[current_face_idx][3]

    # Ajouter les positions qui ne changent pas :

    not_changing_forward_face_pos = get_all_diffent_nb_from_liste(forward_pos)
    not_changing_left_face_pos = get_all_diffent_nb_from_liste(left_pos)
    not_changing_backward_face_pos = get_all_diffent_nb_from_liste(backward_pos)
    not_changing_right_face_pos = get_all_diffent_nb_from_liste(right_pos)

    not_changing_forward_face = [forward_face_data[cell_idx] for cell_idx in not_changing_forward_face_pos]
    not_changing_left_face = [left_face_data[cell_idx] for cell_idx in not_changing_left_face_pos]
    not_changing_backward_face = [backward_face_data[cell_idx] for cell_idx in not_changing_backward_face_pos]
    not_changing_right_face = [right_face_data[cell_idx] for cell_idx in not_changing_right_face_pos]
    



    if dir == "right":
        changed_cell_forward = [left_face_data[cell_idx] for cell_idx in left_pos]
        changed_cell_left = [backward_face_data[cell_idx] for cell_idx in backward_pos]
        changed_cell_backward = [right_face_data[cell_idx] for cell_idx in right_pos]
        changed_cell_right = [forward_face_data[cell_idx] for cell_idx in forward_pos]

    else:
        changed_cell_forward = [right_face_data[cell_idx] for cell_idx in right_pos]
        changed_cell_left = [forward_face_data[cell_idx] for cell_idx in forward_pos]
        changed_cell_backward = [left_face_data[cell_idx] for cell_idx in left_pos]
        changed_cell_right = [backward_face_data[cell_idx] for cell_idx in backward_pos]

    
    changed_forward_face.extend(changed_cell_forward)
    for idx, cell_idx in enumerate(not_changing_forward_face_pos):
        changed_forward_face.insert(cell_idx, not_changing_forward_face[idx])

    changed_left_face.extend(changed_cell_left)
    for idx, cell_idx in enumerate(not_changing_left_face_pos):
        changed_left_face.insert(cell_idx, not_changing_left_face[idx])

    changed_backward_face.extend(changed_cell_backward)
    for idx, cell_idx in enumerate(not_changing_backward_face_pos):
        changed_backward_face.insert(cell_idx, not_changing_backward_face[idx])
    
    changed_right_face.extend(changed_cell_right)
    for idx, cell_idx in enumerate(not_changing_right_face_pos):
        changed_right_face.insert(cell_idx, not_changing_right_face[idx])


    # Changer la liste du cube actuel :

    cube_data[current_face_idx] = changed_current_face
    cube_data[forward_face_idx] = changed_forward_face
    cube_data[left_face_idx] = changed_left_face
    cube_data[backward_face_idx] = changed_backward_face
    cube_data[right_face_idx] = changed_right_face





def get_keyboard_events():
    keys = pg.key.get_pressed()

    dic_faces = {
        pg.K_b: 0,
        pg.K_o: 1,
        pg.K_w: 2,
        pg.K_r: 3,
        pg.K_y: 4,
        pg.K_g: 5
    }

    dic_rotation = {
        pg.K_RIGHT: "right",
        pg.K_LEFT: "left"
    }

    face_idx = 2 # Mise à blanc par défaut

    for face_key_pressed in dic_faces:
        if keys[face_key_pressed]:
            face_idx = dic_faces[face_key_pressed]

    rotation = None

    for rotation_key_pressed in dic_rotation:
        if keys[rotation_key_pressed]:
            rotation = dic_rotation[rotation_key_pressed]

    if not rotation:
        return None, None
    
    return face_idx, rotation

def scramble(cube_data, nb_moves):

    dic_idx_to_faces = {
        0: "bleu",
        1: "orange",
        2: "blanc",
        3: "rouge",
        4: "jaune",
        5: "vert"
    }


    for _ in range(nb_moves):
        face_idx = choice([0, 1, 2, 3, 4, 5])
        rotation = choice(["left", "right"])
        rotate_face(cube_data, face_idx=face_idx, dir=rotation)

        print(f"rotation de {dic_idx_to_faces[face_idx]} à {rotation}")






SCREEN = pg.display.set_mode((800, 600))

#scramble(cube_data=cube_data, nb_moves=10)

cube_cache = draw_cube(cube_data=cube_data)
clock = pg.time.Clock()
FPS = 30
get_event_tick = 0

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    
    face_idx, rotation = get_keyboard_events()
    if rotation:
        if get_event_tick > FPS // 10:
            get_event_tick = 0
            rotate_face(cube_data=cube_data, face_idx=face_idx, dir=rotation)
            cube_cache = draw_cube(cube_data=cube_data)
        

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(cube_cache, (0, 0))

    pg.display.update()

    clock.tick(FPS)

    get_event_tick += 1
