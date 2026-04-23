use anyhow::{Result, anyhow};
use tokio::process::Command;

pub async fn get_youtube_transcript(video_url: &str) -> Result<String> {
    // Use yt-dlp to extract the transcript
    let output = Command::new("yt-dlp")
        .arg("--write-auto-sub")
        .arg("--skip-download")
        .arg("--sub-lang")
        .arg("en")
        .arg("--output")
        .arg("%(id)s.%(ext)s")
        .arg(video_url)
        .output()
        .await?;

    if !output.status.success() {
        return Err(anyhow!("yt-dlp failed: {}", String::from_utf8_lossy(&output.stderr)));
    }

    // yt-dlp writes the transcript to a file, we need to find and read it
    // The filename will be in the format <video_id>.en.vtt or <video_id>.en.srt
    let video_id_regex = regex::Regex::new(r"(?:v=|youtu.be/|embed/|watch\?v=)([^&]+)")?;
    let video_id = video_id_regex.captures(video_url)
        .and_then(|caps| caps.get(1))
        .map(|m| m.as_str())
        .ok_or_else(|| anyhow!("Could not extract video ID from URL"))?;

    let vtt_filename = format!("{}.en.vtt", video_id);
    let srt_filename = format!("{}.en.srt", video_id);

    let transcript_content = if tokio::fs::metadata(&vtt_filename).await.is_ok() {
        tokio::fs::read_to_string(&vtt_filename).await?
    } else if tokio::fs::metadata(&srt_filename).await.is_ok() {
        tokio::fs::read_to_string(&srt_filename).await?
    } else {
        return Err(anyhow!("No English transcript file found for video {}", video_id));
    };

    // Clean up the downloaded transcript file
    let _ = tokio::fs::remove_file(&vtt_filename).await;
    let _ = tokio::fs::remove_file(&srt_filename).await;

    // Basic VTT/SRT cleaning (remove timestamps, metadata)
    let cleaned_transcript = regex::Regex::new(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n|WEBVTT\n|\d+\n")?
        .replace_all(&transcript_content, "")
        .to_string();

    Ok(cleaned_transcript.trim().to_string())
}

