import pandas as pd
import numpy as np
import pygame
import copy

KEREN = 1
AYELET = 2
YOAV = 3
PARENTS = 4

AMOUNT = 4
MAX_AWAY = 7


def normalize_range(data):
    return np.array((data - 0) / (MAX_AWAY - 0))


if __name__ == '__main__':

    # read excel file
    data = pd.read_csv("datesAndLocations.csv").to_numpy()
    data = np.transpose(data)

    # divide data
    location_data = [data[KEREN], data[AYELET], data[YOAV], data[PARENTS]]

    # amount of data
    data_len = data[KEREN].shape[0]

    # organize prints
    prints0 = ['|'] * data_len
    prints1 = ['|'] * data_len
    prints2 = ['|'] * data_len
    prints3 = ['|'] * data_len

    for i in range(0, data_len):
        if location_data[KEREN - 1][i]:
            prints0[i] = ' ' + prints0[i - 1]
        else:
            prints0[i] = '|'

    for i in range(0, data_len):
        if location_data[AYELET - 1][i]:
            prints1[i] = ' ' + prints1[i - 1]
        else:
            prints1[i] = '|'

    for i in range(0, data_len):
        if location_data[YOAV - 1][i]:
            prints2[i] = ' ' + prints2[i - 1]
        else:
            prints2[i] = '|'

    for i in range(0, data_len):
        if location_data[PARENTS - 1][i]:
            prints3[i] = ' ' + prints3[i - 1]
        else:
            prints3[i] = '|'

    # manage data
    # (cumsum) sum the days that were away
    for personData in location_data:
        for i in range(1, len(personData)):
            if personData[i]:
                personData[i] += personData[i - 1]

    time_away = copy.deepcopy(location_data)

    # add values to days before is about to come back
    for personData in location_data:
        for i in range(1, len(personData) - 5):

            if personData[i] >= 1 and personData[i + 1] == 0:
                personData[i] = 1
            elif personData[i] >= 1 and personData[i + 2] == 0:
                personData[i] = 2
            elif personData[i] >= 1 and personData[i + 3] == 0:
                personData[i] = 3
            elif personData[i] >= 1 and personData[i + 4] == 0:
                personData[i] = 4
            elif personData[i] >= 1 and personData[i + 5] == 0:
                personData[i] = 5

    # normalize
    for personData in location_data:
        for i in range(1, len(personData)):
            if personData[i] > MAX_AWAY:
                personData[i] = MAX_AWAY

    # clip and reverse
    for i in range(AMOUNT):
        location_data[i] = normalize_range(location_data[i])
        location_data[i] = 1 - location_data[i]

    # init
    pygame.init()
    clock = pygame.time.Clock()

    # load music
    sounds = []
    for i in range(AMOUNT):
        sound = pygame.mixer.Sound('Beatles/All you need/Track%d.mp3' % i)
        sounds.append(sound)

    # play music (to prevent delay)
    for i in range(AMOUNT):
        sounds[i].play()

    # play until the data ends
    for i in range(365):
        pygame.time.wait(550)  # check according to song

        # prints
        print("Keren- ", prints0[i])
        print("Ayelet- ", prints1[i])
        print("Yoav- ", prints2[i])
        print("Parents- ", prints3[i], "\n")

        # set volumes
        sounds[0].set_volume(location_data[KEREN - 1][i])
        sounds[1].set_volume(location_data[AYELET - 1][i])
        sounds[2].set_volume(location_data[YOAV - 1][i])
        sounds[3].set_volume(location_data[PARENTS - 1][i] - 0.2)

