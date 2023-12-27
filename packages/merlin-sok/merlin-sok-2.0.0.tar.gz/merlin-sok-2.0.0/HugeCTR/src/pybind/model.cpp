/*
 * Copyright (c) 2023, NVIDIA CORPORATION.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <cuda_profiler_api.h>

#include <algorithm>
#include <core/hctr_impl/hctr_backend.hpp>
#include <core23/logger.hpp>
#include <core23/mpi_init_service.hpp>
#include <core23_helper.hpp>
#include <core23_network.hpp>
#include <data_readers/async_reader/async_reader_adapter.hpp>
#include <data_readers/multi_hot/async_data_reader.hpp>
#include <embeddings/hybrid_sparse_embedding.hpp>
#include <fstream>
#include <iomanip>
#include <iterator>
#include <network_buffer_channels.hpp>
#include <pybind/model.hpp>
#include <resource_managers/resource_manager_ext.hpp>
#include <sstream>
using namespace HugeCTR::MultiHot;

namespace HugeCTR {

namespace {

/**
 * check if device is available.
 * lowest available CC is min_major.min_minor
 * @param device_id gpu id
 * @param min_major minimum compute compatibility required
 * @param min_minor minimum compute compatibility required
 */
// #define DATA_READING_TEST 1
static std::vector<std::string>& split(const std::string& s, char delim,
                                       std::vector<std::string>& elems) {
  std::istringstream is(s);
  std::string item;
  while (std::getline(is, item, delim)) {
    elems.push_back(item);
  }
  return elems;
}

static std::string join(std::vector<std::string>& strs, std::string delim) {
  std::string str;
  const std::vector<std::string>::iterator itlast = strs.end() - 1;
  for (auto it = strs.begin(); it != strs.end(); it++) {
    str += *it;
    if (it != itlast) {
      str += delim;
    }
  }
  return str;
}

static std::string get_tensor_shape(std::string tensor_name,
                                    std::map<std::string, std::vector<size_t>> tensor_shape_info) {
  std::string shape = "";
  if (tensor_shape_info.find(tensor_name) != tensor_shape_info.end()) {
    shape += "(";
    for (unsigned int i = 0; i < tensor_shape_info[tensor_name].size(); i++) {
      shape += std::to_string(tensor_shape_info[tensor_name][i]);
      shape += ",";
    }
    shape.back() = ')';
  }
  return shape;
}
static std::string get_tensor_shape(std::string tensor_name,
                                    std::map<std::string, core23::Shape> tensor_shape_info) {
  std::stringstream ss;
  if (tensor_shape_info.find(tensor_name) != tensor_shape_info.end()) {
    ss << tensor_shape_info[tensor_name];
  }
  return ss.str();
}

static void check_device(int device_id, int min_major, int min_minor) {
  int device_count = 0;
  HCTR_LIB_THROW(cudaGetDeviceCount(&device_count));
  if (device_id >= device_count) {
    HCTR_OWN_THROW(Error_t::WrongInput, "device is not available");
  }
  CudaDeviceContext context(device_id);
  cudaDeviceProp deviceProp;
  if (cudaGetDeviceProperties(&deviceProp, device_id) != cudaSuccess) {
    std::ostringstream os;
    os << "Invalid device:" << device_id;
    HCTR_OWN_THROW(Error_t::InvalidEnv, os.str());
    return;
  }
  HCTR_LOG(INFO, WORLD, "Device %d: %s\n", device_id, deviceProp.name);
  int major = deviceProp.major;
  int minor = deviceProp.minor;
  if (major < min_major) {
    HCTR_OWN_THROW(Error_t::InvalidEnv, "Device Compute Compacity is low");
  } else if (major == min_major && minor < min_minor) {
    HCTR_OWN_THROW(Error_t::InvalidEnv, "Device Compute Compacity is low");
  }
  return;
}

template <typename TypeKey>
auto load_key_files(std::vector<std::string> const& key_files) {
  std::vector<TypeKey> keys_vec;
  for (auto const& key_file : key_files) {
    auto key_file_size = std::filesystem::file_size(key_file);
    auto num_new_keys = key_file_size / sizeof(TypeKey);
    std::ifstream key_fs(key_file, std::ifstream::binary);
    if (!key_fs.is_open()) {
      HCTR_OWN_THROW(Error_t::WrongInput, "Cannot open the file: " + key_file);
    }
    auto num_exist_keys = keys_vec.size();
    keys_vec.resize(num_exist_keys + num_new_keys);
    key_fs.read(reinterpret_cast<char*>(&keys_vec[num_exist_keys]), key_file_size);
  }
  std::sort(keys_vec.begin(), keys_vec.end());
  keys_vec.erase(std::unique(keys_vec.begin(), keys_vec.end()), keys_vec.end());
  return keys_vec;
}

}  // end namespace

DenseLayerComputeConfig::DenseLayerComputeConfig() : async_wgrad(false), fuse_wb(false){};

DenseLayerComputeConfig::DenseLayerComputeConfig(bool async_wgrad, bool fuse_wb)
    : async_wgrad(async_wgrad), fuse_wb(fuse_wb){};

DataReaderParams::DataReaderParams(DataReaderType_t data_reader_type,
                                   std::vector<std::string> source, std::vector<std::string> keyset,
                                   std::string eval_source, Check_t check_type, int cache_eval_data,
                                   long long num_samples, long long eval_num_samples,
                                   bool float_label_dense, bool read_file_sequentially,
                                   int num_workers, std::vector<long long>& slot_size_array,
                                   const DataSourceParams& data_source_params,
                                   const AsyncParam& async_param)
    : data_reader_type(data_reader_type),
      source(source),
      keyset(keyset),
      eval_source(eval_source),
      check_type(check_type),
      cache_eval_data(cache_eval_data),
      num_samples(num_samples),
      eval_num_samples(eval_num_samples),
      float_label_dense(float_label_dense),
      read_file_sequentially(read_file_sequentially),
      num_workers(num_workers),
      slot_size_array(slot_size_array),
      data_source_params(data_source_params),
      async_param(async_param) {}

DataReaderParams::DataReaderParams(DataReaderType_t data_reader_type, std::string source,
                                   std::string keyset, std::string eval_source, Check_t check_type,
                                   int cache_eval_data, long long num_samples,
                                   long long eval_num_samples, bool float_label_dense,
                                   bool read_file_sequentially, int num_workers,
                                   std::vector<long long>& slot_size_array,
                                   const DataSourceParams& data_source_params,
                                   const AsyncParam& async_param)
    : data_reader_type(data_reader_type),
      eval_source(eval_source),
      check_type(check_type),
      cache_eval_data(cache_eval_data),
      num_samples(num_samples),
      eval_num_samples(eval_num_samples),
      float_label_dense(float_label_dense),
      read_file_sequentially(read_file_sequentially),
      num_workers(num_workers),
      slot_size_array(slot_size_array),
      data_source_params(data_source_params),
      async_param(async_param) {
  this->source.push_back(source);
  this->keyset.push_back(keyset);
}

Input::Input(int label_dim, std::string label_name, int dense_dim, std::string dense_name,
             std::vector<DataReaderSparseParam>& data_reader_sparse_param_array)
    : dense_dim(dense_dim),
      dense_name(dense_name),
      data_reader_sparse_param_array(data_reader_sparse_param_array) {
  labels_.insert(std::pair<std::string, int>(label_name, label_dim));
  label_weights_.insert(std::pair<std::string, float>(label_name, 1.0));
}

Input::Input(std::vector<int> label_dims, std::vector<std::string> label_names, int dense_dim,
             std::string dense_name,
             std::vector<DataReaderSparseParam>& data_reader_sparse_param_array)
    : dense_dim(dense_dim),
      dense_name(dense_name),
      data_reader_sparse_param_array(data_reader_sparse_param_array) {
  if (label_dims.size() != label_names.size()) {
    HCTR_OWN_THROW(Error_t::WrongInput,
                   "Number of label names does not match number of label dimensions.");
  }

  for (size_t i = 0; i < label_names.size(); ++i) {
    labels_.insert(std::pair<std::string, int>(label_names[i], label_dims[i]));
    label_weights_.insert(std::pair<std::string, float>(label_names[i], 1.0));
  }
}

Input::Input(std::vector<int> label_dims, std::vector<std::string> label_names,
             std::vector<float> label_weights, int dense_dim, std::string dense_name,
             std::vector<DataReaderSparseParam>& data_reader_sparse_param_array)
    : dense_dim(dense_dim),
      dense_name(dense_name),
      data_reader_sparse_param_array(data_reader_sparse_param_array) {
  if (label_dims.size() != label_names.size()) {
    HCTR_OWN_THROW(Error_t::WrongInput,
                   "Number of label names does not match number of label dimensions.");
  }

  for (size_t i = 0; i < label_names.size(); ++i) {
    labels_.insert(std::pair<std::string, int>(label_names[i], label_dims[i]));
    label_weights_.insert(std::pair<std::string, float>(label_names[i], label_weights[i]));
  }
}

SparseEmbedding::SparseEmbedding(Embedding_t embedding_type, size_t workspace_size_per_gpu_in_mb,
                                 size_t embedding_vec_size, const std::string& combiner_str,
                                 std::string sparse_embedding_name, std::string bottom_name,
                                 std::vector<size_t>& slot_size_array,
                                 std::shared_ptr<OptParamsPy>& embedding_opt_params,
                                 const HybridEmbeddingParam& hybrid_embedding_param)
    : embedding_type(embedding_type),
      workspace_size_per_gpu_in_mb(workspace_size_per_gpu_in_mb),
      embedding_vec_size(embedding_vec_size),
      sparse_embedding_name(sparse_embedding_name),
      bottom_name(bottom_name),
      slot_size_array(slot_size_array),
      embedding_opt_params(embedding_opt_params),
      hybrid_embedding_param(hybrid_embedding_param) {
  if (combiner_str == "sum") {
    combiner = 0;
  } else if (combiner_str == "mean") {
    combiner = 1;
  } else {
    HCTR_OWN_THROW(Error_t::WrongInput, "No such combiner type: " + combiner_str);
  }
  // should be match with HugeCTR/src/optimizers/sparse_optimizer.cu
  if (embedding_opt_params->initialized) {
    initialize_max_vocabulary_size_per_gpu();
  }
}

void SparseEmbedding::initialize_max_vocabulary_size_per_gpu() {
  size_t num_opt_state_copies =
      OptParams::num_parameters_per_weight(embedding_opt_params->optimizer);
  if (embedding_opt_params->optimizer == Optimizer_t::Adam &&
      embedding_opt_params->update_type == Update_t::LazyGlobal) {
    num_opt_state_copies += 1;
  }

  max_vocabulary_size_per_gpu = (workspace_size_per_gpu_in_mb * 1024 * 1024) /
                                ((1 + num_opt_state_copies) * sizeof(float) * embedding_vec_size);
}

DenseLayer::DenseLayer(
    Layer_t layer_type, std::vector<std::string>& bottom_names, std::vector<std::string>& top_names,
    float factor, float eps, Initializer_t gamma_init_type, Initializer_t beta_init_type,
    float dropout_rate, float elu_alpha, size_t num_output, Initializer_t weight_init_type,
    Initializer_t bias_init_type, int num_layers, size_t leading_dim, size_t time_step,
    size_t batchsize, size_t SeqLength, size_t vector_size, bool selected,
    std::vector<int> selected_slots, std::vector<std::pair<int, int>> ranges,
    std::vector<int> indices, std::vector<size_t> weight_dims, size_t projection_dim,
    size_t out_dim, int axis, int max_sequence_len_from, int max_sequence_len_to,
    int num_attention_heads, bool transpose_b, std::vector<float> target_weight_vec,
    bool use_regularizer, Regularizer_t regularizer_type, float lambda, FcPosition_t pos_type,
    Activation_t act_type, std::vector<size_t> num_outputs, bool use_bias,
    std::vector<Activation_t> acts, std::vector<bool> biases,
    DenseLayerComputeConfig compute_config, const std::vector<int64_t>& reshape_out_dimension,
    int dim, const std::vector<int64_t>& index)
    : layer_type(layer_type),
      bottom_names(bottom_names),
      top_names(top_names),
      factor(factor),
      eps(eps),
      gamma_init_type(gamma_init_type),
      beta_init_type(beta_init_type),
      dropout_rate(dropout_rate),
      elu_alpha(elu_alpha),
      num_output(num_output),
      weight_init_type(weight_init_type),
      bias_init_type(bias_init_type),
      num_layers(num_layers),
      leading_dim(leading_dim),
      time_step(time_step),
      batchsize(batchsize),
      SeqLength(SeqLength),
      vector_size(vector_size),
      selected(selected),
      selected_slots(selected_slots),
      ranges(ranges),
      indices(indices),
      weight_dims(weight_dims),
      projection_dim(projection_dim),
      out_dim(out_dim),
      axis(axis),
      max_sequence_len_from(max_sequence_len_from),
      max_sequence_len_to(max_sequence_len_to),
      num_attention_heads(num_attention_heads),
      transpose_b(transpose_b),
      target_weight_vec(target_weight_vec),
      use_regularizer(use_regularizer),
      regularizer_type(regularizer_type),
      lambda(lambda),
      pos_type(pos_type),
      act_type(act_type),
      num_outputs(num_outputs),
      use_bias(use_bias),
      acts(acts),
      biases(biases),
      compute_config(compute_config),
      reshape_out_dimension(reshape_out_dimension),
      dim(dim),
      index(index) {}

void init_optimizer_params(OptParams& opt_params, const Solver& solver,
                           const std::shared_ptr<OptParamsPy>& opt_params_py) {
  opt_params.optimizer = opt_params_py->optimizer;
  opt_params.lr = solver.lr;
  opt_params.update_type = opt_params_py->update_type;
  opt_params.scaler = solver.scaler;
  opt_params.hyperparams.ftrl.beta = opt_params_py->hyperparams.ftrl.beta;
  opt_params.hyperparams.ftrl.lambda1 = opt_params_py->hyperparams.ftrl.lambda1;
  opt_params.hyperparams.ftrl.lambda2 = opt_params_py->hyperparams.ftrl.lambda2;
  opt_params.hyperparams.adam.beta1 = opt_params_py->hyperparams.adam.beta1;
  opt_params.hyperparams.adam.beta2 = opt_params_py->hyperparams.adam.beta2;
  opt_params.hyperparams.adam.epsilon = opt_params_py->hyperparams.adam.epsilon;
  opt_params.hyperparams.adagrad.initial_accu_value =
      opt_params_py->hyperparams.adagrad.initial_accu_value;
  opt_params.hyperparams.adagrad.epsilon = opt_params_py->hyperparams.adagrad.epsilon;
  opt_params.hyperparams.momentum.factor = opt_params_py->hyperparams.momentum.factor;
  opt_params.hyperparams.nesterov.mu = opt_params_py->hyperparams.nesterov.mu;
  opt_params.hyperparams.sgd.atomic_update = opt_params_py->hyperparams.sgd.atomic_update;
}

