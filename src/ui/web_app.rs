use actix_files::Files;
use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use anyhow::Result;

async fn index() -> impl Responder {
    HttpResponse::Ok().body(include_str!("../../static/index.html"))
}

pub async fn start_web_app(port: u16) -> Result<()> {
    println!("Starting web app on port {}", port);
    HttpServer::new(|| {
        App::new()
            .service(Files::new("/static", "./static").show_files_listing())
            .route("/", web::get().to(index))
    })
    .bind(format!("127.0.0.1:{}", port))?
    .run()
    .await?;
    Ok(())
}

