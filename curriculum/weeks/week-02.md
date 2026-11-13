## WEEK 02: Linux, SSH & Prime8 Remote Computing

**Learning Objective:**
Master secure remote login to Prime8, OHSU's high-performance computing cluster, and become fluent with terminal navigation and session management.

**Why This Week Matters:**
Most scientific computing at OHSU happens on remote clusters like Prime8, not on your laptop. You need to reliably SSH into remote systems, manage long-running jobs, and navigate Unix filesystems. This is the foundation for all computational work in the Conrad Lab.

**Prerequisites:**
- OHSU NetID and MFA setup complete from Week 01.
- Your NetID has been granted SSH access to Prime8 by the OHSU system administrators.
- You have a terminal application (Terminal on macOS, PowerShell or WSL on Windows, or terminal on Linux).
- You have received an email confirming Prime8 access.

**Expected Time Commitment:**
8-10 hours

**Learning Objectives:**
1. Understand SSH as a secure protocol and why it matters for research data.
2. Complete a two-hop SSH connection: your computer → OHSU gateway → Prime8.
3. Navigate Unix directory structures and understand file permissions.
4. Use tmux to manage multiple terminal sessions on a remote server.
5. Create a persistent work directory on Prime8 and confirm write permissions.
6. Understand basic Unix commands: `ls`, `cd`, `pwd`, `mkdir`, `cp`, `mv`, `rm`, `cat`.

---

## Plan

### Step 1: SSH Concepts and Setup (1–2 hours)

- [ ] **Understand SSH:**
  - Read: "What is SSH?" at https://www.ssh.com/academy/ssh
  - Understand why we use SSH: encrypted communication, no passwords sent in plaintext.
  - Understand public key authentication: we will use keys, not passwords.

