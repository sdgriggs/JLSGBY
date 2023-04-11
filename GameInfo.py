# Defines some timing constants used throughout the game
# Defined out of Context to avoid potential circular dependencies
MIN_PER_HOUR = 60
HOUR_PER_SOL = 24
SOL_PER_YEAR = 668

# Timing Constants
#Target frame rate, don't raise above 30 rn
TARGET_FRAME_RATE = 30
#how many minutes in game should pass for each real life
GAME_MINUTES_PER_SECOND = 10
#how many ticks in an in game minute
TICKS_PER_MINUTE = TARGET_FRAME_RATE / GAME_MINUTES_PER_SECOND
#how many ticks in an in game hour
TICKS_PER_HOUR = TICKS_PER_MINUTE * MIN_PER_HOUR
#how many ticks in an in game sol
TICKS_PER_SOL = TICKS_PER_MINUTE * HOUR_PER_SOL
#How many minutes should pass before the time changes
MINUTE_INCREMENT = 10

