# departing

[![codecov](https://codecov.io/gh/pappacena/departing/branch/main/graph/badge.svg?token=departing_token_here)](https://codecov.io/gh/pappacena/departing)
[![CI](https://github.com/pappacena/departing/actions/workflows/main.yml/badge.svg)](https://github.com/pappacena/departing/actions/workflows/main.yml)

project_description

## Install it from PyPI

```bash
pip install departing
```

## Usage

First, upload your trained model using `RemoteModel.upload(model)` method.

Below, a simple XOR model is trained and uploaded.

Note: remember to install `torch`,`numpy`, `onnx` and `onnxscript`.

```py
import torch
import numpy as np
from departing import RemoteModel

X = torch.Tensor([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = torch.Tensor([[0], [1], [1], [0]])

class XOR(torch.nn.Module):
    def __init__(self, input_dim=2, output_dim=1):
        super(XOR, self).__init__()
        self.lin1 = torch.nn.Linear(input_dim, 2)
        self.lin2 = torch.nn.Linear(2, output_dim)
    
    def forward(self, x):
        x = self.lin1(x)
        x = torch.nn.functional.sigmoid(x)
        x = self.lin2(x)
        return x

model = XOR()
loss_func = torch.nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

# Run the training itself
epochs = 2000
steps = X.size(0)
for i in range(epochs):
    for j in range(steps):
        data_point = np.random.randint(X.size(0))
        x_var = torch.autograd.Variable(X[data_point], requires_grad=False)
        y_var = torch.autograd.Variable(Y[data_point], requires_grad=False)
        
        optimizer.zero_grad()
        y_hat = model(x_var)
        loss = loss_func.forward(y_hat, y_var)
        loss.backward()
        optimizer.step()
        
    if i % 100 == 0:
        print(f"Epoch: {i}, Loss: {loss.data.numpy()}")
  
# Export the model to a single ONNX file, so we can upload it.
example_input = torch.tensor([1.0, 1.0])
onnx_program = torch.onnx.dynamo_export(model, example_input)
onnx_file_path = "/tmp/my-xor-model.onnx"
onnx_program.save(onnx_file_path)

# Instantiate a new version of the remote model using your
# api key, and identifying the model name
remote_model = RemoteModel(
  api_key="dpt_56583436b1ad4acb8fb9371ea72e9a09",
  model="pappacena/my-xor-model",
)
remote_model.upload(onnx_file_path)

# Use the model:
input_values = [
  [1.0, 1.0],
  [0.0, 0.0],
  [0.0, 1.0],
  [1.0, 0.0],
]
for input_value in input_values:
    output = remote_model(input_value)
    print(f"{input_value} ~> {output[0]}")
```

To call a previously uploaded BERT model, for example:

```py
from departing import RemoteModel
from transformers import BertTokenizer
import numpy as np


# Classes used during training
target_classes = {
  0: "happy",
  1: "not-relevant",
  2: "angry",
  3: "disgust",
  4: "sad",
  5: "surprise",
}

# Create a BERT tokenizer
tokenizer = BertTokenizer.from_pretrained(
    "bert-base-uncased",
    do_lower_case=True,
)

test_texts = [
  "I'm so happy today! Uhuu!",
  "My soccer team just lost the finals...",
  "OMG! What is happening here? I just won the lotery!",
]

# Create the tokenized version of 2 test phrases
tokenized_tests = tokenizer.batch_encode_plus(
    test_texts,
    add_special_tokens=True,
    return_attention_mask=True,
    pad_to_max_length=True,
    max_length=256,
    return_tensors="pt",
)

# Convert tensors to numpy
np_tokenized_tests = {k: v.numpy() for k, v in tokenized_tests.items()}

# This will run the model remotely, and return the same result it would
# return if executed locally
model = RemoteModel(
  api_key="dpt_56583436b1ad4acb8fb9371ea72e9a09",
  model="pappacena/my-fine-tuned-bert",
)
outputs = model(**np_tokenized_tests)

for text, logit in zip(test_texts, outputs[0]):
    output_cls = int(np.argmax(logit))
    print(f"Class #{target_classes[output_cls]}: {text}")
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
