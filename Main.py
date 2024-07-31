import pygame
from pygame import display, time, event, draw, font, mixer, image, transform, Surface, Rect
from time import perf_counter
from random import randrange
from math import sin, cos, pi, sqrt


pygame.init()

SCREEN_SIZE = (1000, 600)
screen = display.set_mode(SCREEN_SIZE)

FPS_POLLING_PERIOD = 200  # define the number of milliseconds to wait between each polls of the fps and frametime

# define the hit window for each judgment
WINDOW_MAX_PERFECT = 40
WINDOW_PERFECT = 80
WINDOW_GREAT = 160
WINDOW_EARLY_MISS = 200  # early miss is giving the player a miss judgment if they hit too early before the great hit window

# define the maxiumum average interval between each hits during a drumroll (hitting the large object) to acheive each judgment
DRUMROLL_PERFECT_INTERVAL = 125
DRUMROLL_GREAT_INTERVAL = 250

# define the score achieved for each judgment
SCORE_PERFECT = 100
SCORE_GREAT = 50
SCORE_DRUMROLL_HIT = 10

# define the properties of score bonus
# score bonus is a bonus score applied onto the base score for perfect and great once the player gets a certain amount of combo
SCORE_BONUS_COMBO_STEP = 50  # the combo needed to increase the score bonus
SCORE_BONUS_STEP = 0.2  # the  amount of score bonus increased everytime the step is reached

# define the accuracy of each judgment in percentage
# miss has an accuracy of 0%
ACCURACY_PERFECT = 100
ACCURACY_GREAT = 50

# define the dimenion of the buttons in other pages
OPTION_WIDTH = 200
OPTION_HEIGHT = 60

SONG_PREVIEW_FADE_IN_DURATION = 1000  # the fade-in duration of the preview playback
SONG_PREVIEW_END_WAIT = 1000  # the time in milliseconds to wait to start the song preview agian once the preview ends

# define the duration of animations
DIP_TO_BLACK_ANIMATION_DURATION = 500
SONG_SLIDE_ANIMATION_DURATION = 500
JUDGMENT_ANIMATION_DURATION = 150

SONG_START_HOLD = 3000  # the wait in millisecond before the song's playback in game page
SONG_END_HOLD = 2000  # the wait in millisecond to before the jumping to the result page after the song's play ends

JUDGMENT_DISPLAY_DURATION = 2000  # the maxium number of millisecond a judgment stays on the screen

COMBO_BREAK_ANIMATION_SPEED = 0.1  # the speed of the combo number dropping after a combo break in the unit of combo per millisecond (0.1 means the combo number will go down by 1 every 10 ms)

EXPLOSION_IMG_COUNT = 17  # the nubmer of frames in the explosion gif
EXPLOSION_ANIMATION_SPEED = 0.04  # the speed of the gif being display in frame per millisecond (0.04 frame per millisecond equals 40 fps)

SPACING = 20  # the space between two surface/rectangles, used very often in the program to imporve formatting of the text shown on the screen

MAX_SPEED = 20  # the maximum note that can be configured

# define the dimension and coordinates used in the menu
MENU_TITLE_CENTER_X = 300
MENU_OPTION_CENTER_X = 700
MENU_OPTION_WIDTH = 400
MENU_OPTION_HEIGHT = 50

# define dimensions and coordinates used in the song-select page
SONG_SELECT_IMAGE_HEIGHT = 350  # the height of the song's cover image
SONG_SELECT_IMAGE_CENTER_Y = 350  # the center y-coordinate of the song's cover image
SONG_SELECT_ARROW_RECT_WIDTH = 80  # the width of the two arrows' hitboxes
SONG_SELECT_ARROW_RECT_HEIGHT = 100  # the height of the two arrows' hitboxes
SONG_SELECT_ARROW_IMG_SIDE_LENGTH = 80  # the side length of the arrows' images to scale to (the image is square) 
SONG_SELECT_TITLE_CENTER_Y = 50  # the center y-coordinate of the song title tesxt
SONG_SELECT_ARTIST_CENTER_Y = 80  # the center y-coordinate of the song artist text
SONG_SELECT_INFO_TOP_Y = 110  # the top y-coordinate of the line of song information
SONG_SELECT_INFO_SPACE = 30  # the space between each piece of song information text
SONG_SELECT_SCORE_TOP_Y = 140  # the top y-coordinate of the song's high score text
SONG_SELECT_SCORE_RIGHT_X = 450  # the right x-coordinate of the song' high score text
SONG_SELECT_ACCURACY_LEFT_X = 550  # the left x-coordinate of the song's best accuracy text

# define dimensions and coordinates used in the game page
GAME_PROGRESS_BAR_HEIGHT = 10  # the heigt of the prgress at the top of the screen
GAME_JUDGMENT_LINE_X = 200  # the x-coordinate of the judgment line (where the sircles is)
GAME_OBJECT_HEIGHT = 60  # the height of the blue and red hit objects
GAME_DRUMROLL_HEIGHT = 300  # the height of the drumroll
GAME_GUIDE_CIRCLE_RADIUS = 15  # the radius of the 2 circle on the left
GAME_RED_CENTER_Y = 250  # the center y-coordinate of the red lane
GAME_BLUE_CENTER_Y = 450  # the center y-coordinate of the blue lane
GAME_DRUMROLL_CENTER_Y = 350  # the center y-coordinate of the drumroll object
GAME_EXPLOION_IMG_WIDTH = 80  # the width of the exlosion gif to scale to
GAME_DRUMROLL_EXPLOSION_RANGE = 80  # the possible explosion range from the center of the drumroll
GAME_COMBO_TEXT_CENTER_Y = 60  # the center y-coordinate of the text "combo"
GAME_COMBO_VALUE_CENTER_Y = 90  # The center y-coordinate of the combo value
GAME_JUDGMENT_CENTER_Y = 160  # the center y-coordinate of the judgment text
GAME_SCORE_TOP_RIGHT_MARGIN = 20  # the margin between the score displayed and the top and the right border of the screen

# define dimensions and coordinates used in the result page
RESULT_FILED_LEFT_X = 350  # the left x-coordinate of the field column
RESULT_VALUE_RIGHT_X = 600  # the right x-coordinate of the value column
RESULT_SONG_TITLE_TOP_Y = 100  # the top y-coordinate of the song title text
RESULT_SONG_ARTIST_TOP_Y = 140  # the top y-coordinate of the song artist text
RESULT_SCORE_LEFT_X = 450  # the left x-coordinate of the score text
RESULT_SCORE_CENTER_Y = 200  # the center y-coordinate of the score text
RESULT_NEW_BEST_LEFT_X = 600  # the left x-coordinate of the new best text
RESULT_COMBO_ACCURACY_TOP_Y = 250  # the top y-coordinate of both the combo and accuracy text
RESULT_MAX_COMBO_LEFT_X = 300  # the left x-coordinate of the max combo text
RESULT_ACCURACY_LEFT_X = 550  # the left x-coordinate of the accuracy text

# define dimension and coordinates used in the setting page
SETTING_SLIDER_LEFT_X = 200
SETTING_SLIDER_LENGTH = 600
SETTING_SLIDER_THICKNESS = 5
SETTING_SLIDER_THUMB_RADIUS = 10
SETTING_SLIDER_THUMB_STROKE_WIDTH = 3
SETTING_PLUS_MINUS_RECT_SIDE_LENGTH = 40
SETTING_VOLUME_TEXT_CENTER_Y = 30
SETTING_VOLUME_VALUE_CENTER_Y = 60
SETTING_VOLUME_BAR_CENTER_Y = 100
SETTING_OFFSET_TEXT_CENTER_Y = 150
SETTING_OFFSET_VALUE_CENTER_Y = 180
SETTING_OFFSET_BAR_CENTER_Y = 220
SETTING_SPEED_TEXT_CENTER_Y = 270
SETTING_SPEED_VALUE_CENTER_Y = 300
SETTING_TOGGLE_CENTER_Y = 350
SETTING_TOGGLE_RECT_HEIGHT = 40
SETTING_CHECKBOX_RADIUS = 10
SETTING_CHECKBOX_STROKE_WIDTH = 3
SETTING_HITSOUND_LEFT_X = 300
SETTING_FPS_LEFT_X = 600
SETTING_KEYBIND_TEXT_CENTER_Y = 400
SETTING_KEY_RECT_TOP_Y = 450
SETTING_KEY_RECT_LEFT_X = 400
SETTING_KEY_RECT_SIDE_LENGTH = 50
SETTING_KEY_RECT_STROKE_WIDTH = 3

# stores all keys that the program recognizes
# the first column is the pygame id of each keys (e.g. pygame.K_0 is 48)
# the second column is the character of each keys (this doesn't take shift into consideration)
TYPABLE_KEYS = (
    (39, "'"),
    (44, ','),
    (45, '-'),
    (46, '.'),
    (47, '/'),
    (48, '0'),
    (49, '1'),
    (50, '2'),
    (51, '3'),
    (52, '4'),
    (53, '5'),
    (54, '6'),
    (55, '7'),
    (56, '8'),
    (57, '9'),
    (59, ';'),
    (61, '='),
    (91, '['),
    (92, '\\'),
    (93, ']'),
    (97, 'a'),
    (98, 'b'),
    (99, 'c'),
    (100, 'd'),
    (101, 'e'),
    (102, 'f'),
    (103, 'g'),
    (104, 'h'),
    (105, 'i'),
    (106, 'j'),
    (107, 'k'),
    (108, 'l'),
    (109, 'm'),
    (110, 'n'),
    (111, 'o'),
    (112, 'p'),
    (113, 'q'),
    (114, 'r'),
    (115, 's'),
    (116, 't'),
    (117, 'u'),
    (118, 'v'),
    (119, 'w'),
    (120, 'x'),
    (121, 'y'),
    (122, 'z'),
)

# define all kinds of states
# for difficulty
DIFFICULTY_BEGINNER = 0
DIFFICULTY_ADVANCED = 1

# for the direction of the sliding animtion in the song-select page
SLIDE_LEFT = 0
SLIDE_RIGHT = 1

# for the nnote types in the game
TYPE_RED = 0
TYPE_BLUE = 1
TYPE_DRUMROLL = 2

# for judgment types
JUDGMENT_NONE = 0
JUDGMENT_PERFECT = 1
JUDGMENT_GREAT = 2
JUDGMENT_MISS = 3

SUBJUDGMENT_NONE = 0
SUBJUDGMENT_EARLY = 1
SUBJUDGMENT_LATE = 2

# define states for each page
PAGE_EXIT = 0
PAGE_MENU = 1
PAGE_SONG_SELECT = 2
PAGE_GAME = 3
PAGE_RESULT = 4
PAGE_SETTINGS = 5
PAGE_HELP = 6

# define fonts
FONT_FPS = font.Font("Fonts/SEGOEUI.TTF", 12)
FONT_TITLE = font.Font("Fonts/SEGUISB.TTF", 48)
FONT_MENU_OPTION = font.Font("Fonts/SEGUISB.TTF", 20)
FONT_OPTION = font.Font("Fonts/SEGUISB.TTF", 28)
FONT_SONG_TITLE = font.Font("Fonts/Arial-True-Unicode-Bold.ttf", 32)
FONT_SONG_ARTIST = font.Font("Fonts/Arial-True-Unicode.ttf", 20)
FONT_SONG_INFO = font.Font("Fonts/ARIAL.TTF", 16)
FONT_JUDGMENT = font.Font("Fonts/ARIALBD.TTF", 28)
FONT_SUBJUDGMENT = font.Font("Fonts/ARIALBD.TTF", 12)
FONT_COMBO_TEXT = font.Font("Fonts/ARIAL.TTF", 12)
FONT_COMBO_VALUE = font.Font("Fonts/ARIAL.TTF", 32)
FONT_SCORE = font.Font("Fonts/ARIAL.TTF", 20)
FONT_NEW_BEST = font.Font("Fonts/ARIALBD.TTF", 24)
FONT_RESULT_TITLE = font.Font("Fonts/Arial-True-Unicode-Bold.ttf", 32)
FONT_RESULT_ARTIST = font.Font("Fonts/Arial-True-Unicode.ttf", 24)
FONT_RESULT_FIELD = font.Font("Fonts/ARIALBD.TTF", 20)
FONT_RESULT_VALUE = font.Font("Fonts/ARIAL.TTF", 20)
FONT_SETIING_PLUS_MINUS = font.Font("Fonts/ARIAL.TTF", 28)
FONT_SETTING_FIELD = font.Font("Fonts/ARIALBD.TTF", 24)
FONT_SETTING_VALUE = font.Font("Fonts/ARIAL.TTF", 20)
FONT_HELP = font.Font("Fonts/ARIAL.TTF", 16)

