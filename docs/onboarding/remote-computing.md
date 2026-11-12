# SSH & Remote Computing

SSH (Secure Shell) lets you safely log into remote computers and run programs on them. You'll use SSH to connect to Prime8, the Conrad Lab's compute server.

## What is SSH?

SSH is a protocol for securely connecting to remote computers:

- **Secure:** Encrypted communication (bad actors can't read your data)
- **Shell:** Gives you a command-line prompt on the remote computer
- **Remote:** You control a distant computer from your local computer

## Understanding the Connection Path

Your workflow will likely involve **two separate connections**:

1. **Connection 1:** Your laptop → Institutional gateway (approved access point)
   - This is a security checkpoint
   - Requires institutional authentication
   - Connects you to the approved network

2. **Connection 2:** Institutional gateway → Prime8 (Conrad Lab compute server)
   - Prime8 has the computational power (1TB RAM, 100+ CPUs)
   - This is where your Python code runs
   - Faster file access and research tools

**Important:** The gateway and Prime8 are separate servers. You'll connect to gateway first, then to Prime8.

Your mentors will tell you:
- The exact gateway hostname
- The exact Prime8 hostname
- Whether you need both steps or just one

## SSH Keys vs. Passwords

**SSH Keys (recommended):**
- Public key (safe to share): Like your email address
- Private key (keep secret): Like your password
- Public key goes on the server; private key stays on your computer
- More secure than passwords
- No need to type password every time

**Passwords:**
- Simpler setup
- Less secure if intercepted
- Have to type it every time

Your mentors will set up SSH keys for you (or guide you through it).

## First Connection: Verify the Host Key

**Important:** The first time you connect to any new server, SSH shows you its "fingerprint" - a unique identifier proving you're connecting to the right server.

```bash
The authenticity of host 'approved-gateway.address' can't be established.
ED25519 key fingerprint is SHA256:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.
Are you sure you want to continue connecting (yes/no)?
```

**What to do:**
1. **Ask your mentor:** "What is the correct host key fingerprint for the gateway?"
2. **Compare:** Match the fingerprint in your terminal with the one your mentor gave you
3. **If they match:** Type `yes` and press Enter
4. **If they don't match:** Type `no` and stop - contact your mentor immediately

**Why this matters:** This prevents someone from tricking you into connecting to the wrong server.

## Single-Hop Connection (Direct to Prime8)

If your setup connects directly without a gateway:

```bash
# First time
ssh -i ~/.ssh/prime8_key.pem tobe@prime8.hostname

# SSH shows you the fingerprint
# Verify with your mentor
# Type 'yes' if it matches

# You're now logged into Prime8!
tobe@prime8:~$
```

## Two-Hop Connection (Gateway → Prime8)

If there's an approved gateway between your laptop and Prime8:

**Method 1: Connect in two steps**

```bash
# Step 1: Connect to gateway
ssh -i ~/.ssh/gateway_key.pem tobe@approved-gateway.address
# Verify gateway fingerprint with mentor
# Now you're on the gateway

# Step 2: From gateway, connect to Prime8
ssh -i ~/.ssh/prime8_key.pem tobe@prime8.hostname
# Verify Prime8's fingerprint
# Now you're on Prime8!

# Type 'exit' twice to close both connections
```

**Method 2: Connect through gateway in one command**

```bash
ssh -J tobe@gateway tobe@prime8
```

Your mentors will tell you which method to use.

## You're on Prime8: What Now?

Once logged in, your prompt shows you're on a remote computer:

```bash
# After logging in, you see:
tobe@prime8:~$

# This means you're on Prime8, not your laptop!
# Your current directory (/home/tobe) is on Prime8's filesystem

# Example: check where you are
pwd
# Output: /home/tobe (this is on Prime8)

hostname
# Output: prime8.hostname (proves you're on Prime8)
```

Anything you type now runs on Prime8 until you disconnect.

## Disconnecting

To close the SSH connection and return to your laptop:

```bash
exit
# or
logout
# or press Ctrl+D
```

If you used two-hop, you'll need to `exit` twice (once from Prime8, once from gateway).

## Common SSH Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Permission denied (publickey)" | Check key file path exists; verify permissions with `ls -la ~/.ssh/key.pem`; key might not be added to server |
| "Host key verification failed" | Fingerprint doesn't match! Contact mentor before proceeding |
| "Connection refused" | Remote host might be down; check hostname spelling; verify with mentor |
| "ssh: command not found" | Windows: Use PuTTY or install OpenSSH; Mac/Linux: SSH should be built-in |
| "Permissions too open on key file" | Fix with: `chmod 600 ~/.ssh/key.pem` |

## Security Best Practices

**Do:**
- Keep private SSH keys in `~/.ssh/` directory only
- Set correct permissions: `chmod 600 ~/.ssh/key.pem`
- Verify host key fingerprint before accepting `yes`
- Log out when done (type `exit`)
- Use SSH keys instead of passwords when possible
- Report suspicious login attempts to mentors immediately

**Don't:**
- Share your private SSH key with anyone
- Store private keys outside `~/.ssh/`
- Copy private keys to email, USB drives, or shared folders
- Accept SSH connections without verifying the fingerprint
- Leave terminal session logged in and unattended
- Run `sudo` without understanding what you're doing
- Store passwords in files (use SSH keys instead)

## SSH Config File (Optional, Advanced)

To simplify connections, create `~/.ssh/config`:

```
Host gateway
    HostName approved-gateway.address
    User tobe
    IdentityFile ~/.ssh/gateway_key.pem

Host prime8
    HostName prime8.internal
    User tobe
    IdentityFile ~/.ssh/prime8_key.pem
    ProxyJump gateway
```

Then just type:
```bash
ssh prime8
# SSH handles the gateway connection automatically!
```

## File Transfer (scp & sftp)

Transfer files between your laptop and Prime8:

```bash
# Copy file FROM Prime8 TO your laptop
scp -i ~/.ssh/key.pem tobe@prime8:~/remote_file.txt ~/local_file.txt

# Copy file FROM your laptop TO Prime8
scp -i ~/.ssh/key.pem ~/local_file.txt tobe@prime8:~/remote_file.txt

# Copy entire folder
scp -r -i ~/.ssh/key.pem tobe@prime8:~/remote_folder ~/local_folder
```

## Practice Exercise (Week 02)

**Before starting:**
- Your mentor has verified the host key fingerprints with you
- You have the correct SSH key file (usually `~/.ssh/prime8_key.pem` or similar)
- You know the gateway and Prime8 hostnames

**Steps:**

1. Verify your SSH key file exists:
   ```bash
   ls -la ~/.ssh/prime8_key.pem
   ```

2. Connect to Prime8 (one-hop or two-hop as instructed):
   ```bash
   ssh -i ~/.ssh/prime8_key.pem tobe@prime8.hostname
   # Or if using gateway:
   ssh -J tobe@gateway tobe@prime8
   ```

3. When asked about the fingerprint, compare it carefully with what your mentor told you. Type `yes` only if it matches.

4. Check you're on the remote system:
   ```bash
   pwd
   whoami
   hostname
   ```

5. Create a small test file:
   ```bash
   echo "Hello from Prime8" > test.txt
   cat test.txt
   ```

6. Download the file to your laptop:
   ```bash
   exit  # Log out from Prime8
   scp -i ~/.ssh/key.pem tobe@prime8:~/test.txt ~/test.txt
   cat ~/test.txt  # Verify it downloaded correctly
   ```

## Troubleshooting Your First Connection

**Problem: "Host key verification failed"**
- This is a **security feature**, not an error
- Compare the fingerprint with your mentor's information
- Never type 'yes' without verification

**Problem: "Permission denied (publickey)"**
- Your key file might not have the right permissions
- Fix: `chmod 600 ~/.ssh/your_key.pem`
- Or your key might not be on the server yet (mentor setup issue)

**Problem: "Connection refused"**
- Prime8 might be offline
- Or you typed the hostname wrong
- Check with your mentor

## Next Steps

1. Get SSH key setup from your mentors (Week 02)
2. Get gateway and Prime8 hostnames from your mentors
3. Get host key fingerprints from your mentors
4. Test your connection following the practice exercise above
5. Ask questions if anything is unclear

## Additional Resources

- [SSH Manual](https://linux.die.net/man/1/ssh)
- [Verifying SSH Host Keys](https://www.cyberciti.biz/faq/how-to-verify-ssh-host-fingerprints/)
- [SSH Best Practices](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
- [SSH Config Guide](https://linux.die.net/man/5/ssh_config)

---

**Remember:** SSH is how you access powerful remote computers. Verify fingerprints, keep keys secure, and you're ready for research computing.
