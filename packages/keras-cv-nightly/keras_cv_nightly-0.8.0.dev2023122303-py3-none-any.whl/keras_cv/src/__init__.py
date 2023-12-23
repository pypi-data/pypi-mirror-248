# Copyright 2022 The KerasCV Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    # When using torch and tensorflow, torch needs to be imported first,
    # otherwise it will segfault upon import.
    import torch

    del torch
except ImportError:
    pass

# isort:off
from keras_cv.src import version_check

version_check.check_tf_version()
# isort:on

from keras_cv.src import bounding_box
from keras_cv.src import callbacks
from keras_cv.src import datasets
from keras_cv.src import layers
from keras_cv.src import losses
from keras_cv.src import metrics
from keras_cv.src import models
from keras_cv.src import training
from keras_cv.src import utils
from keras_cv.src import visualization
from keras_cv.src.core import ConstantFactorSampler
from keras_cv.src.core import FactorSampler
from keras_cv.src.core import NormalFactorSampler
from keras_cv.src.core import UniformFactorSampler

__version__ = "0.8.0"

