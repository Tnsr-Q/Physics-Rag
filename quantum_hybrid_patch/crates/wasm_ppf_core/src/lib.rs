
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct PpfInput {
    pub quasienergies: Vec<f64>
}

#[derive(Serialize, Deserialize)]
pub struct PpfAnnotation {
    pub n_state: i32,
    pub collapse_ratio: f32,
    pub galois_order: u32,
    pub k_distinct_primes: u32,
    pub iot_critical: bool,
    pub euler_char: i32,
}

#[wasm_bindgen]
pub fn analyze_ppf(json_input: &str) -> String {
    let input: PpfInput = serde_json::from_str(json_input).unwrap();
    let n_state = (input.quasienergies.iter().sum::<f64>() * 100.0).round() as i32;

    let primes = factorize(n_state.abs());
    let k = primes.len() as u32;

    let collapse_ratio = if n_state == 0 { 0.0 } else { 1.0 / k.max(1) as f32 };
    let galois_order = (k * 2) + 2;
    let iot_critical = collapse_ratio > 0.5;
    let euler_char = 2 - k as i32;

    let out = PpfAnnotation {
        n_state,
        collapse_ratio,
        galois_order,
        k_distinct_primes: k,
        iot_critical,
        euler_char
    };

    serde_json::to_string(&out).unwrap()
}

fn factorize(mut n: i32) -> Vec<i32> {
    let mut f = Vec::new();
    let mut d = 2;
    while d * d <= n {
        if n % d == 0 {
            f.push(d);
            while n % d == 0 {
                n /= d;
            }
        }
        d += 1;
    }
    if n > 1 {
        f.push(n);
    }
    f
}
