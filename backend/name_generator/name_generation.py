import json
import re
from typing import List
import numpy as np

dict_size = 26
awareness = 3

nameFile = open("db.json","r")
names = json.load(nameFile)
names = [i.lower() for i in names]
names = [name for name in names if re.search(r'^[a-z]+$', name)]


class HMM:
  def __init__(self, mat):
    self.mat = mat

  @staticmethod
  def getLetterIndex(letter: str):
    if letter == '^':
      return 0
    return ord(letter) - ord('a') + 1

  def trainModel(self, names: List[str]):
    transition_mattrix = np.zeros(((dict_size+1)**awareness, dict_size+1))
    print(transition_mattrix.shape)
    for name in names:
      currentStatus = 0
      for letter in name:
        newIndex = HMM.getLetterIndex(letter)
        oldRemaining = currentStatus % (dict_size+1)**(awareness-1)
        transition_mattrix[currentStatus][newIndex] += 1
        currentStatus = oldRemaining * (dict_size+1) + newIndex
    # normalize transition_matrix[i]
    for i in range(transition_mattrix.shape[0]):
      if transition_mattrix[i].sum() != 0:
        transition_mattrix[i] /= transition_mattrix[i].sum()
      else:
        transition_mattrix[i] = np.copy(transition_mattrix[0])
    self.mat = transition_mattrix

  def getWord(self, wordSize: int) -> str:
    w = ''
    current_state = 0  # start state
    for i in range(wordSize):
      distro = self.mat[current_state]
      newletter = np.random.choice(range(dict_size+1), p=distro)
      w = w + (chr(newletter + ord('a') - 1))
      current_state = current_state % (
          dict_size+1)**(awareness-1) * (dict_size+1) + newletter
    return w

defaultHMM=HMM(None)
defaultHMM.trainModel(names)