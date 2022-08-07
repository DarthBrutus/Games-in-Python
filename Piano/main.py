import os
import sys
import pygame
import pygame.midi

# Colors for keys and background
color_grey  = (127, 127, 127)
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red   = (255, 0, 0)
color_blue   = (0, 0, 255)

key_to_note = {
        pygame.K_a: (12, False, False),  # C0       (azerty: pygame.K_q)
        pygame.K_w: (13, True,  False),  # C#/Db0   (azerty: pygame.K_z)
        pygame.K_s: (14, False, False),  # D0
        pygame.K_e: (15, True, False),   # D#/Eb0
        pygame.K_d: (16, False,  False), # E0
        pygame.K_f: (17, False, False),  # F0
        pygame.K_t: (18, True,  False),  # F#/Gb0
        pygame.K_g: (19, False, False),  # G0
        pygame.K_y: (20, True, False),   # G#/Ab0
        pygame.K_h: (21, False,  False), # A0
        pygame.K_u: (22, True, False),   # A#/Bb0
        pygame.K_j: (23, False,  False), # B0
}
note_count = 12

velocity = 124

def midi_to_ansi_note(midi_note: int) -> str:
    '''Return the ANSI Note name for a midi number'''
    notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']
    num_notes = 12
    note_name = notes[(midi_note - 21) % num_notes]
    note_number = (midi_note - 12) // num_notes
    return f'{note_name}{note_number}'
octave = int(input('Octave: '))

def midi_device_prompt() -> int:
    '''Dump MIDI devices info and prompt user for a choice'''
    for i in range(0, pygame.midi.get_count()):
        (interf, name, inp, outp, opened) = pygame.midi.get_device_info(i)
        print(f'Device: {i}')
        print(f'\tInterface: {interf.decode("utf-8")}')
        print(f'\tName: {name.decode("utf-8")}')
        print(f'\tInput: {inp == 1}')
        print(f'\tOutput: {outp == 1}')
        print(f'\tOpened: {opened == 1}\n')

    return int(input("Which MIDI device would you like to use ? "))

def draw_keyboard(window) -> None:
    '''Draw the octave keyboard on screen'''

    margin = window.get_width() // 140

    white_width = (window.get_width() - 8 * margin) // 7
    black_width = white_width // 2 + 2 * margin

    left = margin
    top = margin
    bottom = window.get_height() - top

    # Draw white keys
    for key in key_to_note:
        note, black, on = key_to_note[key]
        if black:
            continue
        pygame.draw.rect(window, color_red if on else color_white, (left, top, white_width, bottom - top))
        left += margin + white_width

    # Reset left for black keys
    left = margin + white_width + margin // 2 - black_width // 2

    bottom = bottom - (bottom - top) // 3

    # Draw black keys
    for key in key_to_note:
        note, black, on = key_to_note[key]
        if not black:
            continue
        if note == 18:  # Skip the inexistant black key between E and F
            left += margin + white_width
        pygame.draw.rect(window, color_blue if on else color_black, (left, top, black_width, bottom - top))
        left += margin + white_width

def main() -> None:

    pygame.midi.init()

    # Parse arguments
    if (len(sys.argv) == 2):
        midi_dev = int(sys.argv[1])
    elif (len(sys.argv) == 1):
        midi_dev = midi_device_prompt()
    else:
        print(f'Usage: {os.path.basename(sys.argv[0])} [MIDI_DEVICE]')
        sys.exit(os.EX_USAGE)

    pygame.display.init()
    pygame.display.set_caption('Simple Piano')
    window = pygame.display.set_mode((1000, 700))
    win_IMG = pygame.image.load('Games\Piano\Logo.png')
    pygame.display.set_icon(win_IMG)
    window.fill(color_grey)
    draw_keyboard(window)
    pygame.display.update()

    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP])

    print(f'Setting MIDI device to {midi_dev}')
    midi_hndl = pygame.midi.Output(midi_dev)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break

            # Turn note on if known key
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key in key_to_note:
                    note, black, on = key_to_note[key]
                    if not on:
                        print(f'DOWN: Key: {key} Note: {note + note_count * octave} ', end='')
                        print(f'Name: {midi_to_ansi_note(note + note_count * octave)}')
                        midi_hndl.note_on(note + note_count * octave, velocity)
                        key_to_note[key] = note, black, True

                # Exit is user pressed <escape>
                elif key == pygame.K_ESCAPE:
                    run = False

            # Turn note off if known key
            elif event.type == pygame.KEYUP:
                key = event.key
                if key in key_to_note:
                    note, black, on = key_to_note[key]
                    if on:
                        print(f'UP: Key: {key} Note: {note + note_count * octave} ', end='')
                        print(f'Name: {midi_to_ansi_note(note + note_count * octave)}')
                        midi_hndl.note_off(note + note_count * octave, velocity)
                        key_to_note[key] = note, black, False

        draw_keyboard(window)
        pygame.display.update()
        
main()