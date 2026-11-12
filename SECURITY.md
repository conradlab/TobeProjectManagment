# Security and Conduct Guidelines

This repository is **public**. All files and discussions are visible to the internet.

## What NOT to Publish

Do not commit or share:

### Authentication & Access

- ❌ Passwords
- ❌ Authentication codes or tokens
- ❌ SSH private keys
- ❌ API keys or credentials
- ❌ Personal institutional account numbers
- ❌ Specific usernames for institutional accounts

### Sensitive Data

- ❌ Unapproved research datasets
- ❌ Sensitive biological or clinical data
- ❌ Protected health information (PHI)
- ❌ Personal identifying information
- ❌ Proprietary laboratory procedures or trade secrets
- ❌ Confidential internal documentation

### Infrastructure

This repository is public, so use generic descriptions for institutional systems:

❌ **Do NOT publish:**
- Complete internal server names and network topology
- Specific shared filesystem paths with full context
- Detailed access procedures or network diagrams
- Hardware configurations that could aid unauthorized access

✅ **OK to reference:**
- "The approved institutional gateway" (generic)
- "The Conrad Lab compute server" (generic)
- "The shared lab directory" (generic)
- "Connect to the approved gateway first" (procedural overview)

**Why?** This prevents bad actors from using public documentation to target internal systems.

Once the repository becomes **private**, detailed infrastructure information can be published if your institution approves it.

## Safe Practices

### When Coding

- Use `.gitignore` to exclude sensitive files:
  ```
  .env
  *.pem
  *.key
  secrets.txt
  config/passwords.txt
  ```
- Never hardcode credentials in code
- Use environment variables for sensitive configuration
- If you accidentally commit a secret, tell your mentor immediately (do not just delete it—mentors can help purge it from history)

### When Using Remote Systems

- Use SSH key authentication (not passwords)
- Never type passwords on a shared screen
- Verify you're logged into the correct server before running commands
- Be careful with commands that affect files (especially `rm`, `mv`, `chmod`)
- Never run arbitrary commands you don't understand
- Report any suspicious access attempts

### When Handling Data

- Store unapproved data only in approved locations
- Don't copy sensitive data to your local machine without permission
- Don't share datasets outside the lab without approval
- Document where data came from and how you're using it
- Report any accidental data exposure to your mentors

### Respecting Others' Work

- Don't access or modify other users' files or directories
- Don't run processes that consume excessive shared resources
- Clean up temporary files when done
- Document what you're running on shared systems
- Ask before making changes to shared directories

## Research Ethics

### Scientific Integrity

- Document your methods and results accurately
- Report negative results and failures, not just successes
- Distinguish between what you know and what you assume
- Cite sources for information and ideas
- Be honest about limitations in your work
- Don't manipulate data to match expected outcomes

### Intellectual Honesty

- Do your own thinking and work
- If you use an AI tool (ChatGPT, GitHub Copilot, etc.), you must understand every line
- Do not claim AI-generated code as your own understanding
- Properly cite and credit others' work
- Ask for help when stuck instead of copying solutions

### Informed Use of AI

- AI tools can help you learn, but they don't replace understanding
- You must be able to explain every line of code you submit
- When reviewing AI-suggested code, verify it does what you think
- AI can make confident-sounding mistakes—verify results independently
- Disclose if you used AI assistance when relevant

## If You Accidentally Publish Sensitive Data

**Act quickly:**

1. **Tell your mentor immediately.** Do not wait.
2. **Do not delete the commit.** That doesn't remove it from history.
3. **Let mentors help.** They can purge sensitive data from Git history properly.
4. For serious breaches (credential exposure), contact institutional security.

This happens to experienced developers. The important thing is quick response.

## Respectful Communication

- Use inclusive and respectful language
- Welcome questions and different perspectives
- Assume good intent but address impact
- Give credit for others' ideas and help
- Provide constructive feedback, not criticism
- Report harassment or unsafe conduct to your mentors

## Mental Health & Wellbeing

- Take breaks if you're frustrated or overwhelmed
- It's OK not to know things—that's what learning is
- Ask for help; mentors expect and welcome questions
- If something feels wrong or unsafe, speak up
- Seek out learning resources if you're stuck

## Violations & Concerns

**If you observe:**

- Security breaches or data exposure
- Uncomfortable or inappropriate behavior
- Policy violations
- Anything that seems wrong

**Talk to your mentor (Eisa or Don Conrad).**

Your mentors are there to help, not to punish honest mistakes.

---

## Summary

✅ Assume everything you post is public  
✅ Never commit passwords, keys, or credentials  
✅ Don't publish unapproved sensitive data  
✅ Use generic descriptions for internal systems  
✅ Be honest and accurate in your research  
✅ Understand all code you submit  
✅ Respect shared resources and others' work  
✅ Report problems quickly to your mentors  

When in doubt, ask your mentor before publishing anything.