void init_learning_rate_scheduler(std::shared_ptr<LearningRateScheduler>& lr_sch,
                                  const Solver& solver, GpuLearningRateSchedulers& gpu_lr_sches,
                                  const std::shared_ptr<ResourceManager>& resource_manager) {
  lr_sch.reset(new LearningRateScheduler(solver.lr, solver.warmup_steps, solver.decay_start,
                                         solver.decay_steps, solver.decay_power, solver.end_lr));
  for (size_t i = 0; i < resource_manager->get_local_gpu_count(); i++) {
    auto& gpu_resource = resource_manager->get_local_gpu(i);
    gpu_lr_sches.emplace_back(new GpuLearningRateScheduler(
        solver.lr, solver.warmup_steps, solver.decay_start, solver.decay_steps, solver.decay_power,
        solver.end_lr, gpu_resource));
  }
}

void init_exchange_wgrad(const std::shared_ptr<ResourceManager>& resource_manager,
                         std::shared_ptr<ExchangeWgrad>& exchange_wgrad, const Solver& solver) {
  HCTR_LOG(INFO, ROOT, "Using All-reduce algorithm: %s\n",
           ALLREDUCE_ALGO_TO_STRING[solver.all_reduce_algo].c_str());
  resource_manager->set_ar_comm(solver.all_reduce_algo, solver.use_mixed_precision);
  if (solver.grouped_all_reduce) {
    if (solver.use_mixed_precision) {
      exchange_wgrad = std::make_shared<GroupedExchangeWgrad<__half>>(resource_manager);
    } else {
      exchange_wgrad = std::make_shared<GroupedExchangeWgrad<float>>(resource_manager);
    }
  } else {
    if (solver.use_mixed_precision) {
      exchange_wgrad = std::make_shared<NetworkExchangeWgrad<__half>>(resource_manager);
    } else {
      exchange_wgrad = std::make_shared<NetworkExchangeWgrad<float>>(resource_manager);
    }
  }
}

Model::Model(const Solver& solver, const DataReaderParams& reader_params,
             std::shared_ptr<OptParamsPy>& opt_params_py)
    : solver_(solver),
      reader_params_(reader_params),
      opt_params_py_(opt_params_py),
      data_reader_train_status_(false),
      data_reader_eval_status_(false),
      buff_allocated_(false),
      is_dense_trainable_(true),
      embedding_dependent_(true),
      high_level_eval_(false),
      training_callbacks_(solver_.training_callbacks) {
  if (solver_.perf_logging) {
    timer_log.start();
    HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "init_start");
  }
  HCTR_PRINT(INFO, "HugeCTR Version: %d.%d\n", HUGECTR_VERSION_MAJOR, HUGECTR_VERSION_MINOR);
  HCTR_PRINT(INFO,
             "====================================================Model "
             "Init=====================================================\n");
  if (!solver_.model_name.length()) {
    HCTR_LOG(WARNING, ROOT, "The model name is not specified when creating the solver.\n");
  } else {
    HCTR_LOG(INFO, ROOT, "Initialize model: %s\n", solver_.model_name.c_str());
  }
  resource_manager_ = ResourceManagerExt::create(solver.vvgpu, solver.seed, solver.device_layout);

  embedding_para_io_ = std::shared_ptr<embedding::EmbeddingParameterIO>(
      new embedding::EmbeddingParameterIO(resource_manager_));
  init_exchange_wgrad(resource_manager_, exchange_wgrad_, solver_);

  graph_scheduler_ = std::make_unique<GraphScheduler>(resource_manager_);
  for (auto dev : resource_manager_->get_local_gpu_device_id_list()) {
    if (solver_.use_mixed_precision) {
      check_device(dev, 7,
                   0);  // to support mixed precision training earliest supported device is CC=70
    } else {
      check_device(dev, 6, 0);  // earliest supported device is CC=60
    }
  }
  if (reader_params_.source.size() < 1 || reader_params_.eval_source.empty()) {
    HCTR_OWN_THROW(Error_t::WrongInput,
                   " The data source for training and evaluation should be specified");
  }
  int total_gpu_count = resource_manager_->get_global_gpu_count();
  if (0 != solver_.batchsize % total_gpu_count) {
    HCTR_OWN_THROW(Error_t::WrongInput, "0 != batch_size\%total_gpu_count");
  }
  const auto overflow_check_env = std::getenv("HUGECTR_DISABLE_OVERFLOW_CHECK");
  if (nullptr != overflow_check_env && 1 == std::atoi(overflow_check_env)) {
    overflow_check_ = false;
  }

  create_networks();

  // initialize optimizer
  init_optimizer_params(opt_params_, solver_, opt_params_py);
  init_learning_rate_scheduler(lr_sch_, solver_, gpu_lr_sches_, resource_manager_);
}

Model::~Model() {
  for (auto device : resource_manager_->get_local_gpu_device_id_list()) {
    CudaDeviceContext context(device);
    HCTR_LIB_CHECK_(cudaDeviceSynchronize());
  }
}

void Model::graph_to_json(std::string graph_config_file) {
  if (!graph_finalized_) {
    graph_analysis();
    graph_finalized_ = true;
  }
  nlohmann::json graph_config;
  std::ofstream file_stream(graph_config_file);
  nlohmann::json layer_config_array = nlohmann::json::array();
  save_graph_to_json(layer_config_array, dense_layer_params_, sparse_embedding_params_,
                     input_params_, embedding_opt_params_list_, solver_.use_mixed_precision);
  graph_config["layers"] = layer_config_array;
  // The model_name in dumped JSON will only be used for inference currently
  if (solver_.model_name.length()) {
    graph_config["model_name"] = solver_.model_name;
  }
  file_stream << std::setw(2) << graph_config;
  file_stream.close();
  HCTR_LOG(INFO, ROOT, "Save the model graph to %s successfully\n", graph_config_file.c_str());
}

void Model::construct_from_json(const std::string& graph_config_file, bool include_dense_network) {
  nlohmann::json graph_config = read_json_file(graph_config_file);
  auto j_layers_array = get_json(graph_config, "layers");
  const nlohmann::json& j_input = j_layers_array[0];
  Input input = get_input_from_json(j_input);
  add(input);

  unsigned int dense_layer_start_index = 1;
  for (unsigned int i = 1; i < j_layers_array.size(); i++) {
    const nlohmann::json& j = j_layers_array[i];
    Embedding_t embedding_type;
    auto embedding_type_name = get_value_from_json<std::string>(j, "type");
    if (!find_item_in_map(embedding_type, embedding_type_name, EMBEDDING_TYPE_MAP)) {
      dense_layer_start_index = i;
      break;
    }
    SparseEmbedding sparse_embedding = get_sparse_embedding_from_json(j);
    add(sparse_embedding);
  }

  if (include_dense_network) {
    for (unsigned int i = dense_layer_start_index; i < j_layers_array.size(); i++) {
      const nlohmann::json& j = j_layers_array[i];
      Layer_t layer_type;
      auto layer_type_name = get_value_from_json<std::string>(j, "type");
      if (!find_item_in_map(layer_type, layer_type_name, LAYER_TYPE_MAP) &&
          !find_item_in_map(layer_type, layer_type_name, LAYER_TYPE_MAP_MP)) {
        HCTR_OWN_THROW(Error_t::WrongInput, "No such layer: " + layer_type_name);
      }
      DenseLayer dense_layer = get_dense_layer_from_json(j);
      add(dense_layer);
    }
  }

  HCTR_LOG(INFO, ROOT, "Load the model graph from %s successfully\n", graph_config_file.c_str());
}

// deep copy
void Model::create_copy_ops_for_network_input(const std::string& dense_name,
                                              const std::string& label_name, bool is_train) {
  auto& copy_ops = is_train ? graph_.train_copy_ops_ : graph_.evaluate_copy_ops_;
  auto& tensor_entries_list =
      is_train ? train_tensor_entities_list_ : evaluate_tensor_entities_list_;

  int num_local_gpus = resource_manager_->get_local_gpu_count();
  // copy ops for dense & label
  copy_ops.resize(2 * num_local_gpus);

  for (int id = 0; id < num_local_gpus; ++id) {
    core23::Device device(core23::DeviceType::GPU,
                          resource_manager_->get_local_gpu(id)->get_device_id());
    for (auto& tensor_entry : tensor_entries_list[id]) {
      if (tensor_entry.name == dense_name) {
        copy_ops[id].reset(
            new CopyOpImpl(resource_manager_->get_local_gpu(id), tensor_entry.tensor));
        tensor_entry.tensor = copy_ops[id]->get_tensorbag();
      } else if (tensor_entry.name == label_name) {
        copy_ops[id + num_local_gpus].reset(
            new CopyOpImpl(resource_manager_->get_local_gpu(id), tensor_entry.tensor));
        tensor_entry.tensor = copy_ops[id + num_local_gpus]->get_tensorbag();
      } else {
        HCTR_OWN_THROW(Error_t::WrongInput, "wrong tensor entry name when creating copy_op.");
      }
    }
  }
}

void Model::add(Input& input) {
  std::string label_name = input.labels_.begin()->first;
  int label_dim = input.labels_.begin()->second;

  // If multiple labels, treat them as 1 big label and add a split layer (below)
  if (input.labels_.size() > 1) {
    label_name = "combined_multi_label";
    label_dim = std::accumulate(std::begin(input.labels_), std::end(input.labels_), 0,
                                [](const int previous, const std::pair<std::string, int>& p) {
                                  return previous + p.second;
                                });
  }

  input_params_.push_back(input);
  activate_tensor(tensor_active_, label_name);
  activate_tensor(tensor_active_, input.dense_name);
  data_input_info_.push_back(label_name);
  data_input_info_.push_back(input.dense_name);
  tensor_shape_info_raw_.insert(
      std::make_pair(label_name, std::vector<int>{solver_.batchsize, label_dim}));
  tensor_shape_info_raw_.insert(
      std::make_pair(input.dense_name, std::vector<int>{solver_.batchsize, input.dense_dim}));
  if (solver_.use_embedding_collection) {
    std::vector<std::string> top_name_list;
    std::vector<int> nnz_per_slot;
    bool is_fixed_length = true;
    int num_slot = 0;
    for (size_t i = 0; i < input.data_reader_sparse_param_array.size(); ++i) {
      auto& p = input.data_reader_sparse_param_array[i];
      top_name_list.push_back(p.top_name);
      if (p.slot_num != 1) {
        HCTR_OWN_THROW(
            Error_t::WrongInput,
            "To use embedding collection, slots_num should be set to 1 in each sparse_param. "
            "Please refer to notebooks/embedding_collection.ipynb and separate your multi-slot "
            "output into multiple single-slot output");
      }
      nnz_per_slot.push_back(p.nnz_per_slot[0]);
      if (!p.is_fixed_length) is_fixed_length = false;
      num_slot += 1;
      hotness_map_.insert({p.top_name, p.max_feature_num});
    }
    std::string concat_top_name = join(top_name_list, ",");
    DataReaderSparseParam concat_data_reader_sparse_param{concat_top_name, nnz_per_slot,
                                                          is_fixed_length, num_slot};
    input.data_reader_sparse_param_array = {concat_data_reader_sparse_param};
  }
  std::vector<std::string> sparse_names;
  for (size_t i = 0; i < input.data_reader_sparse_param_array.size(); ++i) {
    sparse_names.push_back(input.data_reader_sparse_param_array[i].top_name);
    tensor_shape_info_raw_.insert(std::make_pair(
        input.data_reader_sparse_param_array[i].top_name,
        std::vector<int>{solver_.batchsize, input.data_reader_sparse_param_array[i].slot_num}));
  }
  data_input_info_.push_back(join(sparse_names, ","));
  for (unsigned int i = 0; i < input.data_reader_sparse_param_array.size(); i++) {
    activate_tensor(tensor_active_, input.data_reader_sparse_param_array[i].top_name);
  }
  if (solver_.i64_input_key) {
    add_input<long long>(input, reader_params_, sparse_input_map_64_, train_tensor_entities_list_,
                         evaluate_tensor_entities_list_, train_data_reader_, evaluate_data_reader_,
                         init_data_reader_, solver_.batchsize, solver_.batchsize_eval,
                         solver_.use_mixed_precision, solver_.repeat_dataset,
                         solver_.train_intra_iteration_overlap, solver_.num_iterations_statistics,
                         resource_manager_);
  } else {
    add_input<unsigned int>(input, reader_params_, sparse_input_map_32_,
                            train_tensor_entities_list_, evaluate_tensor_entities_list_,
                            train_data_reader_, evaluate_data_reader_, init_data_reader_,
                            solver_.batchsize, solver_.batchsize_eval, solver_.use_mixed_precision,
                            solver_.repeat_dataset, solver_.train_intra_iteration_overlap,
                            solver_.num_iterations_statistics, resource_manager_);
  }

  if (solver_.use_embedding_collection and solver_.train_inter_iteration_overlap) {
    create_copy_ops_for_network_input(input.dense_name, label_name, true);
  }
  if (solver_.use_embedding_collection and solver_.eval_inter_iteration_overlap) {
    create_copy_ops_for_network_input(input.dense_name, label_name, false);
  }

  // Add label weights to model
  for (std::map<std::string, float>::iterator iter = input.label_weights_.begin();
       iter != input.label_weights_.end(); ++iter) {
    label_weights_.insert(std::make_pair(iter->first, iter->second));
  }

  // If multiple labels provided, add a Slice layer to handle breaking up the label
  if (input.labels_.size() > 1) {
    std::vector<std::string> label_names;
    std::vector<std::pair<int, int>> ranges;
    int idx = 0;

    for (std::map<std::string, int>::iterator iter = input.labels_.begin();
         iter != input.labels_.end(); ++iter) {
      label_names.push_back(iter->first);
      if (iter->second < 1) {
        HCTR_OWN_THROW(Error_t::WrongInput, "Each label dimension must be at lesat 1.");
      }
      ranges.push_back(std::make_pair(idx, idx + iter->second));
      idx += iter->second;
    }
    std::vector<std::string> bottom_name{"combined_multi_label"};
    DenseLayer label_slice_layer = DenseLayer(Layer_t::Slice, bottom_name, label_names);
    label_slice_layer.ranges = ranges;

    add(label_slice_layer);
  }
}

