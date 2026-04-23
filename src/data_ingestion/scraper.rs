use anyhow::Result;
use reqwest::Client;
use scraper::{Html, Selector};
use url::Url;

pub async fn scrape_web_page(url: &str) -> Result<String> {
    let client = Client::new();
    let res = client.get(url).send().await?.text().await?;

    let document = Html::parse_document(&res);
    let selector = Selector::parse("p, h1, h2, h3, h4, h5, h6, li").unwrap(); // Select common text elements

    let mut content = String::new();
    for element in document.select(&selector) {
        content.push_str(&element.text().collect::<Vec<_>>().join(" "));
        content.push_str("\n");
    }

    Ok(content.trim().to_string())
}

pub async fn get_all_links(url: &str) -> Result<Vec<String>> {
    let client = Client::new();
    let res = client.get(url).send().await?.text().await?;

    let document = Html::parse_document(&res);
    let selector = Selector::parse("a").unwrap();

    let base_url = Url::parse(url)?;
    let mut links = Vec::new();

    for element in document.select(&selector) {
        if let Some(href) = element.value().attr("href") {
            if let Ok(absolute_url) = base_url.join(href) {
                links.push(absolute_url.to_string());
            }
        }
    }
    Ok(links)
}

