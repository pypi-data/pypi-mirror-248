# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Bring in all of the public TensorFlow interface into this module."""

# pylint: disable=g-bad-import-order,g-import-not-at-top,protected-access

import os as _os
import sys as _sys
import typing as _typing

from tensorflow.python.tools import module_util as _module_util
from tensorflow.python.util.lazy_loader import LazyLoader as _LazyLoader
from tensorflow.python.util.lazy_loader import KerasLazyLoader as _KerasLazyLoader

from tensorflow._api.v2.compat.v1 import __internal__
from tensorflow._api.v2.compat.v1 import app
from tensorflow._api.v2.compat.v1 import audio
from tensorflow._api.v2.compat.v1 import autograph
from tensorflow._api.v2.compat.v1 import bitwise
from tensorflow._api.v2.compat.v1 import compat
from tensorflow._api.v2.compat.v1 import config
from tensorflow._api.v2.compat.v1 import data
from tensorflow._api.v2.compat.v1 import debugging
from tensorflow._api.v2.compat.v1 import distribute
from tensorflow._api.v2.compat.v1 import distributions
from tensorflow._api.v2.compat.v1 import dtypes
from tensorflow._api.v2.compat.v1 import errors
from tensorflow._api.v2.compat.v1 import experimental
from tensorflow._api.v2.compat.v1 import feature_column
from tensorflow._api.v2.compat.v1 import gfile
from tensorflow._api.v2.compat.v1 import graph_util
from tensorflow._api.v2.compat.v1 import image
from tensorflow._api.v2.compat.v1 import initializers
from tensorflow._api.v2.compat.v1 import io
from tensorflow._api.v2.compat.v1 import layers
from tensorflow._api.v2.compat.v1 import linalg
from tensorflow._api.v2.compat.v1 import lite
from tensorflow._api.v2.compat.v1 import logging
from tensorflow._api.v2.compat.v1 import lookup
from tensorflow._api.v2.compat.v1 import losses
from tensorflow._api.v2.compat.v1 import manip
from tensorflow._api.v2.compat.v1 import math
from tensorflow._api.v2.compat.v1 import metrics
from tensorflow._api.v2.compat.v1 import mixed_precision
from tensorflow._api.v2.compat.v1 import mlir
from tensorflow._api.v2.compat.v1 import nest
from tensorflow._api.v2.compat.v1 import nn
from tensorflow._api.v2.compat.v1 import profiler
from tensorflow._api.v2.compat.v1 import python_io
from tensorflow._api.v2.compat.v1 import quantization
from tensorflow._api.v2.compat.v1 import queue
from tensorflow._api.v2.compat.v1 import ragged
from tensorflow._api.v2.compat.v1 import random
from tensorflow._api.v2.compat.v1 import raw_ops
from tensorflow._api.v2.compat.v1 import resource_loader
from tensorflow._api.v2.compat.v1 import saved_model
from tensorflow._api.v2.compat.v1 import sets
from tensorflow._api.v2.compat.v1 import signal
from tensorflow._api.v2.compat.v1 import sparse
from tensorflow._api.v2.compat.v1 import spectral
from tensorflow._api.v2.compat.v1 import strings
from tensorflow._api.v2.compat.v1 import summary
from tensorflow._api.v2.compat.v1 import sysconfig
from tensorflow._api.v2.compat.v1 import test
from tensorflow._api.v2.compat.v1 import tpu
from tensorflow._api.v2.compat.v1 import train
from tensorflow._api.v2.compat.v1 import types
from tensorflow._api.v2.compat.v1 import user_ops
from tensorflow._api.v2.compat.v1 import version
from tensorflow._api.v2.compat.v1 import xla
from tensorflow.python.ops.gen_array_ops import batch_to_space_nd # line: 343
from tensorflow.python.ops.gen_array_ops import bitcast # line: 558
from tensorflow.python.ops.gen_array_ops import broadcast_to # line: 829
from tensorflow.python.ops.gen_array_ops import check_numerics # line: 950
from tensorflow.python.ops.gen_array_ops import diag # line: 1949
from tensorflow.python.ops.gen_array_ops import extract_volume_patches # line: 2569
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_args # line: 2698
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_args_gradient # line: 2867
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars # line: 3003
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_gradient # line: 3145
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_per_channel # line: 3276
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_per_channel_gradient # line: 3423
from tensorflow.python.ops.gen_array_ops import identity_n # line: 4226
from tensorflow.python.ops.gen_array_ops import invert_permutation # line: 4592
from tensorflow.python.ops.gen_array_ops import matrix_band_part # line: 4879
from tensorflow.python.ops.gen_array_ops import quantized_concat # line: 8202
from tensorflow.python.ops.gen_array_ops import reverse_v2 as reverse # line: 9140
from tensorflow.python.ops.gen_array_ops import reverse_v2 # line: 9140
from tensorflow.python.ops.gen_array_ops import scatter_nd # line: 9276
from tensorflow.python.ops.gen_array_ops import space_to_batch_nd # line: 10076
from tensorflow.python.ops.gen_array_ops import tensor_scatter_add # line: 11226
from tensorflow.python.ops.gen_array_ops import tensor_scatter_add as tensor_scatter_nd_add # line: 11226
from tensorflow.python.ops.gen_array_ops import tensor_scatter_max as tensor_scatter_nd_max # line: 11382
from tensorflow.python.ops.gen_array_ops import tensor_scatter_min as tensor_scatter_nd_min # line: 11488
from tensorflow.python.ops.gen_array_ops import tensor_scatter_sub as tensor_scatter_nd_sub # line: 11583
from tensorflow.python.ops.gen_array_ops import tensor_scatter_sub # line: 11583
from tensorflow.python.ops.gen_array_ops import tile # line: 11970
from tensorflow.python.ops.gen_array_ops import unravel_index # line: 12731
from tensorflow.python.ops.gen_control_flow_ops import no_op # line: 475
from tensorflow.python.ops.gen_data_flow_ops import dynamic_partition # line: 594
from tensorflow.python.ops.gen_data_flow_ops import dynamic_stitch # line: 736
from tensorflow.python.ops.gen_io_ops import matching_files # line: 391
from tensorflow.python.ops.gen_io_ops import write_file # line: 2269
from tensorflow.python.ops.gen_linalg_ops import cholesky # line: 766
from tensorflow.python.ops.gen_linalg_ops import matrix_determinant # line: 1370
from tensorflow.python.ops.gen_linalg_ops import matrix_inverse # line: 1516
from tensorflow.python.ops.gen_linalg_ops import matrix_solve # line: 1694
from tensorflow.python.ops.gen_linalg_ops import matrix_square_root # line: 1913
from tensorflow.python.ops.gen_linalg_ops import qr # line: 2150
from tensorflow.python.ops.gen_logging_ops import timestamp # line: 886
from tensorflow.python.ops.gen_math_ops import acosh # line: 231
from tensorflow.python.ops.gen_math_ops import asin # line: 991
from tensorflow.python.ops.gen_math_ops import asinh # line: 1091
from tensorflow.python.ops.gen_math_ops import atan # line: 1184
from tensorflow.python.ops.gen_math_ops import atan2 # line: 1284
from tensorflow.python.ops.gen_math_ops import atanh # line: 1383
from tensorflow.python.ops.gen_math_ops import betainc # line: 1844
from tensorflow.python.ops.gen_math_ops import cos # line: 2521
from tensorflow.python.ops.gen_math_ops import cosh # line: 2615
from tensorflow.python.ops.gen_math_ops import cross # line: 2708
from tensorflow.python.ops.gen_math_ops import digamma # line: 3218
from tensorflow.python.ops.gen_math_ops import erf # line: 3511
from tensorflow.python.ops.gen_math_ops import erfc # line: 3603
from tensorflow.python.ops.gen_math_ops import expm1 # line: 3904
from tensorflow.python.ops.gen_math_ops import floor_div # line: 4059
from tensorflow.python.ops.gen_math_ops import floor_mod as floormod # line: 4149
from tensorflow.python.ops.gen_math_ops import greater # line: 4243
from tensorflow.python.ops.gen_math_ops import greater_equal # line: 4344
from tensorflow.python.ops.gen_math_ops import igamma # line: 4537
from tensorflow.python.ops.gen_math_ops import igammac # line: 4696
from tensorflow.python.ops.gen_math_ops import is_finite # line: 4992
from tensorflow.python.ops.gen_math_ops import is_inf # line: 5088
from tensorflow.python.ops.gen_math_ops import is_nan # line: 5184
from tensorflow.python.ops.gen_math_ops import less # line: 5280
from tensorflow.python.ops.gen_math_ops import less_equal # line: 5381
from tensorflow.python.ops.gen_math_ops import lgamma # line: 5482
from tensorflow.python.ops.gen_math_ops import log # line: 5652
from tensorflow.python.ops.gen_math_ops import log1p # line: 5746
from tensorflow.python.ops.gen_math_ops import logical_and # line: 5836
from tensorflow.python.ops.gen_math_ops import logical_not # line: 5975
from tensorflow.python.ops.gen_math_ops import logical_or # line: 6062
from tensorflow.python.ops.gen_math_ops import maximum # line: 6383
from tensorflow.python.ops.gen_math_ops import minimum # line: 6639
from tensorflow.python.ops.gen_math_ops import floor_mod as mod # line: 4149
from tensorflow.python.ops.gen_math_ops import neg as negative # line: 6986
from tensorflow.python.ops.gen_math_ops import polygamma # line: 7240
from tensorflow.python.ops.gen_math_ops import real_div as realdiv # line: 8141
from tensorflow.python.ops.gen_math_ops import reciprocal # line: 8232
from tensorflow.python.ops.gen_math_ops import rint # line: 8729
from tensorflow.python.ops.gen_math_ops import segment_max # line: 9003
from tensorflow.python.ops.gen_math_ops import segment_mean # line: 9237
from tensorflow.python.ops.gen_math_ops import segment_min # line: 9362
from tensorflow.python.ops.gen_math_ops import segment_prod # line: 9596
from tensorflow.python.ops.gen_math_ops import segment_sum # line: 9822
from tensorflow.python.ops.gen_math_ops import sin # line: 10372
from tensorflow.python.ops.gen_math_ops import sinh # line: 10465
from tensorflow.python.ops.gen_math_ops import square # line: 12035
from tensorflow.python.ops.gen_math_ops import squared_difference # line: 12124
from tensorflow.python.ops.gen_math_ops import tan # line: 12425
from tensorflow.python.ops.gen_math_ops import tanh # line: 12519
from tensorflow.python.ops.gen_math_ops import truncate_div as truncatediv # line: 12674
from tensorflow.python.ops.gen_math_ops import truncate_mod as truncatemod # line: 12768
from tensorflow.python.ops.gen_math_ops import unsorted_segment_max # line: 12862
from tensorflow.python.ops.gen_math_ops import unsorted_segment_min # line: 13000
from tensorflow.python.ops.gen_math_ops import unsorted_segment_prod # line: 13134
from tensorflow.python.ops.gen_math_ops import unsorted_segment_sum # line: 13268
from tensorflow.python.ops.gen_math_ops import zeta # line: 13603
from tensorflow.python.ops.gen_nn_ops import approx_top_k # line: 33
from tensorflow.python.ops.gen_nn_ops import conv # line: 1061
from tensorflow.python.ops.gen_nn_ops import conv2d_backprop_filter_v2 # line: 1609
from tensorflow.python.ops.gen_nn_ops import conv2d_backprop_input_v2 # line: 1977
from tensorflow.python.ops.gen_parsing_ops import decode_compressed # line: 144
from tensorflow.python.ops.gen_parsing_ops import parse_tensor # line: 2135
from tensorflow.python.ops.gen_ragged_array_ops import ragged_fill_empty_rows # line: 196
from tensorflow.python.ops.gen_ragged_array_ops import ragged_fill_empty_rows_grad # line: 305
from tensorflow.python.ops.gen_random_index_shuffle_ops import random_index_shuffle # line: 30
from tensorflow.python.ops.gen_spectral_ops import fft # line: 353
from tensorflow.python.ops.gen_spectral_ops import fft2d # line: 442
from tensorflow.python.ops.gen_spectral_ops import fft3d # line: 531
from tensorflow.python.ops.gen_spectral_ops import fftnd # line: 620
from tensorflow.python.ops.gen_spectral_ops import ifft # line: 724
from tensorflow.python.ops.gen_spectral_ops import ifft2d # line: 813
from tensorflow.python.ops.gen_spectral_ops import ifft3d # line: 902
from tensorflow.python.ops.gen_spectral_ops import ifftnd # line: 991
from tensorflow.python.ops.gen_spectral_ops import irfftnd # line: 1347
from tensorflow.python.ops.gen_spectral_ops import rfftnd # line: 1707
from tensorflow.python.ops.gen_string_ops import as_string # line: 29
from tensorflow.python.ops.gen_string_ops import decode_base64 # line: 182
from tensorflow.python.ops.gen_string_ops import encode_base64 # line: 269
from tensorflow.python.ops.gen_string_ops import string_strip # line: 1429
from tensorflow.python.ops.gen_string_ops import string_to_hash_bucket_fast # line: 1583
from tensorflow.python.ops.gen_string_ops import string_to_hash_bucket_strong # line: 1688
from tensorflow.python.client.session import InteractiveSession # line: 1720
from tensorflow.python.client.session import Session # line: 1541
from tensorflow.python.compat.v2_compat import disable_v2_behavior # line: 73
from tensorflow.python.compat.v2_compat import enable_v2_behavior # line: 39
from tensorflow.python.data.ops.optional_ops import OptionalSpec # line: 205
from tensorflow.python.eager.backprop import GradientTape # line: 704
from tensorflow.python.eager.context import executing_eagerly_v1 as executing_eagerly # line: 2391
from tensorflow.python.eager.polymorphic_function.polymorphic_function import function # line: 1300
from tensorflow.python.eager.wrap_function import wrap_function # line: 576
from tensorflow.python.framework.constant_op import constant_v1 as constant # line: 111
from tensorflow.python.framework.device_spec import DeviceSpecV1 as DeviceSpec # line: 420
from tensorflow.python.framework.dtypes import DType # line: 51
from tensorflow.python.framework.dtypes import QUANTIZED_DTYPES # line: 771
from tensorflow.python.framework.dtypes import as_dtype # line: 793
from tensorflow.python.framework.dtypes import bfloat16 # line: 450
from tensorflow.python.framework.dtypes import bool # line: 414
from tensorflow.python.framework.dtypes import complex128 # line: 401
from tensorflow.python.framework.dtypes import complex64 # line: 394
from tensorflow.python.framework.dtypes import double # line: 388
from tensorflow.python.framework.dtypes import float16 # line: 373
from tensorflow.python.framework.dtypes import float32 # line: 380
from tensorflow.python.framework.dtypes import float64 # line: 386
from tensorflow.python.framework.dtypes import half # line: 374
from tensorflow.python.framework.dtypes import int16 # line: 354
from tensorflow.python.framework.dtypes import int32 # line: 360
from tensorflow.python.framework.dtypes import int64 # line: 366
from tensorflow.python.framework.dtypes import int8 # line: 348
from tensorflow.python.framework.dtypes import qint16 # line: 426
from tensorflow.python.framework.dtypes import qint32 # line: 432
from tensorflow.python.framework.dtypes import qint8 # line: 420
from tensorflow.python.framework.dtypes import quint16 # line: 444
from tensorflow.python.framework.dtypes import quint8 # line: 438
from tensorflow.python.framework.dtypes import resource # line: 312
from tensorflow.python.framework.dtypes import string # line: 408
from tensorflow.python.framework.dtypes import uint16 # line: 330
from tensorflow.python.framework.dtypes import uint32 # line: 336
from tensorflow.python.framework.dtypes import uint64 # line: 342
from tensorflow.python.framework.dtypes import uint8 # line: 324
from tensorflow.python.framework.dtypes import variant # line: 318
from tensorflow.python.framework.errors_impl import OpError # line: 57
from tensorflow.python.framework.graph_util_impl import GraphDef # line: 29
from tensorflow.python.framework.importer import import_graph_def # line: 358
from tensorflow.python.framework.indexed_slices import IndexedSlices # line: 54
from tensorflow.python.framework.indexed_slices import IndexedSlicesSpec # line: 203
from tensorflow.python.framework.indexed_slices import convert_to_tensor_or_indexed_slices # line: 277
from tensorflow.python.framework.load_library import load_file_system_library # line: 79
from tensorflow.python.framework.load_library import load_library # line: 120
from tensorflow.python.framework.load_library import load_op_library # line: 31
from tensorflow.python.framework.ops import Graph # line: 1915
from tensorflow.python.framework.ops import GraphKeys # line: 5161
from tensorflow.python.framework.ops import no_gradient as NoGradient # line: 1690
from tensorflow.python.framework.ops import no_gradient as NotDifferentiable # line: 1690
from tensorflow.python.framework.ops import Operation # line: 1035
from tensorflow.python.framework.ops import RegisterGradient # line: 1641
from tensorflow.python.framework.ops import add_to_collection # line: 5319
from tensorflow.python.framework.ops import add_to_collections # line: 5339
from tensorflow.python.framework.ops import _colocate_with as colocate_with # line: 4432
from tensorflow.python.framework.ops import container # line: 4389
from tensorflow.python.framework.ops import control_dependencies # line: 4437
from tensorflow.python.framework.ops import device # line: 4314
from tensorflow.python.framework.ops import disable_eager_execution # line: 4875
from tensorflow.python.framework.ops import enable_eager_execution # line: 4797
from tensorflow.python.framework.ops import executing_eagerly_outside_functions # line: 4743
from tensorflow.python.framework.ops import get_collection # line: 5383
from tensorflow.python.framework.ops import get_collection_ref # line: 5359
from tensorflow.python.framework.ops import get_default_graph # line: 5022
from tensorflow.python.framework.ops import init_scope # line: 4638
from tensorflow.python.framework.ops import is_symbolic_tensor # line: 6088
from tensorflow.python.framework.ops import name_scope_v1 as name_scope # line: 5537
from tensorflow.python.framework.ops import no_gradient # line: 1690
from tensorflow.python.framework.ops import op_scope # line: 5773
from tensorflow.python.framework.ops import reset_default_graph # line: 4992
from tensorflow.python.framework.random_seed import get_seed # line: 38
from tensorflow.python.framework.random_seed import set_random_seed # line: 96
from tensorflow.python.framework.sparse_tensor import SparseTensor # line: 48
from tensorflow.python.framework.sparse_tensor import SparseTensorSpec # line: 377
from tensorflow.python.framework.sparse_tensor import SparseTensorValue # line: 374
from tensorflow.python.framework.sparse_tensor import convert_to_tensor_or_sparse_tensor # line: 534
from tensorflow.python.framework.stack import get_default_session # line: 122
from tensorflow.python.framework.tensor import Tensor # line: 138
from tensorflow.python.framework.tensor import TensorSpec # line: 917
from tensorflow.python.framework.tensor import disable_tensor_equality # line: 783
from tensorflow.python.framework.tensor import enable_tensor_equality # line: 769
from tensorflow.python.framework.tensor_conversion import convert_to_tensor_v1_with_dispatch as convert_to_tensor # line: 33
from tensorflow.python.framework.tensor_conversion_registry import register_tensor_conversion_function # line: 80
from tensorflow.python.framework.tensor_shape import Dimension # line: 188
from tensorflow.python.framework.tensor_shape import TensorShape # line: 747
from tensorflow.python.framework.tensor_shape import dimension_at_index # line: 139
from tensorflow.python.framework.tensor_shape import dimension_value # line: 103
from tensorflow.python.framework.tensor_shape import disable_v2_tensorshape # line: 91
from tensorflow.python.framework.tensor_shape import enable_v2_tensorshape # line: 38
from tensorflow.python.framework.tensor_util import constant_value as get_static_value # line: 896
from tensorflow.python.framework.tensor_util import is_tf_type as is_tensor # line: 1128
from tensorflow.python.framework.tensor_util import MakeNdarray as make_ndarray # line: 633
from tensorflow.python.framework.tensor_util import make_tensor_proto # line: 425
from tensorflow.python.framework.type_spec import TypeSpec # line: 49
from tensorflow.python.framework.type_spec import type_spec_from_value # line: 958
from tensorflow.python.framework.versions import COMPILER_VERSION # line: 41
from tensorflow.python.framework.versions import CXX11_ABI_FLAG # line: 48
from tensorflow.python.framework.versions import CXX_VERSION # line: 54
from tensorflow.python.framework.versions import GIT_VERSION # line: 35
from tensorflow.python.framework.versions import GRAPH_DEF_VERSION # line: 68
from tensorflow.python.framework.versions import GRAPH_DEF_VERSION_MIN_CONSUMER # line: 74
from tensorflow.python.framework.versions import GRAPH_DEF_VERSION_MIN_PRODUCER # line: 82
from tensorflow.python.framework.versions import MONOLITHIC_BUILD # line: 60
from tensorflow.python.framework.versions import VERSION # line: 29
from tensorflow.python.framework.versions import COMPILER_VERSION as __compiler_version__ # line: 41
from tensorflow.python.framework.versions import CXX11_ABI_FLAG as __cxx11_abi_flag__ # line: 48
from tensorflow.python.framework.versions import CXX_VERSION as __cxx_version__ # line: 54
from tensorflow.python.framework.versions import GIT_VERSION as __git_version__ # line: 35
from tensorflow.python.framework.versions import MONOLITHIC_BUILD as __monolithic_build__ # line: 60
from tensorflow.python.framework.versions import VERSION as __version__ # line: 29
from tensorflow.python.module.module import Module # line: 29
from tensorflow.python.ops.array_ops import batch_gather # line: 4983
from tensorflow.python.ops.array_ops import batch_to_space # line: 3798
from tensorflow.python.ops.array_ops import boolean_mask # line: 1411
from tensorflow.python.ops.array_ops import broadcast_dynamic_shape # line: 526
from tensorflow.python.ops.array_ops import broadcast_static_shape # line: 560
from tensorflow.python.ops.array_ops import concat # line: 1316
from tensorflow.python.ops.array_ops import depth_to_space # line: 3779
from tensorflow.python.ops.array_ops import dequantize # line: 5859
from tensorflow.python.ops.array_ops import tensor_diag_part as diag_part # line: 2354
from tensorflow.python.ops.array_ops import edit_distance # line: 3490
from tensorflow.python.ops.array_ops import expand_dims # line: 318
from tensorflow.python.ops.array_ops import extract_image_patches # line: 6258
from tensorflow.python.ops.array_ops import fill # line: 204
from tensorflow.python.ops.array_ops import fingerprint # line: 6307
from tensorflow.python.ops.array_ops import gather # line: 4747
from tensorflow.python.ops.array_ops import gather_nd # line: 5122
from tensorflow.python.ops.array_ops import guarantee_const # line: 6646
from tensorflow.python.ops.array_ops import identity # line: 253
from tensorflow.python.ops.array_ops import matrix_diag # line: 2042
from tensorflow.python.ops.array_ops import matrix_diag_part # line: 2211
from tensorflow.python.ops.array_ops import matrix_set_diag # line: 2399
from tensorflow.python.ops.array_ops import matrix_transpose # line: 1962
from tensorflow.python.ops.array_ops import meshgrid # line: 3344
from tensorflow.python.ops.array_ops import newaxis # line: 60
from tensorflow.python.ops.array_ops import one_hot # line: 3954
from tensorflow.python.ops.array_ops import ones # line: 2883
from tensorflow.python.ops.array_ops import ones_like # line: 2781
from tensorflow.python.ops.array_ops import pad # line: 3222
from tensorflow.python.ops.array_ops import parallel_stack # line: 1134
from tensorflow.python.ops.array_ops import placeholder # line: 2942
from tensorflow.python.ops.array_ops import placeholder_with_default # line: 2997
from tensorflow.python.ops.array_ops import quantize # line: 5820
from tensorflow.python.ops.array_ops import quantize_v2 # line: 5766
from tensorflow.python.ops.array_ops import rank # line: 877
from tensorflow.python.ops.array_ops import repeat # line: 6592
from tensorflow.python.ops.array_ops import required_space_to_batch_paddings # line: 3648
from tensorflow.python.ops.array_ops import reshape # line: 63
from tensorflow.python.ops.array_ops import reverse_sequence # line: 4624
from tensorflow.python.ops.array_ops import searchsorted # line: 6050
from tensorflow.python.ops.array_ops import sequence_mask # line: 4132
from tensorflow.python.ops.array_ops import setdiff1d # line: 482
from tensorflow.python.ops.array_ops import shape # line: 657
from tensorflow.python.ops.array_ops import shape_n # line: 730
from tensorflow.python.ops.array_ops import size # line: 800
from tensorflow.python.ops.array_ops import slice # line: 938
from tensorflow.python.ops.array_ops import space_to_batch # line: 3727
from tensorflow.python.ops.array_ops import space_to_depth # line: 3760
from tensorflow.python.ops.array_ops import sparse_mask # line: 1565
from tensorflow.python.ops.array_ops import sparse_placeholder # line: 3049
from tensorflow.python.ops.array_ops import split # line: 1710
from tensorflow.python.ops.array_ops import squeeze # line: 4199
from tensorflow.python.ops.array_ops import stop_gradient # line: 6665
from tensorflow.python.ops.array_ops import strided_slice # line: 994
from tensorflow.python.ops.array_ops import tensor_scatter_nd_update # line: 5477
from tensorflow.python.ops.array_ops import tensor_scatter_nd_update as tensor_scatter_update # line: 5477
from tensorflow.python.ops.array_ops import transpose # line: 1873
from tensorflow.python.ops.array_ops import unique # line: 1609
from tensorflow.python.ops.array_ops import unique_with_counts # line: 1657
from tensorflow.python.ops.array_ops import where # line: 4330
from tensorflow.python.ops.array_ops import where_v2 # line: 4411
from tensorflow.python.ops.array_ops import zeros # line: 2565
from tensorflow.python.ops.array_ops import zeros_like # line: 2627
from tensorflow.python.ops.array_ops_stack import stack # line: 24
from tensorflow.python.ops.array_ops_stack import unstack # line: 88
from tensorflow.python.ops.batch_ops import batch_function as nondifferentiable_batch_function # line: 28
from tensorflow.python.ops.bincount_ops import bincount_v1 as bincount # line: 190
from tensorflow.python.ops.check_ops import assert_equal # line: 770
from tensorflow.python.ops.check_ops import assert_greater # line: 987
from tensorflow.python.ops.check_ops import assert_greater_equal # line: 1005
from tensorflow.python.ops.check_ops import assert_integer # line: 1448
from tensorflow.python.ops.check_ops import assert_less # line: 950
from tensorflow.python.ops.check_ops import assert_less_equal # line: 968
from tensorflow.python.ops.check_ops import assert_near # line: 858
from tensorflow.python.ops.check_ops import assert_negative # line: 576
from tensorflow.python.ops.check_ops import assert_non_negative # line: 685
from tensorflow.python.ops.check_ops import assert_non_positive # line: 741
from tensorflow.python.ops.check_ops import assert_none_equal # line: 792
from tensorflow.python.ops.check_ops import assert_positive # line: 630
from tensorflow.python.ops.check_ops import assert_proper_iterable # line: 511
from tensorflow.python.ops.check_ops import assert_rank # line: 1098
from tensorflow.python.ops.check_ops import assert_rank_at_least # line: 1196
from tensorflow.python.ops.check_ops import assert_rank_in # line: 1362
from tensorflow.python.ops.check_ops import assert_same_float_dtype # line: 2119
from tensorflow.python.ops.check_ops import assert_scalar # line: 2177
from tensorflow.python.ops.check_ops import assert_type # line: 1522
from tensorflow.python.ops.check_ops import ensure_shape # line: 2219
from tensorflow.python.ops.check_ops import is_non_decreasing # line: 1989
from tensorflow.python.ops.check_ops import is_numeric_tensor # line: 1954
from tensorflow.python.ops.check_ops import is_strictly_increasing # line: 2030
from tensorflow.python.ops.clip_ops import clip_by_average_norm # line: 400
from tensorflow.python.ops.clip_ops import clip_by_global_norm # line: 298
from tensorflow.python.ops.clip_ops import clip_by_norm # line: 152
from tensorflow.python.ops.clip_ops import clip_by_value # line: 34
from tensorflow.python.ops.clip_ops import global_norm # line: 245
from tensorflow.python.ops.cond import cond # line: 39
from tensorflow.python.ops.confusion_matrix import confusion_matrix_v1 as confusion_matrix # line: 199
from tensorflow.python.ops.control_flow_assert import Assert # line: 62
from tensorflow.python.ops.control_flow_case import case # line: 138
from tensorflow.python.ops.control_flow_ops import group # line: 1958
from tensorflow.python.ops.control_flow_ops import tuple # line: 2106
from tensorflow.python.ops.control_flow_switch_case import switch_case # line: 181
from tensorflow.python.ops.control_flow_v2_toggles import control_flow_v2_enabled # line: 63
from tensorflow.python.ops.control_flow_v2_toggles import disable_control_flow_v2 # line: 47
from tensorflow.python.ops.control_flow_v2_toggles import enable_control_flow_v2 # line: 24
from tensorflow.python.ops.critical_section_ops import CriticalSection # line: 121
from tensorflow.python.ops.custom_gradient import custom_gradient # line: 45
from tensorflow.python.ops.custom_gradient import grad_pass_through # line: 777
from tensorflow.python.ops.custom_gradient import recompute_grad # line: 604
from tensorflow.python.ops.data_flow_ops import ConditionalAccumulator # line: 1321
from tensorflow.python.ops.data_flow_ops import ConditionalAccumulatorBase # line: 1241
from tensorflow.python.ops.data_flow_ops import FIFOQueue # line: 712
from tensorflow.python.ops.data_flow_ops import PaddingFIFOQueue # line: 848
from tensorflow.python.ops.data_flow_ops import PriorityQueue # line: 924
from tensorflow.python.ops.data_flow_ops import QueueBase # line: 115
from tensorflow.python.ops.data_flow_ops import RandomShuffleQueue # line: 622
from tensorflow.python.ops.data_flow_ops import SparseConditionalAccumulator # line: 1412
from tensorflow.python.ops.functional_ops import foldl # line: 42
from tensorflow.python.ops.functional_ops import foldr # line: 238
from tensorflow.python.ops.functional_ops import scan # line: 435
from tensorflow.python.ops.gradients_impl import gradients # line: 55
from tensorflow.python.ops.gradients_impl import hessians # line: 388
from tensorflow.python.ops.gradients_util import AggregationMethod # line: 943
from tensorflow.python.ops.histogram_ops import histogram_fixed_width # line: 103
from tensorflow.python.ops.histogram_ops import histogram_fixed_width_bins # line: 31
from tensorflow.python.ops.init_ops import Constant as constant_initializer # line: 219
from tensorflow.python.ops.init_ops import GlorotNormal as glorot_normal_initializer # line: 1627
from tensorflow.python.ops.init_ops import GlorotUniform as glorot_uniform_initializer # line: 1595
from tensorflow.python.ops.init_ops import Ones as ones_initializer # line: 182
from tensorflow.python.ops.init_ops import Orthogonal as orthogonal_initializer # line: 895
from tensorflow.python.ops.init_ops import RandomNormal as random_normal_initializer # line: 487
from tensorflow.python.ops.init_ops import RandomUniform as random_uniform_initializer # line: 397
from tensorflow.python.ops.init_ops import TruncatedNormal as truncated_normal_initializer # line: 577
from tensorflow.python.ops.init_ops import UniformUnitScaling as uniform_unit_scaling_initializer # line: 673
from tensorflow.python.ops.init_ops import VarianceScaling as variance_scaling_initializer # line: 741
from tensorflow.python.ops.init_ops import Zeros as zeros_initializer # line: 97
from tensorflow.python.ops.io_ops import FixedLengthRecordReader # line: 495
from tensorflow.python.ops.io_ops import IdentityReader # line: 605
from tensorflow.python.ops.io_ops import LMDBReader # line: 575
from tensorflow.python.ops.io_ops import ReaderBase # line: 217
from tensorflow.python.ops.io_ops import TFRecordReader # line: 541
from tensorflow.python.ops.io_ops import TextLineReader # line: 462
from tensorflow.python.ops.io_ops import WholeFileReader # line: 431
from tensorflow.python.ops.io_ops import read_file # line: 97
from tensorflow.python.ops.io_ops import serialize_tensor # line: 137
from tensorflow.python.ops.linalg_ops import cholesky_solve # line: 147
from tensorflow.python.ops.linalg_ops import eye # line: 196
from tensorflow.python.ops.linalg_ops import matrix_solve_ls # line: 244
from tensorflow.python.ops.linalg_ops import matrix_triangular_solve # line: 84
from tensorflow.python.ops.linalg_ops import norm # line: 633
from tensorflow.python.ops.linalg_ops import self_adjoint_eig # line: 441
from tensorflow.python.ops.linalg_ops import self_adjoint_eigvals # line: 465
from tensorflow.python.ops.linalg_ops import svd # line: 489
from tensorflow.python.ops.logging_ops import Print # line: 75
from tensorflow.python.ops.logging_ops import print_v2 as print # line: 147
from tensorflow.python.ops.lookup_ops import initialize_all_tables # line: 52
from tensorflow.python.ops.lookup_ops import tables_initializer # line: 67
from tensorflow.python.ops.manip_ops import roll # line: 27
from tensorflow.python.ops.map_fn import map_fn # line: 41
from tensorflow.python.ops.math_ops import abs # line: 359
from tensorflow.python.ops.math_ops import accumulate_n # line: 3976
from tensorflow.python.ops.math_ops import acos # line: 5562
from tensorflow.python.ops.math_ops import add # line: 3835
from tensorflow.python.ops.math_ops import add_n # line: 3916
from tensorflow.python.ops.math_ops import angle # line: 863
from tensorflow.python.ops.math_ops import arg_max # line: 231
from tensorflow.python.ops.math_ops import arg_min # line: 232
from tensorflow.python.ops.math_ops import argmax # line: 245
from tensorflow.python.ops.math_ops import argmin # line: 299
from tensorflow.python.ops.math_ops import cast # line: 938
from tensorflow.python.ops.math_ops import ceil # line: 5392
from tensorflow.python.ops.math_ops import complex # line: 693
from tensorflow.python.ops.math_ops import conj # line: 4349
from tensorflow.python.ops.math_ops import count_nonzero # line: 2269
from tensorflow.python.ops.math_ops import cumprod # line: 4239
from tensorflow.python.ops.math_ops import cumsum # line: 4167
from tensorflow.python.ops.math_ops import div # line: 1488
from tensorflow.python.ops.math_ops import div_no_nan # line: 1520
from tensorflow.python.ops.math_ops import divide # line: 440
from tensorflow.python.ops.math_ops import equal # line: 1784
from tensorflow.python.ops.math_ops import exp # line: 5459
from tensorflow.python.ops.math_ops import floor # line: 5593
from tensorflow.python.ops.math_ops import floordiv # line: 1628
from tensorflow.python.ops.math_ops import imag # line: 829
from tensorflow.python.ops.math_ops import linspace_nd as lin_space # line: 111
from tensorflow.python.ops.math_ops import linspace_nd as linspace # line: 111
from tensorflow.python.ops.math_ops import log_sigmoid # line: 4122
from tensorflow.python.ops.math_ops import logical_xor # line: 1708
from tensorflow.python.ops.math_ops import matmul # line: 3394
from tensorflow.python.ops.math_ops import multiply # line: 475
from tensorflow.python.ops.math_ops import not_equal # line: 1821
from tensorflow.python.ops.math_ops import pow # line: 663
from tensorflow.python.ops.math_ops import range # line: 1940
from tensorflow.python.ops.math_ops import real # line: 788
from tensorflow.python.ops.math_ops import reduce_all_v1 as reduce_all # line: 3025
from tensorflow.python.ops.math_ops import reduce_any_v1 as reduce_any # line: 3131
from tensorflow.python.ops.math_ops import reduce_logsumexp_v1 as reduce_logsumexp # line: 3237
from tensorflow.python.ops.math_ops import reduce_max_v1 as reduce_max # line: 2900
from tensorflow.python.ops.math_ops import reduce_mean_v1 as reduce_mean # line: 2423
from tensorflow.python.ops.math_ops import reduce_min_v1 as reduce_min # line: 2772
from tensorflow.python.ops.math_ops import reduce_prod_v1 as reduce_prod # line: 2713
from tensorflow.python.ops.math_ops import reduce_sum_v1 as reduce_sum # line: 2066
from tensorflow.python.ops.math_ops import round # line: 908
from tensorflow.python.ops.math_ops import rsqrt # line: 5537
from tensorflow.python.ops.math_ops import saturate_cast # line: 1023
from tensorflow.python.ops.math_ops import scalar_mul # line: 586
from tensorflow.python.ops.math_ops import sigmoid # line: 4069
from tensorflow.python.ops.math_ops import sign # line: 741
from tensorflow.python.ops.math_ops import sparse_matmul # line: 3772
from tensorflow.python.ops.math_ops import sparse_segment_mean # line: 4757
from tensorflow.python.ops.math_ops import sparse_segment_sqrt_n # line: 4869
from tensorflow.python.ops.math_ops import sparse_segment_sum # line: 4585
from tensorflow.python.ops.math_ops import sqrt # line: 5420
from tensorflow.python.ops.math_ops import subtract # line: 539
from tensorflow.python.ops.math_ops import tensordot # line: 4967
from tensorflow.python.ops.math_ops import to_bfloat16 # line: 1266
from tensorflow.python.ops.math_ops import to_complex128 # line: 1346
from tensorflow.python.ops.math_ops import to_complex64 # line: 1306
from tensorflow.python.ops.math_ops import to_double # line: 1146
from tensorflow.python.ops.math_ops import to_float # line: 1106
from tensorflow.python.ops.math_ops import to_int32 # line: 1186
from tensorflow.python.ops.math_ops import to_int64 # line: 1226
from tensorflow.python.ops.math_ops import trace # line: 3350
from tensorflow.python.ops.math_ops import truediv # line: 1454
from tensorflow.python.ops.math_ops import unsorted_segment_mean # line: 4472
from tensorflow.python.ops.math_ops import unsorted_segment_sqrt_n # line: 4527
from tensorflow.python.ops.numerics import add_check_numerics_ops # line: 81
from tensorflow.python.ops.numerics import verify_tensor_all_finite # line: 28
from tensorflow.python.ops.parallel_for.control_flow_ops import vectorized_map # line: 452
from tensorflow.python.ops.parsing_config import FixedLenFeature # line: 298
from tensorflow.python.ops.parsing_config import FixedLenSequenceFeature # line: 318
from tensorflow.python.ops.parsing_config import SparseFeature # line: 223
from tensorflow.python.ops.parsing_config import VarLenFeature # line: 44
from tensorflow.python.ops.parsing_ops import decode_csv # line: 1018
from tensorflow.python.ops.parsing_ops import decode_json_example # line: 1147
from tensorflow.python.ops.parsing_ops import decode_raw_v1 as decode_raw # line: 973
from tensorflow.python.ops.parsing_ops import parse_example # line: 310
from tensorflow.python.ops.parsing_ops import parse_single_example # line: 370
from tensorflow.python.ops.parsing_ops import parse_single_sequence_example # line: 691
from tensorflow.python.ops.partitioned_variables import create_partitioned_variables # line: 275
from tensorflow.python.ops.partitioned_variables import fixed_size_partitioner # line: 220
from tensorflow.python.ops.partitioned_variables import min_max_variable_partitioner # line: 155
from tensorflow.python.ops.partitioned_variables import variable_axis_size_partitioner # line: 67
from tensorflow.python.ops.ragged.ragged_string_ops import string_split # line: 528
from tensorflow.python.ops.ragged.ragged_tensor import RaggedTensor # line: 65
from tensorflow.python.ops.ragged.ragged_tensor import RaggedTensorSpec # line: 2319
from tensorflow.python.ops.random_crop_ops import random_crop # line: 30
from tensorflow.python.ops.random_ops import multinomial # line: 362
from tensorflow.python.ops.random_ops import random_gamma # line: 451
from tensorflow.python.ops.random_ops import random_normal # line: 39
from tensorflow.python.ops.random_ops import random_poisson # line: 545
from tensorflow.python.ops.random_ops import random_shuffle # line: 326
from tensorflow.python.ops.random_ops import random_uniform # line: 211
from tensorflow.python.ops.random_ops import truncated_normal # line: 155
from tensorflow.python.ops.resource_variables_toggle import disable_resource_variables # line: 55
from tensorflow.python.ops.resource_variables_toggle import enable_resource_variables # line: 31
from tensorflow.python.ops.resource_variables_toggle import resource_variables_enabled # line: 68
from tensorflow.python.ops.script_ops import numpy_function # line: 804
from tensorflow.python.ops.script_ops import py_func # line: 795
from tensorflow.python.ops.script_ops import eager_py_func as py_function # line: 461
from tensorflow.python.ops.session_ops import delete_session_tensor # line: 219
from tensorflow.python.ops.session_ops import get_session_handle # line: 135
from tensorflow.python.ops.session_ops import get_session_tensor # line: 178
from tensorflow.python.ops.sort_ops import argsort # line: 86
from tensorflow.python.ops.sort_ops import sort # line: 29
from tensorflow.python.ops.sparse_ops import deserialize_many_sparse # line: 2356
from tensorflow.python.ops.sparse_ops import serialize_many_sparse # line: 2224
from tensorflow.python.ops.sparse_ops import serialize_sparse # line: 2176
from tensorflow.python.ops.sparse_ops import sparse_add # line: 460
from tensorflow.python.ops.sparse_ops import sparse_concat # line: 284
from tensorflow.python.ops.sparse_ops import sparse_fill_empty_rows # line: 2109
from tensorflow.python.ops.sparse_ops import sparse_maximum # line: 2734
from tensorflow.python.ops.sparse_ops import sparse_merge # line: 1802
from tensorflow.python.ops.sparse_ops import sparse_minimum # line: 2780
from tensorflow.python.ops.sparse_ops import sparse_reduce_max # line: 1341
from tensorflow.python.ops.sparse_ops import sparse_reduce_max_sparse # line: 1427
from tensorflow.python.ops.sparse_ops import sparse_reduce_sum # line: 1559
from tensorflow.python.ops.sparse_ops import sparse_reduce_sum_sparse # line: 1628
from tensorflow.python.ops.sparse_ops import sparse_reorder # line: 821
from tensorflow.python.ops.sparse_ops import sparse_reset_shape # line: 2004
from tensorflow.python.ops.sparse_ops import sparse_reshape # line: 876
from tensorflow.python.ops.sparse_ops import sparse_retain # line: 1957
from tensorflow.python.ops.sparse_ops import sparse_slice # line: 1136
from tensorflow.python.ops.sparse_ops import sparse_softmax # line: 2671
from tensorflow.python.ops.sparse_ops import sparse_split # line: 991
from tensorflow.python.ops.sparse_ops import sparse_tensor_dense_matmul # line: 2430
from tensorflow.python.ops.sparse_ops import sparse_tensor_to_dense # line: 1681
from tensorflow.python.ops.sparse_ops import sparse_to_dense # line: 1186
from tensorflow.python.ops.sparse_ops import sparse_to_indicator # line: 1737
from tensorflow.python.ops.sparse_ops import sparse_transpose # line: 2824
from tensorflow.python.ops.special_math_ops import einsum # line: 618
from tensorflow.python.ops.special_math_ops import lbeta # line: 45
from tensorflow.python.ops.state_ops import assign # line: 277
from tensorflow.python.ops.state_ops import assign_add # line: 205
from tensorflow.python.ops.state_ops import assign_sub # line: 133
from tensorflow.python.ops.state_ops import batch_scatter_update # line: 946
from tensorflow.python.ops.state_ops import count_up_to # line: 359
from tensorflow.python.ops.state_ops import scatter_add # line: 499
from tensorflow.python.ops.state_ops import scatter_div # line: 784
from tensorflow.python.ops.state_ops import scatter_max # line: 836
from tensorflow.python.ops.state_ops import scatter_min # line: 891
from tensorflow.python.ops.state_ops import scatter_mul # line: 732
from tensorflow.python.ops.state_ops import scatter_nd_add # line: 551
from tensorflow.python.ops.state_ops import scatter_nd_sub # line: 668
from tensorflow.python.ops.state_ops import scatter_nd_update # line: 437
from tensorflow.python.ops.state_ops import scatter_sub # line: 614
from tensorflow.python.ops.state_ops import scatter_update # line: 383
from tensorflow.python.ops.string_ops import reduce_join # line: 305
from tensorflow.python.ops.string_ops import regex_replace # line: 74
from tensorflow.python.ops.string_ops import string_join # line: 551
from tensorflow.python.ops.string_ops import string_to_hash_bucket_v1 as string_to_hash_bucket # line: 536
from tensorflow.python.ops.string_ops import string_to_number_v1 as string_to_number # line: 491
from tensorflow.python.ops.string_ops import substr_deprecated as substr # line: 422
from tensorflow.python.ops.template import make_template # line: 33
from tensorflow.python.ops.tensor_array_ops import TensorArray # line: 971
from tensorflow.python.ops.tensor_array_ops import TensorArraySpec # line: 1363
from tensorflow.python.ops.unconnected_gradients import UnconnectedGradients # line: 22
from tensorflow.python.ops.variable_scope import AUTO_REUSE # line: 194
from tensorflow.python.ops.variable_scope import VariableScope # line: 1058
from tensorflow.python.ops.variable_scope import get_local_variable # line: 1725
from tensorflow.python.ops.variable_scope import get_variable # line: 1549
from tensorflow.python.ops.variable_scope import get_variable_scope # line: 1415
from tensorflow.python.ops.variable_scope import no_regularizer # line: 1051
from tensorflow.python.ops.variable_scope import variable_creator_scope_v1 as variable_creator_scope # line: 2643
from tensorflow.python.ops.variable_scope import variable_op_scope # line: 2531
from tensorflow.python.ops.variable_scope import variable_scope # line: 2091
from tensorflow.python.ops.variable_v1 import VariableV1 as Variable # line: 51
from tensorflow.python.ops.variable_v1 import is_variable_initialized # line: 24
from tensorflow.python.ops.variables import VariableAggregation # line: 141
from tensorflow.python.ops.variables import VariableSynchronization # line: 63
from tensorflow.python.ops.variables import all_variables # line: 1736
from tensorflow.python.ops.variables import assert_variables_initialized # line: 1951
from tensorflow.python.ops.variables import global_variables # line: 1701
from tensorflow.python.ops.variables import global_variables_initializer # line: 1897
from tensorflow.python.ops.variables import initialize_all_variables # line: 1916
from tensorflow.python.ops.variables import initialize_local_variables # line: 1943
from tensorflow.python.ops.variables import initialize_variables # line: 1889
from tensorflow.python.ops.variables import local_variables # line: 1761
from tensorflow.python.ops.variables import local_variables_initializer # line: 1924
from tensorflow.python.ops.variables import model_variables # line: 1789
from tensorflow.python.ops.variables import moving_average_variables # line: 1836
from tensorflow.python.ops.variables import report_uninitialized_variables # line: 1994
from tensorflow.python.ops.variables import trainable_variables # line: 1806
from tensorflow.python.ops.variables import variables_initializer # line: 1858
from tensorflow.python.ops.while_loop import while_loop # line: 255
from tensorflow.python.platform.tf_logging import get_logger # line: 93
from tensorflow.python.proto_exports import AttrValue # line: 26
from tensorflow.python.proto_exports import ConfigProto # line: 27
from tensorflow.python.proto_exports import Event # line: 28
from tensorflow.python.proto_exports import GPUOptions # line: 29
from tensorflow.python.proto_exports import GraphOptions # line: 30
from tensorflow.python.proto_exports import HistogramProto # line: 31
from tensorflow.python.proto_exports import LogMessage # line: 34
from tensorflow.python.proto_exports import MetaGraphDef # line: 35
from tensorflow.python.proto_exports import NameAttrList # line: 38
from tensorflow.python.proto_exports import NodeDef # line: 41
from tensorflow.python.proto_exports import OptimizerOptions # line: 42
from tensorflow.python.proto_exports import RunMetadata # line: 45
from tensorflow.python.proto_exports import RunOptions # line: 46
from tensorflow.python.proto_exports import SessionLog # line: 47
from tensorflow.python.proto_exports import Summary # line: 50
from tensorflow.python.proto_exports import SummaryMetadata # line: 56
from tensorflow.python.proto_exports import TensorInfo # line: 62



