use regex::Regex;
use std::sync::LazyLock;

pub struct Rule {
    pub name: &'static str,
    pub pattern: Regex,
    pub severity: &'static str,
}

pub static RULES: LazyLock<Vec<Rule>> = LazyLock::new(|| {
    vec![
        Rule {
            name: "AWS Access Key",
            pattern: Regex::new(r"(?i)(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}").unwrap(),
            severity: "CRITICAL",
        },
        Rule {
            name: "Generic Private Key",
            pattern: Regex::new(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----").unwrap(),
            severity: "CRITICAL",
        },
        Rule {
            name: "GitHub Token",
            pattern: Regex::new(r"(?i)(github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}|ghp_[a-zA-Z0-9]{36}|ghu_[a-zA-Z0-9]{36}|ghs_[a-zA-Z0-9]{36}|ghr_[a-zA-Z0-9]{36})").unwrap(),
            severity: "CRITICAL",
        },
        Rule {
            name: "Email Address (PII)",
            pattern: Regex::new(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}").unwrap(),
            severity: "LOW",
        },
    ]
});
