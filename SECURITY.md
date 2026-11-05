# Security policy

## Supported code

Security fixes are prioritized for the current default branch. Older commits and previews may not receive updates.

## Reporting a vulnerability

Do not publish exploit details, credentials, personal data, or security findings in a public issue. For public repositories, use GitHub's **Security > Advisories > Report a vulnerability** feature if available. If private reporting is unavailable, request a secure reporting channel without disclosing the issue publicly.

## Testing boundaries

Only test systems and accounts you own or have explicit authorization to assess. Do not conduct intrusive scans against third parties.

## Secrets and data

Never commit access tokens, keys, user event logs, private media, or real customer data. If a credential is exposed, revoke or rotate it through its provider; removing it from Git alone does not invalidate it.

## Scope

This policy does not imply that automated checks guarantee the absence of vulnerabilities.
