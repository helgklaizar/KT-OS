mod heuristics;
mod models;
mod scanner;

use clap::Parser;
use serde_json::json;
use std::path::PathBuf;
use std::time::Instant;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Path to scan
    #[arg(short, long, default_value = ".")]
    path: String,

    /// Output format (text, json, github, sarif)
    #[arg(short, long, default_value = "text")]
    format: String,

    /// Enable AI Verification via local FastAPI brain
    #[arg(long, default_value_t = false)]
    ai: bool,
}

fn main() {
    let args = Args::parse();
    let path = PathBuf::from(&args.path);

    if args.format == "text" {
        println!("🛡️ Starting Aegis local scan on: {}", args.path);
        if args.ai {
            println!("🧠 AI Verification enabled (calling localhost:8001)");
        }
    }

    let start_time = Instant::now();
    let mut findings = scanner::scan_directory(&path);
    let scan_duration = start_time.elapsed();

    // AI Verification step
    if args.ai && !findings.is_empty() {
        let client = reqwest::blocking::Client::new();

        for finding in findings.iter_mut() {
            // Sending exact_match for more resilient RAG memory
            let payload = json!({
                "rule_name": finding.rule_name,
                "file_path": finding.file_path,
                "match_content": finding.exact_match
            });

            match client
                .post("http://localhost:8001/analyze")
                .json(&payload)
                .send()
            {
                Ok(resp) => {
                    if let Ok(json_resp) = resp.json::<serde_json::Value>()
                        && let Some(is_tp) = json_resp["is_true_positive"].as_bool()
                    {
                        if !is_tp {
                            // Mark it as FP in severity
                            finding.severity = format!("{} (AI_FALSE_POSITIVE)", finding.severity);
                        } else {
                            finding.severity = format!("{} (AI_CONFIRMED)", finding.severity);
                        }
                    }
                }
                Err(e) => {
                    if args.format == "text" {
                        eprintln!("⚠️ AI Check failed for {}: {}", finding.file_path, e);
                    }
                }
            }
        }
    }

    let total_duration = start_time.elapsed();

    if args.format == "json" {
        // Create a clone of findings with masked secrets for safe JSON output
        let safe_findings: Vec<_> = findings
            .iter()
            .map(|f| {
                let mut safe_f = f.clone();
                safe_f.exact_match = f.masked_secret();
                safe_f.match_content = f.masked_line();
                safe_f
            })
            .collect();
        let json_output = serde_json::to_string_pretty(&safe_findings).unwrap();
        println!("{}", json_output);
    } else if args.format == "sarif" {
        let results: Vec<_> = findings
            .iter()
            .map(|f| {
                json!({
                    "ruleId": f.rule_name,
                    "message": { "text": format!("Potential leaked {} found.", f.rule_name) },
                    "locations": [{
                        "physicalLocation": {
                            "artifactLocation": { "uri": f.file_path },
                            "region": {
                                "startLine": f.line_number,
                                "snippet": { "text": f.masked_line() }
                            }
                        }
                    }]
                })
            })
            .collect();

        let sarif_output = json!({
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [{
                "tool": {
                    "driver": {
                        "name": "Aegis Security Agent",
                        "informationUri": "https://github.com/helgklaizar/aegis-security-agent"
                    }
                },
                "results": results
            }]
        });
        println!("{}", serde_json::to_string_pretty(&sarif_output).unwrap());
    } else if args.format == "github" {
        for finding in findings {
            // ::error file={name},line={line},title={title}::{message}
            println!(
                "::error file={},line={},title={}::Aegis Security Scanner: Found {} [{}]",
                finding.file_path,
                finding.line_number,
                finding.rule_name,
                finding.rule_name,
                finding.severity
            );
        }
    } else {
        if findings.is_empty() {
            println!(
                "✅ No secrets or PII found! Scan completed in {:.2?}",
                scan_duration
            );
        } else {
            println!(
                "🚨 Found {} potential issues. Scan: {:.2?} | Total: {:.2?}",
                findings.len(),
                scan_duration,
                total_duration
            );
            for finding in findings {
                println!(
                    "[{}] {}:{} -> {}",
                    finding.severity, finding.file_path, finding.line_number, finding.rule_name
                );
                println!("    Match: {}\n", finding.masked_line());
            }
        }
    }
}