# define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_FPS = (255, 255, 255)
COLOR_MENU_BG = (51, 51, 51)
COLOR_SONG_SELECT_BEGINNER_BG = (17, 70, 143)  # blue
COLOR_SONG_SELECT_ADVANDED_BG = (255, 36, 66)  # red
COLOR_TEXT = (255, 255, 255)
COLOR_MENU_BUTTON_FILL = (255, 36, 66)  # red
COLOR_MENU_BUTTON_HOVER = (61, 178, 255)  # blue
COLOR_LANE_RED = (255, 36, 66)  # red
COLOR_LANE_BLUE = (61, 178, 255)  # blue
COLOR_ARROW = (255, 255, 255)
COLOR_HIT_CIRCLE = (251, 241, 211)  # beige
COLOR_SONG_PROGRESS_BAR = (204, 204, 204)
COLOR_JUDGMENT_PERFECT = (247, 251, 118)  # yellow
COLOR_JUDGMENT_GREAT = (147, 237, 142)  # green
COLOR_JUDGMENT_MISS = (250, 85, 85)  # red
COLOR_SUBJUDGMENT_EARLY = (33, 146, 255)  # blue
COLOR_SUBJUDGMENT_LATE = (255, 30, 0)  # red
COLOR_NEW_BEST = (255, 234, 32)  # yellow
COLOR_SLIDER = (255, 255, 255)
COLOR_SLIDER_FILL = (61, 178, 255)  # blue
COLOR_SLIDER_THUMB_STROKE = (61, 178, 255)  # blue
COLOR_CHECKBOX_STROKE = (255, 255, 255)
COLOR_CHECKBOX_FILL = (61, 178, 255)  # blue
COLOR_KEY_RECT_STROKE = (255, 255, 255)

# define alphas (value range: 0-255)
ALPHA_BUTTON_HOVER_FILL = 128  # the alpha of the button's fill when the mouse hovers over it
ALPHA_IMG_BG_DIMM = 180  # the alpha of the surface that dim the background in the result page

# define custom events
EVENT_REPORT_FPS = pygame.USEREVENT + 0
EVENT_PREVIEW_END = pygame.USEREVENT + 1
EVENT_PREVIEW_WAIT_END = pygame.USEREVENT + 2
EVENT_SONG_START = pygame.USEREVENT + 3
EVENT_SONG_END = pygame.USEREVENT + 4
EVENT_RESULT_SCREEN = pygame.USEREVENT + 5

page = PAGE_MENU
timer = time.Clock()
current_time = int()
event_queue = list()

# define two surfaces to temporarily hold the drawn screen
# in each loop, shapes and surfaces are directly drawn onto screen_draw_temp
# the drawn screen is then transfered to screen_draw and onto the main screen
# this avoids displaying a half-finished page on a plane
screen_draw = Surface(SCREEN_SIZE)
screen_draw_temp = Surface(SCREEN_SIZE)

# store the position of the mouse cursor
mouse_x = -1
mouse_y = -1

# intialize the surface used to transition between pages
dip_to_black_mask_surface = Surface(SCREEN_SIZE)
dip_to_black_mask_surface.set_alpha(0)

# define global varibles about the transition
dip_to_black_animation = False
dip_to_black_animation_start_time = int()
dip_to_black_animation_end_page_init_function = None
dip_to_black_animation_end_page_init_function_argument = None

# define global varibles for the fading out transition after fading into black
dip_to_black_reversed_animation = False
dip_to_black_reversed_animation_start_time = int()

# defines global varibles to store the renders of the fps information so they don't need to be rendered multiple times
fps_display = FONT_FPS.render("FPS 0  |  Frametime 0ms", True, COLOR_FPS).convert_alpha()
fps_display_width, fps_display_height = fps_display.get_size()

# stores the three lines of the game title 
game_title = (
    FONT_TITLE.render("E-waste", True, COLOR_TEXT),
    FONT_TITLE.render("no", True, COLOR_TEXT),
    FONT_TITLE.render("Tatsujin", True, COLOR_TEXT),
)
# and their dimension
game_title_dimension = (
    game_title[0].get_size(),
    game_title[1].get_size(),
    game_title[2].get_size(),
)

# stores more text used in the menu page
play_beginner_text = FONT_MENU_OPTION.render("Play (Beginner)", True, COLOR_TEXT)
play_beginner_text_width, text_height = play_beginner_text.get_size()

play_advanced_text = FONT_MENU_OPTION.render("Play (Advanced)", True, COLOR_TEXT)
play_advanced_text_width, play_advanced_text_height = play_advanced_text.get_size()

settings_text = FONT_MENU_OPTION.render("Settings", True, COLOR_TEXT)
settings_text_width, settings_text_height = settings_text.get_size()

help_text = FONT_MENU_OPTION.render("Help", True, COLOR_TEXT)
help_text_width, help_text_height = help_text.get_size()

exit_text = FONT_MENU_OPTION.render("Exit", True, COLOR_TEXT)
exit_text_width, exit_text_height = exit_text.get_size()

# global variables for the song-select page
song_list = list()
song_count = int()
song_selected_index = int()
song_select_bg_color = tuple()
# for the sliding animation
song_slide_animation = False
song_slide_animation_start_time = int()
song_slide_direction = int()

# surfaces used for the sliding animation
previous_song_screen = Surface(SCREEN_SIZE)
current_song_screen = Surface(SCREEN_SIZE)
next_song_screen = Surface(SCREEN_SIZE)

