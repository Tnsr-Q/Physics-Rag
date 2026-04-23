use actix_web::{web, App, HttpServer, Responder};
use anyhow::Result;

async fn index() -> impl Responder {
    "Hello from RAG Physics Agent API!"
}

pub async fn start_api_server(port: u16) -> Result<()> {
    println!("Starting API server on port {}", port);
    HttpServer::new(|| {
        App::new()
            .route("/", web::get().to(index))
            // Add more routes for scraping, memory, agents etc.
    })
    .bind(format!("127.0.0.1:{}", port))?
    .run()
    .await?;
    Ok(())
}

