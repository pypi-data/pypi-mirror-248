from numpy import zeros, shape, tile

def normalize(dataset):
  """
  dataset: the dataset will be normalized
  return:
    retDataset: normalized dataset
    minVals: the minimum values  vector
    ranges: the difference of minVals and maxVals
  """
  minVals = dataset.min(0)
  maxVals = dataset.max(0)
  ranges = maxVals - minVals

  retDataset = zeros(shape(dataset))

  m = dataset.shape[0]
  retDataset = dataset - tile(minVals, (m, 1))
  retDataset = retDataset / tile(ranges, (m, 1))

  return retDataset, minVals, ranges 




def train_test_split(dataset, labels, ratio):
  size  = len(dataset)
  sep = int((size-1) * ratio)
  # train_x, train_y, test_x, test_y
  return dataset[:sep], labels[:sep], \
         dataset[sep:], labels[sep:]

def overSampling(dataset, labels, aimedLabel , times):
  """
  for aimedLabel overSampling n times.
  """
  new_x = []
  new_y = []

  idx = 0
  for label in labels:
    if label == aimedLabel:
      for  i in range(times):
         new_x.append(dataset[idx])
         new_y.append(dataset[idx])
    idx += 1

  return new_x, new_y

def underSampling(dataset, labels, aimedLabel, times):
  new_x = []
  new_y = []
  cnt = 0
  idx = 0
  for label in labels:
    if label == aimedLabel:
      cnt +=1
      if cnt >= times:
        new_x.append(dataset[idx])
        new_y.append(label)
    idx += 1
  
  return new_x, new_y
