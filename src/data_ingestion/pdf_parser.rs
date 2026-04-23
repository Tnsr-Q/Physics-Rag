use anyhow::{Result, anyhow};
use tokio::process::Command;
use tokio::fs;

pub async fn extract_text_from_pdf(file_path: &str) -> Result<String> {
    let output = Command::new("pdftotext")
        .arg(file_path)
        .arg("-") // Output to stdout
        .output()
        .await?;

    if !output.status.success() {
        return Err(anyhow!("pdftotext failed: {}\n{}",
                           String::from_utf8_lossy(&output.stdout),
                           String::from_utf8_lossy(&output.stderr)));
    }

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}