void Model::add(SparseEmbedding& sparse_embedding) {
  if (resource_manager_->get_num_process() == 1 && solver_.grouped_all_reduce &&
      sparse_embedding.embedding_type == Embedding_t::HybridSparseEmbedding) {
    HCTR_DIE("Grouped all reduce for HybridEmbedding is not supported on single node\n");
  }
  if ((reader_params_.data_reader_type == DataReaderType_t::RawAsync &&
       sparse_embedding.embedding_type != Embedding_t::HybridSparseEmbedding) ||
      (reader_params_.data_reader_type != DataReaderType_t::RawAsync &&
       sparse_embedding.embedding_type == Embedding_t::HybridSparseEmbedding)) {
    HCTR_OWN_THROW(Error_t::WrongInput, "Raw async reader and hybrid embedding must come together");
  }
  OptParams embedding_opt_params;
  if (!(sparse_embedding.embedding_opt_params)->initialized) {
    sparse_embedding.embedding_opt_params = opt_params_py_;
    sparse_embedding.initialize_max_vocabulary_size_per_gpu();
  }
  sparse_embedding.max_vocabulary_size_global =
      sparse_embedding.max_vocabulary_size_per_gpu * resource_manager_->get_global_gpu_count();
  sparse_embedding_params_.push_back(sparse_embedding);
  deactivate_tensor(tensor_active_, sparse_embedding.bottom_name);
  activate_tensor(tensor_active_, sparse_embedding.sparse_embedding_name);
  int slot_num = tensor_shape_info_raw_[sparse_embedding.bottom_name][1];
  tensor_shape_info_raw_.insert(
      std::make_pair(sparse_embedding.sparse_embedding_name,
                     std::vector<int>{solver_.batchsize, slot_num,
                                      static_cast<int>(sparse_embedding.embedding_vec_size)}));
  input_output_info_.push_back(
      std::make_pair(sparse_embedding.bottom_name, sparse_embedding.sparse_embedding_name));
  layer_info_.push_back(EMBEDDING_TYPE_TO_STRING[sparse_embedding.embedding_type]);

  embedding_opt_params_list_.push_back(sparse_embedding.embedding_opt_params);
  init_optimizer_params(embedding_opt_params, solver_, sparse_embedding.embedding_opt_params);
  if (solver_.i64_input_key && !solver_.use_mixed_precision) {
    add_sparse_embedding<long long, float>(
        sparse_embedding, sparse_input_map_64_, train_tensor_entities_list_,
        evaluate_tensor_entities_list_, embeddings_, resource_manager_, solver_.batchsize,
        solver_.batchsize_eval, embedding_opt_params, exchange_wgrad_, solver_.use_cuda_graph,
        solver_.grouped_all_reduce, solver_.num_iterations_statistics, gpu_lr_sches_);
  } else if (solver_.i64_input_key && solver_.use_mixed_precision) {
    add_sparse_embedding<long long, __half>(
        sparse_embedding, sparse_input_map_64_, train_tensor_entities_list_,
        evaluate_tensor_entities_list_, embeddings_, resource_manager_, solver_.batchsize,
        solver_.batchsize_eval, embedding_opt_params, exchange_wgrad_, solver_.use_cuda_graph,
        solver_.grouped_all_reduce, solver_.num_iterations_statistics, gpu_lr_sches_);
  } else if (!solver_.i64_input_key && !solver_.use_mixed_precision) {
    add_sparse_embedding<unsigned int, float>(
        sparse_embedding, sparse_input_map_32_, train_tensor_entities_list_,
        evaluate_tensor_entities_list_, embeddings_, resource_manager_, solver_.batchsize,
        solver_.batchsize_eval, embedding_opt_params, exchange_wgrad_, solver_.use_cuda_graph,
        solver_.grouped_all_reduce, solver_.num_iterations_statistics, gpu_lr_sches_);
  } else {
    add_sparse_embedding<unsigned int, __half>(
        sparse_embedding, sparse_input_map_32_, train_tensor_entities_list_,
        evaluate_tensor_entities_list_, embeddings_, resource_manager_, solver_.batchsize,
        solver_.batchsize_eval, embedding_opt_params, exchange_wgrad_, solver_.use_cuda_graph,
        solver_.grouped_all_reduce, solver_.num_iterations_statistics, gpu_lr_sches_);
  }
  embeddings_map_.insert(
      std::make_pair(sparse_embedding.sparse_embedding_name, embeddings_.back()));
  embedding_dependent_tensors_.insert(sparse_embedding.sparse_embedding_name);
}

void Model::add(DenseLayer& dense_layer) {
  for (auto& top_name : dense_layer.top_names) {
    if (tensor_shape_info_raw_.find(top_name) != tensor_shape_info_raw_.end()) {
      HCTR_OWN_THROW(Error_t::WrongInput, top_name + ", top tensor name already exists");
    }
  }
  for (auto& bottom_name : dense_layer.bottom_names) {
    if (tensor_shape_info_raw_.find(bottom_name) == tensor_shape_info_raw_.end()) {
      HCTR_OWN_THROW(Error_t::WrongInput, bottom_name + ", bottom tensor name does not exists");
    }
  }
  calculate_tensor_dimensions(tensor_shape_info_raw_, dense_layer);
  dense_layer_params_raw_.push_back(dense_layer);
}

template <typename emb_t>
void allocate_ebc_output_helper_for_feature_major(
    std::shared_ptr<ResourceManager> resource_manager_, size_t batch_size_per_gpu,
    const EmbeddingCollectionConfig& ebc_config,
    const embedding::EmbeddingCollectionParam& ebc_param,
    std::vector<std::vector<TensorEntity>>& tensor_entries_list_,
    std::vector<core23::Tensor>& ebc_output) {
  HCTR_CHECK(ebc_config.output_layout_ == embedding::EmbeddingLayout::FeatureMajor);
  int num_local_gpus = resource_manager_->get_local_gpu_count();
  for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
    CudaDeviceContext context(resource_manager_->get_local_gpu(local_gpu_id)->get_device_id());
    core23::Device device(core23::DeviceType::GPU,
                          resource_manager_->get_local_gpu(local_gpu_id)->get_device_id());
    auto buffer_channel = core23::GetRandomBufferChannel();
    core23::Tensor head_tensor;
    core23::BufferParams buffer_param{.channel = buffer_channel};
    core23::TensorParams tensor_param = core23::TensorParams().buffer_params(buffer_param);
    int64_t concat_dims = 0;
    for (int lookup_id = 0; lookup_id < ebc_param.num_lookup; ++lookup_id) {
      const embedding::LookupParam& lookup_param = ebc_param.lookup_params[lookup_id];
      std::string top_name = ebc_config.top_names_[lookup_id];
      int64_t emb_out_dims = (lookup_param.combiner == embedding::Combiner::Concat)
                                 ? lookup_param.max_hotness * lookup_param.ev_size
                                 : lookup_param.ev_size;

      core23::Tensor tmp_tensor(tensor_param.shape({(int64_t)batch_size_per_gpu, 1ll, emb_out_dims})
                                    .device(device)
                                    .data_type(core23::ToScalarType<emb_t>::value));
      concat_dims += emb_out_dims;
      tensor_entries_list_[local_gpu_id].push_back({top_name, tmp_tensor});
      if (!lookup_id) {
        head_tensor = tmp_tensor;
      }
    }
    // allocate
    void* starting_address = head_tensor.data();
    core23::Tensor continous_emb_output = core23::Tensor::bind(
        starting_address, core23::Shape({static_cast<int64_t>(batch_size_per_gpu), concat_dims}),
        core23::ToScalarType<emb_t>::value, device);
    ebc_output.push_back(continous_emb_output);
  }
}

template <typename emb_t>
void allocate_ebc_output_helper_for_batch_major(
    std::shared_ptr<ResourceManager> resource_manager_, size_t batch_size_per_gpu,
    const EmbeddingCollectionConfig& ebc_config,
    const embedding::EmbeddingCollectionParam& ebc_param,
    std::vector<std::vector<TensorEntity>>& tensor_entries_list_,
    std::vector<core23::Tensor>& ebc_output) {
  int num_local_gpus = resource_manager_->get_local_gpu_count();
  for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
    CudaDeviceContext context(resource_manager_->get_local_gpu(local_gpu_id)->get_device_id());

    core23::Device device(core23::DeviceType::GPU,
                          resource_manager_->get_local_gpu(local_gpu_id)->get_device_id());
    core23::TensorParams tensor_param;
    int64_t emb_out_dims = 0;
    for (int lookup_id = 0; lookup_id < ebc_param.num_lookup; ++lookup_id) {
      const embedding::LookupParam& lookup_param = ebc_param.lookup_params[lookup_id];

      emb_out_dims += (lookup_param.combiner == embedding::Combiner::Concat)
                          ? lookup_param.max_hotness * lookup_param.ev_size
                          : lookup_param.ev_size;
    }

    core23::Tensor continous_emb_output(
        tensor_param.shape({(int64_t)batch_size_per_gpu, emb_out_dims})
            .device(device)
            .data_type(core23::ToScalarType<emb_t>::value));
    continous_emb_output.data();
    ebc_output.push_back(continous_emb_output);

    tensor_entries_list_[local_gpu_id].push_back(
        {ebc_config.batch_major_output_name_, continous_emb_output});
  }
}

std::vector<int> get_table_id_to_vocabulary_size(
    const std::vector<embedding::EmbeddingTableParam>& table_params, bool need_vocabulary_size) {
  // indices only need to initialize table offset
  if (!need_vocabulary_size) {
    return {};
  }

  // 2. init table_id_to_vocabulary_size and check if there is dynamic table
  std::vector<int> table_id_to_vocabulary_size;
  std::transform(table_params.begin(), table_params.end(),
                 std::back_inserter(table_id_to_vocabulary_size),
                 [](const embedding::EmbeddingTableParam& table_param) {
                   return table_param.max_vocabulary_size;
                 });

  std::for_each(table_id_to_vocabulary_size.begin(), table_id_to_vocabulary_size.end(),
                [](int vocabulary_size) {
                  HCTR_CHECK_HINT(vocabulary_size > 0, "vocabuary_size should > 0.");
                });
  return table_id_to_vocabulary_size;
}

