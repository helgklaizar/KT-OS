const axios = require('axios');

/**
 * This is the main entrypoint to your Probot app
 * @param {import('probot').Probot} app
 */
module.exports = (app) => {
  app.log.info("Aegis Bot was loaded!");

  app.on(["pull_request.opened", "pull_request.synchronize"], async (context) => {
    app.log.info(`Processing PR #${context.payload.pull_request.number}`);

    // Get the diff of the pull request
    const diffUrl = context.payload.pull_request.diff_url;
    
    try {
      const diffResponse = await axios.get(diffUrl);
      const diffText = diffResponse.data;
      
      // Basic regex parsing to extract added lines
      // In a production environment, you would run the rust core `aegis-core`
      // on the checked out repository, or send the diff to a new endpoint on the `brain`
      
      const addedLines = diffText.split('\n').filter(line => line.startsWith('+') && !line.startsWith('+++'));
      
      for (const line of addedLines) {
        // Simple heuristic fallback if core is not used
        if (line.match(/(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}/i)) {
          
          // Verify with AI Brain
          try {
             const aiResponse = await axios.post('http://localhost:8001/analyze', {
                 rule_name: "AWS Access Key",
                 file_path: "diff",
                 match_content: line
             });

             if (aiResponse.data.is_true_positive) {
                // Create a review comment
                const issueComment = context.issue({
                  body: `🚨 **Aegis Security Scanner**\nFound potential AWS Key in diff.\n**AI Analysis**: ${aiResponse.data.reasoning}`,
                });
                await context.octokit.issues.createComment(issueComment);
             }
          } catch (e) {
             app.log.error("AI Brain offline or failed", e);
          }
        }
      }

    } catch (error) {
      app.log.error("Failed to fetch diff", error);
    }
  });
};
