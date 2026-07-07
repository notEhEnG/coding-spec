# coding-spec FAQ

### Q: Why not use a database for specs?
A: Keeping specs as Markdown files in your git repository ensures that documentation changes are version-controlled alongside code changes, facilitating branching, pull-request reviews, and history tracking.

### Q: How does this help with AI coding tools?
A: AI models are context-driven. Providing them with an explicit, structured Markdown specification and a step-by-step technical plan reduces hallucinations and prevents deviations from the desired architecture.

### Q: Can this be integrated into CI/CD pipelines?
A: The `validate` command already returns a non-zero exit code for incomplete specs, so you can run it as a pre-commit hook or build step today. Deeper CI checks for missing spec artifacts arrive in Phase 3. The shipped workflow is init → spec → validate → plan → review.