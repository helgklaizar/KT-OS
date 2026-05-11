use ignore::WalkBuilder;
use rayon::prelude::*;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use crate::heuristics::RULES;
use crate::models::Finding;

pub fn scan_directory(path: &Path) -> Vec<Finding> {
    let walker = WalkBuilder::new(path).hidden(true).git_ignore(true).build();

    let files: Vec<_> = walker
        .filter_map(Result::ok)
        .filter(|entry| entry.file_type().is_some_and(|ft| ft.is_file()))
        .collect();

    files
        .par_iter()
        .flat_map(|entry| scan_file(entry.path()))
        .collect()
}

fn scan_file(path: &Path) -> Vec<Finding> {
    let mut findings = Vec::new();

    // File size limit: skip files > 5MB to prevent any potential OOM or slowdowns
    if let Ok(metadata) = std::fs::metadata(path)
        && metadata.len() > 5 * 1024 * 1024
    {
        return findings;
    }

    let file = match File::open(path) {
        Ok(f) => f,
        Err(_) => return findings,
    };

    let reader = BufReader::new(file);

    for (line_idx, line_result) in reader.lines().enumerate() {
        let line = match line_result {
            Ok(l) => l,
            Err(_) => break, // Stop reading on binary/invalid utf8
        };

        let line_number = line_idx + 1;

        for rule in RULES.iter() {
            if let Some(mat) = rule.pattern.find(&line) {
                findings.push(Finding {
                    file_path: path.to_string_lossy().to_string(),
                    line_number,
                    match_content: line.trim().chars().take(200).collect(),
                    exact_match: mat.as_str().to_string(),
                    rule_name: rule.name.to_string(),
                    severity: rule.severity.to_string(),
                });
            }
        }
    }

    findings
}
