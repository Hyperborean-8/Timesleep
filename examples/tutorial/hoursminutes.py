from icecream import ic

seconds = 10020

hours = seconds // 3600
ic(hours)
seconds = seconds % 3600
ic(seconds)
minutes = seconds // 60
ic(minutes)
seconds = seconds % 60
ic(seconds)