void Model::add(const EmbeddingCollectionConfig& user_ebc_config) {
  auto ebc_config = split_column_wise_sharding_config(user_ebc_config);
  TableNameToIDDict table_name_to_id_dict =
      create_table_name_to_id_dict_from_ebc_config(ebc_config);
  int global_ebc_id = static_cast<int>(ebc_list_.size());
  for (auto& [name, id] : table_name_to_id_dict) {
    HCTR_CHECK_HINT(ebc_name_to_global_id_dict_.find(name) == ebc_name_to_global_id_dict_.end(),
                    "Duplicate table name: ", name, "\n");
    ebc_name_to_global_id_dict_[name] = {global_ebc_id, id};
  }
  int num_total_gpus = resource_manager_->get_global_gpu_count();
  int num_local_gpus = resource_manager_->get_local_gpu_count();

  int num_lookup = ebc_config.lookup_configs_.size();
  core23::DataType key_type =
      solver_.i64_input_key ? core23::ScalarType::Int64 : core23::ScalarType::UInt32;
  core23::DataType index_type =
      solver_.i64_input_key ? core23::ScalarType::UInt64 : core23::ScalarType::UInt32;
  core23::DataType offset_type =
      solver_.i64_input_key ? core23::ScalarType::Int64 : core23::ScalarType::UInt32;
  core23::DataType emb_type =
      solver_.use_mixed_precision ? core23::ScalarType::Half : core23::ScalarType::Float;
  core23::DataType wgrad_type =
      solver_.use_mixed_precision ? core23::ScalarType::Half : core23::ScalarType::Float;
  embedding::EmbeddingLayout input_layout_ =
      reader_params_.data_reader_type == DataReaderType_t::RawAsync
          ? embedding::EmbeddingLayout::FeatureMajor
          : embedding::EmbeddingLayout::BatchMajor;

  std::vector<std::string> bottom_name_list;
  for (auto& bottom_name : ebc_config.bottom_names_) {
    bottom_name_list.push_back(bottom_name);
  }

  std::string bottom_name = join(bottom_name_list, ",");
  deactivate_tensor(tensor_active_, bottom_name);

  layer_info_.push_back("EmbeddingCollection" + std::to_string(ebc_list_.size()));

  auto lookup_params = create_lookup_params_from_ebc_config(table_name_to_id_dict, ebc_config);
  for (int lookup_id = 0; lookup_id < num_lookup; ++lookup_id) {
    auto b_name = ebc_config.bottom_names_[ebc_config.dr_lookup_ids_[lookup_id]];
    lookup_params[lookup_id].max_hotness = hotness_map_[b_name];
  }

  auto shard_matrix = create_shard_matrix_from_ebc_config(table_name_to_id_dict, ebc_config);

  auto grouped_emb_params =
      create_grouped_embedding_param_from_ebc_config(table_name_to_id_dict, ebc_config);

  int num_table = ebc_config.emb_table_config_list_.size();
  auto emb_table_list = create_table_params_from_ebc_config(table_name_to_id_dict, ebc_config);
  for (auto& p : emb_table_list) {
    if (p.opt_param.optimizer == Optimizer_t::NOT_INITIALIZED) {
      p.opt_param = opt_params_;
    }
  }

  embedding::AllreduceStrategy allreduce_strategy = ebc_config.allreduce_strategy_;
  if (solver_.grouped_all_reduce) {
    allreduce_strategy = embedding::AllreduceStrategy::GroupDense;
  }

  auto compression_param =
      create_compression_param_from_ebc_config(table_name_to_id_dict, ebc_config);
  embedding::EmbeddingCollectionParam ebc_param{num_table,
                                                num_lookup,
                                                lookup_params,
                                                shard_matrix,
                                                grouped_emb_params,
                                                solver_.batchsize,
                                                key_type,
                                                index_type,
                                                offset_type,
                                                emb_type,
                                                wgrad_type,
                                                input_layout_,
                                                ebc_config.output_layout_,
                                                ebc_config.sort_strategy_,
                                                ebc_config.keys_preprocess_strategy_,
                                                allreduce_strategy,
                                                ebc_config.comm_strategy_,
                                                compression_param};

  embedding::EmbeddingCollectionParam eval_ebc_param{num_table,
                                                     num_lookup,
                                                     lookup_params,
                                                     shard_matrix,
                                                     grouped_emb_params,
                                                     solver_.batchsize_eval,
                                                     key_type,
                                                     index_type,
                                                     offset_type,
                                                     emb_type,
                                                     wgrad_type,
                                                     input_layout_,
                                                     ebc_config.output_layout_,
                                                     ebc_config.sort_strategy_,
                                                     ebc_config.keys_preprocess_strategy_,
                                                     ebc_config.allreduce_strategy_,
                                                     ebc_config.comm_strategy_,
                                                     compression_param};

  std::vector<std::shared_ptr<core::CoreResourceManager>> core_list;

  for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
    auto core_resource_manager =
        std::make_shared<hctr_internal::HCTRCoreResourceManager>(resource_manager_, local_gpu_id);
    core_list.push_back(core_resource_manager);
  }
  ebc_list_.push_back(std::make_unique<embedding::EmbeddingCollection>(
      resource_manager_, core_list, ebc_param, eval_ebc_param, emb_table_list, exchange_wgrad_));
  embedding_para_io_->add_embedding_collection((ebc_list_[ebc_list_.size() - 1]).get());

  auto prepare_ebc_input = [&](auto& sparse_input_map, bool is_longlong) {
    core23::DataType SparseType = is_longlong ? core23::DataType(core23::ScalarType::Int64)
                                              : core23::DataType(core23::ScalarType::UInt32);
    auto tensor_as_type = [&](core23::Tensor input, core23::DataType expected_type) {
      auto origin_type = input.data_type();
      HCTR_CHECK_HINT(origin_type.size() == expected_type.size(),
                      "Size not equal, cannot reinterpret type");
      return core23::Tensor::bind(input.data(), input.shape(), expected_type, input.device());
    };
    auto train_sparse_tensors = sparse_input_map[bottom_name].train_sparse_tensors;
    auto evaluate_sparse_tensors = sparse_input_map[bottom_name].evaluate_sparse_tensors;

    for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
      CudaDeviceContext context(resource_manager_->get_local_gpu(local_gpu_id)->get_device_id());
      core23::Device device{core23::DeviceType::GPU,
                            static_cast<core23::DeviceIndex>(
                                resource_manager_->get_local_gpu(local_gpu_id)->get_device_id())};
      auto train_key_tensor =
          tensor_as_type(train_sparse_tensors[local_gpu_id].get_value_tensor(), SparseType);
      train_ebc_key_list_.push_back(train_key_tensor);

      auto train_bucket_range_tensor =
          tensor_as_type(train_sparse_tensors[local_gpu_id].get_rowoffset_tensor(), SparseType);
      train_ebc_bucket_range_list_.push_back(train_bucket_range_tensor);

      train_ebc_num_keys_list_.push_back(train_sparse_tensors[local_gpu_id].get_nnz_ptr().get());

      auto evaluate_key_tensor =
          tensor_as_type(evaluate_sparse_tensors[local_gpu_id].get_value_tensor(), SparseType);
      evaluate_ebc_key_list_.push_back(evaluate_key_tensor);

      auto evaluate_bucket_range_tensor =
          tensor_as_type(evaluate_sparse_tensors[local_gpu_id].get_rowoffset_tensor(), SparseType);
      evaluate_ebc_bucket_range_list_.push_back(evaluate_bucket_range_tensor);

      evaluate_ebc_num_keys_list_.push_back(
          evaluate_sparse_tensors[local_gpu_id].get_nnz_ptr().get());
    }
  };

  if (reader_params_.data_reader_type != DataReaderType_t::RawAsync) {
    if (solver_.i64_input_key) {
      prepare_ebc_input(sparse_input_map_64_, true);
    } else {
      prepare_ebc_input(sparse_input_map_32_, false);
    }
  }

  // activate_ebc_output_tensor
  size_t batch_size_per_gpu = solver_.batchsize / num_total_gpus;
  size_t eval_batch_size_per_gpu = solver_.batchsize_eval / num_total_gpus;
  if (ebc_param.output_layout_ == embedding::EmbeddingLayout::FeatureMajor) {
    std::vector<std::string> top_name_list;
    for (int lookup_id = 0; lookup_id < ebc_param.num_lookup; ++lookup_id) {
      embedding::LookupParam& lookup_param = ebc_param.lookup_params[lookup_id];
      int emb_out_dims = (lookup_param.combiner == embedding::Combiner::Concat)
                             ? lookup_param.max_hotness * lookup_param.ev_size
                             : lookup_param.ev_size;

      std::string top_name = ebc_config.top_names_[lookup_id];
      top_name_list.push_back(top_name);

      activate_tensor(tensor_active_, top_name);
      tensor_shape_info_raw_.insert({top_name, {solver_.batchsize, 1, emb_out_dims}});
      embedding_dependent_tensors_.insert(top_name);
    }
    input_output_info_.push_back(std::make_pair(bottom_name, join(top_name_list, ",")));
    if (solver_.use_mixed_precision) {
      allocate_ebc_output_helper_for_feature_major<__half>(
          resource_manager_, batch_size_per_gpu, ebc_config, ebc_param, train_tensor_entities_list_,
          train_ebc_outptut_);
      allocate_ebc_output_helper_for_feature_major<__half>(
          resource_manager_, eval_batch_size_per_gpu, ebc_config, ebc_param,
          evaluate_tensor_entities_list_, evaluate_ebc_outptut_);
    } else {
      allocate_ebc_output_helper_for_feature_major<float>(
          resource_manager_, batch_size_per_gpu, ebc_config, ebc_param, train_tensor_entities_list_,
          train_ebc_outptut_);
      allocate_ebc_output_helper_for_feature_major<float>(
          resource_manager_, eval_batch_size_per_gpu, ebc_config, ebc_param,
          evaluate_tensor_entities_list_, evaluate_ebc_outptut_);
    }
  } else {
    int concate_out_dims = 0;
    for (int lookup_id = 0; lookup_id < ebc_param.num_lookup; ++lookup_id) {
      embedding::LookupParam& lookup_param = ebc_param.lookup_params[lookup_id];

      int emb_out_dims = (lookup_param.combiner == embedding::Combiner::Concat)
                             ? lookup_param.max_hotness * lookup_param.ev_size
                             : lookup_param.ev_size;
      concate_out_dims += emb_out_dims;
    }

    activate_tensor(tensor_active_, ebc_config.batch_major_output_name_);
    tensor_shape_info_raw_.insert(
        {ebc_config.batch_major_output_name_, {solver_.batchsize, concate_out_dims}});
    input_output_info_.push_back(std::make_pair(bottom_name, ebc_config.batch_major_output_name_));
    embedding_dependent_tensors_.insert(ebc_config.batch_major_output_name_);

    // allocate output buffer
    if (solver_.use_mixed_precision) {
      allocate_ebc_output_helper_for_batch_major<__half>(
          resource_manager_, batch_size_per_gpu, ebc_config, ebc_param, train_tensor_entities_list_,
          train_ebc_outptut_);
      allocate_ebc_output_helper_for_batch_major<__half>(
          resource_manager_, eval_batch_size_per_gpu, ebc_config, ebc_param,
          evaluate_tensor_entities_list_, evaluate_ebc_outptut_);
    } else {
      allocate_ebc_output_helper_for_batch_major<float>(
          resource_manager_, batch_size_per_gpu, ebc_config, ebc_param, train_tensor_entities_list_,
          train_ebc_outptut_);
      allocate_ebc_output_helper_for_batch_major<float>(
          resource_manager_, eval_batch_size_per_gpu, ebc_config, ebc_param,
          evaluate_tensor_entities_list_, evaluate_ebc_outptut_);
    }
  }

  train_ddl_output_.clear();
  cache_train_ddl_output_.clear();
  evaluate_ddl_output_.clear();
  cache_evaluate_ddl_output_.clear();
  for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
    train_ddl_output_.push_back(
        allocate_output_for_data_distributor(core_list[local_gpu_id], ebc_param));
    if (solver_.train_inter_iteration_overlap) {
      cache_train_ddl_output_.push_back(
          allocate_output_for_data_distributor(core_list[local_gpu_id], ebc_param));
    }
    evaluate_ddl_output_.push_back(
        allocate_output_for_data_distributor(core_list[local_gpu_id], eval_ebc_param));
    if (solver_.eval_inter_iteration_overlap) {
      cache_evaluate_ddl_output_.push_back(
          allocate_output_for_data_distributor(core_list[local_gpu_id], eval_ebc_param));
    }
  }

  // create data distributors
  train_data_distributor_ = std::make_shared<DataDistributor>(core_list, ebc_param, emb_table_list,
                                                              ebc_config.dr_lookup_ids_);
  eval_data_distributor_ = std::make_shared<DataDistributor>(
      core_list, eval_ebc_param, emb_table_list, ebc_config.dr_lookup_ids_);
}

void Model::pre_add_dense_layer(DenseLayer& dense_layer) {
  embedding_dependent_ = false;
  for (auto& bottom_name : dense_layer.bottom_names) {
    deactivate_tensor(tensor_active_, bottom_name);
    if (embedding_dependent_tensors_.find(bottom_name) != embedding_dependent_tensors_.end()) {
      embedding_dependent_ = true;
    }
  }
  for (auto& top_name : dense_layer.top_names) {
    activate_tensor(tensor_active_, top_name);
    if (embedding_dependent_) {
      embedding_dependent_tensors_.insert(top_name);
    }
  }
  std::string input_names = join(dense_layer.bottom_names, ",");
  std::string output_names = join(dense_layer.top_names, ",");
  input_output_info_.push_back(std::make_pair(input_names, output_names));
  if (solver_.use_mixed_precision) {
    layer_info_.push_back(LAYER_TYPE_TO_STRING_MP[dense_layer.layer_type]);
  } else {
    layer_info_.push_back(LAYER_TYPE_TO_STRING[dense_layer.layer_type]);
  }
}

void Model::graph_analysis() {
  HCTR_LOG(INFO, ROOT, "Graph analysis to resolve tensor dependency\n");
  std::map<std::string, unsigned int> tensor_usage;
  std::map<std::string, DenseLayer> tensor_slice_layer;
  std::map<std::string, unsigned int> tensor_slice_index;
  for (auto& dense_layer : dense_layer_params_raw_) {
    for (auto& bottom_name : dense_layer.bottom_names) {
      analyze_tensor(tensor_usage, bottom_name);
    }
  }
  for (auto iter = tensor_usage.begin(); iter != tensor_usage.end(); iter++) {
    if (iter->second > 5) {
      HCTR_OWN_THROW(Error_t::WrongInput, "The graph should not include more than 5-way branches");
    }
    if (iter->second > 1) {
      std::vector<std::string> bottom_names{iter->first};
      std::vector<std::string> top_names;
      std::vector<std::pair<int, int>> ranges;
      for (unsigned int i = 0; i < iter->second; i++) {
        top_names.push_back(iter->first + "_slice" + std::to_string(i));
        auto dims = tensor_shape_info_raw_[iter->first].size();
        ranges.emplace_back(std::make_pair(0, tensor_shape_info_raw_[iter->first][dims - 1]));
      }
      DenseLayer slice_layer(Layer_t::Slice, bottom_names, top_names);
      slice_layer.ranges = ranges;
      tensor_slice_layer.insert(std::pair<std::string, DenseLayer>(iter->first, slice_layer));
      tensor_slice_index.insert(std::pair<std::string, unsigned int>(iter->first, 0));
      HCTR_LOG(INFO, ROOT, "Add Slice layer for tensor: %s, creating %d copies\n",
               iter->first.c_str(), iter->second);
    }
  }
  for (auto& dense_layer : dense_layer_params_raw_) {
    bool flag = true;
    for (auto& bottom_name : dense_layer.bottom_names) {
      if (tensor_usage[bottom_name] > 1) {
        flag = false;
        break;
      }
    }
    if (flag) {
      dense_layer_params_.push_back(dense_layer);
    } else {
      DenseLayer new_dense_layer = dense_layer;
      for (unsigned int i = 0; i < new_dense_layer.bottom_names.size(); i++) {
        std::string old_bottom_name = new_dense_layer.bottom_names[i];
        if (tensor_slice_index.find(old_bottom_name) != tensor_slice_index.end()) {
          auto iter = tensor_slice_layer.find(old_bottom_name);
          if (tensor_slice_index[old_bottom_name] == 0) {
            dense_layer_params_.push_back(iter->second);
          }
          std::string new_bottom_name = iter->second.top_names[tensor_slice_index[old_bottom_name]];
          tensor_slice_index[old_bottom_name] += 1;
          new_dense_layer.bottom_names[i] = new_bottom_name;
        }
      }
      dense_layer_params_.push_back(new_dense_layer);
    }
  }
  add_dense_layers(dense_layer_params_);
}

void Model::compile() {
  if (!graph_finalized_) {
    graph_analysis();
    graph_finalized_ = true;
  }
  if (data_input_info_.size() < 3 || layer_info_.size() < 2) {
    HCTR_OWN_THROW(Error_t::IllegalCall, "The model should include input and at least two layers");
  }
  HCTR_PRINT(INFO,
             "===================================================Model "
             "Compile===================================================\n");
  build_networks();

  // TODO: this is a WAR; need to find a way to remove the preallocation
  for (int local_gpu_id = 0; local_gpu_id < resource_manager_->get_local_gpu_count();
       ++local_gpu_id) {
    auto device_id = resource_manager_->get_local_gpu(local_gpu_id)->get_device_id();
    core23::Device device(core23::DeviceType::GPU, device_id);
    bool success = core23::AllocateBuffers(device);
    if (!success) {
      HCTR_LOG_S(DEBUG, ROOT) << "Nothing to preallocate" << std::endl;
    }
  }
  core23::Device device_h(core23::DeviceType::CPU);
  bool success = core23::AllocateBuffers(device_h);
  if (!success) {
    HCTR_LOG_S(DEBUG, ROOT) << "Nothing to preallocate" << std::endl;
  }
  initialize();
  create_metrics();
  create_pipelines();
}

