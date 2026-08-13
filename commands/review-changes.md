Review all uncommitted code changes (staged and unstaged) in the current git repository for quality issues.

## Steps
1. Run `git diff` and `git diff --cached` to get all changes.
2. Analyze the diff for:
   - **Debugging artifacts**: `console.log`, `console.debug`, `debugger` statements, `print()` calls left in
   - **TODO/FIXME/HACK comments**: Flag any that were newly added
   - **Obvious bugs**: Null reference risks, off-by-one errors, missing error handling, race conditions
   - **Dead code**: Commented-out code blocks, unused imports, unreachable code
   - **Security issues**: Hardcoded secrets, SQL injection, XSS vulnerabilities
   - **Type issues**: `any` types in TypeScript, missing type annotations on public APIs
   - **Code smells**: Duplicated logic, overly complex functions, magic numbers

3. Present findings organized by severity (critical → warning → info).
4. If no issues found, confirm the changes look clean.
