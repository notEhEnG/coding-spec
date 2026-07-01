# coding-spec FAQ

### Q: Why not use a database for specs?
A: Keeping specs as Markdown files in your git repository ensures that documentation changes are version-controlled alongside code changes, facilitating branching, pull-request reviews, and history tracking.

### Q: How does this help with AI coding tools?
A: AI models like Claude, GPT-4, and Copilot are context-driven. Providing them with an explicit, structured Markdown specification and a step-by-step technical plan reduces hallucinations and prevents deviations from the desired architecture.

### Q: Can this be integrated into CI/CD pipelines?
A: Yes! You can run the `validate` command as a CI pre-commit hook or build step to prevent merging features that lack documented specs or test consideration coverage.