from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "", public_apis=None, deprecation=False,
      has_lite=False)


# Hook external TensorFlow modules.
_current_module = _sys.modules[__name__]

# Lazy-load estimator.
_estimator_module = "tensorflow_estimator.python.estimator.api._v1.estimator"
estimator = _LazyLoader("estimator", globals(), _estimator_module)
_module_dir = _module_util.get_parent_dir_for_name(_estimator_module)
if _module_dir:
  _current_module.__path__ = [_module_dir] + _current_module.__path__
setattr(_current_module, "estimator", estimator)

# Lazy load Keras v1
_tf_uses_legacy_keras = (
    _os.environ.get("TF_USE_LEGACY_KERAS", None) in ("true", "True", "1"))
setattr(_current_module, "keras", _KerasLazyLoader(globals(), mode="v1"))
if _tf_uses_legacy_keras:
  _module_dir = _module_util.get_parent_dir_for_name("tf_keras.api._v1.keras")
else:
  _module_dir = _module_util.get_parent_dir_for_name("keras.api._v1.keras")
_current_module.__path__ = [_module_dir] + _current_module.__path__


from tensorflow.python.platform import flags  # pylint: disable=g-import-not-at-top
_current_module.app.flags = flags  # pylint: disable=undefined-variable
setattr(_current_module, "flags", flags)

