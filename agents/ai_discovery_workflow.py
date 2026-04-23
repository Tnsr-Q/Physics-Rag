# agents/ai_discovery_workflow.py
from crewai import Agent, Task, Crew, Process
from agents.tools.rtx_ppf_tools import analyze_rtx_ppf_parquet
from agents.tools.webgpu_tools import (
    extract_webgpu_tensors,
    trigger_onnx_inference,
    control_tfjs_training
)

def setup_ai_discovery_crew():
    """
    Use WebGPU AI engine to discover novel quantum phases.
    """
    
    # Task 1: Feynman extracts tensor data
    tensor_task = Task(
        description="""
        Extract tensor data from the current WebGPU visualization using the
        WebGPU Tensor Extractor tool.
        
        Target region: JT ∈ [0.9, 1.1], ω ∈ [1.0, 3.0]
        
        Analyze the PPF statistics in the returned data:
        - What's the average collapse ratio?
        - How many tiles are toroidal (euler_char = 0)?
        - What fraction is in quantum regime?
        """,
        expected_output="Tensor statistics with PPF topology summary",
        agent=feynman_agent
    )
    
    # Task 2: Dirac trains classifier
    training_task = Task(
        description="""
        Based on the tensor data Feynman extracted, start TensorFlow.js training
        using the TensorFlow Training Controller tool.
        
        Goal: Train a model to predict collapse_ratio from quasienergies.
        
        Configuration:
        - Epochs: 20
        - Learning rate: 0.001 (Adam optimizer)
        - Loss: Quantum entanglement-aware (built into tfjs_training_pipeline.js)
        
        Monitor training metrics and report when validation loss plateaus.
        """,
        expected_output="Training metrics and model performance",
        agent=dirac_agent,
        context=[tensor_task]
    )
    
    # Task 3: Einstein validates with ONNX
    inference_task = Task(
        description="""
        After Dirac's model is trained, use ONNX Inference Trigger to validate
        predictions on held-out test data.
        
        Test on 5 random eigenvalue sequences and compare:
        - Model predicted collapse_ratio
        - PPF bridge computed collapse_ratio
        - Relative error
        
        If error > 10%, propose model improvements.
        """,
        expected_output="Validation results with error analysis",
        agent=einstein_agent,
        context=[training_task]
    )
    
    # Task 4: Schrödinger interprets predictions
    interpretation_task = Task(
        description="""
        Examine the trained model's predictions through wave mechanics lens.
        
        Questions:
        1. Does the model capture quantum collapse correctly?
        2. Are there systematic errors in quantum vs classical regime?
        3. What does this reveal about measurement in quantum systems?
        
        Connect findings to the Copenhagen interpretation debate.
        """,
        expected_output="Physical interpretation of AI predictions",
        agent=schrodinger_agent,
        context=[inference_task]
    )
    
    crew = Crew(
        agents=[feynman_agent, dirac_agent, einstein_agent, schrodinger_agent],
        tasks=[tensor_task, training_task, inference_task, interpretation_task],
        process=Process.sequential,
        memory=True,
        verbose=2
    )
    
    return crew


if __name__ == "__main__":
    print("\n=== AI-Guided Quantum Phase Discovery ===")
    
    # Ensure API server is running
    print("Checking API server...")
    import requests
    try:
        requests.get("http://localhost:8081/api/health", timeout=2)
        print("✓ API server online")
    except:
        print("✗ API server offline - start rust-gpui-app first")
        exit(1)
    
    crew = setup_ai_discovery_crew()
    result = crew.kickoff()
    
    print("\n=== Discovery Results ===")
    print(result)