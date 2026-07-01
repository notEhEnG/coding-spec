# coding-spec FAQ

### Q: Why not use a database for specs?
A: Keeping specs as Markdown files in your git repository ensures that documentation changes are version-controlled alongside code changes, facilitating branching, pull-request reviews, and history tracking.

### Q: How does this help with AI coding tools?
A: AI models are context-driven. Providing them with an explicit, structured Markdown specification and a step-by-step technical plan reduces hallucinations and prevents deviations from the desired architecture.

### Q: Can this be integrated into CI/CD pipelines?
A: Phase 3 will add CI checks for missing spec artifacts. Phase 1 focuses on the core init → spec → plan workflow.