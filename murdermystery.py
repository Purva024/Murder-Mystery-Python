import pygame
import sys
import os

# Pygame Setup
pygame.init()
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700

pygame.display.set_caption("Murder at Royal Crescent Theatre")
clock = pygame.time.Clock()

flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)

# Colors and Fonts
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
RED_CLUE = (255, 100, 100)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (180, 180, 180)
CLUE_HIGHLIGHT_COLOR = (200, 200, 255)
LIGHT_BLUE = (140, 228, 255)

TITLE_FONT = pygame.font.Font(None, 70)
REPORT_TITLE_FONT = pygame.font.Font(None, 45)
HEADER_FONT = pygame.font.Font(None, 35)
SCENE1_FONT = pygame.font.Font(None, 30)
DETAIL_FONT = pygame.font.Font(None, 25)
NARRATION_FONT = pygame.font.Font(None, 25)


# Suspect Data
SUSPECT_DATA = {
    "Clara Vale": {"Age": "26","Relation": "Evelyn’s replacement","Access": "Has reasons to visit dressing rooms to prepare costumes.","Motive": "Ambition + Jealousy"},
    "Marcus Reed": {"Age": "34","Relation": "Lead Actor & Evelyn’s Ex","Access": "Could enter the dressing rooms freely as a star.","Motive": "Obsession or Revenge"},
    "Victor Lang": {"Age": "48","Relation": "Theater Director","Access": "Complete authority to disable cameras.","Motive": "Career/Financial Risk"},
    "Lena Brooke": {"Age": "30","Relation": "Makeup Artist and close friend","Access": "Direct physical proximity to victim","Motive": "Betrayal + Resentment"}
}

# Interrogation process
CLARA_INTER = [
    ("BEHAVIOR: Defensive, anxious", 4),
    ("Clara: “I wanted the role, yes. But not like this! I was on stage rehearsing my cues when Evelyn… collapsed. Everyone knows where I was!”", 10),
    ("Her fingers incessantly fidgeting with the clasp of her handbag.", 6),
    ("You: “I see… Something in your hand is distracting me. Can you please hand over the bag?”", 7),
    ("Clara froze, her movements halting.", 5),
    ("A tube of lipstick found in her bag — shade identical to the smudge on the champagne glass.", 7),
    ("Clara: “That’s just a popular color! Lots of people use it!”", 6),
    ("You: “Thank you miss Clara. You may please leave.”", 6)
]

MARCUS_INTER = [
    ("BEHAVIOR: Irritated, defensive", 4),
    ("Marcus: “Evelyn needed space. I respected that! I was in the green room prepping for the final act.”", 8),
    ("You: “But there is no confirmation of your alibi.”", 5),
    ("Marcus: “That is because I was alone in the green room.”", 6),
    ("A fresh scratch was found on his hand.", 5),
    ("Marcus: “It was an accidental scratch from handling stage props.”", 6),
    ("You: “Mr. Reed, we know Evelyn kept a spare dressing room key. Where was it usually kept?”", 7),
    ("Marcus: “How would I know? We broke up months ago.”", 6),
    ("His behavior shifts uncomfortably as he avoids eye contact", 6),
    ("You: “Odd. Because we found a small, almost imperceptible smudge of a blue paint on the key hook, matching the color of your green room door, inside Evelyn's dressing room. Care to explain that coincidence, Mr. Reed?“", 22),
    ("Marcus: “Fine. She... she showed me once. Years ago, when we were together. Said she always kept it hidden behind the loose brick in the prop fireplace in the green room. Just in case.”", 16)
]

VICTOR_INTER = [
    ("BEHAVIOR: Agitated, sweating noticeably", 5),
    ("Victor: “Do you think I’d sabotage my own production? She was difficult tonight, but she was essential!”", 8),
    ("You: “Why was she essential for you?”", 5),
    ("Victor: “My financial investors warned me that ‘Evelyn leaves, the show collapses’.” Keeps emphasizing financial stakes", 8),
    ("You: “So, she was going to leave the production?”", 6),
    ("Victor: “Yes, Evelyn hinted at leaving the production after opening night.”", 7),
    ("You: “Mr. Lang, as the director, you have administrative access to all theater systems, correct? Including the security cameras?“", 9),
    ("Victor: “Technically, yes. But I wouldn't... I wouldn't mess with that. That's for security, not for directors.”", 8),
    ("You: “Yet, the hallway camera outside Evelyn's dressing room went offline precisely before her death. And then came back online just after. A very convenient blackout, wouldn't you say?”", 16),
    ("Victor: “I swear, I didn't touch it! Maybe it was a glitch! These old systems... they fail all the time!”", 8)
]

