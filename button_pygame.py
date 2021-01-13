def button(size_text, message, center_message, colour_message, colour_button, surface,
           new_colour_msg=None, new_colour_button=None, font=None):
    """
    Pygame function that draws button, allows change of colours is mouse is positioned
    on the button and returns True if you click on it

    :param size_text: int
    :param message:   str
    :param center_message:  (n1, n2)
    :param colour_message:  (n1, n2, n3) # RGB values or string
    :param colour_button:   (n1, n2, n3) # RGB values or string
    :param surface: any
    :param new_colour_msg:    (n1, n2, n3) # RGB values or string
    :param new_colour_button:  (n1, n2, n3) # RGB values or string
    :param font: path
    :return: bool
    """
    import pygame

    if new_colour_msg == None:
        new_colour_msg = colour_message
    if new_colour_button == None:
        new_colour_button = colour_button

    lista = [colour_message, new_colour_msg, colour_button, new_colour_button]
    for item in lista:
        if str(item).isalpha():
            if item == 'white':
                index = lista.index(item)
                lista[index] = (255,255,255)
            elif item == 'black':
                index = lista.index(item)
                lista[index] = (0,0,0)
            elif item == 'blue':
                index = lista.index(item)
                lista[index] = (0,0,255)
            elif item == 'green':
                index = lista.index(item)
                lista[index] = (0,255,0)
            elif item == 'red':
                index = lista.index(item)
                lista[index]= (255,0,0)
            elif item == 'pink':
                index = lista.index(item)
                lista[index] = (255,0,255)
            elif item == 'yellow':
                index = lista.index(item)
                lista[index] = (255,255,0)
            else:
                raise Exception ('colour not known, try:\n'
                                 'black,white,yellow,green,blue,red or pink')


    font = pygame.font.Font(font, size_text)
    text = font.render(message, True, lista[0]) # lista[0] == colour_message
    
    xButaoInicio = center_message[0] - (text.get_width() // 2) - 20
    yButaoInicio = center_message[1] - (text.get_height() // 2) - 20
    xButaoFinal = text.get_width() + 40
    yButaoFinal = text.get_height() + 40
    pygame.draw.rect(surface, lista[2], (xButaoInicio, yButaoInicio, xButaoFinal, yButaoFinal))
    surface.blit(text, text.get_rect(center=center_message))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if xButaoInicio < mouse[0] < xButaoInicio + xButaoFinal and yButaoInicio < mouse[1] < yButaoFinal + yButaoInicio:
        pygame.draw.rect(surface, lista[3], (xButaoInicio, yButaoInicio, xButaoFinal, yButaoFinal))
        text = font.render(message, True, lista[1])
        surface.blit(text, text.get_rect(center=center_message))
        if click[0] == 1:
            return True
