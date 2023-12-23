# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.train namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.train import experimental
from tensorflow._api.v2.compat.v1.train import queue_runner
from tensorflow.python.ops.gen_sdca_ops import sdca_fprint # line: 27
from tensorflow.python.ops.gen_sdca_ops import sdca_optimizer # line: 115
from tensorflow.python.ops.gen_sdca_ops import sdca_shrink_l1 # line: 750
from tensorflow.python.checkpoint.checkpoint import CheckpointV1 as Checkpoint # line: 1619
from tensorflow.python.checkpoint.checkpoint_management import CheckpointManager # line: 518
from tensorflow.python.checkpoint.checkpoint_management import checkpoint_exists # line: 395
from tensorflow.python.checkpoint.checkpoint_management import generate_checkpoint_state_proto # line: 64
from tensorflow.python.checkpoint.checkpoint_management import get_checkpoint_mtimes # line: 417
from tensorflow.python.checkpoint.checkpoint_management import get_checkpoint_state # line: 250
from tensorflow.python.checkpoint.checkpoint_management import latest_checkpoint # line: 328
from tensorflow.python.checkpoint.checkpoint_management import remove_checkpoint # line: 463
from tensorflow.python.checkpoint.checkpoint_management import update_checkpoint_state # line: 133
from tensorflow.python.checkpoint.checkpoint_options import CheckpointOptions # line: 25
from tensorflow.python.framework.graph_io import write_graph # line: 28
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import cosine_decay # line: 457
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import cosine_decay_restarts # line: 520
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import exponential_decay # line: 28
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import inverse_time_decay # line: 374
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import linear_cosine_decay # line: 597
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import natural_exp_decay # line: 286
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import noisy_linear_cosine_decay # line: 682
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import piecewise_constant # line: 104
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import piecewise_constant as piecewise_constant_decay # line: 104
from tensorflow.python.keras.optimizer_v2.legacy_learning_rate_decay import polynomial_decay # line: 185
from tensorflow.python.summary.summary_iterator import summary_iterator # line: 39
from tensorflow.python.training.adadelta import AdadeltaOptimizer # line: 24
from tensorflow.python.training.adagrad import AdagradOptimizer # line: 27
from tensorflow.python.training.adagrad_da import AdagradDAOptimizer # line: 25
from tensorflow.python.training.adam import AdamOptimizer # line: 27
from tensorflow.python.training.basic_loops import basic_train_loop # line: 20
from tensorflow.python.training.basic_session_run_hooks import CheckpointSaverHook # line: 523
from tensorflow.python.training.basic_session_run_hooks import CheckpointSaverListener # line: 456
from tensorflow.python.training.basic_session_run_hooks import FeedFnHook # line: 994
from tensorflow.python.training.basic_session_run_hooks import FinalOpsHook # line: 950
from tensorflow.python.training.basic_session_run_hooks import GlobalStepWaiterHook # line: 901
from tensorflow.python.training.basic_session_run_hooks import LoggingTensorHook # line: 168
from tensorflow.python.training.basic_session_run_hooks import NanLossDuringTrainingError # line: 753
from tensorflow.python.training.basic_session_run_hooks import NanTensorHook # line: 760
from tensorflow.python.training.basic_session_run_hooks import ProfilerHook # line: 1012
from tensorflow.python.training.basic_session_run_hooks import SecondOrStepTimer # line: 85
from tensorflow.python.training.basic_session_run_hooks import StepCounterHook # line: 673
from tensorflow.python.training.basic_session_run_hooks import StopAtStepHook # line: 392
from tensorflow.python.training.basic_session_run_hooks import SummarySaverHook # line: 792
from tensorflow.python.training.checkpoint_utils import checkpoints_iterator # line: 181
from tensorflow.python.training.checkpoint_utils import init_from_checkpoint # line: 247
from tensorflow.python.training.checkpoint_utils import list_variables # line: 117
from tensorflow.python.training.checkpoint_utils import load_checkpoint # line: 46
from tensorflow.python.training.checkpoint_utils import load_variable # line: 83
from tensorflow.python.training.coordinator import Coordinator # line: 27
from tensorflow.python.training.coordinator import LooperThread # line: 409
from tensorflow.python.training.device_setter import replica_device_setter # line: 130
from tensorflow.python.training.ftrl import FtrlOptimizer # line: 25
from tensorflow.python.training.gradient_descent import GradientDescentOptimizer # line: 26
from tensorflow.python.training.input import batch # line: 928
from tensorflow.python.training.input import batch_join # line: 1084
from tensorflow.python.training.input import input_producer # line: 115
from tensorflow.python.training.input import limit_epochs # line: 79
from tensorflow.python.training.input import match_filenames_once # line: 56
from tensorflow.python.training.input import maybe_batch # line: 1027
from tensorflow.python.training.input import maybe_batch_join # line: 1194
from tensorflow.python.training.input import maybe_shuffle_batch # line: 1354
from tensorflow.python.training.input import maybe_shuffle_batch_join # line: 1516
from tensorflow.python.training.input import range_input_producer # line: 278
from tensorflow.python.training.input import shuffle_batch # line: 1251
from tensorflow.python.training.input import shuffle_batch_join # line: 1418
from tensorflow.python.training.input import slice_input_producer # line: 320
from tensorflow.python.training.input import string_input_producer # line: 203
from tensorflow.python.training.momentum import MomentumOptimizer # line: 24
from tensorflow.python.training.monitored_session import ChiefSessionCreator # line: 622
from tensorflow.python.training.monitored_session import MonitoredSession # line: 957
from tensorflow.python.training.monitored_session import MonitoredTrainingSession # line: 427
from tensorflow.python.training.monitored_session import Scaffold # line: 51
from tensorflow.python.training.monitored_session import SessionCreator # line: 612
from tensorflow.python.training.monitored_session import SingularMonitoredSession # line: 1057
from tensorflow.python.training.monitored_session import WorkerSessionCreator # line: 676
from tensorflow.python.training.moving_averages import ExponentialMovingAverage # line: 283
from tensorflow.python.training.optimizer import Optimizer # line: 217
from tensorflow.python.training.proximal_adagrad import ProximalAdagradOptimizer # line: 25
from tensorflow.python.training.proximal_gradient_descent import ProximalGradientDescentOptimizer # line: 26
from tensorflow.python.training.py_checkpoint_reader import NewCheckpointReader # line: 81
from tensorflow.python.training.quantize_training import do_quantize_training_on_graphdef # line: 26
from tensorflow.python.training.queue_runner_impl import QueueRunner # line: 33
from tensorflow.python.training.queue_runner_impl import add_queue_runner # line: 391
from tensorflow.python.training.queue_runner_impl import start_queue_runners # line: 417
from tensorflow.python.training.rmsprop import RMSPropOptimizer # line: 49
from tensorflow.python.training.saver import Saver # line: 641
from tensorflow.python.training.saver import export_meta_graph # line: 1644
from tensorflow.python.training.saver import import_meta_graph # line: 1477
from tensorflow.python.training.server_lib import ClusterSpec # line: 242
from tensorflow.python.training.server_lib import Server # line: 94
from tensorflow.python.training.session_manager import SessionManager # line: 74
from tensorflow.python.training.session_run_hook import SessionRunArgs # line: 185
from tensorflow.python.training.session_run_hook import SessionRunContext # line: 210
from tensorflow.python.training.session_run_hook import SessionRunHook # line: 93
from tensorflow.python.training.session_run_hook import SessionRunValues # line: 262
from tensorflow.python.training.supervisor import Supervisor # line: 39
from tensorflow.python.training.sync_replicas_optimizer import SyncReplicasOptimizer # line: 41
from tensorflow.python.training.training import BytesList # line: 131
from tensorflow.python.training.training import ClusterDef # line: 132
from tensorflow.python.training.training import Example # line: 133
from tensorflow.python.training.training import Feature # line: 134
from tensorflow.python.training.training import FeatureList # line: 136
from tensorflow.python.training.training import FeatureLists # line: 137
from tensorflow.python.training.training import Features # line: 135
from tensorflow.python.training.training import FloatList # line: 138
from tensorflow.python.training.training import Int64List # line: 139
from tensorflow.python.training.training import JobDef # line: 140
from tensorflow.python.training.training import SaverDef # line: 141
from tensorflow.python.training.training import SequenceExample # line: 142
from tensorflow.python.training.training import ServerDef # line: 143
from tensorflow.python.training.training_util import assert_global_step # line: 329
from tensorflow.python.training.training_util import create_global_step # line: 164
from tensorflow.python.training.training_util import get_global_step # line: 70
from tensorflow.python.training.training_util import get_or_create_global_step # line: 258
from tensorflow.python.training.training_util import global_step # line: 39
from tensorflow.python.training.warm_starting_util import VocabInfo # line: 32
from tensorflow.python.training.warm_starting_util import warm_start # line: 405

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "train", public_apis=None, deprecation=False,
      has_lite=False)