# Add module aliases from Keras to TF.
# Some tf endpoints actually lives under Keras.
_current_module.layers = _KerasLazyLoader(
    globals(),
    submodule="__internal__.legacy.layers",
    name="layers",
    mode="v1")
if _tf_uses_legacy_keras:
  _module_dir = _module_util.get_parent_dir_for_name(
      "tf_keras.api._v1.keras.__internal__.legacy.layers")
else:
  _module_dir = _module_util.get_parent_dir_for_name(
      "keras.api._v1.keras.__internal__.legacy.layers")
_current_module.__path__ = [_module_dir] + _current_module.__path__

_current_module.nn.rnn_cell = _KerasLazyLoader(
    globals(),
    submodule="__internal__.legacy.rnn_cell",
    name="rnn_cell",
    mode="v1")
if _tf_uses_legacy_keras:
  _module_dir = _module_util.get_parent_dir_for_name(
      "tf_keras.api._v1.keras.__internal__.legacy.rnn_cell")
else:
  _module_dir = _module_util.get_parent_dir_for_name(
      "keras.api._v1.keras.__internal__.legacy.rnn_cell")
_current_module.nn.__path__ = [_module_dir] + _current_module.nn.__path__

# Explicitly import lazy-loaded modules to support autocompletion.
# pylint: disable=g-import-not-at-top
if _typing.TYPE_CHECKING:
  from tensorflow_estimator.python.estimator.api._v1 import estimator as estimator
# pylint: enable=g-import-not-at-top
