import numpy as np
import onnx
import onnx.helper as oh
import onnx.numpy_helper as onh

# Define input/output tensors
input_tensor = oh.make_tensor_value_info("input", onnx.TensorProto.FLOAT, [1, 16])
output_tensor = oh.make_tensor_value_info("output", onnx.TensorProto.FLOAT, [1, 2])

# Create weight/bias tensors
weights = np.random.randn(16, 2).astype(np.float32)
bias = np.random.randn(2).astype(np.float32)

# Convert weight/bias to ONNX initializers
weight_node = onh.from_array(weights, name="weights")
bias_node = onh.from_array(bias, name="bias")

# Define computational nodes: MatMul → ReLU → Add
matmul_node = oh.make_node("MatMul", ["input", "weights"], ["matmul_out"])
relu_node = oh.make_node("Relu", ["matmul_out"], ["relu_out"])
bias_add_node = oh.make_node("Add", ["relu_out", "bias"], ["output"])

# Create the ONNX graph
graph = oh.make_graph(
    [matmul_node, relu_node, bias_add_node],
    "Quantum_Contextuality_Model",
    [input_tensor],
    [output_tensor],
    [weight_node, bias_node]
)

# Create the model
onnx_model = oh.make_model(graph, producer_name="Quantum AI Generator")

# Save the model
onnx.save(onnx_model, "quantum_contextuality.onnx")
print("✅ Quantum Contextuality ONNX model successfully generated: quantum_contextuality.onnx")