- [ ] **Generate SSH Key Pair (if you don't have one):**
  - Open your terminal.
  - Run: `ssh-keygen -t ed25519 -C "your_email@ohsu.edu"`
  - Press Enter to accept the default location (~/.ssh/id_ed25519).
  - Set a passphrase (you will type this passphrase each time you use the key).
  - Confirm the key was created: `ls -la ~/.ssh/` should show `id_ed25519` and `id_ed25519.pub`.
  - Document the output (do NOT paste your private key anywhere; do NOT screenshot it).

- [ ] **Verify SSH is working locally:**
  - Run: `ssh -V` to confirm SSH is installed.
  - Run: `ssh-add -l` to see if your key is loaded (it may say "no identities" initially).

- [ ] **Test SSH access to OHSU gateway (ohsuxlogin.ohsu.edu):**
  - Run: `ssh your_netid@ohsuxlogin.ohsu.edu`
  - You will be prompted for your OHSU password and then for Duo MFA.
  - If successful, you are now logged into the OHSU gateway.
  - Run: `whoami` to confirm you are logged in as your_netid.
  - Run: `exit` to log out.

---

### Step 2: Two-Hop SSH to Prime8 (2–3 hours)

- [ ] **Understand the two-hop connection:**
  - Your computer cannot directly reach Prime8 (it is behind a firewall).
  - You must first SSH to the OHSU gateway (ohsuxlogin.ohsu.edu).
  - From the gateway, you can SSH to Prime8 (prime8.ohsu.edu).

- [ ] **Configure SSH for two-hop access (ProxyJump method):**
  - Open your SSH config file: `nano ~/.ssh/config` (or your preferred editor).
  - Add the following lines:
    ```
    Host ohsu-gateway
        HostName ohsuxlogin.ohsu.edu
        User your_netid
        AddKeysToAgent yes
        IdentityFile ~/.ssh/id_ed25519

    Host prime8
        HostName prime8.ohsu.edu
        User your_netid
        ProxyJump ohsu-gateway
        AddKeysToAgent yes
        IdentityFile ~/.ssh/id_ed25519
    ```
  - Save and close the file.
  - Replace `your_netid` with your actual OHSU NetID.

- [ ] **Test the two-hop connection:**
  - Run: `ssh prime8`
  - You should be prompted for your passphrase, then your OHSU password, then Duo MFA.
  - If successful, you are now on Prime8. Run: `hostname` to confirm (should print something like `prime8.ohsu.edu`).
  - Run: `exit` to log out.

- [ ] **Understand and navigate Prime8:**
  - Log back in: `ssh prime8`
  - Run: `pwd` to see your current directory (should be `/home/your_netid` or similar).
  - Run: `ls -la` to see your home directory contents.
  - Run: `ls -la /` to see the root filesystem (this is informational only; you don't have write access to most directories).

---

### Step 3: Unix Filesystem Basics (1–2 hours)

- [ ] **Understand Unix directory structure:**
  - `/home/your_netid` is your home directory (you have full read/write access here).
  - `/tmp` is a temporary directory (files may be deleted after 30 days).
  - `/opt/software` typically contains installed research software.
  - `/data/shared` is the shared research data directory (you may have read-only access).

- [ ] **Practice filesystem navigation:**
  - Run: `pwd` to print your current directory.
  - Run: `cd ..` to go up one level, then `pwd` to confirm.
  - Run: `cd ~` to return to your home directory.
  - Run: `cd /opt/software` to navigate to the software directory.
  - Run: `ls` to see available software.
  - Run: `cd ~` to return home.

- [ ] **Understand file permissions (read, write, execute):**
  - Run: `ls -la ~/.ssh/` to see permissions on your SSH keys.
  - Explanation: `-rw-------` means you (owner) can read and write; others cannot.
  - Explanation: `-rw-r--r--` means you can read/write; others can only read.
  - Document your understanding: Why should your private SSH key have `-rw-------` permissions?

---

### Step 4: Create Your Work Directory on Prime8 (1 hour)

- [ ] **Create a persistent project directory:**
  - Log in to Prime8: `ssh prime8`
  - Run: `cd ~` (ensure you are in your home directory).
  - Run: `mkdir -p work/satinn-project` (creates nested directories).
  - Run: `cd work/satinn-project`
  - Run: `pwd` to confirm the full path.
  - Run: `ls -la` (directory is empty initially; this is expected).
  - Document the full path of your work directory.

- [ ] **Test write permissions:**
  - Run: `touch test_file.txt` to create an empty file.
  - Run: `echo "This is a test on Prime8" > test_file.txt` to write content.
  - Run: `cat test_file.txt` to confirm the content was written.
  - Run: `rm test_file.txt` to clean up the test file.

- [ ] **Create subdirectories for your work:**
  - Run: `mkdir -p data scripts results notebooks`
  - Run: `ls -la` to confirm the subdirectories were created.

---

### Step 5: Terminal Multiplexing with tmux (1–2 hours)

- [ ] **Understand why tmux matters:**
  - When you disconnect from an SSH session, programs stop running.
  - tmux creates persistent sessions: you can disconnect and reconnect without losing work.
  - tmux allows multiple terminal windows and panes in one session.

- [ ] **Install or verify tmux (if not already installed):**
  - Log in to Prime8: `ssh prime8`
  - Run: `tmux -V` to check if tmux is installed (should print `tmux X.Y`).
  - If not installed, ask Eisa or Don to request installation.

- [ ] **Create and manage tmux sessions:**
  - Run: `tmux new-session -s work` to create a new session named "work".
  - Inside the tmux session, run: `cd ~/work/satinn-project`
  - Run: `ls -la` to confirm you are in the right directory.
  - **Tmux commands (type `Ctrl+B` then the key):**
    - `Ctrl+B c`: Create a new window within the session.
    - `Ctrl+B n`: Move to the next window.
    - `Ctrl+B p`: Move to the previous window.
    - `Ctrl+B d`: Detach from the session (closes tmux UI, but session keeps running).
    - `Ctrl+B "`: Split window horizontally (creates two panes).
    - `Ctrl+B %`: Split window vertically (creates two panes).
    - `Ctrl+B →`: Move to the pane on the right.

- [ ] **Practice detaching and reattaching:**
  - Inside tmux, run: `echo "This text is in my tmux session"`
  - Press: `Ctrl+B` then `d` to detach.
  - You should be back at your regular shell prompt.
  - Run: `tmux list-sessions` to see all tmux sessions.
  - Run: `tmux attach-session -t work` to reattach to your "work" session.
  - You should see the same terminal state you left.
  - Document this behavior in your reflection.

- [ ] **Clean up:**
  - Inside tmux, run: `exit` to close the session window.
  - After all windows are closed, the session ends.
  - Or press `Ctrl+B` then `d` and don't return to the session (it persists).

---

### Step 6: Verify Setup and Document (1 hour)

- [ ] **Confirm you can SSH to Prime8 and access your work directory:**
  - Run: `ssh prime8`
  - Run: `cd ~/work/satinn-project && pwd`
  - Document the output (full path).

- [ ] **Test a multi-step workflow:**
  - Run: `tmux new-session -s test-workflow`
  - Inside tmux:
    - Run: `cd ~/work/satinn-project`
    - Run: `echo "Starting research work" > workflow_log.txt`
    - Run: `date >> workflow_log.txt`
    - Run: `cat workflow_log.txt`
  - Detach: `Ctrl+B d`
  - Reattach: `tmux attach-session -t test-workflow`
  - Confirm the file still exists and has the same content.
  - Run: `rm workflow_log.txt` to clean up.

- [ ] **Document your setup:**
  - Your home directory path on Prime8.
  - Your work directory path: `/home/your_netid/work/satinn-project`.
  - Confirmation that you can read/write files.
  - Your SSH config for two-hop access (paste the config, not your credentials).

---

## Deliverable

Document your setup completion in a GitHub comment or document:

```markdown
**Week 02 Setup Completion**

- SSH key generated and verified: [Yes / No]
- Two-hop SSH to Prime8 working: [Yes / No]
- Prime8 home directory verified: [path confirmed]
- Work directory created: [path: /home/your_netid/work/satinn-project]
- File write permissions tested: [Working / Not working]
- tmux installed and tested: [Yes / No / Asked for installation]
- Successfully detached and reattached to tmux session: [Yes / No]
```

---

## Objective Completion Criteria

✅ You have completed this week when:

1. You can SSH to Prime8 from your computer using the configured SSH setup.
2. You can navigate the Prime8 filesystem and understand Unix directory structure.
3. You have created a persistent work directory (`~/work/satinn-project`) with read/write access.
4. You can use tmux to create, detach, and reattach terminal sessions.
5. You understand SSH key authentication and why it is more secure than passwords.
6. You have tested writing a file to your work directory and confirmed it persists.
7. You have documented your setup with the configuration and paths above.

---

## Student Reflection Questions

Answer in a GitHub comment or your learning journal:

1. **SSH Security:** Why is public key authentication (SSH keys) more secure than password-based authentication?
2. **Two-Hop Concept:** Why can't you directly SSH to Prime8? What role does the gateway play?
3. **tmux Workflow:** How would you use tmux if you had a long-running analysis job (that takes 6 hours) on Prime8?
4. **Directory Structure:** What is the difference between `/tmp` and your home directory? When would you use each?
5. **Challenges:** What was the most difficult part of this week? How did you overcome it?

---

## Mentor Review Checklist

- [ ] Tobe has generated an SSH key pair with ed25519 encryption.
- [ ] Tobe can successfully complete a two-hop SSH connection to Prime8.
- [ ] Tobe has created a persistent work directory on Prime8 with confirmed write access.
- [ ] Tobe can navigate Unix filesystems and understands basic permissions.
- [ ] Tobe can use tmux to create, detach, and reattach sessions.
- [ ] Tobe has documented the SSH config and work directory path.
- [ ] Tobe has answered reflection questions demonstrating understanding.
- [ ] No SSH or connectivity issues remain unresolved.
- [ ] Approve Tobe to proceed to Week 03 (Python, Git & GitHub).

---

## Optional Stretch Activities

- [ ] Configure SSH agent forwarding to simplify multi-hop authentication.
- [ ] Explore Prime8 module system: `module avail` and `module load`.
- [ ] Set up `.bashrc` aliases for frequently used commands (e.g., `alias ss-prime8='ssh prime8'`).
- [ ] Research and document what software is available on Prime8: `ls /opt/software`.

---

## Reporting a Blocker

If you cannot SSH to Prime8 or encounter permission errors:

1. Verify your NetID has Prime8 access: contact OHSU IT.
2. Test gateway access first: `ssh your_netid@ohsuxlogin.ohsu.edu` (this should work if NetID is correct).
3. Verify your SSH key is in the right location: `ls -la ~/.ssh/id_ed25519`.
4. Check the SSH config: `cat ~/.ssh/config` (ensure Host and HostName are correct).
5. Run SSH with verbose output: `ssh -v prime8` (shows detailed connection steps).
6. Document the error message and the step at which it fails.
7. Comment on this assignment with the blocker, or create a GitHub Issue labeled `blocker`.

---

## Links and Resources

- **SSH Academy:** https://www.ssh.com/academy/ssh
- **OHSU Prime8 Documentation:** (Ask Eisa or Don for the internal link)
- **tmux Tutorial:** https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
- **Unix File Permissions:** https://www.tutorialspoint.com/unix/unix-file-permissions.htm
- **ssh_config Manual:** `man ssh_config` (run on your computer's terminal)

---

## Related Epics

- **SATINN Research Track:** All computational work depends on reliable Prime8 access.
- **Python Development:** Next week, you will run Python scripts on Prime8.