void Model::compile(std::vector<std::string>& label_names, std::vector<float>& label_weights) {
  update_label_weights(label_names, label_weights);
  compile();
}

void Model::update_label_weights(std::vector<std::string>& label_names,
                                 std::vector<float>& label_weights) {
  // Add implementation and support in next merge request
  if (label_names.size() != label_weights.size()) {
    HCTR_OWN_THROW(Error_t::WrongInput, "Must have the same number of label names and weights");
  }
  std::map<std::string, float>::iterator loss_lookup;
  for (size_t i = 0; i < label_names.size(); ++i) {
    loss_lookup = label_weights_.find(label_names[i]);
    if (loss_lookup == label_weights_.end()) {
      HCTR_OWN_THROW(Error_t::WrongInput, "Label name not found: " + label_names[i]);
    }
    loss_lookup->second = label_weights[i];
  }
}

void Model::load_dense_optimizer_states(const std::string& dense_opt_states_file) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the dense optimizer states before calling Model.compile()");
  }
  load_opt_states_for_dense_(dense_opt_states_file);
}

void Model::load_sparse_optimizer_states(const std::vector<std::string>& sparse_opt_states_files) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the sparse optimizer states before "
                   "calling Model.compile()");
  }
  if (sparse_opt_states_files.size() != embeddings_.size()) {
    HCTR_OWN_THROW(Error_t::WrongInput,
                   "The size of sparse opt state files should be "
                   "equal to the number of embeddings");
  }
  load_opt_states_for_sparse_(sparse_opt_states_files);
}

void Model::load_sparse_optimizer_states(
    const std::map<std::string, std::string>& sparse_opt_states_files_map) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the sparse optimizer states before "
                   "calling Model.compile()");
  }
  for (auto iter = sparse_opt_states_files_map.begin(); iter != sparse_opt_states_files_map.end();
       iter++) {
    if (embeddings_map_.find(iter->first) == embeddings_map_.end()) {
      HCTR_OWN_THROW(Error_t::WrongInput, "No such embedding name: " + iter->first);
    }
    auto embedding_target = embeddings_map_.find(iter->first)->second;
    HCTR_LOG_S(INFO, ROOT) << "Loading sparse optimizer states: " << iter->first << std::endl;
    embedding_target->load_opt_states(iter->first);
  }
}

void Model::load_dense_weights(const std::string& dense_model_file) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the dense weights before "
                   "calling Model.compile()");
  }
  load_params_for_dense_(dense_model_file);
}

void Model::load_sparse_weights(const std::vector<std::string>& sparse_embedding_files) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the sparse weights before "
                   "calling Model.compile()");
  }
  if (sparse_embedding_files.size() != embeddings_.size()) {
    HCTR_OWN_THROW(Error_t::WrongInput,
                   "The size of sparse embedding files should be "
                   "equal to the number of embeddings");
  }
  load_params_for_sparse_(sparse_embedding_files);
}

void Model::load_sparse_weights(
    const std::map<std::string, std::string>& sparse_embedding_files_map) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot load the sparse weights before "
                   "calling Model.compile()");
  }

  for (auto iter = sparse_embedding_files_map.begin(); iter != sparse_embedding_files_map.end();
       iter++) {
    if (embeddings_map_.find(iter->first) == embeddings_map_.end()) {
      HCTR_OWN_THROW(Error_t::WrongInput, "No such embedding name: " + iter->first);
    }
    auto embedding_target = embeddings_map_.find(iter->first)->second;
    HCTR_LOG_S(INFO, ROOT) << "Loading sparse model: " << iter->second << std::endl;
    embedding_target->load_parameters(iter->second);
  }
}

void Model::embedding_load(const std::string& path, const std::vector<std::string>& table_names) {
  TableNameToGlobalIDDict table_id_map;
  if (!table_names.empty()) {
    check_table_name_correct(ebc_name_to_global_id_dict_, table_names);
    for (auto& name : table_names) {
      table_id_map[name] = ebc_name_to_global_id_dict_.at(name);
    }
  } else {
    for (auto& [name, ids] : ebc_name_to_global_id_dict_) {
      table_id_map[name] = ids;
    }
  }

  int num_total_gpus = resource_manager_->get_global_gpu_count();
  int num_local_gpus = resource_manager_->get_local_gpu_count();
  std::vector<std::shared_ptr<core::CoreResourceManager>> core_list;

  for (int local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
    auto core_resource_manager =
        std::make_shared<hctr_internal::HCTRCoreResourceManager>(resource_manager_, local_gpu_id);
    core_list.push_back(core_resource_manager);
  }

  for (auto& [name, ids] : table_id_map) {
    int embedding_collection_id = ids.first;
    int file_table_id = ids.second;
    int model_table_id = ids.second;
    auto& tmp_embedding_collection = ebc_list_[embedding_collection_id];
    auto& tmp_ebc_param = tmp_embedding_collection->ebc_param_;
    auto& tmp_shard_matrix = tmp_ebc_param.shard_matrix;

    struct embedding::EmbeddingParameterInfo tmp_epi = embedding::EmbeddingParameterInfo();
    embedding_para_io_->load_metadata(path, embedding_collection_id, tmp_epi);

    int target_grouped_id = -1;
    embedding::TablePlacementStrategy target_placement;
    for (int grouped_id = 0; grouped_id < tmp_ebc_param.grouped_table_params.size(); ++grouped_id) {
      auto& tmp_table_ids = tmp_ebc_param.grouped_table_params[grouped_id].table_ids;

      auto tmp_it = std::find(tmp_table_ids.begin(), tmp_table_ids.end(), model_table_id);
      if (tmp_it != tmp_table_ids.end()) {
        target_grouped_id = grouped_id;
        target_placement = tmp_ebc_param.grouped_table_params[grouped_id].table_placement_strategy;
        break;
      }
    }
    if (target_grouped_id == -1) {
      HCTR_OWN_THROW(Error_t::WrongInput,
                     "can not find table_id in model table_ids,please check your input");
    }

    if (target_placement == embedding::TablePlacementStrategy::DataParallel) {
      auto tmp_filter = [=](size_t key) { return true; };
      core23::Tensor keys;
      core23::Tensor embedding_weights;
      auto& target_key_type = tmp_ebc_param.key_type;
      auto& target_value_type = tmp_ebc_param.emb_type;
      embedding_para_io_->load_embedding_weight(tmp_epi, file_table_id, keys, embedding_weights,
                                                tmp_filter, core_list[0], target_key_type,
                                                target_value_type);
      for (size_t local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
        HugeCTR::CudaDeviceContext context(core_list[local_gpu_id]->get_device_id());
        auto& grouped_table =
            tmp_embedding_collection->embedding_tables_[local_gpu_id][target_grouped_id];
        grouped_table->load_by_id(&keys, &embedding_weights, model_table_id);
      }
    } else if (target_placement == embedding::TablePlacementStrategy::ModelParallel) {
      for (size_t local_gpu_id = 0; local_gpu_id < num_local_gpus; ++local_gpu_id) {
        HugeCTR::CudaDeviceContext context(core_list[local_gpu_id]->get_device_id());
        size_t global_id = resource_manager_->get_gpu_global_id_from_local_id(local_gpu_id);
        auto& target_key_type = tmp_ebc_param.key_type;
        auto& target_value_type = tmp_ebc_param.emb_type;
        std::vector<int> shard_gpu_list;
        for (int gpu_id = 0; gpu_id < num_total_gpus; ++gpu_id) {
          HCTR_CHECK_HINT(model_table_id < static_cast<int>(tmp_shard_matrix[gpu_id].size()),
                          "table_id is out of range");
          if (tmp_ebc_param.shard_matrix[gpu_id][model_table_id] == 1) {
            shard_gpu_list.push_back(gpu_id);
          }
        }
        int num_shards = static_cast<int>(shard_gpu_list.size());
        auto find_shard_id_iter =
            std::find(shard_gpu_list.begin(), shard_gpu_list.end(), global_id);
        if (find_shard_id_iter == shard_gpu_list.end()) {
          continue;
        }
        int shard_id = static_cast<int>(std::distance(shard_gpu_list.begin(), find_shard_id_iter));

        auto tmp_filter = [=](size_t key) { return key % num_shards == shard_id; };
        core23::Tensor keys;
        core23::Tensor embedding_weights;
        embedding_para_io_->load_embedding_weight(tmp_epi, file_table_id, keys, embedding_weights,
                                                  tmp_filter, core_list[0], target_key_type,
                                                  target_value_type);
        auto& grouped_table =
            tmp_embedding_collection->embedding_tables_[local_gpu_id][target_grouped_id];
        grouped_table->load_by_id(&keys, &embedding_weights, model_table_id);
      }
    } else {
      HCTR_OWN_THROW(Error_t::UnspecificError, "unsupported parallel mode");
    }
  }
}

void Model::embedding_dump(const std::string& path, const std::vector<std::string>& table_names) {
  std::vector<struct embedding::EmbeddingParameterInfo> epis;

  embedding_para_io_->get_parameter_info_from_model(path, epis);
  std::map<int, std::vector<int>> table_ids;

  if (!table_names.empty()) {
    check_table_name_correct(ebc_name_to_global_id_dict_, table_names);
    for (auto& name : table_names) {
      auto& id_pair = ebc_name_to_global_id_dict_.at(name);
      int embedding_collection_id = id_pair.first;
      int table_id = id_pair.second;
      if (table_ids.find(embedding_collection_id) == table_ids.end()) {
        table_ids[embedding_collection_id] = std::vector<int>();
        table_ids.at(embedding_collection_id).push_back(table_id);
      } else {
        table_ids.at(embedding_collection_id).push_back(table_id);
      }
    }
  } else {
    for (auto& [name, id_pair] : ebc_name_to_global_id_dict_) {
      int embedding_collection_id = id_pair.first;
      int table_id = id_pair.second;
      if (table_ids.find(embedding_collection_id) == table_ids.end()) {
        table_ids[embedding_collection_id] = std::vector<int>();
        table_ids.at(embedding_collection_id).push_back(table_id);
      } else {
        table_ids.at(embedding_collection_id).push_back(table_id);
      }
    }
  }

  for (auto collection_id_iter = table_ids.begin(); collection_id_iter != table_ids.end();
       ++collection_id_iter) {
    auto& cid = collection_id_iter->first;
    auto& tmp_table_ids = collection_id_iter->second;
    std::sort(tmp_table_ids.begin(), tmp_table_ids.end());
    embedding_para_io_->dump_metadata(path, epis[cid], tmp_table_ids);
    embedding_para_io_->dump_embedding_weight(path, epis[cid], tmp_table_ids);
  }
}

void Model::summary() {
  if (!graph_finalized_) {
    graph_analysis();
    graph_finalized_ = true;
  }
  if (data_input_info_.size() < 3 || layer_info_.size() < 2) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "The model should include input and at "
                   "least two layers");
  }
  for (auto tensor_entry : train_tensor_entities_list_[0]) {
    tensor_shape_info_.insert(std::make_pair(tensor_entry.name, tensor_entry.tensor.shape()));
  }
  HCTR_PRINT(INFO,
             "============================================"
             "=======Model "
             "Summary====================================="
             "==============\n");
  auto log = HCTR_LOG_S(INFO, ROOT);
  log << "Model structure on each GPU" << std::endl;
  log << std::left << std::setw(40) << std::setfill(' ') << "Label" << std::left << std::setw(30)
      << std::setfill(' ') << "Dense" << std::left << std::setw(30) << std::setfill(' ') << "Sparse"
      << std::endl;
  log << std::left << std::setw(40) << std::setfill(' ') << data_input_info_[0] << std::left
      << std::setw(30) << std::setfill(' ') << data_input_info_[1] << " " << std::left
      << std::setw(30) << std::setfill(' ') << data_input_info_[2] << std::endl;
  log << std::left << std::setw(40) << std::setfill(' ')
      << get_tensor_shape(data_input_info_[0], tensor_shape_info_) << std::left << std::setw(40)
      << std::setfill(' ') << get_tensor_shape(data_input_info_[1], tensor_shape_info_)
      << std::endl;
  log << "————————————————————————————————————————————————"
         "—————————————————————————————————"
         "—————————————————————————————————"
      << std::endl;
  log << std::left << std::setw(40) << std::setfill(' ') << "Layer Type" << std::left
      << std::setw(30) << std::setfill(' ') << "Input Name" << std::left << std::setw(30)
      << std::setfill(' ') << "Output Name" << std::left << std::setw(30) << std::setfill(' ')
      << "Output Shape" << std::endl;
  log << "————————————————————————————————————————————————"
         "—————————————————————————————————"
         "—————————————————————————————————"
      << std::endl;
  for (size_t i = 0; i < layer_info_.size(); ++i) {
    std::vector<std::string> layer_type{layer_info_[i]};
    std::vector<std::string> input_names;
    std::vector<std::string> output_names;
    split(input_output_info_[i].first, ',', input_names);
    split(input_output_info_[i].second, ',', output_names);
    size_t lines =
        input_names.size() > output_names.size() ? input_names.size() : output_names.size();
    layer_type.insert(layer_type.end(), lines - 1, "");
    if (lines > input_names.size()) {
      input_names.insert(input_names.end(), lines - input_names.size(), "");
    }
    if (lines > output_names.size()) {
      output_names.insert(output_names.end(), lines - output_names.size(), "");
    }
    for (size_t j = 0; j < lines; j++) {
      log << std::left << std::setw(40) << std::setfill(' ') << layer_type[j] << std::left
          << std::setw(30) << std::setfill(' ') << input_names[j] << std::left << std::setw(30)
          << std::setfill(' ') << output_names[j] << std::left << std::setw(30) << std::setfill(' ')
          << get_tensor_shape(output_names[j], tensor_shape_info_) << std::endl;
    }
    log << "----------------------------------------------"
           "-----------------------------------"
           "---------------------------------"
        << std::endl;
  }
}

void Model::set_source(std::string source, std::string eval_source) {
  if (solver_.repeat_dataset) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "The set source method can only be "
                   "used under the epoch mode");
  }
  std::vector<std::string>().swap(reader_params_.source);
  reader_params_.source.push_back(source);
  reader_params_.eval_source.assign(eval_source);
}

