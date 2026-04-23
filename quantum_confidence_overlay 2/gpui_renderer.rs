// crates/host_ui/src/gpui_renderer.rs

use floem::View;
use floem::canvas::{Canvas, Color, Rect};
use crate::data_model::QuantumPrediction;

pub fn draw_confidence_heatmap(tile_id: u32, prediction: QuantumPrediction, canvas: &mut Canvas) {
    // Normalize prediction values to [0, 1]
    let score0 = prediction.class0.clamp(0.0, 1.0);
    let score1 = prediction.class1.clamp(0.0, 1.0);

    // Determine color intensity based on prediction score
    let color0 = Color::rgba(255, 0, 0, (score0 * 255.0) as u8); // Red for class 0
    let color1 = Color::rgba(0, 255, 0, (score1 * 255.0) as u8); // Green for class 1

    // Define overlay rectangles (adjust to match tile layout)
    let tile_rect = get_tile_rect(tile_id);
    let (x, y, w, h) = (tile_rect.x, tile_rect.y, tile_rect.width, tile_rect.height);

    let left_rect = Rect::new(x, y, x + w / 2, y + h);
    let right_rect = Rect::new(x + w / 2, y, x + w, y + h);

    // Draw semi-transparent heat overlays
    canvas.fill_rect(left_rect, color0);
    canvas.fill_rect(right_rect, color1);

    // Optional: draw borders or IDs
    canvas.draw_text(format!("Tile {}", tile_id), x + 4.0, y + 16.0, Color::WHITE);
}

fn get_tile_rect(tile_id: u32) -> Rect {
    // Example tile layout (placeholder logic)
    let cols = 10;
    let size = 48.0;
    let margin = 2.0;
    let row = tile_id / cols;
    let col = tile_id % cols;
    let x = col as f32 * (size + margin);
    let y = row as f32 * (size + margin);
    Rect::new(x, y, x + size, y + size)
}