LENA_INTER = [
    ("BEHAVIOR: Emotional, teary — unclear if genuine", 5),
    ("Lena: “I was finishing her makeup… She asked for a moment alone before the scene. When I left, she was fine.”", 4),
    ("You: “When did you leave?”", 5),
    ("Lena: “I left Evelyn at 9:15. After leaving, I heard a glass falling but thought she was nervous.”", 4),
    ("You: “A glass falling? A glass of champagne? Was it a part of prep or did Evelyn have it?”", 5),
    ("Lena: “No, champagne wasn’t part of the prep. And Evelyn avoids alcohol before stage”", 5),
    ("You: “Okay. We have also found perfume residue on your hands. Could you please explain?”", 5),
    ("Lena: “While returning, I slipped on the shattered perfume bottle. Maybe that’s how the residue stayed.”", 6),
    ("You: “One more thing, Miss Brooke. We also found a small, unlabeled vial in your makeup kit. It contained a powerful sedative, easily dissolvable in a drink. Would you know anything about that?”", 4),
    ("Her eyes dart from the detective to her hands, her lower lip trembles, her composure visibly fracturing.", 4),
    ("Lena: “A... a sedative? No, I... I don't know anything about that vial.”", 5),
    ("You: “Thank you miss Lena. You may please leave.”", 4)
]


# Case Analysis Data
CASE_ANALYSIS_DATA = {
    "Clara Vale": {
        "verdict": "UNLIKELY KILLER - POSSIBLE PAWN OR DISTRACTION",
        "color": (255, 165, 0),
        "points": [
            "✅ Motive: Ambition/Jealousy (Threat Note)",
            "→  Career-defining role if Evelyn is removed",
            "→  Known jealousy and resentment toward Evelyn",
            "→  Threat note in Evelyn’s room: “This role belongs to me…”",
            "✅ Physical Evidence:",
            "→ Lipstick in her bag matches the smudge on Evelyn’s champagne glass",
            "→ Could mean she handled the glass",
            "⚠️ BUT that shade is a common brand used by many cast members",
            "⚠️ Confirmed by multiple alibi on stage between 9:25–9:35 PM (Critical poison window).",
        ]
    },
    "Marcus Reed": {
        "verdict": "HIGHLY SUSPICIOUS - LIKELY FOUGHT EVELYN, BUT LACKS MEANS",
        "color": (255, 165, 0),
        "points": [
            "✅ Motive: Emotional Instability",
            "→  Messy breakup",
            "→  Didn’t want Evelyn to move on (professionally or personally)",
            "✅ Opportunity:",
            "→  Unconfirmed alibi",
            "→  Knew the spare key location",
            "✅ Physical Evidence:",
            "→  Fresh scratch on his hand",
            "→  Evelyn’s missing earring found in his locker",
            "⚠️ But the murder weapon was **poison**, not force. No known access to the sedative.",
            "⚠️ Would be more likely to confront violently, not plan a subtle poisoning",
            "⚠️ Doesn’t handle Evelyn’s drinks or makeup"
        ]
    },
    "Victor Lang": {
        "verdict": "STRONGEST COVER-UP SUSPECT - LACKS DIRECT MEANS/ACCESS",
        "color": (255, 165, 0),
        "points": [
            "✅ Motive: Strong financial risk; Evelyn was preparing to leave.",
            "✅ Opportunity/Control:",
            "→  Full backstage access",
            "→  Disabled security console logs exactly during timeframe of murder (9:10-9:30 PM)",
            "⚠️ But no direct physical evidence found near the victim",
            "⚠️ No sign he handled the champagne or poison"
        ]
    },
    "Lena Brooke": {
        "verdict": "STRONGEST MATCH - MOTIVE, MEANS, AND OPPORTUNITY ALIGN",
        "color": (0, 200, 0),
        "points": [
            "✅ Motive:",
            "→  Personal Betrayal",
            "→  Professional Humiliation (Pay cut)",
            "✅ Opportunity: Last person to see her alive; legitimate reason to be alone with her.",
            "→  No camera footage to confirm when she actually left",
            "→  Emotional motives can be stronger than ambition or money",
            "→  Handles liquids and consumable items used on performers",
            "→  could have: tampered with champagne during makeup session",
            "✅ Means:",
            "→  Mysterious sedative-like vial from her makeup kit",
            "→  Perfume may have been smashed to mask the smell of chemicals",
            "✅ Also: Confirmed Evelyn avoids pre-show alcohol but heard the glass fall immediately after leaving."
        ]
    }
}

