use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Finding {
    pub file_path: String,
    pub line_number: usize,
    pub match_content: String, // The full line for context
    pub exact_match: String,   // The exact secret
    pub rule_name: String,
    pub severity: String,
}

impl Finding {
    pub fn masked_secret(&self) -> String {
        if self.exact_match.len() <= 4 {
            return "****".to_string();
        }
        let prefix = &self.exact_match[..4];
        format!("{}********", prefix)
    }

    pub fn masked_line(&self) -> String {
        self.match_content
            .replace(&self.exact_match, &self.masked_secret())
    }
}
