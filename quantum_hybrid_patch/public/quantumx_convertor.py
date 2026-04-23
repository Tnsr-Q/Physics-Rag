import onnx

def convert_to_quantumx(onnx_model_path):
    model = onnx.load(onnx_model_path)
    for node in model.graph.node:
        if node.op_type == "MatMul":
            node.attribute.append(onnx.helper.make_attribute("dtype", "float16"))
    onnx.save(model, "quantumx_model.qx")