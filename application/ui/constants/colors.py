#!/usr/bin/env python

STATUS_COLORS = {
    "off": [0.25, 0.25, 0.25, 1],
    "good": [0, 0.5, 0, 1],
    "bad": [0.5, 0, 0, 1],
    "warning": [0.5, 0.5, 0, 1]
}

STATUS_OPTIONS = list(STATUS_COLORS.keys())

BLACK_BG = [0.0, 0.0, 0.0, 0.5]
BLUE_BG = [0.31, 0.54, 0.73, 0.5]
RED_BG = [0.67, 0.26, 0.28, 0.5]