# Utility Function: Draw Text (Corrected to handle alignment)
def draw_text(surface, text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)
    elif align == "right":
        text_rect.topright = (x, y)
        
    surface.blit(text_surface, text_rect)


try:
    BACKGROUND_IMG = pygame.image.load('bgtheatre(1).png').convert()
    BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    BACKGROUND_IMG = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND_IMG.fill((100, 100, 100))


# SCENE 1: NARRATIVE INTRODUCTION
SCENE_SCRIPT = [
    ("The story takes place inside the grand and historic Royal Crescent Theater...", 4),
    ("A luxurious venue famous for hosting elite classical productions.", 4),
    ("Velvet curtains, ornate balconies, and golden chandeliers set the tone...", 5),
    ("It’s the opening night of a highly anticipated new play: “Curtain Call”.", 5),
    ("The house is full—critics, celebrities, and devoted fans fill every seat.", 5),
    ("Backstage, there’s a mix of excitement, stress, and whispered rivalries...", 6),
    ("The clock strikes 9:30 PM. The final act is about to begin...", 4),
    ("But... the lead actress, Evelyn Hart, suddenly fails to appear for her big entrance.", 6),
    ("A confused pause in the performance leads to panic behind the curtains.", 5),
    ("A backstage assistant rushes to Evelyn’s private dressing room.", 4),
    ("...", 2),
    ("The door is unlocked!", 2),
    ("Inside, Evelyn lies motionless on the floor near her vanity.", 5),
    ("...", 2),
    ("The show is halted. The theater is locked down.", 4),
    ("Someone inside this glamorous palace wanted Evelyn gone...", 5)
]

def run_scene_one():
    current_line_index = 0
    start_time = pygame.time.get_ticks()
    fade_alpha = 0
    FADE_SPEED = 5

    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.fill((0, 0, 0))  # Fill with black
    dark_overlay.set_alpha(150)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Skip to the end or the next game state
                    return "TOXICOLOGY_REPORT" 

        if current_line_index < len(SCENE_SCRIPT):
            current_text, duration = SCENE_SCRIPT[current_line_index]
            duration_ms = duration * 1000
            
            if pygame.time.get_ticks() - start_time > duration_ms:
                current_line_index += 1
                start_time = pygame.time.get_ticks()
                fade_alpha = 0 # Restart fade for the next line
        else:
            return "TOXICOLOGY_REPORT" 

        screen.blit(BACKGROUND_IMG, (0, 0)) 
        screen.blit(dark_overlay, (0, 0))    # 2. The Dark Filter
        
        if current_line_index < len(SCENE_SCRIPT):
            elapsed_time = pygame.time.get_ticks() - (start_time)
            if elapsed_time < (duration_ms / 2):
                 fade_alpha = min(255, fade_alpha + FADE_SPEED)
            else:
                 fade_alpha = max(0, fade_alpha - FADE_SPEED)

            text_color = WHITE
            font_to_use = SCENE1_FONT
            
            if current_text.startswith("***") or current_text.startswith("**"):
                text_color = GOLD
                current_text = current_text.strip(" *") 

            # Create a surface for the text that supports alpha (transparency)
            text_surface = font_to_use.render(current_text, True, text_color)
            text_surface.set_alpha(fade_alpha)
            
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text_surface, text_rect)
            
        # Draw a prompt to advance/skip
        draw_text(screen, "Press SPACE to skip...", NARRATION_FONT, (100, 100, 100), SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30)


        pygame.display.flip()
        clock.tick(60)


# SCENE 2: TOXICOLOGY REPORT
REPORT_DETAILS = {
    "Deceased Name": ("Evelyn Hart", LIGHT_GRAY),
    "Age": ("32", LIGHT_GRAY),
    "Occupation": ("Lead actress in the play “Curtain Call”", LIGHT_GRAY),
    "Time of Discovery": ("~9:35 PM", LIGHT_GRAY),
    "": ("", LIGHT_GRAY), 
    "Room Condition": ("Locked only by a simple turn-latch. No forced entry.", LIGHT_BLUE),
    "Body Position": ("Collapsed sideways by the vanity chair.", LIGHT_BLUE),
    "Physical Evidence 1": ("Small scratch marks on the side of her neck.", LIGHT_BLUE),
    "Physical Evidence 2": ("Makeup for one eye fully done, the other only partially.", LIGHT_BLUE),
    "Preliminary Cause": ("Lips faintly blue. Possible poisoning or chemical exposure.", RED_CLUE)
}