void print_class_aucs(std::vector<float> class_aucs) {
  if (class_aucs.size() > 1) {
    HCTR_LOG_S(INFO, ROOT) << "Evaluation, AUC: {";
    for (size_t i = 0; i < class_aucs.size(); i++) {
      if (i > 0) {
        HCTR_PRINT(INFO, ", ");
      }
      HCTR_PRINT(INFO, "%f", class_aucs[i]);
    }
    HCTR_PRINT(INFO, "}\n");
  }
}

void Model::fit(int num_epochs, int max_iter, int display, int eval_interval, int snapshot,
                std::string snapshot_prefix) {
  if (!buff_allocated_) {
    HCTR_OWN_THROW(Error_t::IllegalCall,
                   "Cannot start the training process "
                   "before calling Model.compile()");
  }
  if (solver_.repeat_dataset && max_iter <= 0) {
    HCTR_OWN_THROW(Error_t::WrongInput, "Require max_iter>0 under non-epoch mode");
  }
  if (!solver_.repeat_dataset && num_epochs <= 0) {
    HCTR_OWN_THROW(Error_t::WrongInput, "Require num_epochs>0 under epoch mode");
  }
  high_level_eval_ = true;

  HugeCTR::Timer timer;
  HugeCTR::Timer timer_train;
  HugeCTR::Timer timer_eval;

  bool epoch_mode = !solver_.repeat_dataset;
  HCTR_PRINT(INFO,
             "============================================"
             "=========Model "
             "Fit========================================="
             "============\n");
  if (epoch_mode) {
    HCTR_LOG(INFO, ROOT, "Use epoch mode with number of epochs: %d\n", num_epochs);
  } else {
    HCTR_LOG(INFO, ROOT,
             "Use non-epoch mode with number of "
             "iterations: %d\n",
             max_iter);
  }
  HCTR_LOG(INFO, ROOT, "Training batchsize: %d, evaluation batchsize: %d\n", solver_.batchsize,
           solver_.batchsize_eval);
  HCTR_LOG(INFO, ROOT, "Evaluation interval: %d, snapshot interval: %d\n", eval_interval, snapshot);
  // FYI, A string literal is statically allocated so we
  // can assume it is safe to return it.
  auto b2s = [](const char val) { return val ? "True" : "False"; };

  HCTR_LOG(INFO, ROOT, "Dense network trainable: %s\n", b2s(is_dense_trainable_));
  for (auto iter = embeddings_map_.begin(); iter != embeddings_map_.end(); iter++) {
    HCTR_LOG(INFO, ROOT, "Sparse embedding %s trainable: %s\n", iter->first.c_str(),
             b2s(iter->second->is_trainable()));
  }
  HCTR_LOG(INFO, ROOT,
           "Use mixed precision: %s, scaler: %f, use cuda "
           "graph: %s\n",
           b2s(solver_.use_mixed_precision), solver_.scaler, b2s(solver_.use_cuda_graph));
  HCTR_LOG(INFO, ROOT, "lr: %f, warmup_steps: %zu, end_lr: %f\n", solver_.lr, solver_.warmup_steps,
           solver_.end_lr);
  HCTR_LOG(INFO, ROOT,
           "decay_start: %zu, decay_steps: %zu, "
           "decay_power: %f\n",
           solver_.decay_start, solver_.decay_steps, solver_.decay_power);
  timer.start();
  timer_train.start();

  bool use_embedding_collection_without_overlapping =
      (!solver_.use_embedding_collection) ||
      (solver_.use_embedding_collection && !solver_.train_inter_iteration_overlap &&
       !solver_.train_intra_iteration_overlap && !solver_.eval_inter_iteration_overlap &&
       !solver_.eval_intra_iteration_overlap);
  if (epoch_mode) {
    HCTR_THROW_IF(
        !use_embedding_collection_without_overlapping, Error_t::WrongInput,
        "Use embedding collection  "
        "train_inter_iteration_overlap/train_intra_iteration_overlap/eval_inter_iteration_overlap/"
        "eval_intra_iteration_overlap is not allowed in epoch_mode");
    int iter = 0;
    int batches;
    auto data_reader_train = this->get_train_data_reader();
    auto data_reader_eval = this->get_evaluate_data_reader();
    if (!data_reader_eval_status_) {
      data_reader_eval->set_source(reader_params_.eval_source);
      data_reader_eval_status_ = true;
    }
    HCTR_LOG_S(INFO, ROOT) << "Training source file: " << reader_params_.source[0] << std::endl;
    HCTR_LOG_S(INFO, ROOT) << "Evaluation source file: " << reader_params_.eval_source << std::endl;
    for (int e = 0; e < num_epochs; e++) {
      HCTR_LOG_S(INFO, ROOT) << "-----------------------------------Epoch " << e
                             << "-----------------------------------" << std::endl;
      data_reader_train->set_source(reader_params_.source[0]);
      data_reader_train_status_ = true;
      do {
        float lr = 0;
        if (!this->use_gpu_learning_rate_scheduling()) {
          lr = lr_sch_->get_next();
          this->set_learning_rate(lr);
        }
        // We can not decide the last train batch so we assume every batch is both first and last.
        graph_.is_first_train_batch_ = true;
        graph_.is_last_train_batch_ = true;
        data_reader_train_status_ = this->train();
        if (display > 0 && (iter + 1) % display == 0) {
          timer_train.stop();
          float loss = 0;
          this->get_current_loss(&loss);
          if (isnan(loss)) {
            throw std::runtime_error(std::string("Train Runtime error: Loss "
                                                 "cannot converge") +
                                     " " + __FILE__ + ":" + std::to_string(__LINE__) + " \n");
          }
          if (!use_gpu_learning_rate_scheduling()) {
            HCTR_LOG_S(INFO, ROOT) << "Iter: " << iter + 1 << " Time(" << display
                                   << " iters): " << timer_train.elapsedSeconds()
                                   << "s Loss: " << loss << " lr:" << lr << std::endl;
          } else {
            HCTR_LOG_S(INFO, ROOT)
                << "Iter: " << iter + 1 << " Time(" << display
                << " iters): " << timer_train.elapsedSeconds() << "s Loss: " << loss << std::endl;
          }
          timer_train.start();
        }
        if (eval_interval > 0 && (iter + 1) % eval_interval == 0) {
          this->check_overflow();
          this->copy_weights_for_evaluation();
          batches = 0;
          timer_eval.start();
          while (data_reader_eval_status_) {
            if (solver_.max_eval_batches == 0 || batches >= solver_.max_eval_batches) {
              break;
            }
            graph_.is_first_eval_batch_ = (batches == 0);
            graph_.is_last_eval_batch_ = (batches == solver_.max_eval_batches - 1);
            data_reader_eval_status_ = this->eval();
            batches++;
          }
          if (!data_reader_eval_status_) {
            data_reader_eval->set_source(reader_params_.eval_source);
            data_reader_eval_status_ = true;
          }
          timer_eval.stop();
          auto eval_metrics = this->get_eval_metrics();
          size_t metric_id = 0;
          for (auto& eval_metric : eval_metrics) {
            metric_id++;
            HCTR_LOG_S(INFO, ROOT)
                << "Evaluation, " << eval_metric.first << ": " << eval_metric.second << std::endl;
            if (!eval_metric.first.compare("AUC")) {
              print_class_aucs(metrics_[metric_id - 1]->get_per_class_metric());
              const auto auc_threshold = solver_.metrics_spec[HugeCTR::metrics::Type::AUC];
              if (eval_metric.second > auc_threshold) {
                timer.stop();
                HCTR_LOG(INFO, ROOT,
                         "Hit target accuracy AUC %f at "
                         "%d / %d epochs"
                         " %d global iterations with "
                         "batchsize %d in %.2fs."
                         " Average speed %f records/s.\n",
                         auc_threshold, e, num_epochs, iter, solver_.batchsize,
                         timer.elapsedSeconds(),
                         float(iter) * solver_.batchsize / timer.elapsedSeconds());
                return;
              }
            }
          }
          HCTR_LOG_S(INFO, ROOT) << "Eval Time for " << solver_.max_eval_batches
                                 << " iters: " << timer_eval.elapsedSeconds() << "s" << std::endl;
        }
        if (snapshot > 0 && (iter + 1) % snapshot == 0 && iter != 0) {
          this->download_params_to_files(snapshot_prefix, iter + 1);
        }
        iter++;
      } while (data_reader_train_status_);
      timer.stop();
    }  // end for epoch
    HCTR_LOG(INFO, ROOT,
             "Finish %d epochs %d global iterations with "
             "batchsize %d in %.2fs.\n",
             num_epochs, iter, solver_.batchsize, timer.elapsedSeconds());
  } else {
    HCTR_LOG_S(INFO, ROOT) << "Training source file: " << reader_params_.source[0] << std::endl;
    HCTR_LOG_S(INFO, ROOT) << "Evaluation source file: " << reader_params_.eval_source << std::endl;

    if (solver_.perf_logging) {
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "epoch_start", 0);
    }

    for (auto tc : training_callbacks_) {
      tc->on_training_start();
    }
    this->start_data_reading();
    this->init_data_reader_.reset();

    for (int iter = 0; iter < max_iter; iter++) {
      float lr = 0;
      if (!this->use_gpu_learning_rate_scheduling()) {
        lr = lr_sch_->get_next();
        this->set_learning_rate(lr);
      }
      graph_.is_first_train_batch_ = (iter == 0);
      graph_.is_last_train_batch_ = (iter == max_iter - 1);
      this->train();
      if (display > 0 && (iter + 1) % display == 0) {
        timer_train.stop();
        float loss = 0.0f;
        if (solver_.gen_loss_summary) {
          this->get_current_loss(&loss);
          if (isnan(loss)) {
            throw std::runtime_error(std::string("Train Runtime error: Loss "
                                                 "cannot converge") +
                                     " " + __FILE__ + ":" + std::to_string(__LINE__) + " \n");
          }
        }
        if (!use_gpu_learning_rate_scheduling()) {
          HCTR_LOG_S(INFO, ROOT) << "Iter: " << iter + 1 << " Time(" << display
                                 << " iters): " << timer_train.elapsedSeconds()
                                 << "s Loss: " << loss << " lr:" << lr << std::endl;
        } else {
          HCTR_LOG_S(INFO, ROOT) << "Iter: " << iter + 1 << " Time(" << display
                                 << " iters): " << timer_train.elapsedSeconds()
                                 << "s Loss: " << loss << std::endl;
        }
        timer_train.start();
      }
      if (eval_interval > 0 && (iter + 1) % eval_interval == 0) {
        if (solver_.all_reduce_algo == AllReduceAlgo::NCCL) {
#pragma omp parallel num_threads(number_of_networks())
          {
            size_t id = omp_get_thread_num();
            CudaCPUDeviceContext ctx(resource_manager_->get_local_gpu(id)->get_device_id());
            cudaStreamSynchronize(resource_manager_->get_local_gpu(id)->get_stream());
          }
        }
        this->check_overflow();
        this->copy_weights_for_evaluation();
        timer_eval.start();
        if (solver_.perf_logging) {
          HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "eval_start", float(iter) / max_iter);
        }
        for (auto tc : training_callbacks_) {
          tc->on_eval_start(iter);
        }
        for (int batches = 0; batches < solver_.max_eval_batches; batches++) {
          graph_.is_first_eval_batch_ = (batches == 0);
          graph_.is_last_eval_batch_ = (batches == solver_.max_eval_batches - 1);
          this->eval();
        }
        auto eval_metrics = this->get_eval_metrics();
        std::map<std::string, float> eval_results;
        for (auto& eval_metric : eval_metrics) {
          eval_results[eval_metric.first] = eval_metric.second;
        }
        bool early_stop = false;
        for (auto tc : training_callbacks_) {
          early_stop = tc->on_eval_end(iter, eval_results) || early_stop;
        }
        if (early_stop) {
          for (auto tc : training_callbacks_) {
            tc->on_training_end(iter);
          }
          return;
        }
        size_t metric_id = 0;
        for (auto& eval_metric : eval_metrics) {
          metric_id++;
          HCTR_LOG_S(INFO, ROOT) << "Evaluation, " << eval_metric.first << ": "
                                 << eval_metric.second << std::endl;
          if (solver_.perf_logging) {
            HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "eval_accuracy", eval_metric.second,
                          float(iter) / max_iter, iter);
          }
          if (!eval_metric.first.compare("AUC")) {
            print_class_aucs(metrics_[metric_id - 1]->get_per_class_metric());
            const auto auc_threshold = solver_.metrics_spec[HugeCTR::metrics::Type::AUC];
            if (eval_metric.second > auc_threshold) {
              timer.stop();
              if (solver_.perf_logging) {
                size_t train_samples =
                    static_cast<size_t>(iter + 1) * static_cast<size_t>(solver_.batchsize);

                HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "eval_stop", float(iter) / max_iter);
                HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "epoch_stop", 0);
                HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "run_stop", "success");
                HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "train_samples", train_samples);
                timer_log.stop();
              }
              HCTR_LOG(INFO, ROOT,
                       "Hit target accuracy AUC %.5f at "
                       "%d / %d iterations with batchsize %d "
                       "in %.2fs. Average speed %f "
                       "records/s.\n",
                       auc_threshold, iter, max_iter, solver_.batchsize, timer.elapsedSeconds(),
                       float(iter) * solver_.batchsize / timer.elapsedSeconds());
              return;
            }
          }
        }
        timer_eval.stop();
        HCTR_LOG_S(INFO, ROOT) << "Eval Time for " << solver_.max_eval_batches
                               << " iters: " << timer_eval.elapsedSeconds() << "s" << std::endl;
        if (solver_.perf_logging) {
          HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "eval_stop",
                        float(iter) / max_iter);  // use iteration to calculate it's in which epoch
        }
      }
      if (snapshot > 0 && (iter + 1) % snapshot == 0 && iter != 0) {
        this->download_params_to_files(snapshot_prefix, iter + 1);
      }
    }  // end for iter
    for (auto tc : training_callbacks_) {
      tc->on_training_end(max_iter - 1);
    }
    if (solver_.perf_logging) {
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "epoch_stop", 0);
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "run_stop", "aborted");
      size_t train_samples = static_cast<size_t>(max_iter) * static_cast<size_t>(solver_.batchsize);
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "train_samples", train_samples);
      timer_log.stop();
    }

    timer.stop();
    HCTR_LOG(INFO, ROOT,
             "Finish %d iterations with batchsize: %d in "
             "%.2fs.\n",
             max_iter, solver_.batchsize, timer.elapsedSeconds());

  }  // end if else
  high_level_eval_ = false;
}
void Model::exchange_wgrad(size_t device_id) {
  auto& gpu_resource = resource_manager_->get_local_gpu(device_id);
  CudaCPUDeviceContext context(gpu_resource->get_device_id());
  if (resource_manager_->get_global_gpu_count() > 1) {
    exchange_wgrad_->allreduce(device_id, gpu_resource->get_stream());
  }
}

