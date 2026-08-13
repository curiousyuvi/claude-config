Review a GitHub pull request for code quality issues.

## Arguments
- `$ARGUMENTS` — the PR URL or number to review

## Steps
1. Fetch the PR diff using `gh pr diff $ARGUMENTS`.
2. Also fetch PR details with `gh pr view $ARGUMENTS` for context.
3. Analyze the full diff for:
   - **Debugging artifacts**: `console.log`, `console.debug`, `debugger` statements, `print()` calls left in
   - **TODO/FIXME/HACK comments**: Flag any that were newly added
   - **Obvious bugs**: Null reference risks, off-by-one errors, missing error handling, race conditions
   - **Dead code**: Commented-out code blocks, unused imports, unreachable code
   - **Security issues**: Hardcoded secrets, SQL injection, XSS vulnerabilities
   - **Type issues**: `any` types in TypeScript, missing type annotations on public APIs
   - **Code smells**: Duplicated logic, overly complex functions, magic numbers

4. Present findings organized by severity (critical → warning → info), referencing specific files and line numbers.
5. If no issues found, confirm the PR looks clean.