def display_toxicology_report():
    try:
        victim_img = pygame.image.load("evelyn.png").convert()
        victim_img = pygame.transform.scale(victim_img, (300, 400))
    except pygame.error:
        victim_img = pygame.Surface((300, 400))
        victim_img.fill((30, 30, 30))
        draw_text(victim_img, "No Image", DETAIL_FONT, LIGHT_GRAY, 150, 200)

    img_x, img_y = 100, 150        # Image Position (Left side)
    text_start_x = 450             # Text starts to the right of the image
    detail_offset = 220            # Distance between "Label:" and "Value"
    start_y = 150
    line_spacing = 40
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return "CRIME_SCENE_INVESTIGATION" 

        screen.fill(DARK_GRAY)

        draw_text(screen, "Initial Investigation Report", REPORT_TITLE_FONT, GOLD, SCREEN_WIDTH // 2, 50)
        screen.blit(victim_img, (img_x, img_y))
        current_y = start_y
        
        for header, (detail, color) in REPORT_DETAILS.items():
            if header:
                draw_text(screen, f"{header}:", DETAIL_FONT, WHITE, text_start_x, current_y, align="left")
                draw_text(screen, detail, DETAIL_FONT, color, text_start_x + detail_offset, current_y, align="left")
            
            current_y += line_spacing

        draw_text(screen, "Press SPACE to enter the Crime Scene...", NARRATION_FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        pygame.display.flip()
        clock.tick(60)


# SCENE 3: CRIME SCENE INVESTIGATION
CSI_BOUNDARY_X = 900
CHECKLIST_START_X = 900

CLUE_ZONES = {
    "Spilled Champagne Glass": (504, 523, 100, 70, "Glass intact, liquid on floor."),
    "Shattered Perfume Bottle": (613, 410, 80, 80, "Strong perfume smell."),
    "Threat Note": (337, 293, 50, 40, "Handwritten note: 'This role belongs to me...'"),
    "Missing Earring": (389, 288, 40, 45, "One earring is missing from her jewelry box."),
    "Champagne Bottle": (295, 267, 30, 72, "Bottle on the vanity was already opened."),
    "Awkward Chair": (474, 349, 110, 110, "Chair tipped slightly."),
    "Camera Offline": (499, 105, 50, 50, "Hallway security camera was offline.") 
} #(co-ords,co-ords, width, height)

CSI_BOUNDARY_X = 900  # left side for image area
CHECKLIST_START_X = CSI_BOUNDARY_X + 10

clock = pygame.time.Clock()

clues_found = []
TOTAL_CLUES = len(CLUE_ZONES)

def draw_clue_checklist(surface, found_clues):
    checklist_area = pygame.Rect(CHECKLIST_START_X, 0, surface.get_width() - CHECKLIST_START_X, surface.get_height())
    pygame.draw.rect(surface, BLACK, checklist_area)
    pygame.draw.line(surface, GOLD, (CHECKLIST_START_X, 0), (CHECKLIST_START_X, surface.get_height()), 3)

    center_x = CHECKLIST_START_X + (surface.get_width() - CHECKLIST_START_X) // 2
    draw_text(surface, "EVIDENCE CHECKLIST", HEADER_FONT, GOLD, center_x, 30)
    draw_text(surface, f"Found: {len(found_clues)} / {TOTAL_CLUES}", DETAIL_FONT, LIGHT_GRAY, center_x, 60)

    y_offset = 120
    for name in CLUE_ZONES.keys():
        is_found = name in found_clues
        color = (0, 200, 0) if is_found else LIGHT_GRAY
        box_x = CHECKLIST_START_X + 30
        box_y = y_offset - 10
        pygame.draw.rect(surface, color, (box_x, box_y, 20, 20), 1)

        if is_found:
            pygame.draw.line(surface, color, (box_x + 3, box_y + 10), (box_x + 9, box_y + 17), 3)
            pygame.draw.line(surface, color, (box_x + 9, box_y + 17), (box_x + 18, box_y + 5), 3)

        draw_text(surface, name, DETAIL_FONT, WHITE, box_x + 30, y_offset, align="left")
        y_offset += 40

def run_investigation_scene():
    try:
        CRIME_SCENE_BG = pygame.image.load("crimescene.png").convert()
        CRIME_SCENE_BG = pygame.transform.scale(CRIME_SCENE_BG, (CSI_BOUNDARY_X, SCREEN_HEIGHT))
    except:
        CRIME_SCENE_BG = pygame.Surface((CSI_BOUNDARY_X, SCREEN_HEIGHT))
        CRIME_SCENE_BG.fill((20, 20, 50))

    current_hover_clue = None
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_hover_clue = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, (x, y, w, h, detail) in CLUE_ZONES.items():
                    clue_rect = pygame.Rect(x, y, w, h)
                    if clue_rect.collidepoint(mouse_pos) and mouse_pos[0] < CSI_BOUNDARY_X:
                        if name not in clues_found:
                            clues_found.append(name)
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(clues_found) == TOTAL_CLUES:
                    return "SUSPECT_REVIEW"

        # --- Drawing ---
        screen.fill(BLACK)
        screen.blit(CRIME_SCENE_BG, (0, 0))

        # Highlight clues
        for name, (x, y, w, h, detail) in CLUE_ZONES.items():
            clue_rect = pygame.Rect(x, y, w, h)
            if clue_rect.collidepoint(mouse_pos) and mouse_pos[0] < CSI_BOUNDARY_X:
                pygame.draw.rect(screen, CLUE_HIGHLIGHT_COLOR, clue_rect, 3)
                current_hover_clue = (name, detail)
            if name in clues_found:
                pygame.draw.rect(screen, GOLD, clue_rect, 1)

        # Hover text
        if current_hover_clue and current_hover_clue[0] not in clues_found:
            hover_name = current_hover_clue[0]
            draw_text(screen, f"Investigate: {hover_name}", DETAIL_FONT, WHITE, mouse_pos[0] + 15, mouse_pos[1] + 15, align="left")

        # Checklist Sidebar
        draw_clue_checklist(screen, clues_found)

        # Progress prompt
        center_x = CHECKLIST_START_X + (screen.get_width() - CHECKLIST_START_X) // 2
        prompt_text = f"Find ALL {TOTAL_CLUES} Clues to Proceed"
        if len(clues_found) == TOTAL_CLUES:
            prompt_text = "Press SPACE to proceed to get Suspect list."
        draw_text(screen, prompt_text, DETAIL_FONT, RED_CLUE, center_x, screen.get_height() - 30)

        pygame.display.flip()
        clock.tick(60)

# Wrapper function
def draw_text_wrapped(surface, text, font, color, x, y, max_width):
    words = text.split(" ")
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "

    lines.append(line)

    for line in lines:
        surface.blit(font.render(line, True, color), (x, y))
        y += font.get_height() + 4  # line spacing


# SCENE 4: SUSPECT REVIEW

INTERROGATION_DATA = {
    "Clara Vale": CLARA_INTER,
    "Marcus Reed": MARCUS_INTER,
    "Victor Lang": VICTOR_INTER,
    "Lena Brooke": LENA_INTER
}

PORTRAITS = {
    "Victor Lang": pygame.image.load("victor.png"),
    "Marcus Reed": pygame.image.load("marcus.png"),
    "Clara Vale": pygame.image.load("clara.png"),
    "Lena Brooke": pygame.image.load("Lena.png")
}

def run_interrogation(name):
    dialogue = INTERROGATION_DATA[name]

    portrait = PORTRAITS.get(name)
    portrait = pygame.transform.scale(portrait, (250, 250))

    # Timeline system
    start_time = pygame.time.get_ticks()
    next_line_index = 0
    visible_lines = []

    # Scroll system
    scroll_y = 0
    SCROLL_SPEED = 30

    # Create a virtual tall surface for the log
    log_surface = pygame.Surface((SCREEN_WIDTH - 350, 2000), pygame.SRCALPHA)

    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return "BACK_TO_LIST"

                # Optional skip
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if next_line_index < len(dialogue):
                        text, delay = dialogue[next_line_index]
                        visible_lines.append(text)
                        next_line_index += 1
                        start_time = now  # reset for next auto timing

                # Scroll
                if event.key == pygame.K_DOWN:
                    scroll_y -= SCROLL_SPEED
                if event.key == pygame.K_UP:
                    scroll_y += SCROLL_SPEED

            if event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * 40  # smooth mousewheel scroll

        # Auto-add timed lines
        if next_line_index < len(dialogue):
            text, delay = dialogue[next_line_index]
            if now - start_time >= delay:
                visible_lines.append(text)
                next_line_index += 1
                start_time = now

        # Prevent scroll going out of bounds
        scroll_y = max(min(scroll_y, 0), -1400)

        # Draw background
        screen.fill(BLACK)

        # Draw portrait
        screen.blit(portrait, (50, 100))

        # Draw heading
        draw_text(screen, f"{name} – Interrogation", HEADER_FONT, GOLD,
                  SCREEN_WIDTH // 2, 40)

        # Clear log surface
        log_surface.fill((0, 0, 0, 0))

        # Draw all visible lines onto log surface
        y_offset = 0
        for line in visible_lines:
            draw_text_wrapped(log_surface, line, DETAIL_FONT, WHITE,
                              10, y_offset, log_surface.get_width() - 20)
            y_offset += 40

        # Draw the scrolling log
        screen.blit(log_surface, (320, 100 + scroll_y))

        # Instructions
        draw_text(screen,
                  "BACKSPACE: for interrogating other suspects",
                  DETAIL_FONT, RED_CLUE,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)

        pygame.display.flip()
        clock.tick(60)


def run_suspect_review():
    start_y = 120
    running = True
    
    # Get the names only once
    suspect_names = list(SUSPECT_DATA.keys())
    
    COL_WIDTH = SCREEN_WIDTH // len(suspect_names)

    name_rects = {}
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return "TIMELINE"
    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for name, rect in name_rects.items():
                    if rect.collidepoint(mouse_pos):
                        # run interrogation for this suspect
                        result = run_interrogation(name)

                        # If interrogation ends (Backspace pressed), continue showing suspect list again
                        if result == "BACK_TO_LIST":
                            pass  # simply refresh
                        else:
                            return result

        screen.fill(DARK_GRAY)
        draw_text(screen, "SUSPECT PROFILES: Click to interrogate", REPORT_TITLE_FONT, GOLD, SCREEN_WIDTH // 2, 50)
        
        current_x = COL_WIDTH // 2
        name_rects.clear()
        
        for name in suspect_names:
            data = SUSPECT_DATA[name]
            current_y = start_y

            name_surface = HEADER_FONT.render(name, True, WHITE)
            name_rect = name_surface.get_rect(center=(current_x, current_y))
            screen.blit(name_surface, name_rect)

            current_y += 40
            pygame.draw.line(screen, WHITE, (current_x - 100, current_y), (current_x + 100, current_y), 1)
            current_y += 10

            # store for clicking
            name_rects[name] = name_rect

            detail_x = current_x - 100
            
            # Detail 1: Relation
            draw_text(screen, "RELATION:", DETAIL_FONT, RED_CLUE, detail_x, current_y, align="left")
            draw_text(screen, data['Relation'], DETAIL_FONT, LIGHT_GRAY, detail_x, current_y + 20, align="left")
            current_y += 60

            # Detail 2: Motive
            draw_text(screen, "MOTIVE:", DETAIL_FONT, RED_CLUE, detail_x, current_y, align="left")
            draw_text(screen, data['Motive'], DETAIL_FONT, LIGHT_GRAY, detail_x, current_y + 20, align="left")
            current_y += 60

            # Detail 3: Access
            draw_text(screen, "ACCESS:", DETAIL_FONT, RED_CLUE, detail_x, current_y, align="left")
            draw_text_wrapped(screen, data['Access'], DETAIL_FONT, LIGHT_GRAY, detail_x, current_y + 20, 250)
            current_y += 60

            # Move to the next column
            current_x += COL_WIDTH 
            
        draw_text(screen, "Press SPACE to proceed to get the Timeline...", HEADER_FONT, RED_CLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()
        clock.tick(60)

# SCENE 5: TIMELINE
TIMELINE = {
    "8:45 PM": ("Cast preparations underway backstage", LIGHT_GRAY),
    "9:00 PM": ("Lena seen applying makeup in Evelyn’s dressing room", LIGHT_GRAY),
    "9:10 PM": ("Marcus seen arguing quietly with Evelyn in hallway", LIGHT_GRAY),
    "9:15 PM": ("Lena leaves Evelyn’s dressing room — Evelyn alive (last seen)", LIGHT_GRAY),
    "9:20 PM": ("Hallway security camera recorded its last frame before going offline", LIGHT_GRAY), 
    "9:25 PM": ("Clara confirmed on stage, rehearsing cues", LIGHT_GRAY),
    "9:30 PM": ("Final act cue — Evelyn fails to appear", LIGHT_GRAY),
    "9:35 PM": ("Assistant discovers Evelyn’s body", LIGHT_GRAY)
}

def display_timeline():
    start_y = 180
    line_spacing = 40
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return "FINAL_ACCUSATION" 

        screen.fill(DARK_GRAY)

        draw_text(screen, "Timeline", REPORT_TITLE_FONT, GOLD, SCREEN_WIDTH // 2, 50)
        current_y = start_y
        
        for header, (detail, color) in TIMELINE.items():
            if header:
                draw_text(screen, f"{header}:", DETAIL_FONT, WHITE, SCREEN_WIDTH // 4, current_y, align="left")
                draw_text(screen, detail, DETAIL_FONT, color, SCREEN_WIDTH // 4 + 250, current_y, align="left")
            
            current_y += line_spacing

        draw_text(screen, "Press SPACE for Final Accusation...", NARRATION_FONT, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

        pygame.display.flip()
        clock.tick(60)


# SCENE 6: FINAL ACCUSATION (Decision Point)
def run_accusation_phase():
    
    suspect_names = list(SUSPECT_DATA.keys())
    selected_suspect_index = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    selected_suspect_index = (selected_suspect_index - 1) % len(suspect_names)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    selected_suspect_index = (selected_suspect_index + 1) % len(suspect_names)
                
                elif event.key == pygame.K_RETURN:
                    return suspect_names[selected_suspect_index] 

        screen.fill(DARK_GRAY)

        draw_text(screen, "WHO KILLED EVELYN HART?", REPORT_TITLE_FONT, WHITE, SCREEN_WIDTH // 2, 100)
        
        y_suspect = 200
        for i, name in enumerate(suspect_names):
            color = GOLD if i == selected_suspect_index else LIGHT_GRAY
            center_x = SCREEN_WIDTH // 2
            
            if i == selected_suspect_index:
                rect_x = center_x - 200
                pygame.draw.rect(screen, GOLD, (rect_x, y_suspect - 20, 400, 60), 3) 
                
            draw_text(screen, name, HEADER_FONT, color, center_x, y_suspect)
            draw_text(screen, f"({SUSPECT_DATA[name]['Motive']})", DETAIL_FONT, LIGHT_GRAY, center_x, y_suspect + 25)
            y_suspect += 80

        draw_text(screen, "Use [← →] or [↑ ↓] to Select | [ENTER] to ACCUSE", HEADER_FONT, RED_CLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()
        clock.tick(60)


# SCENE 7: CASE ANALYSIS REVIEW (Confirmation)
def run_case_analysis_review(accused_suspect):
    
    analysis = CASE_ANALYSIS_DATA.get(accused_suspect)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return accused_suspect 
                elif event.key == pygame.K_BACKSPACE:
                    return "RESTART_ACCUSATION" 

        screen.fill(DARK_GRAY)

        draw_text(screen, f"ANALYSIS: {accused_suspect}", REPORT_TITLE_FONT, GOLD, SCREEN_WIDTH // 2, 50)
        
        y_dp = 100
        for line in analysis["points"]:
            color = WHITE
            font = DETAIL_FONT
            if line.startswith("✅"): color = (0, 255, 0)
            elif line.startswith("⚠️"): color = (255, 165, 0)
            elif line.startswith("🏆"): 
                color = GOLD
                font = HEADER_FONT

            draw_text(screen, line, font, color, 50, y_dp, align="left")
            y_dp += 30

        y_verdict = SCREEN_HEIGHT - 180
        pygame.draw.rect(screen, analysis["color"], (50, y_verdict - 20, SCREEN_WIDTH - 100, 80), 3)
        draw_text(screen, "FINAL VERDICT:", HEADER_FONT, WHITE, SCREEN_WIDTH // 2, y_verdict)
        draw_text(screen, analysis["verdict"], REPORT_TITLE_FONT, analysis["color"], SCREEN_WIDTH // 2, y_verdict + 35)

        draw_text(screen, "Press [ENTER] to CONFIRM ACCUSATION | Press [BACKSPACE] to RETURN", 
                  HEADER_FONT, RED_CLUE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()
        clock.tick(60)


# SCENE 8: THE FINAL REVEAL (Case Closed)

def run_final_reveal(accused_killer):
    
    TRUE_KILLER = "Lena Brooke"

    reveal_narratives = {
        "Lena Brooke": {
            "title": "🏆 CASE CLOSED: LENA BROOKE CONVICTED 🏆",
            "text": [
                "**Detective Verdict: You analyzed motive, means, opportunity, and evidence perfectly.**",
                "Evelyn’s cruel reprimand and pay cut, which destroyed Lena’s career dreams, fueled quiet resentment and **personal betrayal**.",
                "",
                "**The Method:**",
                "While applying Evelyn’s final look, Lena **added poison** (the sedative from her kit) into the champagne.",
                "She encouraged Evelyn to 'relax before the scene' with the drink, knowing Evelyn **never drank** pre-show, making the delivery deliberate.",
                "Lena left the room, pretending to give space, and confirmed the moment of death by listening for the **glass falling** right after the poison took effect.",
                "",
                "**The Scene Cover-Up:**",
                "The **Perfume bottle** was smashed to **mask the chemical smell** from the sedative.",
                "The **Lipstick smudge** on the glass was done intentionally to shift suspicion toward Clara.",
                "Lena exploited Victor’s simultaneous **camera blackout** to slip away unseen.",
                "She staged confusion and cleverly leveraged existing tensions to blur the truth."
            ],
            "is_correct": True
        },
        "Clara Vale": {
            "title": "❌ ACCUSATION FAILED: CLARA VALE ❌",
            "text": [
                "Clara had the motive (ambition), and the matching lipstick placed her in contact with the glass.",
                "However, her confirmed alibi on stage between 9:25–9:35 PM proves she was not present during the critical poison window.",
                "Clara was merely a **pawn**; the lipstick was used as a **red herring** to shift suspicion toward the most obvious rival."
            ],
            "is_correct": False
        },
        "Marcus Reed": {
            "title": "❌ ACCUSATION FAILED: MARCUS REED ❌",
            "text": [
                "Marcus had powerful motive (obsession/jealousy) and access (spare key). The **scratches** and **missing earring** confirm a violent confrontation around 9:10 PM.",
                "But the cause of death was **poison**, not force.",
                "Marcus likely confronted Evelyn, causing the struggle, but he did **not deliver the poison**. He lacked the means and the subtle intent."
            ],
            "is_correct": False
        },
        "Victor Lang": {
            "title": "❌ ACCUSATION FAILED: VICTOR LANG ❌",
            "text": [
                "Victor's strong financial motive and the **wiped security logs** from 9:10–9:30 PM made him look guilty of the murder.",
                "However, Victor was responsible for the **cover-up**, not the act itself. He disabled the cameras to protect the production’s reputation, knowing the murder happened backstage.",
                "He lacked the direct means and physical access to administer the poison."
            ],
            "is_correct": False
        }
    }

    narrative = reveal_narratives.get(accused_killer)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return "GAME_OVER" 

        screen.fill(BLACK)
        bg_color = (20, 0, 0) if not narrative["is_correct"] else (0, 20, 0)
        title_color = RED_CLUE if not narrative["is_correct"] else GOLD
        screen.fill(bg_color)
        
        draw_text(screen, narrative["title"], REPORT_TITLE_FONT, title_color, SCREEN_WIDTH // 2, 70)
        
        y_offset = 150
        for line in narrative["text"]:
            font = DETAIL_FONT
            color = WHITE
            
            if line.startswith("**"): 
                color = GOLD
                font = HEADER_FONT
            elif line.strip() == "": 
                y_offset += 10
                continue
            
            draw_text(screen, line.strip("*"), font, color, SCREEN_WIDTH // 2, y_offset, align="center")
            y_offset += 40
            
        draw_text(screen, "Press any key to finish...", HEADER_FONT, LIGHT_GRAY, 
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()
        clock.tick(60)


# =====================================================================
# --- Main Game Loop (Controller) ---
# =====================================================================

def main_game_loop():
    game_state = "INTRO"
    accused_killer = None

    while True:
        if game_state == "INTRO":
            game_state = run_scene_one()
        
        elif game_state == "TOXICOLOGY_REPORT":
            game_state = display_toxicology_report()

        elif game_state == "CRIME_SCENE_INVESTIGATION":
            game_state = run_investigation_scene()

        elif game_state == "SUSPECT_REVIEW":
            game_state = run_suspect_review()

        elif game_state == "TIMELINE":
            game_state = display_timeline()
            
        elif game_state == "FINAL_ACCUSATION":
            accused_killer = run_accusation_phase()
            game_state = "ANALYSIS_REVIEW"

        elif game_state == "ANALYSIS_REVIEW":
            next_action = run_case_analysis_review(accused_killer)
            if next_action == "RESTART_ACCUSATION":
                game_state = "FINAL_ACCUSATION"
            else:
                accused_killer = next_action # Confirmed killer
                game_state = "FINAL_REVEAL"

        elif game_state == "FINAL_REVEAL":
            game_state = run_final_reveal(accused_killer)

        elif game_state == "GAME_OVER":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main_game_loop()