bool Model::skip_prefetch_in_last_batch(bool is_train) {
  bool inter_overlap =
      is_train ? solver_.train_inter_iteration_overlap : solver_.eval_inter_iteration_overlap;
  bool is_first_batch = is_train ? graph_.is_first_train_batch_ : graph_.is_first_eval_batch_;
  bool is_last_batch = is_train ? graph_.is_last_train_batch_ : graph_.is_last_eval_batch_;

  return !is_first_batch && is_last_batch && solver_.use_embedding_collection && inter_overlap;
}

long long Model::read_a_batch(bool is_train) {
  auto& data_reader = is_train ? train_data_reader_ : evaluate_data_reader_;
  bool drop_incomplete_batch = is_train ? solver_.drop_incomplete_batch : false;
  bool skip_prefetch_data_reading = skip_prefetch_in_last_batch(is_train);

  if (skip_prefetch_data_reading) {
    return data_reader->get_current_batchsize();
  }

  long long current_batchsize = 0;

  while ((current_batchsize = data_reader->read_a_batch_to_device_delay_release()) &&
         (current_batchsize < data_reader->get_full_batchsize()) && drop_incomplete_batch) {
    HCTR_LOG_S(INFO, ROOT) << "train drop incomplete batch. batchsize:" << current_batchsize
                           << std::endl;
    data_reader->ready_to_collect();
  }
  data_reader->ready_to_collect();
  // when the data reader is doing prefetch, we should not return current batch size in data reader
  bool inter_overlap =
      is_train ? solver_.train_inter_iteration_overlap : solver_.eval_inter_iteration_overlap;
  if (inter_overlap && solver_.use_embedding_collection) return data_reader->get_full_batchsize();
  return current_batchsize;
}

bool is_first_h2d = true;
bool Model::train() {
  try {
    if (train_data_reader_->is_started() == false) {
      HCTR_OWN_THROW(Error_t::IllegalCall,
                     "Start the data reader first before "
                     "calling Model::train()");
    }

#ifndef DATA_READING_TEST
    // TODO: assuming the there are enough training
    // iterations, incomplete batches are discarded, so
    // that we can bypass the runtime error in the epoch
    // mode, whilst maintaining the dense network training
    // logic. To minimize the wasted batches, consider to
    // adjust # of data reader workers. For instance, with
    // a file list source, set "num_workers" to a dvisior
    // of the number of data files in the file list. We
    // will look into some alternatives in the long term.
    if (is_scheduled_datareader() and is_scheduled_embedding()) {
      graph_scheduler_->trickling();
    }

    const char* const skip_h2d_env = std::getenv("SKIP_H2D");
    bool skip_h2d = (skip_h2d_env != nullptr && 1 == std::atoi(skip_h2d_env));

    bool is_train = true;
    long long current_batchsize = (skip_h2d && !is_first_h2d)
                                      ? train_data_reader_->get_full_batchsize()
                                      : read_a_batch(is_train);
    is_first_h2d = false;
    if (!current_batchsize) {
      return false;
    }

    if (solver_.all_reduce_algo == AllReduceAlgo::NCCL and
        train_data_reader_->current_batch_incomplete()) {
#pragma omp parallel num_threads(number_of_networks())
      {
        size_t id = omp_get_thread_num();
        CudaCPUDeviceContext ctx(resource_manager_->get_local_gpu(id)->get_device_id());
        cudaStreamSynchronize(resource_manager_->get_local_gpu(id)->get_stream());
      }
    }
    this->check_overflow();

    if (solver_.use_embedding_collection) {
      train_pipeline_with_ebc();
      return true;
    }

    if (is_scheduled_datareader() && is_scheduled_embedding()) {
      train_pipeline(current_batchsize);
      return true;
    }

    auto network_update = [&](int id) { networks_[id]->update_params(); };

    for (auto& one_embedding : embeddings_) {
      one_embedding->forward(true);
    }

#pragma omp parallel num_threads(number_of_networks())
    {
      size_t id = omp_get_thread_num();
      CudaCPUDeviceContext ctx(resource_manager_->get_local_gpu(id)->get_device_id());
      if (solver_.use_cuda_graph && !train_data_reader_->current_batch_incomplete()) {
        graph_.train_pipeline_[id].run_graph();
      } else {
        graph_.train_pipeline_[id].run();
      }
    }

    // Embedding backward
    for (auto& one_embedding : embeddings_) {
      one_embedding->backward();
    }

    // Exchange wgrad and update params
#pragma omp parallel num_threads(number_of_networks())
    {
      size_t id = omp_get_thread_num();
      CudaCPUDeviceContext ctx(resource_manager_->get_local_gpu(id)->get_device_id());
      exchange_wgrad(id);
      network_update(id);
    }

    for (const auto& one_embedding : embeddings_) {
      one_embedding->update_params();
    }
    return true;
#else
    train_data_reader_->read_a_batch_to_device();
    return true;
#endif
  } catch (const std::exception& err) {
    HCTR_LOG_S(ERROR, WORLD) << err.what() << std::endl;
    throw err;
  }
}

bool Model::eval() {
  try {
    if (evaluate_data_reader_ == nullptr) return true;
    if (evaluate_data_reader_->is_started() == false) {
      HCTR_OWN_THROW(Error_t::IllegalCall,
                     "Start the data reader first before calling Model::eval()");
    }
    if (!high_level_eval_) {
      this->check_overflow();
      this->copy_weights_for_evaluation();
    }
    bool is_train = false;
    long long current_batchsize = read_a_batch(is_train);

    for (auto& metric : metrics_) {
      metric->set_current_batch_size(current_batchsize);
    }
    if (!current_batchsize) {
      return false;
    }
    assert(current_batchsize > 0 && "Received batch of  size 0");

#ifndef DATA_READING_TEST
    assert((networks_.size() >= 1) && "(core23)networks_.size() should not less than 1.");

    if (solver_.use_embedding_collection) {
      evaluate_pipeline_with_ebc();
      return true;
    }

    if (is_scheduled_datareader() && is_scheduled_embedding()) {
      evaluate_pipeline(current_batchsize);
    } else {
      for (size_t i = 0; i < embeddings_.size(); ++i) {
        auto& one_embedding = embeddings_.at(i);
        one_embedding->forward(false);
      }

#pragma omp parallel num_threads(number_of_networks())
      {
        size_t id = omp_get_thread_num();
        auto gpu = resource_manager_->get_local_gpu(id);

        // doesn't do anything if eval_overlap disabled
        graph_.evaluate_pipeline_[id].run();
      }

      for (auto& metric : metrics_) {
        metric->global_reduce(number_of_networks());
      }
    }
#endif

    return true;
  } catch (const std::exception& err) {
    HCTR_LOG_S(ERROR, WORLD) << err.what() << std::endl;
    throw err;
  }
}  // namespace HugeCTR

std::vector<std::pair<std::string, float>> Model::get_eval_metrics() {
  std::vector<std::pair<std::string, float>> metrics;
  for (auto& metric : metrics_) {
    metrics.push_back(std::make_pair(metric->name(), metric->finalize_metric()));
  }
  return metrics;
}

