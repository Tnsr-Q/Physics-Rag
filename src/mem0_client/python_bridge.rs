use anyhow::{Result, anyhow};
use serde::{Serialize, Deserialize};
use std::process::Stdio;
use tokio::io::{AsyncWriteExt, AsyncBufReadExt, BufReader};

#[derive(Debug, Serialize, Deserialize)]
pub struct Mem0Response {
    pub status: String,
    pub message: Option<String>,
    pub results: Option<Vec<Mem0Memory>>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Mem0Memory {
    pub id: String,
    pub data: String,
    pub metadata: serde_json::Value,
    pub category: Option<String>,
    pub created_at: Option<String>,
    pub updated_at: Option<String>,
}

pub async fn call_mem0_python_client(
    action: &str,
    payload: serde_json::Value,
) -> Result<Mem0Response> {
    let python_script_path = "./src/mem0_client/mem0_python_client.py";

    let mut child = tokio::process::Command::new("python3")
        .arg(python_script_path)
        .arg(action)
        .arg(serde_json::to_string(&payload)?)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;

    let stdout = child.stdout.take().ok_or_else(|| anyhow!("Failed to capture stdout"))?;
    let stderr = child.stderr.take().ok_or_else(|| anyhow!("Failed to capture stderr"))?;

    let stdout_reader = BufReader::new(stdout);
    let stderr_reader = BufReader::new(stderr);

    let stdout_lines = stdout_reader.lines().collect::<Result<Vec<String>, _>>().await?;
    let stderr_lines = stderr_reader.lines().collect::<Result<Vec<String>, _>>().await?;

    let status = child.wait().await?;

    if !status.success() {
        let err_msg = format!("Python script failed with status: {:?}\nStdout: {}\nStderr: {}",
                               status,
                               stdout_lines.join("\n"),
                               stderr_lines.join("\n"));
        return Err(anyhow!(err_msg));
    }

    let output = stdout_lines.join("\n");
    if output.is_empty() {
        return Err(anyhow!("Python script returned empty output. Stderr: {}", stderr_lines.join("\n")));
    }

    serde_json::from_str(&output).map_err(|e| anyhow!("Failed to parse JSON from Python script: {}. Output: {}", e, output))
}

pub async fn add_memory(
    data: String,
    user_id: Option<String>,
    metadata: Option<serde_json::Value>,
    category: Option<String>,
) -> Result<Mem0Response> {
    let mut payload = serde_json::json!({ "data": data });
    if let Some(id) = user_id { payload["user_id"] = serde_json::json!(id); }
    if let Some(meta) = metadata { payload["metadata"] = meta; }
    if let Some(cat) = category { payload["category"] = serde_json::json!(cat); }

    call_mem0_python_client("add", payload).await
}

pub async fn search_memory(
    query: String,
    user_id: Option<String>,
    category: Option<String>,
    limit: Option<usize>,
) -> Result<Mem0Response> {
    let mut payload = serde_json::json!({ "query": query });
    if let Some(id) = user_id { payload["user_id"] = serde_json::json!(id); }
    if let Some(cat) = category { payload["category"] = serde_json::json!(cat); }
    if let Some(lim) = limit { payload["limit"] = serde_json::json!(lim); }

    call_mem0_python_client("search", payload).await
}

