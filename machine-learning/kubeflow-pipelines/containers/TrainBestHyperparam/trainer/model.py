import six

import tensorflow as tf
from tensorflow.python.estimator.model_fn import ModeKeys as Modes

# Define the format of your input data including unused columns.
CSV_COLUMNS = [
    'slug', 'date', 'open',
    'high', 'low', 'close'
]
CSV_COLUMN_DEFAULTS = [[''], [''], [0.0], [0.0], [0.0], [0.0]]
LABEL_COLUMN = 'close'

# Define the initial ingestion of each feature used by your model.
# Additionally, provide metadata about the feature.
INPUT_COLUMNS = [
    # Continuous base columns.
    tf.feature_column.numeric_column('open'),
    tf.feature_column.numeric_column('high'),
    tf.feature_column.numeric_column('low'),
]

UNUSED_COLUMNS = set(CSV_COLUMNS) - {col.name for col in INPUT_COLUMNS} - \
    {LABEL_COLUMN}

def build_estimator(config, hidden_units=None, learning_rate=None):
    """Deep NN Regressor model for predicting flower class.
    Args:
    config: (tf.contrib.learn.RunConfig) defining the runtime environment for
      the estimator (including model_dir).
    hidden_units: [int], the layer sizes of the DNN (input layer first)
    learning_rate: (int), the learning rate for the optimizer.
    Returns:
    A DNNCombinedLinearClassifier
    """
    (open_, high, low) = INPUT_COLUMNS

    columns = [
        open_,
        high,
        low
    ]

    return tf.estimator.DNNRegressor(
      config=config,
      feature_columns=columns,
      hidden_units=hidden_units or [256, 128, 64],
      optimizer=tf.train.AdamOptimizer(learning_rate)
    )


# ************************************************************************
# YOU NEED NOT MODIFY ANYTHING BELOW HERE TO ADAPT THIS MODEL TO YOUR DATA
# ************************************************************************

def csv_serving_input_fn():
    """Build the serving inputs."""
    csv_row = tf.placeholder(shape=[None], dtype=tf.string)
    features = _decode_csv(csv_row)
    # Ignore label column
    features.pop(LABEL_COLUMN)
    return tf.estimator.export.ServingInputReceiver(features,
                                              {'csv_row': csv_row})

def example_serving_input_fn():
    """Build the serving inputs."""
    example_bytestring = tf.placeholder(
      shape=[None],
      dtype=tf.string,
    )
    features = tf.parse_example(
      example_bytestring,
      tf.feature_column.make_parse_example_spec(INPUT_COLUMNS))
    return tf.estimator.export.ServingInputReceiver(
      features, {'example_proto': example_bytestring})


# [START serving-function]
def json_serving_input_fn():
    """Build the serving inputs."""
    inputs = {}
    for feat in INPUT_COLUMNS:
        inputs[feat.name] = tf.placeholder(shape=[None], dtype=feat.dtype)

    return tf.estimator.export.ServingInputReceiver(inputs, inputs)

# [END serving-function]

SERVING_FUNCTIONS = {
  'JSON': json_serving_input_fn,
  'EXAMPLE': example_serving_input_fn,
  'CSV': csv_serving_input_fn
}

def _decode_csv(line):
    """Takes the string input tensor and returns a dict of rank-2 tensors."""

    # Takes a rank-1 tensor and converts it into rank-2 tensor
    row_columns = tf.expand_dims(line, -1)
    columns = tf.decode_csv(row_columns, record_defaults=CSV_COLUMN_DEFAULTS)
    features = dict(zip(CSV_COLUMNS, columns))

    # Remove unused columns
    for col in UNUSED_COLUMNS:
      features.pop(col)
    return features

def input_fn(filenames,
         num_epochs=None,
         shuffle=True,
         skip_header_lines=1,
         batch_size=200):
    """Generates features and labels for training or evaluation.
    This uses the input pipeline based approach using file name queue
    to read data so that entire data is not loaded in memory.
    Args:
      filenames: [str] A List of CSV file(s) to read data from.
      num_epochs: (int) how many times through to read the data. If None will
        loop through data indefinitely
      shuffle: (bool) whether or not to randomize the order of data. Controls
        randomization of both file order and line order within files.
      skip_header_lines: (int) set to non-zero in order to skip header lines in
        CSV files.
      batch_size: (int) First dimension size of the Tensors returned by input_fn
    Returns:
      A (features, indices) tuple where features is a dictionary of
        Tensors, and indices is a single Tensor of label indices.
    """
    dataset = tf.data.TextLineDataset(filenames).skip(skip_header_lines).map(
      _decode_csv)

    if shuffle:
        dataset = dataset.shuffle(buffer_size=batch_size * 10)
    iterator = dataset.repeat(num_epochs).batch(
        batch_size).make_one_shot_iterator()
    features = iterator.get_next()
    return features, features.pop(LABEL_COLUMN)