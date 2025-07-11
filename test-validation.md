# prpr Validation Test

This file is created to test the prpr CLI functionality with a real pull request.

## Test Scenarios

1. Basic comment syncing
2. Comment filtering by author type
3. Replying to comments
4. Checking for new comments

## Expected Results

- [ ] `prpr sync` creates `.prpr/threads.json`
- [ ] `prpr ls` lists all comments
- [ ] `prpr ls --author ai_bot` filters bot comments
- [ ] `prpr reply` posts responses to GitHub
- [ ] `prpr check-new` identifies recent comments

This PR will be used to validate all the CLI commands work as expected.