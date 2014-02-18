import unittest
import xbob.boosting
import numpy
import bob

import xbob.db.mnist

class TestBoosting(unittest.TestCase):
  """Class to test the LUT trainer """

  @classmethod
  def setUpClass(self):
    # create a single copy of the MNIST database to avoid downloading the packages several times
    self.database = xbob.db.mnist.Database("Database")
    #self.database = xbob.db.mnist.Database()

  @classmethod
  def tearDownClass(self):
    # Clean up the mess that we created
    del self.database

  def _data(self, digits = [3, 0], count = 20):
    # get the data
    inputs, targets = [], []
    for digit in digits:
      input, target = self.database.data(labels = digit)
      inputs.append(input[:count])
      targets.append(target[:count])
    return numpy.vstack(inputs), numpy.hstack(targets)

  def _align_uni(self, targets):
    # align target data to be used in a uni-variate classification
    aligned = numpy.ones(targets.shape)
    aligned[targets != targets[0]] = -1
    return aligned

  def _align_multi(self, targets, digits):
    aligned = - numpy.ones((targets.shape[0], len(digits)))
    for i, d in enumerate(digits):
      aligned[targets==d, i] = 1
    return aligned

  def test01_stump_boosting(self):
    # get test input data
    inputs, targets = self._data()
    aligned = self._align_uni(targets)

    # for stump trainers, the exponential loss function is preferred
    loss_function = xbob.boosting.loss.ExponentialLoss()
    weak_trainer = xbob.boosting.trainer.StumpTrainer()
    booster = xbob.boosting.trainer.Boosting(weak_trainer, loss_function, number_of_rounds=1)

    # perform boosting
    machine = booster.train(inputs.astype(numpy.float64), aligned)
    # check the result
    weight = 1.83178082
    self.assertEqual(machine.weights.shape, (1,1))
    self.assertAlmostEqual(machine.weights, -weight)
    self.assertEqual(len(machine.weak_machines), 1)
    self.assertEqual(machine.indices, [483])
    weak = machine.weak_machines[0]
    self.assertTrue(isinstance(weak, xbob.boosting.StumpMachine))
    self.assertEqual(weak.threshold, 15.5)
    self.assertEqual(weak.polarity, 1.)

    # check first training image
    single = machine(inputs[0].astype(numpy.uint16))
    self.assertAlmostEqual(single, weight)
    # check all training images
    scores = numpy.ndarray(aligned.shape)
    labels = numpy.ndarray(aligned.shape)
    machine(inputs.astype(numpy.uint16), scores, labels)
    # assert that 39 (out of 40) labels are correctly classified by a single feature position
    self.assertTrue(numpy.allclose(labels * scores, weight))
    self.assertEqual(numpy.count_nonzero(labels == aligned), 39)



  def test02_lut_boosting(self):
    # get test input data
    inputs, targets = self._data()
    aligned = self._align_uni(targets)

    # for stump trainers, the logit loss function is preferred
    loss_function = xbob.boosting.loss.LogitLoss()
    weak_trainer = xbob.boosting.trainer.LUTTrainer(256,inputs.shape[1])
    booster = xbob.boosting.trainer.Boosting(weak_trainer, loss_function, number_of_rounds=1)

    # perform boosting
    weight = 15.46452387
    machine = booster.train(inputs.astype(numpy.uint16), aligned)
    self.assertEqual(machine.weights.shape, (1,1))
    self.assertAlmostEqual(machine.weights, -weight)
    self.assertEqual(len(machine.weak_machines), 1)
    self.assertEqual(machine.indices, [379])
    weak = machine.weak_machines[0]
    self.assertTrue(isinstance(weak, xbob.boosting.LUTMachine))
    self.assertEqual(weak.lut.shape, (256,1))

    # check first training image
    single = machine(inputs[0].astype(numpy.uint16))
    self.assertAlmostEqual(single, weight)

    # check all training images
    scores = numpy.ndarray(aligned.shape)
    labels = numpy.ndarray(aligned.shape)
    machine(inputs.astype(numpy.uint16), scores, labels)
    # assert that 40 (out of 40) labels are correctly classified by a single feature position
    self.assertTrue(numpy.allclose(labels * scores, weight))
    self.assertEqual(numpy.count_nonzero(labels == aligned), 40)


  def test03_multi_shared(self):
     # get test input data
    digits = [1, 4, 7, 9]
    inputs, targets = self._data(digits)
    aligned = self._align_multi(targets, digits)

    # for stump trainers, the logit loss function is preferred
    loss_function = xbob.boosting.loss.LogitLoss()
    weak_trainer = xbob.boosting.trainer.LUTTrainer(256, inputs.shape[1], len(digits), 'shared')
    booster = xbob.boosting.trainer.Boosting(weak_trainer, loss_function, number_of_rounds=1)

    # perform boosting
    weights = numpy.array([2.5123104, 2.19725677, 2.34455412, 1.94584326])
    machine = booster.train(inputs.astype(numpy.uint16), aligned)
    self.assertEqual(machine.weights.shape, (1,len(digits)))
    self.assertTrue(numpy.allclose(machine.weights, -weights))
    self.assertEqual(len(machine.weak_machines), 1)
    self.assertEqual(machine.indices, [437])
    weak = machine.weak_machines[0]
    self.assertTrue(isinstance(weak, xbob.boosting.LUTMachine))
    self.assertEqual(weak.lut.shape, (256,4))

    # check first training image
    score = numpy.ndarray(4)
    machine(inputs[0].astype(numpy.uint16), score)
    self.assertTrue(numpy.allclose(score, weights * numpy.array([1., -1., -1., -1.])))

    # check all training images
    scores = numpy.ndarray(aligned.shape)
    labels = numpy.ndarray(aligned.shape)
    machine(inputs.astype(numpy.uint16), scores, labels)
    # assert that 286 (out of 360) labels are correctly classified by a single feature position
    self.assertTrue(all([numpy.allclose(numpy.abs(scores[i]), weights) for i in range(labels.shape[0])]))
    self.assertEqual(numpy.count_nonzero(labels == aligned), 286)


  def test04_multi_independent(self):
    # get test input data
    digits = [1, 4, 7, 9]
    inputs, targets = self._data(digits)
    aligned = self._align_multi(targets, digits)

    # for stump trainers, the logit loss function is preferred
    loss_function = xbob.boosting.loss.LogitLoss()
    weak_trainer = xbob.boosting.trainer.LUTTrainer(256, inputs.shape[1], len(digits), 'independent')
    booster = xbob.boosting.trainer.Boosting(weak_trainer, loss_function, number_of_rounds=1)

    # perform boosting
    weights = numpy.array([2.94443872, 2.70805517, 2.34454354, 2.94443872])
    machine = booster.train(inputs.astype(numpy.uint16), aligned)
    self.assertEqual(machine.weights.shape, (1,len(digits)))
    self.assertTrue(numpy.allclose(machine.weights, -weights))
    self.assertEqual(len(machine.weak_machines), 1)
    print machine.indices
    self.assertTrue(all(machine.indices == [215, 236, 264, 349]))
    weak = machine.weak_machines[0]
    self.assertTrue(isinstance(weak, xbob.boosting.LUTMachine))
    self.assertEqual(weak.lut.shape, (256,4))

    # check first training image
    score = numpy.ndarray(4)
    machine(inputs[0].astype(numpy.uint16), score)
    self.assertTrue(numpy.allclose(score, weights * numpy.array([1., -1., -1., -1.])))

    # check all training images
    scores = numpy.ndarray(aligned.shape)
    labels = numpy.ndarray(aligned.shape)
    machine(inputs.astype(numpy.uint16), scores, labels)
    # assert that 294 (out of 360) labels are correctly classified by a single feature position
    self.assertTrue(all([numpy.allclose(numpy.abs(scores[i]), weights) for i in range(labels.shape[0])]))
    self.assertEqual(numpy.count_nonzero(labels == aligned), 294)