Error_t Model::get_current_loss(float* loss) {
  try {
    float loss_sum = 0.f;
    float loss_reduced = 0.f;

    // Collect all the loss from every network and average
    auto accum_loss = [&loss_sum](auto& networks) {
      for (auto& network : networks) {
        loss_sum += network->get_loss();
      }
    };
    accum_loss(networks_);

    if (resource_manager_->get_num_process() > 1) {
#ifdef ENABLE_MPI
      HCTR_MPI_THROW(
          MPI_Reduce(&loss_sum, &loss_reduced, 1, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD));
#endif
    } else {
      loss_reduced = loss_sum;
    }
    *loss = loss_reduced / resource_manager_->get_global_gpu_count();
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::download_params_to_files(std::string prefix, int iter) {
  std::string snapshot_dense_name = prefix + "_dense_" + std::to_string(iter) + ".model";
  std::string snapshot_dense_opt_name = prefix + "_opt_dense_" + std::to_string(iter) + ".model";
  std::vector<std::string> snapshot_sparse_names;
  std::vector<std::string> snapshot_sparse_opt_names;
  for (unsigned int i = 0; i < embeddings_.size(); i++) {
    snapshot_sparse_names.push_back(prefix + std::to_string(i) + "_sparse_" + std::to_string(iter) +
                                    ".model");
    snapshot_sparse_opt_names.push_back(prefix + std::to_string(i) + "_opt_sparse_" +
                                        std::to_string(iter) + ".model");
  }
  download_sparse_params_to_files_(snapshot_sparse_names, snapshot_sparse_opt_names);
  return download_dense_params_to_files_(snapshot_dense_name, snapshot_dense_opt_name);
}

void Model::check_overflow() const {
  if (!overflow_check_) {
    return;
  }
  for (auto& one_embedding : embeddings_) {
    one_embedding->check_overflow();
  }
}

void Model::copy_weights_for_evaluation() {
  auto op = [](auto& networks) {
    for (auto& network : networks) {
      network->copy_weights_from_train_layers_to_evaluate_layers();
      network->copy_non_trainable_params_from_train_layers_to_evaluate_layers();
    }
  };
  op(networks_);
}

Error_t Model::download_dense_params_to_files_(std::string weights_file,
                                               std::string dense_opt_states_file) {
  try {
    if (resource_manager_->is_master_process()) {
      auto op = [&](auto& network) {
        network->download_params_to_host(weights_file);
        HCTR_LOG(INFO, ROOT, "Dumping dense weights to file, successful\n");
        network->download_opt_states_to_host(dense_opt_states_file);
        HCTR_LOG(INFO, ROOT, "Dumping dense optimizer states to file, successful\n");
        std::string no_trained_params = network->get_no_trained_params_in_string();
        if (no_trained_params.length() != 0) {
          std::string ntp_file = weights_file + ".ntp.json";
          auto fs = FileSystemBuilder::build_unique_by_path(ntp_file);
          fs->write(ntp_file, no_trained_params.c_str(), no_trained_params.length(), true);
          HCTR_LOG(INFO, ROOT, "Dumping untrainable weights to file, successful\n");
        }
      };

      op(networks_[0]);
    }
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::download_sparse_params_to_files_(
    const std::vector<std::string>& embedding_files,
    const std::vector<std::string>& sparse_opt_state_files) {
  try {
    {
      int i = 0;
      for (auto& embedding_file : embedding_files) {
        embeddings_[i]->dump_parameters(embedding_file);
        i++;
      }
    }
    HCTR_LOG(INFO, ROOT, "Dumping sparse weights to files, successful\n");
    {
      int i = 0;
      for (auto& sparse_opt_state_file : sparse_opt_state_files) {
        embeddings_[i]->dump_opt_states(sparse_opt_state_file);
        i++;
      }
    }
    HCTR_LOG(INFO, ROOT, "Dumping sparse optimzer states to files, successful\n");
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::load_opt_states_for_dense_(const std::string& dense_opt_states_file) {
  try {
    auto op = [&dense_opt_states_file](auto& networks) {
      size_t opt_states_size_in_byte = networks[0]->get_opt_states_size_in_byte();
      std::unique_ptr<char[]> opt_states(new char[opt_states_size_in_byte]());

      auto fs = FileSystemBuilder::build_unique_by_path(dense_opt_states_file);
      fs->read(dense_opt_states_file, opt_states.get(), fs->get_file_size(dense_opt_states_file),
               0);
      HCTR_LOG_S(INFO, ROOT) << "Loading dense opt states: " << dense_opt_states_file << std::endl;
      for (auto& network : networks) {
        network->upload_opt_states_to_device(opt_states.get());
      }
    };

    op(networks_);
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::load_opt_states_for_sparse_(
    const std::vector<std::string>& sparse_opt_states_files) {
  try {
    for (size_t i = 0; i < embeddings_.size(); i++) {
      // TODO: Move to self-contained DataSourceBackend implementation.
      if (i < sparse_opt_states_files.size()) {
        HCTR_LOG_S(INFO, ROOT) << "Loading sparse optimizer states: " << sparse_opt_states_files[i]
                               << std::endl;
        embeddings_[i]->load_opt_states(sparse_opt_states_files[i]);
      }
    }
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::load_params_for_dense_(const std::string& model_file) {
  try {
    auto op = [&model_file](auto& networks) {
      std::unique_ptr<float[]> weight(new float[networks[0]->get_params_num()]());
      auto fs = FileSystemBuilder::build_unique_by_path(model_file);
      fs->read(model_file, weight.get(), fs->get_file_size(model_file), 0);
      for (auto& network : networks) {
        network->upload_params_to_device(weight.get());
      }
    };
    op(networks_);
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

Error_t Model::load_params_for_sparse_(const std::vector<std::string>& embedding_model_files) {
  try {
    for (size_t i = 0; i < embeddings_.size(); i++) {
      if (i < embedding_model_files.size()) {
        HCTR_LOG_S(INFO, ROOT) << "Loading sparse model: " << embedding_model_files[i] << std::endl;
        embeddings_[i]->load_parameters(embedding_model_files[i]);
      }
    }
  } catch (const core23::RuntimeError& rt_err) {
    Logger::get().print(rt_err);
    return rt_err.error;
  } catch (const std::exception& err) {
    Logger::get().print(err);
    return Error_t::UnspecificError;
  }
  return Error_t::Success;
}

void Model::init_params_for_dense_() {
  auto op = [&](auto& networks) {
    for (size_t i = 0; i < resource_manager_->get_local_gpu_count(); i++) {
      networks[i]->init_params(i);
    }
  };

  op(networks_);
  for (size_t i = 0; i < resource_manager_->get_local_gpu_count(); i++) {
    HCTR_LIB_THROW(cudaStreamSynchronize(resource_manager_->get_local_gpu(i)->get_stream()));
  }
}

void Model::init_params_for_sparse_() {
  for (size_t i = 0; i < embeddings_.size(); i++) {
    embeddings_[i]->init_params();
  }
}

std::tuple<size_t, size_t, std::vector<size_t>, int> Model::get_tensor_info_by_name(
    const std::string& tensor_name, Tensor_t tensor_type) {
  const auto& tensor_entries_list =
      tensor_type == Tensor_t::Train ? train_tensor_entities_list_ : evaluate_tensor_entities_list_;
  const int global_gpu_count = resource_manager_->get_global_gpu_count();

  auto fn = [](const std::string& tensor_name, const std::vector<TensorEntity>& tensor_entries) {
    for (int i{0}; i < static_cast<int>(tensor_entries.size()); i++) {
      if (tensor_entries[i].name == tensor_name) {
        return i;
      }
    }
    return -1;
  };
  const int index = fn(tensor_name, tensor_entries_list[0]);
  HCTR_CHECK_HINT(index != -1, "Cannot find tensor with name", tensor_name);

  size_t tensor_size_in_bytes = tensor_entries_list[0][index].tensor.num_bytes();
  size_t tensor_num_of_elements = tensor_entries_list[0][index].tensor.num_elements();
  auto shape = tensor_entries_list[0][index].tensor.shape();
  std::vector<size_t> dimensions(shape.data(), shape.data() + shape.dims());
  dimensions[0] *= global_gpu_count;
  return std::make_tuple(global_gpu_count * tensor_size_in_bytes,
                         global_gpu_count * tensor_num_of_elements, dimensions, index);
}

void Model::check_out_tensor(Tensor_t tensor_type, int index, float* global_result) {
  const auto& tensor_entries_list =
      tensor_type == Tensor_t::Train ? train_tensor_entities_list_ : evaluate_tensor_entities_list_;
  const int local_gpu_count = resource_manager_->get_local_gpu_count();
  size_t tensor_size_in_bytes = tensor_entries_list[0][index].tensor.num_bytes();
  size_t tensor_num_of_elements = tensor_entries_list[0][index].tensor.num_elements();
  size_t bytes_per_element = tensor_size_in_bytes / tensor_num_of_elements;

  std::unique_ptr<float[]> local_result(new float[local_gpu_count * tensor_num_of_elements]);
  if (bytes_per_element == 4) {
    for (int local_gpu_id{}; local_gpu_id < local_gpu_count; ++local_gpu_id) {
      HCTR_LIB_THROW(cudaMemcpy(local_result.get() + local_gpu_id * tensor_num_of_elements,
                                tensor_entries_list[local_gpu_id][index].tensor.data(),
                                tensor_size_in_bytes, cudaMemcpyDeviceToHost));
    }
  } else {
    std::unique_ptr<__half[]> local_result_half(
        new __half[local_gpu_count * tensor_num_of_elements]);
    for (int local_gpu_id{}; local_gpu_id < local_gpu_count; ++local_gpu_id) {
      HCTR_LIB_THROW(cudaMemcpy(local_result_half.get() + local_gpu_id * tensor_num_of_elements,
                                tensor_entries_list[local_gpu_id][index].tensor.data(),
                                tensor_size_in_bytes, cudaMemcpyDeviceToHost));
    }
    auto transform = [](float* dst_ptr, const __half* src_ptr, size_t num_of_elements) {
      for (size_t i{0}; i < num_of_elements; ++i) {
        dst_ptr[i] = static_cast<float>(src_ptr[i]);
      }
    };
    transform(local_result.get(), local_result_half.get(),
              local_gpu_count * tensor_num_of_elements);
  }

  const int numprocs{core23::MpiInitService::get().world_size()};
  if (numprocs > 1) {
#ifdef ENABLE_MPI
    HCTR_MPI_THROW(MPI_Gather(local_result.get(), local_gpu_count * tensor_num_of_elements,
                              MPI_FLOAT, global_result, local_gpu_count * tensor_num_of_elements,
                              MPI_FLOAT, 0, MPI_COMM_WORLD));
#endif
  } else {
    memcpy(global_result, local_result.get(),
           local_gpu_count * tensor_num_of_elements * sizeof(float));
  }
}

void Model::create_networks() {
  for (size_t i = 0; i < resource_manager_->get_local_gpu_count(); i++) {
    networks_.emplace_back(new Network(resource_manager_->get_local_cpu(),
                                       resource_manager_->get_local_gpu(i),
                                       solver_.use_mixed_precision));
  }
  train_tensor_entities_list_.resize(resource_manager_->get_local_gpu_count());
  evaluate_tensor_entities_list_.resize(resource_manager_->get_local_gpu_count());
}

void Model::build_networks() {
  for (size_t i = 0; i < resource_manager_->get_local_gpu_count(); i++) {
    networks_[i]->create_and_set_optimizer(opt_params_);
  }
  auto aligned_size = 16 * resource_manager_->get_local_gpu_count();
  core23::BufferParams bp{.channel = solver_.use_mixed_precision ? GetWgradHalfBufferChannel()
                                                                 : GetWgradBufferChannel()};
  for (int g = 0; g < resource_manager_->get_local_gpu_count(); g++) {
    auto device_id = resource_manager_->get_local_gpu(g)->get_device_id();
    core23::Device device(core23::DeviceType::GPU, device_id);
    auto wgrad_buffer = core23::GetBuffer(bp, device);
    auto wgrad_size = wgrad_buffer->reserved_size();
    size_t padded_bytes = wgrad_size % aligned_size;
    padded_bytes += aligned_size - padded_bytes;
    // alignment requirements from grouped allreduce.
    wgrad_tensor_successor_.emplace_back(core23::TensorParams()
                                             .device(device)
                                             .shape({static_cast<int64_t>(padded_bytes)})
                                             .data_type(core23::ScalarType::Char)
                                             .buffer_params(bp));
  }
  buff_allocated_ = true;
}

void Model::initialize() {
#ifndef DATA_READING_TEST

#pragma omp parallel num_threads(number_of_networks())
  {
    size_t id = omp_get_thread_num();
    networks_[id]->initialize();
    if (solver_.use_algorithm_search) {
      networks_[id]->search_algorithm();
    }
    HCTR_LIB_THROW(cudaStreamSynchronize(resource_manager_->get_local_gpu(id)->get_stream()));
  }

  int num_gpus = resource_manager_->get_local_gpu_count();
  std::vector<void*> wgrad_buffer_ptrs;
  size_t wgrad_buffer_size{};
  core23::BufferParams bp{.channel = solver_.use_mixed_precision ? GetWgradHalfBufferChannel()
                                                                 : GetWgradBufferChannel()};
  for (int g = 0; g < num_gpus; g++) {
    auto device_id = resource_manager_->get_local_gpu(g)->get_device_id();
    core23::Device device(core23::DeviceType::GPU, device_id);
    auto wgrad_buffer = core23::GetBuffer(bp, device);
    auto [ptr_, size_] = wgrad_buffer->decay();
    wgrad_buffer_size = size_;
    HCTR_CHECK_HINT(size_ && ptr_, "wgrad is null or it's a confederal buffer");
    wgrad_buffer_ptrs.push_back(ptr_);
  }
  exchange_wgrad_->init_ar_comm(wgrad_buffer_ptrs, wgrad_buffer_size);
#endif
  init_params_for_dense_();
  if (solver_.perf_logging) {
    for (size_t i = 0; i < dense_layer_params_.size(); i++) {
      bool is_trainable =
          TRAINABLE_LAYERS.find(dense_layer_params_[i].layer_type) != TRAINABLE_LAYERS.end();
      if (is_trainable) {
        std::string output_names = join(dense_layer_params_[i].top_names, "-");
        HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "weights_initialization", output_names);
      }
    }
  }
  init_params_for_sparse_();
}  // namespace HugeCTR
void Model::create_metrics() {
  int num_total_gpus = resource_manager_->get_global_gpu_count();
  int label_dim = input_params_[0].labels_.begin()->second;
  if (input_params_[0].labels_.size() > 1) {
    auto labs = input_params_[0].labels_;
    label_dim = std::accumulate(std::begin(labs), std::end(labs), 0,
                                [](const int previous, const std::pair<std::string, int>& p) {
                                  return previous + p.second;
                                });
  }

  auto num_metrics = [&]() { return networks_[0]->get_raw_metrics_all().size(); };
  for (const auto& metric : solver_.metrics_spec) {
    // Only AUC is currently supported for models with more than one loss layer
    if ((metric.first != metrics::Type::AUC) && num_metrics() > 1) {
      HCTR_OWN_THROW(Error_t::WrongInput,
                     "Metrics besides AUC are not supported for multi-task models.");
    }

    metrics_.emplace_back(std::move(metrics::Metric::Create(
        metric.first, solver_.use_mixed_precision, solver_.batchsize_eval / num_total_gpus,
        solver_.max_eval_batches, label_dim, resource_manager_)));
  }
}

void Model::create_pipelines() {
  // TODO: currently it is only for HE
  if (embeddings_.size() == 1) {
    auto lr_scheds = embeddings_[0]->get_learning_rate_schedulers();
    for (size_t i = 0; i < lr_scheds.size(); i++) {
      networks_[i]->set_learning_rate_scheduler(lr_scheds[i]);
    }
  }

  if (is_scheduled_datareader() && is_scheduled_embedding()) {
    // will create pipeline for sparse embedding and dense network
    create_train_pipeline(networks_);
    create_evaluate_pipeline(networks_);
  } else {
    if (solver_.use_embedding_collection) {
      create_train_pipeline_with_ebc(networks_);
      create_evaluate_pipeline_with_ebc(networks_);
    } else {
      // will create pipeline for dense network.
      create_train_network_pipeline(networks_);
      create_eval_network_pipeline(networks_);
    }
  }

  size_t embed_wgrad_size = 0;
  if (!reader_params_.async_param.multi_hot_reader) {
    auto train_data_reader_ar_i64 = dynamic_cast<AsyncReader<long long>*>(train_data_reader_.get());
    auto eval_data_reader_ar_i64 =
        dynamic_cast<AsyncReader<long long>*>(evaluate_data_reader_.get());
    auto init_data_reader_ar_i64 = dynamic_cast<AsyncReader<long long>*>(init_data_reader_.get());

    auto train_data_reader_ar_i32 =
        dynamic_cast<AsyncReader<unsigned int>*>(train_data_reader_.get());
    auto eval_data_reader_ar_i32 =
        dynamic_cast<AsyncReader<unsigned int>*>(evaluate_data_reader_.get());
    auto init_data_reader_ar_i32 =
        dynamic_cast<AsyncReader<unsigned int>*>(init_data_reader_.get());

    // FIXME:
    // If doing async indices, the Hybrid Sparse Embedding needs access to the sparse tensor buffers
    // since we need to initialize the Frequent & Infrequent indices with those exact buffers.
    // Otherwise we allocate two copies (one in AsyncReader and the other in HSE) which will cause
    // us to OOM. We need to refactor the Frequent/Infrequent Embedding and IndicesView classes to
    // not require the sparse tensor buffers on construction.
    for (size_t i = 0; i < sparse_embedding_params_.size(); i++) {
      if (sparse_embedding_params_[i].embedding_type == Embedding_t::HybridSparseEmbedding) {
        if (solver_.use_mixed_precision && solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<long long, __half>*>(embeddings_[i].get());
          if (solver_.train_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(true, train_data_reader_ar_i64);
          }
          if (solver_.eval_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(false, eval_data_reader_ar_i64);
          }
        } else if (solver_.use_mixed_precision && !solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<unsigned int, __half>*>(embeddings_[i].get());
          if (solver_.train_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(true, train_data_reader_ar_i32);
          }
          if (solver_.eval_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(false, eval_data_reader_ar_i32);
          }
        } else if (!solver_.use_mixed_precision && solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<long long, float>*>(embeddings_[i].get());
          if (solver_.train_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(true, train_data_reader_ar_i64);
          }
          if (solver_.eval_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(false, eval_data_reader_ar_i64);
          }
        } else {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<unsigned int, float>*>(embeddings_[i].get());
          if (solver_.train_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(true, train_data_reader_ar_i32);
          }
          if (solver_.eval_inter_iteration_overlap) {
            hybrid_embedding->setup_buffered_indices(false, eval_data_reader_ar_i32);
          }
        }
      }
    }

    // start to touch dataset, so we can record run_start
    if (solver_.perf_logging) {
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "init_stop");
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "run_start");
    }

    if (init_data_reader_ar_i32) {
      init_data_reader_ar_i32->start();
      init_data_reader_ar_i32->read_a_batch_to_device();
    }
    if (init_data_reader_ar_i64) {
      init_data_reader_ar_i64->start();
      init_data_reader_ar_i64->read_a_batch_to_device();
    }

    for (size_t i = 0; i < sparse_embedding_params_.size(); i++) {
      if (sparse_embedding_params_[i].embedding_type == Embedding_t::HybridSparseEmbedding) {
        if (solver_.use_mixed_precision && solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<long long, __half>*>(embeddings_[i].get());
          hybrid_embedding->init_model(init_data_reader_ar_i64->get_value_tensors(),
                                       embed_wgrad_size);
        } else if (solver_.use_mixed_precision && !solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<unsigned int, __half>*>(embeddings_[i].get());
          hybrid_embedding->init_model(init_data_reader_ar_i32->get_value_tensors(),
                                       embed_wgrad_size);
        } else if (!solver_.use_mixed_precision && solver_.i64_input_key) {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<long long, float>*>(embeddings_[i].get());
          hybrid_embedding->init_model(init_data_reader_ar_i64->get_value_tensors(),
                                       embed_wgrad_size);
        } else {
          auto hybrid_embedding =
              dynamic_cast<HybridSparseEmbedding<unsigned int, float>*>(embeddings_[i].get());
          hybrid_embedding->init_model(init_data_reader_ar_i32->get_value_tensors(),
                                       embed_wgrad_size);
        }
      }
    }
  } else {
    if (solver_.perf_logging) {
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "init_stop");
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "run_start");
    }
  }

  if (solver_.perf_logging) {
    for (size_t i = 0; i < sparse_embedding_params_.size(); i++) {
      HCTR_LOG_ARGS(timer_log.elapsedMilliseconds(), "weights_initialization",
                    sparse_embedding_params_[i].sparse_embedding_name);
    }
  }

#ifdef ENABLE_MPI
  if (resource_manager_->get_num_process() > 1) {
    resource_manager_->set_ready_to_transfer();
  }
#endif
}

size_t Model::number_of_networks() const { return networks_.size(); }

}  // namespace HugeCTR