# create hitboxes for some buttons to check for their collision with the mouse later
left_arrow_rect = Rect(0, SCREEN_SIZE[1]//2-SONG_SELECT_ARROW_RECT_HEIGHT//2, SONG_SELECT_ARROW_RECT_WIDTH, SONG_SELECT_ARROW_RECT_HEIGHT)
right_arrow_rect = Rect(SCREEN_SIZE[0]-SONG_SELECT_ARROW_RECT_WIDTH, SCREEN_SIZE[1]//2-SONG_SELECT_ARROW_RECT_HEIGHT//2, SONG_SELECT_ARROW_RECT_WIDTH, SONG_SELECT_ARROW_RECT_HEIGHT)
option_bottom_left_rect = Rect(0, SCREEN_SIZE[1]-OPTION_HEIGHT, OPTION_WIDTH, OPTION_HEIGHT)
option_bottom_right_rect = Rect(SCREEN_SIZE[0]-OPTION_WIDTH, SCREEN_SIZE[1]-OPTION_HEIGHT, OPTION_WIDTH, OPTION_HEIGHT)
option_start_rect = Rect(500-OPTION_WIDTH//2, SCREEN_SIZE[1]-OPTION_HEIGHT, OPTION_WIDTH, OPTION_HEIGHT)

# create surfaces for some buttons to create a translucent fill for the buttons once the mouse hovers over it
arrow_button_surface = Surface((SONG_SELECT_ARROW_RECT_WIDTH, SONG_SELECT_ARROW_RECT_HEIGHT))
arrow_button_surface.fill(COLOR_BLACK)
arrow_button_surface.set_alpha(ALPHA_BUTTON_HOVER_FILL)

option_button_surface = Surface((OPTION_WIDTH, OPTION_HEIGHT))
option_button_surface.fill(COLOR_BLACK)
option_button_surface.set_alpha(ALPHA_BUTTON_HOVER_FILL)

# load images and render text that will be used in the game page
left_arrow_img = image.load("Left Arrow.png").convert_alpha()
left_arrow_img = transform.smoothscale(left_arrow_img, (SONG_SELECT_ARROW_IMG_SIDE_LENGTH, SONG_SELECT_ARROW_IMG_SIDE_LENGTH))

right_arrow_img = image.load("Right Arrow.png").convert_alpha()
right_arrow_img = transform.smoothscale(right_arrow_img, (SONG_SELECT_ARROW_IMG_SIDE_LENGTH, SONG_SELECT_ARROW_IMG_SIDE_LENGTH))

option_back_text = FONT_OPTION.render("Back", True, COLOR_TEXT)
option_back_text_width, option_back_text_height = option_back_text.get_size()

option_start_text = FONT_OPTION.render("Start", True, COLOR_TEXT)
option_start_text_width, option_start_text_height = option_start_text.get_size()

option_continue_text = FONT_OPTION.render("Continue", True, COLOR_TEXT)
option_continue_text_width, option_continue_text_height = option_continue_text.get_size()

option_retry_text = FONT_OPTION.render("Retry", True, COLOR_TEXT)
option_retry_text_width, option_retry_text_height = option_retry_text.get_size()

# global variables for the game page
song = None
song_restartable = bool()  # define if the user can restart the song by pressing the grave accent
song_start_time = int()  # the time in millisecond the song starts at
total_objects = int()  # the total number of objects the song has
song_duration = int()  # the duration of the song in milliseconds
note_speed = int()  # the speed of the note (e-waste) move from left to right of the screen in pixel per millisecond
hit_objects_red = list()  # stores all the red hit object in a chart
hit_objects_blue = list()  # stores all the blue hit object in a chart
hit_objects_drumroll = list()  # stores all the drumroll in a chart
drumroll_missed = list()  # stores all the missed drumroll in a chart (missed drumroll doesn't dissapear once its hit window ends unlike the other hit objects)
explosion_queue = list()  # the queue for storing all the ongoing explosion effects that need to be displayed

# the image for each hit objecs
red_img = image.load("Red.png").convert_alpha()
width, height = red_img.get_size()
red_img_height = GAME_OBJECT_HEIGHT
red_img_width = width * red_img_height // height
red_img = transform.smoothscale(red_img, (red_img_width, red_img_height))

blue_img = image.load("Blue.png").convert_alpha()
width, height = blue_img.get_size()
blue_img_height = GAME_OBJECT_HEIGHT
blue_img_width = width * blue_img_height // height
blue_img = transform.smoothscale(blue_img, (blue_img_width, blue_img_height))

drumroll_img = image.load("Drumroll.png").convert_alpha()
width, height = blue_img.get_size()
drumroll_img_height = GAME_DRUMROLL_HEIGHT
drumroll_img_width = width * drumroll_img_height // height
drumroll_img = transform.smoothscale(drumroll_img, (drumroll_img_width, drumroll_img_height))

combo_animation = False
combo_animation_start_time = int()
combo_animation_start_combo = int()

combo_text = FONT_COMBO_TEXT.render("COMBO", True, COLOR_TEXT)
combo_text_width, combo_text_height = combo_text.get_size()

score_text = FONT_SCORE.render('Score', True, COLOR_TEXT)
score_text_width, score_text_height = score_text.get_size()

score_value_text = None
score_value_text_width = int()
score_value_text_height = int()

# global variables for displaying the judgment animation and the judgment itself
judgment_animation = False
judgment_animation_start_time = int()
judgment_text = None
judgment_text_width = int()
judgment_text_height = int()
subjudgment_text = None
subjudgment_text_width = int()
subjudgment_text_height = int()

# define global varibles used to store scores
combo = int()
max_combo = int()
score = int()
total_accuracy = int()
count_perfect = int()
count_great = int()
count_miss = int()
count_early = int()
count_late = int()

# define global variables for the result page
new_best = bool()

# render text used in the result page
result_new_best_text = FONT_NEW_BEST.render("NEW BEST!!", True, COLOR_NEW_BEST)
result_new_best_text_width, result_new_best_text_height = result_new_best_text.get_size()

result_score_text = FONT_RESULT_FIELD.render("SCORE", True, COLOR_TEXT)
result_score_text_width, result_score_text_height = result_score_text.get_size()

result_max_combo_text = FONT_RESULT_FIELD.render("MAX COMBO", True, COLOR_TEXT)
result_max_combo_text_width, result_max_combo_text_height = result_max_combo_text.get_size()

result_accuracy_text = FONT_RESULT_FIELD.render("ACCURACY", True, COLOR_TEXT)
result_accuracy_text_width, result_accuracy_text_height = result_accuracy_text.get_size()

result_perfect_text = FONT_RESULT_FIELD.render("PERFECT", True, COLOR_JUDGMENT_PERFECT)
result_perfect_text_width, result_perfect_text_height = result_perfect_text.get_size()

result_great_text = FONT_RESULT_FIELD.render("GREAT", True, COLOR_JUDGMENT_GREAT)
result_great_text_width, result_great_text_height = result_great_text.get_size()

result_miss_text = FONT_RESULT_FIELD.render("MISS", True, COLOR_JUDGMENT_MISS)
result_miss_text_width, result_miss_text_height = result_miss_text.get_size()

result_early_text = FONT_RESULT_FIELD.render("Early", True, COLOR_SUBJUDGMENT_EARLY)
result_early_text_width, result_early_text_height = result_early_text.get_size()

result_late_text = FONT_RESULT_FIELD.render("Late", True, COLOR_SUBJUDGMENT_LATE)
result_late_text_width, result_late_text_height = result_late_text.get_size()

# initialize the surface used to dim the background down
result_bg_mask_surface = Surface(SCREEN_SIZE)
result_bg_mask_surface.set_alpha(ALPHA_IMG_BG_DIMM)

# global variables waited to be initialized to store text used in the result page
result_bg = None
result_bg_width = int()
result_bg_height = int()

result_score_value_text = None
result_score_value_text_width = int()
result_score_value_text_height = int()

result_song_title_text = None
result_song_title_text_width = int()
result_song_title_text_height = int()

result_song_artist_text = None
result_song_artist_text_width = int()
result_song_artist_text_height = int()

result_max_combo_value_text = None
result_max_combo_value_text_width = int()
result_max_combo_value_text_height = int()

result_accuracy_value_text = None
result_accuracy_value_text_width = int()
result_accuracy_value_text_height = int()

result_perfect_count_text = None
result_perfect_count_text_width = int()
result_perfect_count_text_height = int()

result_great_count_text = None
result_great_count_text_width = int()
result_great_count_text_height = int()

result_miss_count_text = None
result_miss_count_text_width = int()
result_miss_count_text_height = int()

result_early_count_text = None
result_early_count_text_width = int()
result_early_count_text_height = int()

result_late_count_text = None
result_late_count_text_width = int()
result_late_count_text_height = int()

# define global variables for the setting page
volume_thumb_center_x = int()  # the x-coordinate of the thumb of the volume slider
offset_thumb_center_x = int()  # the x-coordinate of the thumb of the offset slider
volume_slider_dragging = bool()  # if the user is dragging the volume slider
offset_slider_dragging = bool()  # if the user is draggin the offset slider
keybind_change = bool()  # if the user is modifying a keybind
key_index = int()  # the keybind the user is modifying

# render text used in the setting page
setting_plus_text = FONT_SETIING_PLUS_MINUS.render('+', True, COLOR_TEXT)
setting_plus_text_width, setting_plus_text_height = setting_plus_text.get_size()

setting_minus_text = FONT_SETIING_PLUS_MINUS.render('-', True, COLOR_TEXT)
setting_minus_text_width, setting_minus_text_height = setting_minus_text.get_size()

setting_volume_text = FONT_SETTING_FIELD.render("Volume", True, COLOR_TEXT)
setting_volume_text_width, setting_volume_text_height = setting_volume_text.get_size()

setting_offset_text = FONT_SETTING_FIELD.render("Offset", True, COLOR_TEXT)
setting_offset_text_width, setting_offset_text_height = setting_offset_text.get_size()

setting_speed_text = FONT_SETTING_FIELD.render("Note Speed", True, COLOR_TEXT)
setting_speed_text_width, setting_speed_text_height = setting_speed_text.get_size()

setting_hitsound_text = FONT_SETTING_VALUE.render("Play Hitsound", True, COLOR_TEXT)
setting_hitsound_text_width, setting_hitsound_text_height = setting_hitsound_text.get_size()

setting_fps_text = FONT_SETTING_VALUE.render("Show FPS", True, COLOR_TEXT)
setting_fps_text_width, setting_fps_text_height = setting_fps_text.get_size()

setting_keybind_text = FONT_SETTING_FIELD.render("Keybinds", True, COLOR_TEXT)
setting_keybind_text_width, setting_keybind_text_height = setting_keybind_text.get_size()

setting_R1_text = FONT_SETTING_VALUE.render("R1", True, COLOR_LANE_RED)
setting_R1_text_width, setting_R1_text_height = setting_R1_text.get_size()

setting_R2_text = FONT_SETTING_VALUE.render("R2", True, COLOR_LANE_RED)
setting_R2_text_width, setting_R2_text_height = setting_R2_text.get_size()

setting_B1_text = FONT_SETTING_VALUE.render("B1", True, COLOR_LANE_BLUE)
setting_B1_text_width, setting_B1_text_height = setting_B1_text.get_size()

setting_B2_text = FONT_SETTING_VALUE.render("B2", True, COLOR_LANE_BLUE)
setting_B2_text_width, setting_B2_text_height = setting_B2_text.get_size()

# global variables waited to be initialized
setting_volume_value_text = None
setting_volume_value_text_width = int()
setting_volume_value_text_height = int()

setting_offset_value_text = None
setting_offset_value_text_width = int()
setting_offset_value_text_height = int()

setting_speed_value_text = None
setting_speed_value_text_width = int()
setting_speed_value_text_height = int()

# the rectangualar hitbox of some objects in the setting page
setting_volume_slider_rect = Rect(SETTING_SLIDER_LEFT_X-SETTING_SLIDER_THUMB_RADIUS, SETTING_VOLUME_BAR_CENTER_Y-SETTING_SLIDER_THUMB_RADIUS, SETTING_SLIDER_LENGTH+SETTING_SLIDER_THUMB_RADIUS*2, SETTING_SLIDER_THUMB_RADIUS*2)
setting_offset_slider_rect = Rect(SETTING_SLIDER_LEFT_X-SETTING_SLIDER_THUMB_RADIUS, SETTING_OFFSET_BAR_CENTER_Y-SETTING_SLIDER_THUMB_RADIUS, SETTING_SLIDER_LENGTH+SETTING_SLIDER_THUMB_RADIUS*2, SETTING_SLIDER_THUMB_RADIUS*2)

setting_hitsound_rect = Rect(SETTING_HITSOUND_LEFT_X-SPACING, SETTING_TOGGLE_CENTER_Y-SETTING_TOGGLE_RECT_HEIGHT//2, SETTING_CHECKBOX_RADIUS*2+setting_hitsound_text_width+SPACING*3, SETTING_TOGGLE_RECT_HEIGHT)
setting_fps_rect = Rect(SETTING_FPS_LEFT_X-SPACING, SETTING_TOGGLE_CENTER_Y-SETTING_TOGGLE_RECT_HEIGHT//2, SETTING_CHECKBOX_RADIUS*2+setting_fps_text_width+SPACING*3, SETTING_TOGGLE_RECT_HEIGHT)

# stores all the text the text used in the help page
tutorial_text = (
    FONT_HELP.render("Press down the \"d\" or \"f\" key to eliminate the red e-waste.", True, COLOR_TEXT),
    FONT_HELP.render("Press \"j\" or \"k\" to eliminate the blue e-waste.", True, COLOR_TEXT),
    FONT_HELP.render("Hit the keys once the e-waste reaches the circles on the left.", True, COLOR_TEXT),
    FONT_HELP.render("Smash \"d\", \"f\", \"j\", and \"k\" as fast as you can", True, COLOR_TEXT),
    FONT_HELP.render("when you see the e-easte pile reaches the circles.", True, COLOR_TEXT),
    FONT_HELP.render("Get a high score by eliminating the e-waste accurately.", True, COLOR_TEXT),
    FONT_HELP.render("Hit the e-waste as close to the circles as possible,", True, COLOR_TEXT),
    FONT_HELP.render("and not letting any e-waste go past the screen.", True, COLOR_TEXT),
    FONT_HELP.render("A more detailed version of this tutorial can be found in README.md.", True, COLOR_TEXT),
)
# and their dimension
tutorial_text_dimension = (
    tutorial_text[0].get_size(),
    tutorial_text[1].get_size(),
    tutorial_text[2].get_size(),
    tutorial_text[3].get_size(),
    tutorial_text[4].get_size(),
    tutorial_text[5].get_size(),
    tutorial_text[6].get_size(),
    tutorial_text[7].get_size(),
    tutorial_text[8].get_size(),
)

# load images used in the help page
tutorial_img = [
    image.load("Tutorial_Hit_Objects.png"),
    image.load("Tutorial_Drumroll.png"),
]

def get_time_ms() -> int:
    """Get the current time in milliseconds."""
    return perf_counter() * 1000

# easing functions (retrieved from: https://easings.net/)
def ease_out_sine(x: float) -> float:
    return sin((x * pi) / 2)

def ease_in_out_quad(x: float) -> float:
    if x < 0.5:
        return 2 * x * x
    else:
        return 1 - (-2 * x + 2) ** 2 / 2

def ease_out_back(x: float) -> float:
    C1 = 1.70158
    C3 = C1 + 1
    return 1 + C3 * (x - 1) ** 3 + C1 * (x - 1) ** 2

# fucntions used throughout the program
def dip_to_black_animation_init(init_func=None, arg=None) -> None:
    """The initlization of the dip to black animation. The page initialzation function (init_func) will be called once the dip to black anmimation has finished."""
    global dip_to_black_animation, dip_to_black_animation_start_time, dip_to_black_animation_end_page_init_function, dip_to_black_animation_end_page_init_function_argument

    dip_to_black_animation = True
    dip_to_black_animation_start_time = current_time
    dip_to_black_animation_end_page_init_function = init_func
    dip_to_black_animation_end_page_init_function_argument = arg

def dip_to_black_animation_exit() -> None:
    """The exit of the dip to black animation ends. Also setting up the next animation and calling the page intialization function."""
    global dip_to_black_animation, dip_to_black_mask_surface, page, dip_to_black_animation_end_page_init_function, dip_to_black_animation_end_page_init_function_argument

    dip_to_black_animation = False
    dip_to_black_mask_surface.set_alpha(255)

    if dip_to_black_animation_end_page_init_function != None:
        if dip_to_black_animation_end_page_init_function_argument == None:
            dip_to_black_animation_end_page_init_function()
        else:
            dip_to_black_animation_end_page_init_function(dip_to_black_animation_end_page_init_function_argument)

    dip_to_black_reversed_animation_init()

def dip_to_black_reversed_animation_init() -> None:
    """The initialization of the fade out animation. This is called after the initiazation function of a page if there is one. This way the initialization happens during a black screen, so the user won't notice the stutter of loading."""
    global dip_to_black_reversed_animation, dip_to_black_reversed_animation_start_time

    dip_to_black_reversed_animation = True
    dip_to_black_reversed_animation_start_time = get_time_ms()

def dip_to_black_reversed_animation_exit() -> None:
    """The exit of the fade out animation."""
    global dip_to_black_reversed_animation, dip_to_black_mask_surface

    dip_to_black_reversed_animation = False
    dip_to_black_mask_surface.set_alpha(0)

def find_key(key: int) -> int:
    """ A binary search to find the unicode of a key inside TYPABLE_KEYS using Pygame ID, and return the index. The returned index is -1 when the key is not found."""
    lo = 0
    hi = len(TYPABLE_KEYS) - 1
    while hi - lo > 1:
        mid = (lo+hi) // 2
        if TYPABLE_KEYS[mid][0] == key:
            return mid
        elif TYPABLE_KEYS[mid][0] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    if TYPABLE_KEYS[hi][0] == key:
        return hi
    elif TYPABLE_KEYS[lo][0] == key:
        return lo
    else:
        return -1

# functions used in the menu page
def draw_menu() -> int:
    """Draw the main menu."""
    global mouse_x, mouse_y

    mouse_clicked = False
    screen_draw_temp.fill(COLOR_MENU_BG)

    for e in event_queue:
        if e[0] == pygame.MOUSEBUTTONDOWN:
            if e[1] == 1:
                mouse_clicked = True

    # draw the game title
    screen_draw_temp.blit(game_title[0], (MENU_TITLE_CENTER_X-game_title_dimension[0][0]//2, 200-game_title_dimension[0][1]//2))
    screen_draw_temp.blit(game_title[1], (MENU_TITLE_CENTER_X-game_title_dimension[1][0]//2, 250-game_title_dimension[1][1]//2))
    screen_draw_temp.blit(game_title[2], (MENU_TITLE_CENTER_X-game_title_dimension[2][0]//2, 300-game_title_dimension[2][1]//2))

    # draw the option buttons
    play_beginner_rect = draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_FILL, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 75, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
    play_advanced_rect = draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_FILL, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 175, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
    settings_rect = draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_FILL, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 275, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
    help_rect = draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_FILL, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 375, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
    exit_rect = draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_FILL, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 475, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))

    # check for collisions for each button
    if play_beginner_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_HOVER, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 75, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        if mouse_clicked:
            dip_to_black_animation_init(song_select_init, DIFFICULTY_BEGINNER)
            return PAGE_SONG_SELECT
    elif play_advanced_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_HOVER, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 175, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        if mouse_clicked:
            dip_to_black_animation_init(song_select_init, DIFFICULTY_ADVANCED)
            return PAGE_SONG_SELECT
    elif settings_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_HOVER, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 275, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        if mouse_clicked:
            dip_to_black_animation_init(setting_init)
            return PAGE_SETTINGS
    elif help_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_HOVER, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 375, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        if mouse_clicked:
            dip_to_black_animation_init()
            return PAGE_HELP
    elif exit_rect.collidepoint(mouse_x, mouse_y):
        draw.rect(screen_draw_temp, COLOR_MENU_BUTTON_HOVER, (MENU_OPTION_CENTER_X-MENU_OPTION_WIDTH//2, 475, MENU_OPTION_WIDTH, MENU_OPTION_HEIGHT))
        if mouse_clicked:
            dip_to_black_animation_init()
            return PAGE_EXIT
    
    # draw the text on these buttons
    screen_draw_temp.blit(play_beginner_text, (MENU_OPTION_CENTER_X-play_beginner_text_width//2, 100-text_height//2, play_beginner_text_width, text_height))
    screen_draw_temp.blit(play_advanced_text, (MENU_OPTION_CENTER_X-play_advanced_text_width//2, 200-text_height//2, play_advanced_text_width, text_height))
    screen_draw_temp.blit(settings_text, (MENU_OPTION_CENTER_X-settings_text_width//2, 300-text_height//2, settings_text_width, text_height))
    screen_draw_temp.blit(help_text, (MENU_OPTION_CENTER_X-help_text_width//2, 400-text_height//2, help_text_width, text_height))
    screen_draw_temp.blit(exit_text, (MENU_OPTION_CENTER_X-exit_text_width//2, 500-text_height//2, exit_text_width, text_height))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_MENU

# functions used in the song-select page
def draw_song_screen(song_screen: Surface, song_index: int) -> None:
    """Draw the screen for one song. By drawing multiple of these, I can acheive the sliding animation."""
    song_screen.fill(song_select_bg_color)

    song_info = song_list[song_index]
    song_id = int(song_info[0])

    # load the background image
    bg = image.load("Songs/%s/bg.jpg" % (song_info[1]))
    width, height = bg.get_size()
    width = width * SONG_SELECT_IMAGE_HEIGHT // height
    height = SONG_SELECT_IMAGE_HEIGHT
    bg = transform.smoothscale(bg, (width, height))
    song_screen.blit(bg, (500-width//2, SONG_SELECT_IMAGE_CENTER_Y-height//2))

    # draw the song tile and artist
    title = FONT_SONG_TITLE.render(song_info[2], True, COLOR_TEXT)
    title_width, title_height = title.get_size()
    song_screen.blit(title, (500-title_width//2, SONG_SELECT_TITLE_CENTER_Y-title_height//2))

    artist = FONT_SONG_ARTIST.render("By %s" % (song_info[3]), True, COLOR_TEXT)
    artist_width, artist_height = artist.get_size()
    song_screen.blit(artist, (500-artist_width//2, SONG_SELECT_ARTIST_CENTER_Y-artist_height//2))

    # draw other song information
    info_width = 0  # find the width sum of the all the information to center it

    creator = FONT_SONG_INFO.render("Mapped by %s" % (song_info[4]), True, COLOR_TEXT)
    creator_width, creator_height = creator.get_size()
    info_width += creator_width

    duration = FONT_SONG_INFO.render("Duration: %s" % (song_info[8]), True, COLOR_TEXT)
    duration_width, duration_height = duration.get_size()
    info_width += duration_width

    bpm = FONT_SONG_INFO.render("BPM: %s" % (song_info[5]), True, COLOR_TEXT)
    bpm_width, bpm_height = bpm.get_size()
    info_width += bpm_width

    difficulty = FONT_SONG_INFO.render("Difficulty: %.1f" % (float(song_info[6])), True, COLOR_TEXT)
    difficulty_width, difficulty_height = difficulty.get_size()
    info_width += difficulty_width

    info_width += SONG_SELECT_INFO_SPACE * 3  # calculate the total width with spacing between each piece of information considered

    # draw all the information with spacings
    song_info_left_x = 500 - info_width//2  # the left x-coordinate of the first piece of information

    # increase song_info_left_x to use it to store and left-s-coordinate of the next piece of information
    song_screen.blit(creator, (song_info_left_x, SONG_SELECT_INFO_TOP_Y))
    song_info_left_x += creator_width + SONG_SELECT_INFO_SPACE

    song_screen.blit(duration, (song_info_left_x, SONG_SELECT_INFO_TOP_Y))
    song_info_left_x += duration_width + SONG_SELECT_INFO_SPACE

    song_screen.blit(bpm, (song_info_left_x, SONG_SELECT_INFO_TOP_Y))
    song_info_left_x += bpm_width + SONG_SELECT_INFO_SPACE

    song_screen.blit(difficulty, (song_info_left_x, SONG_SELECT_INFO_TOP_Y))

    # draw the high score and best accuracy
    score = FONT_SONG_INFO.render("High Score: %i" % (scores[song_id][0]), True, COLOR_TEXT)
    score_width, score_height = score.get_size()
    song_screen.blit(score, (SONG_SELECT_SCORE_RIGHT_X-score_width, SONG_SELECT_SCORE_TOP_Y))

    accuracy = FONT_SONG_INFO.render("Accuracy: %.2f%%" % (scores[song_id][1]), True, COLOR_TEXT)
    accuracy_width, accuracy_height = accuracy.get_size()
    song_screen.blit(accuracy, (SONG_SELECT_ACCURACY_LEFT_X, SONG_SELECT_SCORE_TOP_Y))

def song_select_music_init() -> None:
    """Intialize and play the music from the set preview point."""
    mixer.music.load("Songs/%s/audio.mp3" % (song_list[song_selected_index][1]))
    mixer.music.set_volume(song_volume)
    mixer.music.set_endevent(EVENT_PREVIEW_END)
    mixer.music.play(fade_ms=SONG_PREVIEW_FADE_IN_DURATION)
    mixer.music.set_pos(int(song_list[song_selected_index][7])/1000)

def song_select_init(difficulty: int) -> None:
    """Initialize variable for the song selet page."""
    global song_list, song_slide_animation, song_select_bg_color, song_count, song_selected_index, previous_song_screen, current_song_screen, next_song_screen

    song_list = []
    song_slide_animation = False

    # load song information file based on the difficulty the user chose
    if difficulty == DIFFICULTY_BEGINNER:
        song_list_file = open("Songs_beginner.csv", 'r', encoding="UTF-8")
        song_select_bg_color = COLOR_SONG_SELECT_BEGINNER_BG
    else:
        song_list_file = open("Songs_advanced.csv", 'r', encoding="UTF-8")
        song_select_bg_color = COLOR_SONG_SELECT_ADVANDED_BG
    song_list_file.readline()

    # create a list of song information from the file using '|' as separator
    for line in song_list_file.readlines():
        line = line.rstrip()
        song_list.append(line.split('|'))

    song_count = len(song_list)
    song_selected_index = randrange(0, song_count)

    # draw only the previous, current, and next song screen as these are the only screen that can possibly be seen during the next sliding animation
    draw_song_screen(previous_song_screen, (song_selected_index-1)%song_count)
    draw_song_screen(current_song_screen, song_selected_index)
    draw_song_screen(next_song_screen, (song_selected_index+1)%song_count)

    song_select_music_init()

    dip_to_black_reversed_animation_init()

def slide_transition_init(direction: int) -> None:
    """Initialization for the slide transition animation for song-select page."""
    global song_slide_animation, song_slide_animation_start_time, song_slide_direction

    if song_slide_animation:
        return

    mixer.music.unload()

    song_slide_animation = True
    song_slide_animation_start_time = current_time
    song_slide_direction = direction

def slide_transition_exit() -> None:
    """The exit of the slide transition animation."""
    global song_slide_animation, song_selected_index, next_song_screen, current_song_screen, next_song_screen

    song_slide_animation = False

    if song_slide_direction == SLIDE_LEFT:
        next_song_screen.blit(current_song_screen, (0, 0))
        current_song_screen.blit(previous_song_screen, (0, 0))
        song_selected_index = (song_selected_index-1) % song_count
        draw_song_screen(previous_song_screen, (song_selected_index-1)%song_count)
    else:
        previous_song_screen.blit(current_song_screen, (0, 0))
        current_song_screen.blit(next_song_screen, (0, 0))
        song_selected_index = (song_selected_index+1) % song_count
        draw_song_screen(next_song_screen, (song_selected_index+1)%song_count)

    song_select_music_init()

def draw_song_select() -> int:
    """Draw the song-select page."""
    global song_selected_index, song_list, previous_song_screen, current_song_screen, next_song_screen, song_slide_animation

    mouse_clicked = False

    for e in event_queue:
        if e[0] == pygame.MOUSEBUTTONDOWN:
            if e[1] == 1:
                mouse_clicked = True
            elif e[1] == 3:
                # exit the song-select page
                song_select_exit(True)
                dip_to_black_animation_init()
                return PAGE_MENU
            elif e[1] == 4:
                # go to the previous song if not in a sliding transition already
                if not song_slide_animation:
                    slide_transition_init(SLIDE_LEFT)
            elif e[1] == 5:
                # go to the next song if not in a sliding transition already
                if not song_slide_animation:
                    slide_transition_init(SLIDE_RIGHT)
        elif e[0] == pygame.KEYDOWN:
            if e[1] == pygame.K_ESCAPE:
                # exit the song-select page
                song_select_exit(True)
                dip_to_black_animation_init()
                return PAGE_MENU
            elif e[1] == pygame.K_RETURN:
                # start the game if not in a sliding transition
                if not song_slide_animation:
                    song_select_exit(False)
                    dip_to_black_animation_init(game_init)
                    return PAGE_GAME
            elif e[1] == pygame.K_LEFT:
                # go to the previous song if not in a sliding transition already
                if not song_slide_animation:
                    slide_transition_init(SLIDE_LEFT)
            elif e[1] == pygame.K_RIGHT:
                # go to the next song if not in a sliding transition already
                if not song_slide_animation:
                    slide_transition_init(SLIDE_RIGHT)
        elif e[0] == EVENT_PREVIEW_END:
            # wait a set amount of time before playing the preview again
            time.set_timer(EVENT_PREVIEW_WAIT_END, SONG_PREVIEW_END_WAIT, 1)
        elif e[0] == EVENT_PREVIEW_WAIT_END:
            # play the preview agin once the wait is over
            mixer.music.play(fade_ms=SONG_PREVIEW_FADE_IN_DURATION)
            mixer.music.set_pos(int(song_list[song_selected_index][7])/1000)

    # check for collision between mouse and the arrows
    if mouse_clicked:
        if left_arrow_rect.collidepoint(mouse_x, mouse_y):
            slide_transition_init(SLIDE_LEFT)
        elif right_arrow_rect.collidepoint(mouse_x, mouse_y):
            slide_transition_init(SLIDE_RIGHT)

    # draw the sliding transition animation
    if song_slide_animation:
        animation_elapsed = current_time - song_slide_animation_start_time
        if animation_elapsed > SONG_SLIDE_ANIMATION_DURATION:
            slide_transition_exit()
        else:
            animation_completion = ease_in_out_quad(animation_elapsed/SONG_SLIDE_ANIMATION_DURATION)
            if song_slide_direction == SLIDE_LEFT:
                screen_draw_temp.blit(previous_song_screen, (-SCREEN_SIZE[0]+animation_completion*SCREEN_SIZE[0], 0))
                screen_draw_temp.blit(current_song_screen, (animation_completion*SCREEN_SIZE[0], 0))
            else:
                screen_draw_temp.blit(current_song_screen, (-animation_completion*SCREEN_SIZE[0], 0))
                screen_draw_temp.blit(next_song_screen, (SCREEN_SIZE[0]-animation_completion*SCREEN_SIZE[0], 0))

    if not song_slide_animation:
        screen_draw_temp.blit(current_song_screen, (0, 0))
    
        # draw arrows and option buttons
        if left_arrow_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked:
                slide_transition_init(SLIDE_LEFT)
            else:
                top_left_coordinate = left_arrow_rect.topleft
                screen_draw_temp.blit(arrow_button_surface, top_left_coordinate)
        elif right_arrow_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked:
                slide_transition_init(SLIDE_RIGHT)
            else:
                top_left_coordinate = right_arrow_rect.topleft
                screen_draw_temp.blit(arrow_button_surface, top_left_coordinate)
        elif option_bottom_left_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked:
                song_select_exit(True)
                dip_to_black_animation_init()
                return PAGE_MENU
            top_left_coordinate = option_bottom_left_rect.topleft
            screen_draw_temp.blit(option_button_surface, top_left_coordinate)
        elif option_start_rect.collidepoint(mouse_x, mouse_y):
            if mouse_clicked:
                song_select_exit(False)
                dip_to_black_animation_init(game_init)
                return PAGE_GAME
            top_left_coordinate = option_start_rect.topleft
            screen_draw_temp.blit(option_button_surface, top_left_coordinate)

    # display the text on top of each button
    center_x, center_y = left_arrow_rect.center
    screen_draw_temp.blit(left_arrow_img, (center_x-SONG_SELECT_ARROW_IMG_SIDE_LENGTH//2, center_y-SONG_SELECT_ARROW_IMG_SIDE_LENGTH//2))

    center_x, center_y = right_arrow_rect.center
    screen_draw_temp.blit(right_arrow_img, (center_x-SONG_SELECT_ARROW_IMG_SIDE_LENGTH//2, center_y-SONG_SELECT_ARROW_IMG_SIDE_LENGTH//2))

    center_x, center_y = option_bottom_left_rect.center
    screen_draw_temp.blit(option_back_text, (center_x-option_back_text_width//2, center_y-option_back_text_height//2))

    center_x, center_y = option_start_rect.center
    screen_draw_temp.blit(option_start_text, (center_x-option_start_text_width//2, center_y-option_start_text_height//2))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_SONG_SELECT

def song_select_exit(delete: bool) -> None:
    """The exit of the song-select page."""
    global song_list

    mixer.music.unload()

    time.set_timer(EVENT_PREVIEW_WAIT_END, 0)

    # check if song_list needs to be deleted
    if delete:
        del song_list

# functions used in the game page
def game_init() -> None:
    """Initialization for the game."""
    global song, song_restartable, song_duration, combo, max_combo, score, total_accuracy, count_perfect, count_great, count_miss, count_early, count_late, total_objects, hit_objects_red, hit_objects_blue, hit_objects_drumroll, drumroll_missed, explosion_queue, song_start_time, combo_value_text, combo_value_text_width, combo_value_text_height, score_value_text, score_value_text_width, score_value_text_height, combo_animation, judgment_animation

    # load the song
    song_name = song_list[song_selected_index][1]
    song = mixer.Sound("Songs/%s/audio.mp3" % (song_name))
    song.set_volume(song_volume)
    song_duration = int(song.get_length() * 1000)

    # initalize a bunch of variables
    song_restartable = True

    combo = 0
    max_combo = 0
    score = 0
    total_accuracy = 0
    count_perfect = 0
    count_great = 0
    count_miss = 0
    count_early = 0
    count_late = 0

    total_objects = 0
    hit_objects_red = []
    hit_objects_blue = []
    hit_objects_drumroll = []
    drumroll_missed = []
    explosion_queue = []
 
    combo_animation = False
    judgment_animation = False

    # initlaize text for combo and score
    combo_value_text = FONT_COMBO_VALUE.render('0', True, COLOR_TEXT)
    combo_value_text_width, combo_value_text_height = combo_value_text.get_size()

    score_value_text = FONT_SCORE.render('0', True, COLOR_TEXT)
    score_value_text_width, score_value_text_height = score_value_text.get_size()

    # load the hit objects
    hit_objects_file = open("Songs/%s/chart.csv" % (song_name), 'r')
    for line in hit_objects_file.readlines():
        line = line.rstrip()
        total_objects += 1
        hit_object_str = line.split(',')
        hit_object = []
        for data_str in hit_object_str:
            hit_object.append(int(data_str))
        del hit_object_str
        # add offset to the hit time
        hit_object[1] += offset
        if hit_object[0] == TYPE_RED:
            hit_objects_red.append(hit_object[1])
        elif hit_object[0] == TYPE_BLUE:
            hit_objects_blue.append(hit_object[1])
        else:
            hit_object[2] += offset
            duration = hit_object[2] - hit_object[1]
            hit_objects_drumroll.append(hit_object[1:3]+[duration//DRUMROLL_PERFECT_INTERVAL, duration//DRUMROLL_GREAT_INTERVAL])  # add two additional value that stores the minimum number of hits to the drumroll to acheive a prefect or great judgment
        del hit_object
    hit_objects_file.close()

    # set a time to signal the song's playpack
    time.set_timer(EVENT_SONG_START, SONG_START_HOLD, 1)
    song_start_time = get_time_ms() + SONG_START_HOLD

def hit_judge(hit_type: int, hit_time: int) -> tuple[int, int]:
    """Determine the judgment of a hit by its timing."""
    global hit_objects_drumroll, score, score_value_text, score_value_text_width, score_value_text_height, explosion_queue

    # check if the hit hits a drumroll
    if len(hit_objects_drumroll) > 0 and hit_time >= hit_objects_drumroll[0][0]:
        if play_hitsound:
            hitsound.stop()
            hitsound.play()
        explosion_queue.append([GAME_JUDGMENT_LINE_X, randrange(GAME_DRUMROLL_CENTER_Y-GAME_DRUMROLL_EXPLOSION_RANGE, GAME_DRUMROLL_CENTER_Y+GAME_DRUMROLL_EXPLOSION_RANGE+1), hit_time])
        # decrease the counts by 1 for every hits to the drumroll
        hit_objects_drumroll[0][2] -= 1
        hit_objects_drumroll[0][3] -= 1
        score += SCORE_DRUMROLL_HIT
        score_value_text = FONT_SCORE.render(str(score), True, COLOR_TEXT)
        score_value_text_width, score_value_text_height = score_value_text.get_size()
        return JUDGMENT_NONE, SUBJUDGMENT_NONE
    
    # if not, determine the judgment
    if hit_type == TYPE_RED:
        if len(hit_objects_red) > 0:
            object_time = hit_objects_red[0]
        else:
            return JUDGMENT_NONE, SUBJUDGMENT_NONE
    else:
        if len(hit_objects_blue) > 0:
            object_time = hit_objects_blue[0]
        else:
            return JUDGMENT_NONE, SUBJUDGMENT_NONE
    if hit_time < object_time:
        diff = object_time - hit_time
        if diff <= WINDOW_MAX_PERFECT:
            return JUDGMENT_PERFECT, SUBJUDGMENT_NONE
        elif diff <= WINDOW_PERFECT:
            return JUDGMENT_PERFECT, SUBJUDGMENT_EARLY
        elif diff <= WINDOW_GREAT:
            return JUDGMENT_GREAT, SUBJUDGMENT_EARLY
        elif diff <= WINDOW_EARLY_MISS:
            return JUDGMENT_MISS, SUBJUDGMENT_EARLY
        else:
            return JUDGMENT_NONE, SUBJUDGMENT_NONE
    else:
        diff = hit_time - object_time
        if diff <= WINDOW_MAX_PERFECT:
            return JUDGMENT_PERFECT, SUBJUDGMENT_NONE
        elif diff <= WINDOW_PERFECT:
            return JUDGMENT_PERFECT, SUBJUDGMENT_LATE
        else:
            return JUDGMENT_GREAT, SUBJUDGMENT_LATE

def add_judgment(judgment: int, subjudgment: int, time_elapsed: int) -> None:
    """Initialize the judgment and combo animation. Modify combo, accuracy, scores, etc. based on the judgment."""
    global combo, max_combo, score, total_accuracy, count_perfect, count_great, count_miss, count_early, count_late, judgment_text, judgment_text_width, judgment_text_height, subjudgment_text, subjudgment_text_width, subjudgment_text_height, judgment_animation, judgment_animation_start_time, combo_value_text, combo_value_text_width, combo_value_text_height, combo_animation, combo_animation_start_time, combo_animation_start_combo, score_value_text, score_value_text_width, score_value_text_height

    if judgment == JUDGMENT_PERFECT:
        judgment_text = FONT_JUDGMENT.render("PERFECT", True, COLOR_JUDGMENT_PERFECT)
        score += int(SCORE_PERFECT*(1+SCORE_BONUS_STEP*(combo//SCORE_BONUS_COMBO_STEP)))
        count_perfect += 1
        total_accuracy += ACCURACY_PERFECT
        combo += 1
        combo_animation = False

    elif judgment == JUDGMENT_GREAT:
        judgment_text = FONT_JUDGMENT.render("GREAT", True, COLOR_JUDGMENT_GREAT)
        score += int(SCORE_GREAT*(1+SCORE_BONUS_STEP*(combo//SCORE_BONUS_COMBO_STEP)))
        count_great += 1
        total_accuracy += ACCURACY_GREAT
        combo += 1
        combo_animation = False
    else:
        judgment_text = FONT_JUDGMENT.render("Miss", True, COLOR_JUDGMENT_MISS)
        count_miss += 1
        if combo != 0:
            combo_animation = True
            combo_animation_start_time = time_elapsed
            combo_animation_start_combo = combo
            if combo > max_combo:
                max_combo = combo
            combo = 0

    judgment_text_width, judgment_text_height = judgment_text.get_size()
    
    if subjudgment == SUBJUDGMENT_NONE:
        subjudgment_text = FONT_SUBJUDGMENT.render("", True, COLOR_WHITE)
    elif subjudgment == SUBJUDGMENT_EARLY:
        subjudgment_text = FONT_SUBJUDGMENT.render("EARLY", True, COLOR_SUBJUDGMENT_EARLY)
        if judgment != JUDGMENT_MISS:
            count_early += 1
    else:
        subjudgment_text = FONT_SUBJUDGMENT.render("LATE", True, COLOR_SUBJUDGMENT_LATE)
        if judgment != JUDGMENT_MISS:
            count_late += 1

    subjudgment_text_width, subjudgment_text_height = subjudgment_text.get_size()

    combo_value_text = FONT_COMBO_VALUE.render(str(combo), True, COLOR_TEXT)
    combo_value_text_width, combo_value_text_height = combo_value_text.get_size()

    score_value_text = FONT_SCORE.render(str(score), True, COLOR_TEXT)
    score_value_text_width, score_value_text_height = score_value_text.get_size()

    judgment_animation = True
    judgment_animation_start_time = time_elapsed

def draw_game() -> int:
    """Draw the game page."""
    global song, song_restartable, song_start_time, combo_animation, judgment_animation, hit_objects_red, hit_objects_blue, hit_objects_drumroll, drumroll_missed

    song_time_elapsed = current_time - song_start_time

    for e in event_queue:
        if e[0] == pygame.KEYDOWN:
            if e[1] == pygame.K_ESCAPE:
                # exit the game
                game_exit()
                dip_to_black_animation_init(song_select_music_init)
                return PAGE_SONG_SELECT
            elif e[1] == pygame.K_BACKQUOTE:
                # restart the game
                if song_restartable:
                    game_exit()
                    dip_to_black_animation_init(game_init)
                return PAGE_GAME
            else:
                key_index = find_key(e[1])
                if key_index == -1:
                    continue
                key_pressed = TYPABLE_KEYS[key_index][1]
                if key_pressed in keys[0:2]:
                    judgment, subjudgment = hit_judge(TYPE_RED, song_time_elapsed)
                    if judgment != JUDGMENT_NONE:
                        if judgment != JUDGMENT_MISS or subjudgment != SUBJUDGMENT_EARLY:
                            if play_hitsound:
                                hitsound.stop()
                                hitsound.play()
                            explosion_queue.append([int((hit_objects_red[0]-song_time_elapsed)*note_speed)+GAME_JUDGMENT_LINE_X, GAME_RED_CENTER_Y, song_time_elapsed])
                        del hit_objects_red[0]
                        add_judgment(judgment, subjudgment, song_time_elapsed)
                elif key_pressed in keys[2:4]:
                    judgment, subjudgment = hit_judge(TYPE_BLUE, song_time_elapsed)
                    if judgment != JUDGMENT_NONE:
                        if judgment != JUDGMENT_MISS or subjudgment != SUBJUDGMENT_EARLY:
                            if play_hitsound:
                                hitsound.stop()
                                hitsound.play()
                            explosion_queue.append([int((hit_objects_blue[0]-song_time_elapsed)*note_speed)+GAME_JUDGMENT_LINE_X, GAME_BLUE_CENTER_Y, song_time_elapsed])
                        del hit_objects_blue[0]
                        add_judgment(judgment, subjudgment, song_time_elapsed)
        elif e[0] == EVENT_SONG_START:
            song.play()
            time.set_timer(EVENT_SONG_END, song_duration, 1)
            song_start_time = current_time
        elif e[0] == EVENT_SONG_END:
            song_restartable = False  # prevent the user from restarting the song since they finished playing the song already
            time.set_timer(EVENT_RESULT_SCREEN, SONG_END_HOLD, 1)
        elif e[0] == EVENT_RESULT_SCREEN:
            game_exit()
            dip_to_black_animation_init(result_init)
            return PAGE_RESULT
    
    screen_draw_temp.fill(COLOR_BLACK)

    # draw the 2 guide circles
    draw.circle(screen_draw_temp, COLOR_HIT_CIRCLE, (GAME_JUDGMENT_LINE_X, GAME_RED_CENTER_Y), GAME_GUIDE_CIRCLE_RADIUS, 3)
    draw.circle(screen_draw_temp, COLOR_HIT_CIRCLE, (GAME_JUDGMENT_LINE_X, GAME_BLUE_CENTER_Y), GAME_GUIDE_CIRCLE_RADIUS, 3)

    # draw the progress bar on top of the screen
    draw.rect(screen_draw_temp, COLOR_SONG_PROGRESS_BAR, (0, 0, song_time_elapsed*SCREEN_SIZE[0]/song_duration, GAME_PROGRESS_BAR_HEIGHT))

    # draw the word "combo"
    screen_draw_temp.blit(combo_text, (500-combo_text_width//2, GAME_COMBO_TEXT_CENTER_Y-combo_text_height//2))

    # draw the combo value
    if combo_animation:
        animation_elapsed = song_time_elapsed - combo_animation_start_time
        if animation_elapsed*COMBO_BREAK_ANIMATION_SPEED >= combo_animation_start_combo:
            combo_animation = False
        else:
            # determine the combo value based on how long the animation has elapsed
            combo_value_display = FONT_COMBO_VALUE.render(str(combo_animation_start_combo-int(animation_elapsed*COMBO_BREAK_ANIMATION_SPEED)), True, COLOR_TEXT)
            combo_value_display_width, combo_value_display_height = combo_value_display.get_size()
            screen_draw_temp.blit(combo_value_display, (500-combo_value_display_width//2, GAME_COMBO_VALUE_CENTER_Y-combo_value_display_height//2))
    if not combo_animation:
        screen_draw_temp.blit(combo_value_text, (500-combo_value_text_width//2, GAME_COMBO_VALUE_CENTER_Y-combo_value_text_height//2))

    # draw judgment if any
    if judgment_animation:
        animation_elapsed = song_time_elapsed - judgment_animation_start_time
        if animation_elapsed > JUDGMENT_DISPLAY_DURATION:
            judgment_animation = False
        else:
            if animation_elapsed <= JUDGMENT_ANIMATION_DURATION:
                # scale the judgment text based on ease_out_back() and how long the animation has elapsed
                scale = ease_out_back(animation_elapsed/JUDGMENT_ANIMATION_DURATION)
                judgment_display_width = int(judgment_text_width * scale)
                judgment_display_height = int(judgment_text_height * scale)
                judgment_display = transform.smoothscale(judgment_text, (judgment_display_width, judgment_display_height))
                screen_draw_temp.blit(judgment_display, (500-judgment_display_width//2, GAME_JUDGMENT_CENTER_Y-judgment_display_height))

                subjudgment_display_width = int(subjudgment_text_width * scale)
                subjudgment_display_height = int(subjudgment_text_height * scale)
                subjudgment_display = transform.smoothscale(subjudgment_text, (subjudgment_display_width, subjudgment_display_height))
                screen_draw_temp.blit(subjudgment_display, (500-subjudgment_display_width//2, GAME_JUDGMENT_CENTER_Y))
            else:
                screen_draw_temp.blit(judgment_text, (500-judgment_text_width//2, GAME_JUDGMENT_CENTER_Y-judgment_text_height))
                screen_draw_temp.blit(subjudgment_text, (500-subjudgment_text_width//2, GAME_JUDGMENT_CENTER_Y))

    # draw the score text
    screen_draw_temp.blit(score_text, (SCREEN_SIZE[0]-score_text_width-SPACING-score_value_text_width-GAME_SCORE_TOP_RIGHT_MARGIN, GAME_SCORE_TOP_RIGHT_MARGIN))
    screen_draw_temp.blit(score_value_text, (SCREEN_SIZE[0]-score_value_text_width-GAME_SCORE_TOP_RIGHT_MARGIN, GAME_SCORE_TOP_RIGHT_MARGIN))

    # delete any drumroll object that passed the view window
    while len(drumroll_missed) > 0 and (drumroll_missed[0][1]-song_time_elapsed)*note_speed+GAME_JUDGMENT_LINE_X < 0:
        del drumroll_missed[0]

    # determine judgments of drumroll objects that passed their hit window
    while len(hit_objects_drumroll) > 0 and song_time_elapsed > hit_objects_drumroll[0][1]:
        # check if the values are less than 0; if yes, it means the user acheived the corresponding judgment
        if hit_objects_drumroll[0][2] <= 0:
            add_judgment(JUDGMENT_PERFECT, SUBJUDGMENT_NONE, song_time_elapsed)
        elif hit_objects_drumroll[0][3] <= 0:
            add_judgment(JUDGMENT_GREAT, SUBJUDGMENT_NONE, song_time_elapsed)
        else:
            add_judgment(JUDGMENT_MISS, SUBJUDGMENT_NONE, song_time_elapsed)
            drumroll_missed.append(hit_objects_drumroll[0])

        del hit_objects_drumroll[0]

    # delete any red hit object that passed its hit window
    while len(hit_objects_red) > 0 and song_time_elapsed-hit_objects_red[0] > WINDOW_GREAT:
        add_judgment(JUDGMENT_MISS, SUBJUDGMENT_LATE, song_time_elapsed)
        del hit_objects_red[0]

    # delete any blue hit object that passed its hit window
    while len(hit_objects_blue) > 0 and song_time_elapsed-hit_objects_blue[0] > WINDOW_GREAT:
        add_judgment(JUDGMENT_MISS, SUBJUDGMENT_LATE, song_time_elapsed)
        del hit_objects_blue[0]

    # draw any drumroll the user missed but still should be visible in the view window
    for hit_object in drumroll_missed:
        screen_draw_temp.blit(drumroll_img, ((hit_object[1]-song_time_elapsed)*note_speed+GAME_JUDGMENT_LINE_X-drumroll_img_width, GAME_DRUMROLL_CENTER_Y-drumroll_img_height//2))

    # draw any drumroll that is visible and hasn't pass its hit window yet
    for hit_object in hit_objects_drumroll:
        if song_time_elapsed >= hit_object[0]:
            screen_draw_temp.blit(drumroll_img, (GAME_JUDGMENT_LINE_X-(song_time_elapsed-hit_object[0])*drumroll_img_width/(hit_object[1]-hit_object[0]), GAME_DRUMROLL_CENTER_Y-drumroll_img_height//2))
        else:
            x = int((hit_object[0]-song_time_elapsed)*note_speed) + GAME_JUDGMENT_LINE_X
            if x > SCREEN_SIZE[0]:
                break
            screen_draw_temp.blit(drumroll_img, (x, GAME_DRUMROLL_CENTER_Y-drumroll_img_height//2))

    # draw any red hit object that is visible and hasn't pass its hit window yet
    for hit_object in hit_objects_red:
        x = int((hit_object-song_time_elapsed)*note_speed) + GAME_JUDGMENT_LINE_X - red_img_width//2
        if x > SCREEN_SIZE[0]:
            break
        screen_draw_temp.blit(red_img, (x, GAME_RED_CENTER_Y-red_img_height//2))

    # draw any blue hit object that is visible and hasn't pass its hit window yet
    for hit_object in hit_objects_blue:
        x = int((hit_object-song_time_elapsed)*note_speed) + GAME_JUDGMENT_LINE_X - blue_img_width//2
        if x > SCREEN_SIZE[0]:
            break
        screen_draw_temp.blit(blue_img, (x, GAME_BLUE_CENTER_Y-blue_img_height//2))

    # delete any explosion object that passed its animation period
    while len(explosion_queue) > 0 and int((song_time_elapsed-explosion_queue[0][2])*EXPLOSION_ANIMATION_SPEED) >= EXPLOSION_IMG_COUNT:
        del explosion_queue[0]
    
    # draw the explosion effect
    for explosion in explosion_queue:
        screen_draw_temp.blit(explosion_img[int((song_time_elapsed-explosion[2])*EXPLOSION_ANIMATION_SPEED)], (explosion[0]-explosion_img_width//2, explosion[1]-explosion_img_height//2))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_GAME

def game_exit() -> None:
    """"""
    global song, max_combo, hit_objects_red, hit_objects_blue, hit_objects_drumroll, drumroll_missed, explosion_queue

    song.stop()

    if combo > max_combo:
        max_combo = combo

    # disable timer
    time.set_timer(EVENT_SONG_START, 0)
    time.set_timer(EVENT_SONG_END, 0)
    time.set_timer(EVENT_RESULT_SCREEN, 0)

    del hit_objects_red
    del hit_objects_blue
    del hit_objects_drumroll
    del drumroll_missed
    del explosion_queue

# functions used in the result page
def save_scores() -> None:
    SONGS_CSV_HEAD = "Score,Accuracy"

    file = open("Scores.csv", 'w')

    file.write(SONGS_CSV_HEAD+'\n')

    for score, accuracy in scores:
        file.write("%i,%f\n" % (score, accuracy))

    file.close()

def result_init() -> None:
    global scores, new_best, song_list, result_bg, result_bg_width, result_bg_height, result_song_title_text, result_song_title_text_width, result_song_title_text_height, result_song_artist_text, result_song_artist_text_width, result_song_artist_text_height, result_score_value_text, result_score_value_text_width, result_score_value_text_height, result_max_combo_value_text, result_max_combo_value_text_width, result_max_combo_value_text_height, result_accuracy_value_text, result_accuracy_value_text_width, result_accuracy_value_text_height, result_perfect_count_text, result_perfect_count_text_width, result_perfect_count_text_height, result_great_count_text, result_great_count_text_width, result_great_count_text_height, result_miss_count_text, result_miss_count_text_width, result_miss_count_text_height, result_early_count_text, result_early_count_text_width, result_early_count_text_height, result_late_count_text, result_late_count_text_width, result_late_count_text_height

    update = False
    new_best = False

    song_info = song_list[song_selected_index]
    song_id = int(song_info[0])

    if score > scores[song_id][0]:
        scores[song_id][0] = score
        update = True
        new_best = True
    accuracy = total_accuracy / total_objects
    if accuracy > scores[song_id][1]:
        scores[song_id][1] = accuracy
        update = True
    
    if update:
        save_scores()
        draw_song_screen(current_song_screen, song_selected_index)

    result_bg = image.load("Songs/%s/bg.jpg" % (song_info[1])).convert()
    result_bg_width, result_bg_height = result_bg.get_size()
    result_bg_width = result_bg_width * SCREEN_SIZE[1] // result_bg_height
    result_bg_height = SCREEN_SIZE[1]
    result_bg = transform.smoothscale(result_bg, (result_bg_width, result_bg_height))

    result_song_title_text = FONT_RESULT_TITLE.render(song_info[2], True, COLOR_TEXT)
    result_song_title_text_width, result_song_title_text_height = result_song_title_text.get_size()

    result_song_artist_text = FONT_RESULT_ARTIST.render(song_info[3], True, COLOR_TEXT)
    result_song_artist_text_width, result_song_artist_text_height = result_song_artist_text.get_size()

    result_score_value_text = FONT_RESULT_VALUE.render(str(score), True, COLOR_TEXT)
    result_score_value_text_width, result_score_value_text_height = result_score_value_text.get_size()

    result_max_combo_value_text = FONT_RESULT_VALUE.render(str(max_combo), True, COLOR_TEXT)
    result_max_combo_value_text_width, result_max_combo_value_text_height = result_max_combo_value_text.get_size()

    result_accuracy_value_text = FONT_RESULT_VALUE.render("%.2f%%" % (accuracy), True, COLOR_TEXT)
    result_accuracy_value_text_width, result_accuracy_value_text_height = result_accuracy_value_text.get_size()

    result_perfect_count_text = FONT_RESULT_VALUE.render(str(count_perfect), True, COLOR_TEXT)
    result_perfect_count_text_width, result_perfect_count_text_height = result_perfect_count_text.get_size()

    result_great_count_text = FONT_RESULT_VALUE.render(str(count_great), True, COLOR_TEXT)
    result_great_count_text_width, result_great_count_text_height = result_great_count_text.get_size()

    result_miss_count_text = FONT_RESULT_VALUE.render(str(count_miss), True, COLOR_TEXT)
    result_miss_count_text_width, result_miss_count_text_height = result_miss_count_text.get_size()

    result_early_count_text = FONT_RESULT_VALUE.render(str(count_early), True, COLOR_TEXT)
    result_early_count_text_width, result_early_count_text_height = result_early_count_text.get_size()

    result_late_count_text = FONT_RESULT_VALUE.render(str(count_late), True, COLOR_TEXT)
    result_late_count_text_width, result_late_count_text_height = result_late_count_text.get_size()

def draw_result() -> int:
    global song_list

    mouse_clicked = False

    screen_draw_temp.fill(COLOR_BLACK)

    for e in event_queue:
        if e[0] == pygame.MOUSEBUTTONDOWN:
            if e[1] == 1:
                mouse_clicked = True
            elif e[1] == 3:
                dip_to_black_animation_init(song_select_music_init)
                return PAGE_SONG_SELECT
        elif e[0] == pygame.KEYDOWN:
            if e[1] == pygame.K_ESCAPE or e[1] == pygame.K_RETURN:
                dip_to_black_animation_init(song_select_music_init)
                return PAGE_SONG_SELECT
            elif e[1] == pygame.K_BACKQUOTE:
                dip_to_black_animation_init(game_init)
                return PAGE_GAME

    screen_draw_temp.blit(result_bg, (500-result_bg_width//2, 0))
    screen_draw_temp.blit(result_bg_mask_surface, (0, 0))

    screen_draw_temp.blit(result_song_title_text, (500-result_song_title_text_width//2, RESULT_SONG_TITLE_TOP_Y))
    screen_draw_temp.blit(result_song_artist_text, (500-result_song_artist_text_width//2, RESULT_SONG_ARTIST_TOP_Y))

    total_score_width = result_score_text_width + SPACING + result_score_value_text_width
    screen_draw_temp.blit(result_score_text, (500-total_score_width//2, RESULT_SCORE_CENTER_Y-score_text_height//2))
    screen_draw_temp.blit(result_score_value_text, (500-total_score_width//2+result_score_text_width+SPACING, RESULT_SCORE_CENTER_Y-score_text_height//2))
    if new_best:
        screen_draw_temp.blit(result_new_best_text, (RESULT_NEW_BEST_LEFT_X, RESULT_SCORE_CENTER_Y-result_new_best_text_height//2))

    screen_draw_temp.blit(result_max_combo_text, (RESULT_MAX_COMBO_LEFT_X, RESULT_COMBO_ACCURACY_TOP_Y))
    screen_draw_temp.blit(result_max_combo_value_text, (RESULT_MAX_COMBO_LEFT_X+result_max_combo_text_width+SPACING, RESULT_COMBO_ACCURACY_TOP_Y))
    screen_draw_temp.blit(result_accuracy_text, (RESULT_ACCURACY_LEFT_X, RESULT_COMBO_ACCURACY_TOP_Y))
    screen_draw_temp.blit(result_accuracy_value_text, (RESULT_ACCURACY_LEFT_X+result_accuracy_text_width+SPACING, RESULT_COMBO_ACCURACY_TOP_Y))

    screen_draw_temp.blit(result_perfect_text, (RESULT_FILED_LEFT_X, 300))
    screen_draw_temp.blit(result_great_text, (RESULT_FILED_LEFT_X, 340))
    screen_draw_temp.blit(result_miss_text, (RESULT_FILED_LEFT_X, 380))
    screen_draw_temp.blit(result_early_text, (RESULT_FILED_LEFT_X, 420))
    screen_draw_temp.blit(result_late_text, (RESULT_FILED_LEFT_X, 460))

    screen_draw_temp.blit(result_perfect_count_text, (RESULT_VALUE_RIGHT_X-result_perfect_count_text_width, 300))
    screen_draw_temp.blit(result_great_count_text, (RESULT_VALUE_RIGHT_X-result_great_count_text_width, 340))
    screen_draw_temp.blit(result_miss_count_text, (RESULT_VALUE_RIGHT_X-result_miss_count_text_width, 380))
    screen_draw_temp.blit(result_early_count_text, (RESULT_VALUE_RIGHT_X-result_early_count_text_width, 420))
    screen_draw_temp.blit(result_late_count_text, (RESULT_VALUE_RIGHT_X-result_late_count_text_width, 460))

    if option_bottom_left_rect.collidepoint(mouse_x, mouse_y):
        if mouse_clicked:
            dip_to_black_animation_init(game_init)
            return PAGE_GAME
        top_left_coordinate = option_bottom_left_rect.topleft
        screen_draw_temp.blit(option_button_surface, top_left_coordinate)
    elif option_bottom_right_rect.collidepoint(mouse_x, mouse_y):
        if mouse_clicked:
            dip_to_black_animation_init(song_select_music_init)
            return PAGE_SONG_SELECT
        top_left_coordinate = option_bottom_right_rect.topleft
        screen_draw_temp.blit(option_button_surface, top_left_coordinate)

    center_x, center_y = option_bottom_left_rect.center
    screen_draw_temp.blit(option_retry_text, (center_x-option_retry_text_width//2, center_y-option_retry_text_height//2))

    center_x, center_y = option_bottom_right_rect.center
    screen_draw_temp.blit(option_continue_text, (center_x-option_continue_text_width//2, center_y-option_continue_text_height//2))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_RESULT

# functions used in the setting page
def setting_init() -> None:
    global volume_thumb_center_x, offset_thumb_center_x, volume_slider_dragging, offset_slider_dragging, keybind_change

    volume_thumb_center_x = song_volume_percent * SETTING_SLIDER_LENGTH // 100 + SETTING_SLIDER_LEFT_X
    offset_thumb_center_x = (offset+300) * SETTING_SLIDER_LENGTH // 600 + SETTING_SLIDER_LEFT_X

    volume_slider_dragging = False
    offset_slider_dragging = False
    keybind_change = False

    dip_to_black_reversed_animation_init()

def save_settings() -> None:
    CSV_HEAD = "Volume,Offset,Speed,Hitsound,FPS,KeyR1,KeyR2,KeyB1,KeyB2"

    file = open("Settings.csv", 'w')

    file.write(CSV_HEAD+'\n')

    file.write("%i,%i,%i,%i,%i,%s,%s,%s,%s\n" % ((song_volume_percent, offset, note_speed_int, play_hitsound, display_fps) + tuple(keys)))
    file.close()

def volume_slider_exit() -> None:
    global volume_slider_dragging, volume_thumb_center_x

    if not volume_slider_dragging:
        return

    volume_slider_dragging = False
    volume_thumb_center_x = song_volume_percent * SETTING_SLIDER_LENGTH // 100 + SETTING_SLIDER_LEFT_X
    
    save_settings()

def offset_slider_exit() -> None:
    global offset_slider_dragging, offset_thumb_center_x

    if not offset_slider_dragging:
        return

    offset_slider_dragging = False
    offset_thumb_center_x = (offset+300) * SETTING_SLIDER_LENGTH // 600 + SETTING_SLIDER_LEFT_X

    save_settings()

def keybind_change_exit(new_key: str = "") -> None:
    global keybind_change, key_index, keys

    if not keybind_change:
        return
    
    keybind_change = False
    keys[key_index] = new_key

    save_settings()

def draw_setting() -> int:
    global song_volume_percent, offset, note_speed_int, play_hitsound, display_fps, volume_slider_dragging, volume_thumb_center_x, offset_slider_dragging, offset_thumb_center_x, keybind_change, key_index, setting_volume_value_text, setting_volume_value_text_width, setting_volume_value_text_height, setting_offset_value_text, setting_offset_value_text_width, setting_offset_value_text_height, setting_speed_value_text, setting_speed_value_text_width, setting_speed_value_text_height

    mouse_clicked = False
    
    for e in event_queue:
        if e[0] == pygame.MOUSEBUTTONDOWN:
            if e[1] == 1:
                mouse_clicked = True
            elif e[1] == 3:
                if keybind_change:
                    keybind_change = False
                else:
                    dip_to_black_animation_init()
                    setting_exit()
                    return PAGE_MENU
        elif e[0] == pygame.MOUSEBUTTONUP:
            if e[1] == 1:
                volume_slider_exit()
                offset_slider_exit()
        elif e[0] == pygame.KEYDOWN:
            if e[1] == pygame.K_ESCAPE:
                if keybind_change:
                    keybind_change = False
                else:
                    dip_to_black_animation_init()
                    setting_exit()
                    return PAGE_MENU
            elif keybind_change:
                index = find_key(e[1])
                if index != -1:
                    keybind_change_exit(TYPABLE_KEYS[index][1])

    screen_draw_temp.fill(COLOR_MENU_BG)

    if volume_slider_dragging:
        volume_thumb_center_x = mouse_x
    elif offset_slider_dragging:
        offset_thumb_center_x = mouse_x

    if offset_thumb_center_x < SETTING_SLIDER_LEFT_X:
        offset_thumb_center_x = SETTING_SLIDER_LEFT_X
    elif offset_thumb_center_x > SETTING_SLIDER_LEFT_X+SETTING_SLIDER_LENGTH:
        offset_thumb_center_x = SETTING_SLIDER_LEFT_X + SETTING_SLIDER_LENGTH

    if volume_thumb_center_x < SETTING_SLIDER_LEFT_X:
        volume_thumb_center_x = SETTING_SLIDER_LEFT_X
    elif volume_thumb_center_x > SETTING_SLIDER_LEFT_X+SETTING_SLIDER_LENGTH:
        volume_thumb_center_x = SETTING_SLIDER_LEFT_X + SETTING_SLIDER_LENGTH

    song_volume_percent = round((volume_thumb_center_x-SETTING_SLIDER_LEFT_X) * 100 / SETTING_SLIDER_LENGTH)
    offset = round((offset_thumb_center_x-SETTING_SLIDER_LEFT_X)*600/SETTING_SLIDER_LENGTH) - 300

    setting_volume_value_text = FONT_SETTING_VALUE.render("%i%%" % song_volume_percent, True, COLOR_TEXT)
    setting_volume_value_text_width, setting_volume_value_text_height = setting_volume_value_text.get_size()

    setting_offset_value_text = FONT_SETTING_VALUE.render("%ims" % (offset), True, COLOR_TEXT)
    setting_offset_value_text_width, setting_offset_value_text_height = setting_offset_value_text.get_size()

    setting_speed_value_text = FONT_SETTING_VALUE.render(str(note_speed_int), True, COLOR_TEXT)
    setting_speed_value_text_width, setting_speed_value_text_height = setting_speed_value_text.get_size()

    R1_key = FONT_SETTING_VALUE.render(keys[0].upper(), True, COLOR_TEXT)
    R1_key_width, R1_key_height = R1_key.get_size()
    R2_key = FONT_SETTING_VALUE.render(keys[1].upper(), True, COLOR_TEXT)
    R2_key_width, R2_key_height = R2_key.get_size()
    B1_key = FONT_SETTING_VALUE.render(keys[2].upper(), True, COLOR_TEXT)
    B1_key_width, B1_key_height = B1_key.get_size()
    B2_key = FONT_SETTING_VALUE.render(keys[3].upper(), True, COLOR_TEXT)
    B2_key_width, B2_key_height = B2_key.get_size()

    if option_bottom_left_rect.collidepoint(mouse_x, mouse_y):
        if mouse_clicked:
            dip_to_black_animation_init()
            setting_exit()
            return PAGE_MENU
        top_left_coordinate = option_bottom_left_rect.topleft
        screen_draw_temp.blit(option_button_surface, top_left_coordinate)

    center_x, center_y = option_bottom_left_rect.center
    screen_draw_temp.blit(option_back_text, (center_x-option_back_text_width//2, center_y-option_back_text_height//2))
    screen_draw_temp.blit(setting_volume_text, (500-setting_volume_text_width//2, SETTING_VOLUME_TEXT_CENTER_Y-setting_volume_text_height//2))
    screen_draw_temp.blit(setting_volume_value_text, (500-setting_volume_value_text_width//2, SETTING_VOLUME_VALUE_CENTER_Y-setting_volume_value_text_height//2))

    draw.line(screen_draw_temp, COLOR_SLIDER, (SETTING_SLIDER_LEFT_X, SETTING_VOLUME_BAR_CENTER_Y), (SETTING_SLIDER_LEFT_X+SETTING_SLIDER_LENGTH, SETTING_VOLUME_BAR_CENTER_Y), SETTING_SLIDER_THICKNESS)
    draw.line(screen_draw_temp, COLOR_SLIDER_FILL, (SETTING_SLIDER_LEFT_X, SETTING_VOLUME_BAR_CENTER_Y), (volume_thumb_center_x, SETTING_VOLUME_BAR_CENTER_Y), SETTING_SLIDER_THICKNESS)
    draw.circle(screen_draw_temp, COLOR_SLIDER, (volume_thumb_center_x, SETTING_VOLUME_BAR_CENTER_Y), SETTING_SLIDER_THUMB_RADIUS)
    draw.circle(screen_draw_temp, COLOR_SLIDER_THUMB_STROKE, (volume_thumb_center_x, SETTING_VOLUME_BAR_CENTER_Y), SETTING_SLIDER_THUMB_RADIUS, SETTING_SLIDER_THUMB_STROKE_WIDTH)

    screen_draw_temp.blit(setting_offset_text, (500-setting_offset_text_width//2, SETTING_OFFSET_TEXT_CENTER_Y-setting_offset_text_height//2))
    screen_draw_temp.blit(setting_offset_value_text, (500-setting_offset_value_text_width//2, SETTING_OFFSET_VALUE_CENTER_Y-setting_offset_value_text_height//2))
    screen_draw_temp.blit(setting_plus_text, (500+setting_offset_value_text_width//2+SPACING, SETTING_OFFSET_VALUE_CENTER_Y-setting_plus_text_height//2))
    screen_draw_temp.blit(setting_minus_text, (500-setting_offset_value_text_width//2-SPACING-setting_minus_text_width, SETTING_OFFSET_VALUE_CENTER_Y-setting_minus_text_height//2))

    setting_offset_plus_rect = Rect(500+setting_offset_value_text_width//2+SPACING, SETTING_OFFSET_VALUE_CENTER_Y-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH//2, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH)
    setting_offset_minus_rect = Rect(500-setting_offset_value_text_width//2-SPACING-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_OFFSET_VALUE_CENTER_Y-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH//2, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH)

    draw.line(screen_draw_temp, COLOR_SLIDER, (SETTING_SLIDER_LEFT_X, SETTING_OFFSET_BAR_CENTER_Y), (SETTING_SLIDER_LEFT_X+SETTING_SLIDER_LENGTH, SETTING_OFFSET_BAR_CENTER_Y), SETTING_SLIDER_THICKNESS)
    draw.line(screen_draw_temp, COLOR_SLIDER_FILL, (SETTING_SLIDER_LEFT_X, SETTING_OFFSET_BAR_CENTER_Y), (offset_thumb_center_x, SETTING_OFFSET_BAR_CENTER_Y), SETTING_SLIDER_THICKNESS)
    draw.circle(screen_draw_temp, COLOR_SLIDER, (offset_thumb_center_x, SETTING_OFFSET_BAR_CENTER_Y), SETTING_SLIDER_THUMB_RADIUS)
    draw.circle(screen_draw_temp, COLOR_SLIDER_THUMB_STROKE, (offset_thumb_center_x, SETTING_OFFSET_BAR_CENTER_Y), SETTING_SLIDER_THUMB_RADIUS, SETTING_SLIDER_THUMB_STROKE_WIDTH)

    screen_draw_temp.blit(setting_speed_text, (500-setting_speed_text_width//2, SETTING_SPEED_TEXT_CENTER_Y-setting_speed_text_height//2))
    screen_draw_temp.blit(setting_speed_value_text, (500-setting_speed_value_text_width//2, SETTING_SPEED_VALUE_CENTER_Y-setting_speed_value_text_height//2))
    screen_draw_temp.blit(setting_plus_text, (500+setting_speed_value_text_width//2+SPACING, SETTING_SPEED_VALUE_CENTER_Y-setting_plus_text_height//2))
    screen_draw_temp.blit(setting_minus_text, (500-setting_speed_value_text_width//2-SPACING-setting_minus_text_width, SETTING_SPEED_VALUE_CENTER_Y-setting_minus_text_height//2))

    setting_speed_plus_rect = Rect(500+setting_speed_value_text_width//2+SPACING, SETTING_SPEED_VALUE_CENTER_Y-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH//2, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH)
    setting_speed_minus_rect = Rect(500-setting_speed_value_text_width//2-SPACING-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_SPEED_VALUE_CENTER_Y-SETTING_PLUS_MINUS_RECT_SIDE_LENGTH//2, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH, SETTING_PLUS_MINUS_RECT_SIDE_LENGTH)

    if play_hitsound:
        draw.circle(screen_draw_temp, COLOR_CHECKBOX_FILL, (SETTING_HITSOUND_LEFT_X, SETTING_TOGGLE_CENTER_Y), SETTING_CHECKBOX_RADIUS)
    draw.circle(screen_draw_temp, COLOR_CHECKBOX_STROKE, (SETTING_HITSOUND_LEFT_X, SETTING_TOGGLE_CENTER_Y), SETTING_CHECKBOX_RADIUS, SETTING_CHECKBOX_STROKE_WIDTH)
    screen_draw_temp.blit(setting_hitsound_text, (SETTING_HITSOUND_LEFT_X+SPACING, SETTING_TOGGLE_CENTER_Y-setting_hitsound_text_height//2))

    if display_fps:
        draw.circle(screen_draw_temp, COLOR_CHECKBOX_FILL, (SETTING_FPS_LEFT_X, SETTING_TOGGLE_CENTER_Y), SETTING_CHECKBOX_RADIUS)
    draw.circle(screen_draw_temp, COLOR_CHECKBOX_STROKE, (SETTING_FPS_LEFT_X, SETTING_TOGGLE_CENTER_Y), SETTING_CHECKBOX_RADIUS, SETTING_CHECKBOX_STROKE_WIDTH)
    screen_draw_temp.blit(setting_fps_text, (SETTING_FPS_LEFT_X+SPACING, SETTING_TOGGLE_CENTER_Y-setting_fps_text_height//2))

    screen_draw_temp.blit(setting_keybind_text, (500-setting_keybind_text_width//2, SETTING_KEYBIND_TEXT_CENTER_Y-setting_keybind_text_height//2))

    left_x = SETTING_KEY_RECT_LEFT_X

    R1_rect = draw.rect(screen_draw_temp, COLOR_LANE_RED, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH), SETTING_KEY_RECT_STROKE_WIDTH)
    screen_draw_temp.blit(R1_key, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-R1_key_width//2, SETTING_KEY_RECT_TOP_Y+SETTING_KEY_RECT_SIDE_LENGTH//2-R1_key_height//2))
    screen_draw_temp.blit(setting_R1_text, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-setting_R1_text_width//2, SETTING_KEY_RECT_TOP_Y-setting_R1_text_height))
    left_x += SETTING_KEY_RECT_SIDE_LENGTH

    R2_rect = draw.rect(screen_draw_temp, COLOR_LANE_RED, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH), SETTING_KEY_RECT_STROKE_WIDTH)
    screen_draw_temp.blit(R2_key, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-R2_key_width//2, SETTING_KEY_RECT_TOP_Y+SETTING_KEY_RECT_SIDE_LENGTH//2-R2_key_height//2))
    screen_draw_temp.blit(setting_R2_text, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-setting_R2_text_width//2, SETTING_KEY_RECT_TOP_Y-setting_R2_text_height))
    left_x += SETTING_KEY_RECT_SIDE_LENGTH

    B1_rect = draw.rect(screen_draw_temp, COLOR_LANE_BLUE, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH), SETTING_KEY_RECT_STROKE_WIDTH)
    screen_draw_temp.blit(B1_key, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-B1_key_width//2, SETTING_KEY_RECT_TOP_Y+SETTING_KEY_RECT_SIDE_LENGTH//2-B1_key_height//2))
    screen_draw_temp.blit(setting_B1_text, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-setting_B1_text_width//2, SETTING_KEY_RECT_TOP_Y-setting_B1_text_height))
    left_x += SETTING_KEY_RECT_SIDE_LENGTH

    B2_rect = draw.rect(screen_draw_temp, COLOR_LANE_BLUE, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH), SETTING_KEY_RECT_STROKE_WIDTH)
    screen_draw_temp.blit(B2_key, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-B2_key_width//2, SETTING_KEY_RECT_TOP_Y+SETTING_KEY_RECT_SIDE_LENGTH//2-B2_key_height//2))
    screen_draw_temp.blit(setting_B2_text, (left_x+SETTING_KEY_RECT_SIDE_LENGTH//2-setting_B2_text_width//2, SETTING_KEY_RECT_TOP_Y-setting_B2_text_height))

    if mouse_clicked:
        if setting_volume_slider_rect.collidepoint(mouse_x, mouse_y):
            volume_slider_dragging = True
            keybind_change_exit()
        elif setting_offset_slider_rect.collidepoint(mouse_x, mouse_y):
            offset_slider_dragging = True
            keybind_change_exit()
        elif setting_offset_plus_rect.collidepoint(mouse_x, mouse_y):
            offset += 1
            offset_thumb_center_x = (offset+300) * SETTING_SLIDER_LENGTH // 600 + SETTING_SLIDER_LEFT_X
            keybind_change_exit()
            save_settings()
        elif setting_offset_minus_rect.collidepoint(mouse_x, mouse_y):
            offset -= 1
            offset_thumb_center_x = (offset+300) * SETTING_SLIDER_LENGTH // 600 + SETTING_SLIDER_LEFT_X
            keybind_change_exit()
            save_settings()
        elif setting_speed_plus_rect.collidepoint(mouse_x, mouse_y):
            note_speed_int += 1
            if note_speed_int > MAX_SPEED:
                note_speed_int = MAX_SPEED
            keybind_change_exit()
            save_settings()
        elif setting_speed_minus_rect.collidepoint(mouse_x, mouse_y):
            note_speed_int -= 1
            if note_speed_int < 1:
                note_speed_int = 1
            keybind_change_exit()
            save_settings()
        elif setting_hitsound_rect.collidepoint(mouse_x, mouse_y):
            play_hitsound = not play_hitsound
            keybind_change_exit()
            save_settings()
        elif setting_fps_rect.collidepoint(mouse_x, mouse_y):
            display_fps = not display_fps
            keybind_change_exit()
            save_settings()
        elif R1_rect.collidepoint(mouse_x, mouse_y):
            if keybind_change:
                if key_index != 0:
                    keybind_change_exit()
            keybind_change = True
            key_index = 0
        elif R2_rect.collidepoint(mouse_x, mouse_y):
            if keybind_change:
                if key_index != 1:
                    keybind_change_exit()
            keybind_change = True
            key_index = 1
        elif B1_rect.collidepoint(mouse_x, mouse_y):
            if keybind_change:
                if key_index != 2:
                    keybind_change_exit()
            keybind_change = True
            key_index = 2
        elif B2_rect.collidepoint(mouse_x, mouse_y):
            if keybind_change:
                if key_index != 3:
                    keybind_change_exit()
            keybind_change = True
            key_index = 3
        else:
            keybind_change_exit()

    if keybind_change:
        left_x = SETTING_KEY_RECT_LEFT_X
        if key_index == 0:
            draw.rect(screen_draw_temp, COLOR_LANE_RED, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH))
        else:
            left_x += SETTING_KEY_RECT_SIDE_LENGTH
            if key_index == 1:
                draw.rect(screen_draw_temp, COLOR_LANE_RED, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH))
            else:
                left_x += SETTING_KEY_RECT_SIDE_LENGTH
                if key_index == 2:
                    draw.rect(screen_draw_temp, COLOR_LANE_BLUE, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH))
                else:
                    left_x += SETTING_KEY_RECT_SIDE_LENGTH
                    draw.rect(screen_draw_temp, COLOR_LANE_BLUE, (left_x, SETTING_KEY_RECT_TOP_Y, SETTING_KEY_RECT_SIDE_LENGTH, SETTING_KEY_RECT_SIDE_LENGTH))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_SETTINGS

def setting_exit() -> None:
    global song_volume, note_speed

    song_volume = song_volume_percent / 100
    note_speed = note_speed_int / 10

# functions used in the help page
def draw_help() -> None:
    mouse_clicked = False

    screen_draw_temp.fill(COLOR_MENU_BG)

    for e in event_queue:
        if e[0] == pygame.MOUSEBUTTONDOWN:
            if e[1] == 1:
                mouse_clicked = True
            elif e[1] == 3:
                dip_to_black_animation_init()
                return PAGE_MENU
        elif e[0] == pygame.KEYDOWN:
            if e[1] == pygame.K_ESCAPE:
                dip_to_black_animation_init()
                return PAGE_MENU

    if option_bottom_left_rect.collidepoint(mouse_x, mouse_y):
        if mouse_clicked:
            dip_to_black_animation_init()
            return PAGE_MENU
        top_left_coordinate = option_bottom_left_rect.topleft
        screen_draw_temp.blit(option_button_surface, top_left_coordinate)

    center_x, center_y = option_bottom_left_rect.center
    screen_draw_temp.blit(option_back_text, (center_x-option_back_text_width//2, center_y-option_back_text_height//2))

    screen_draw_temp.blit(tutorial_text[0], (50, 50))
    screen_draw_temp.blit(tutorial_text[1], (50, 80))
    screen_draw_temp.blit(tutorial_img[0], (50, 120))
    screen_draw_temp.blit(tutorial_text[2], (50, 350))
    screen_draw_temp.blit(tutorial_text[3], (550, 50))
    screen_draw_temp.blit(tutorial_text[4], (550, 80))
    screen_draw_temp.blit(tutorial_img[1], (550, 120))
    screen_draw_temp.blit(tutorial_text[5], (50, 380))
    screen_draw_temp.blit(tutorial_text[6], (550, 350))
    screen_draw_temp.blit(tutorial_text[7], (550, 380))
    # screen_draw_temp.blit(tutorial_text[8], (500-tutorial_text_dimension[8][0]//2, 450))

    screen_draw.blit(screen_draw_temp, (0, 0))

    return PAGE_HELP
    
time.set_timer(EVENT_REPORT_FPS, FPS_POLLING_PERIOD)

settings_file = open("Settings.csv", 'r')
settings_file.readline()
settings = settings_file.readline().rstrip().split(',')
song_volume_percent = int(settings[0])
if song_volume_percent < 0:
    song_volume_percent = 0
elif song_volume_percent > 100:
    song_volume_percent = 100
song_volume = song_volume_percent / 100
offset = int(settings[1])
note_speed_int = int(settings[2])
if note_speed_int < 1:
    note_speed_int = 1
note_speed = note_speed_int / 10
play_hitsound = bool(int(settings[3]))
display_fps = bool(int(settings[4]))
keys = settings[5:9]
settings_file.close()
save_settings()

scores = []
scores_file = open("Scores.csv", 'r')
scores_file.readline()
for line in scores_file.readlines():
    line = line.rstrip()
    score_str, accuracy_str = line.split(',')
    scores.append([int(score_str), float(accuracy_str)])

hitsound = mixer.Sound("Explosion.wav")

explosion_img = []
for i in range(EXPLOSION_IMG_COUNT):
    explosion_img.append(image.load("Explosion/%i.png" % (i)).convert_alpha())

explosion_img_width, explosion_img_height = explosion_img[0].get_size()
explosion_img_height = explosion_img_height * GAME_EXPLOION_IMG_WIDTH // explosion_img_width
explosion_img_width = GAME_EXPLOION_IMG_WIDTH

for i in range(EXPLOSION_IMG_COUNT):
    explosion_img[i] = transform.smoothscale(explosion_img[i], (explosion_img_width, explosion_img_height))

for i in range(len(tutorial_img)):
    tutorial_img[i] = transform.smoothscale(tutorial_img[i], (333, 200))

while True:
    screen.fill(COLOR_BLACK)

    del event_queue
    event_queue = []

    get_fps = False

    current_time = get_time_ms()

    for e in event.get():
        if e.type == pygame.QUIT:
            dip_to_black_animation_init()
            page = PAGE_EXIT
        elif e.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = e.pos
        elif e.type == EVENT_REPORT_FPS:
            if e.type == EVENT_REPORT_FPS:
                get_fps = True
        elif not dip_to_black_reversed_animation:
            if e.type == pygame.MOUSEBUTTONDOWN:
                event_queue.append([e.type, e.button])
            elif e.type == pygame.MOUSEBUTTONUP:
                event_queue.append([e.type, e.button])
            elif e.type == pygame.KEYDOWN:
                event_queue.append([e.type, e.key, e.unicode])
            elif e.type == pygame.KEYUP:
                event_queue.append([e.type, e.key, e.unicode])
            elif e.type >= pygame.USEREVENT:
                event_queue.append([e.type])

    if dip_to_black_animation:
        animation_time_elasped = current_time - dip_to_black_animation_start_time
        if animation_time_elasped > DIP_TO_BLACK_ANIMATION_DURATION:
            dip_to_black_animation_exit()
        else:
            dip_to_black_mask_surface.set_alpha(ease_out_sine(animation_time_elasped/DIP_TO_BLACK_ANIMATION_DURATION)*255)
    elif dip_to_black_reversed_animation:
        animation_time_elasped = current_time - dip_to_black_reversed_animation_start_time
        if animation_time_elasped > DIP_TO_BLACK_ANIMATION_DURATION:
            dip_to_black_reversed_animation_exit()
        else:
            dip_to_black_mask_surface.set_alpha(255-ease_out_sine(animation_time_elasped/DIP_TO_BLACK_ANIMATION_DURATION)*255)

    if not dip_to_black_animation:
        if page == PAGE_MENU:
            page = draw_menu()
        elif page == PAGE_SONG_SELECT:
            page = draw_song_select()
        elif page == PAGE_GAME:
            page = draw_game()
        elif page == PAGE_RESULT:
            page = draw_result()
        elif page == PAGE_SETTINGS:
            page = draw_setting()
        elif page == PAGE_HELP:
            page = draw_help()
        else:
            break

    screen.blit(screen_draw, (0, 0))
    screen.blit(dip_to_black_mask_surface, (0, 0))
    
    if get_fps:
        fps_display = FONT_FPS.render("FPS %i  |  Frametime %ims" % (timer.get_fps(), timer.get_rawtime()), True, COLOR_FPS).convert_alpha()
        fps_display_width, fps_display_height = fps_display.get_size()

    if display_fps:
        screen.blit(fps_display, (SCREEN_SIZE[0]-fps_display_width, SCREEN_SIZE[1]-fps_display_height))
      
    display.flip()
    timer.tick_busy_loop(240)

pygame.quit()
