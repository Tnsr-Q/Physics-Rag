async function createWebGPUComputePipeline(device) {
    const shaderModule = device.createShaderModule({
        code: `
struct Matrix {
    data: array<f16>;
};

@group(0) @binding(0) var<storage, read> inputMatrix: Matrix;
@group(0) @binding(1) var<storage, write> outputMatrix: Matrix;

@compute @workgroup_size(16, 16)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let index = id.x + id.y * 16u;
    outputMatrix.data[index] = inputMatrix.data[index] * f16(2.0);
}
        `
    });

    return device.createComputePipeline({
        compute: { module: shaderModule, entryPoint: "main" }
    });
}
