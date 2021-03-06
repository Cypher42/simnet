import numpy as np

"""
General implementation of the generator patters that basically represent a iterable. This pattern is heavily used
in keras. Because this pattern is very simple and provide very high flexibility and make the code much more readable
we decide to use it here.
"""

class SimnetGenerator():
    def __init__(self, helper, num_samples: int):
        self._helper = helper
        self._samples = num_samples

    def get_batch(self, batch_size):
        """
        Iterable of triple of sample data and corresponding labels of batch_size
        :param batch_size: the number of samples per batch
        :return: triple of batch of data for one simnet part, batch of data for other simnet part and batch of corresponding labels
        """
        half_batch = batch_size // 2
        for samples, labels in self._helper(batch_size):
            samples = samples.reshape((samples.shape[0], 28, 28, 1))
            x1 = samples[:half_batch]
            x2 = samples[half_batch:]

            y1 = labels[:half_batch]
            y2 = labels[half_batch:]

            y = np.zeros((half_batch, 1))

            # calculate binary labels for the siamnese network
            y[y1 == y2] = 0.0
            y[y1 != y2] = 1.0

            yield [x1, x2], y

    def steps(self, batch_size) -> int:
        return self._samples // batch_size


class SimpleGenerator():

    def __init__(self, helper, num_samples: int, num_classes=10):
        self._num_classes = num_classes
        self._helper = helper
        self._samples = num_samples

    def get_batch(self, batch_size):
        """
        Iterable of tuples of sample data and corresponding labels of batch_size
        :param batch_size: the number of samples per batch
        :return: tuple of batch of data and batch of corresponding labels
        """
        for samples, labels in self._helper(batch_size):
            samples = samples.reshape((samples.shape[0], 28, 28, 1))
            labels = self.get_one_hot(labels)
            yield samples, labels

    def get_one_hot(self, labels):
        oh_labels = np.zeros((len(labels), self._num_classes))
        for i in range(len(labels)):
            oh_labels[i][labels[i]] = 1
        return oh_labels

    def steps(self, batch_size) -> int:
        return self._samples // batch_size
