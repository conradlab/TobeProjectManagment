# SSH & Remote Computing

SSH (Secure Shell) lets you safely log into remote computers and run programs on them. Prime8 is accessed via SSH.

## What is SSH?

SSH is a protocol for securely connecting to remote computers:

- **Secure:** Encrypted communication (bad actors can't read your data)
- **Shell:** Gives you a command-line prompt on the remote computer
- **Remote:** You control a distant computer from your local computer

Example workflow:
1. You sit at your laptop
2. SSH to Prime8 (Conrad Lab's compute server)
3. Run Python scripts on Prime8 (which has 1TB RAM and 100+ CPUs)
4. View results on your laptop

## SSH Keys vs. Passwords

**SSH Keys (recommended):**
- Public key (safe to share): Like your email address
- Private key (keep secret): Like your password
- Public key goes on Prime8; private key stays on your computer
- More secure than passwords
- No need to type password every time

**Passwords:**
- Simpler setup
- Less secure if intercepted
- Have to type it every time

Your mentors will set up SSH keys for you (or guide you through it).

## First-Time SSH Connection

Your mentors will tell you:
- Gateway hostname (approved access host)
- Your username on Prime8
- Path to your private SSH key file (or password)

Typical first connection:

```bash
# Windows: Use PuTTY or OpenSSH
# Mac/Linux: Use terminal

ssh -i ~/path/to/key.pem username@approved-gateway.address

# If using password (instead of key):
ssh username@approved-gateway.address
# Then type your password when prompted
```

Example (with sample names):
```bash
ssh -i ~/.ssh/prime8_key.pem tobe@approved-gateway.internal
```

**First time you connect:**
- SSH will show a fingerprint and ask "Are you sure you want to continue?"
- Type `yes` (compare the fingerprint with your mentor if paranoid)
- You'll be logged in!

## After Connecting: You're on Prime8

Once logged in, your prompt changes. You're now running commands **on Prime8** not your computer:

```bash
# You type this
ssh -i ~/.ssh/prime8_key.pem tobe@gateway

# Result: prompt changes
tobe@prime8:~$

# Now you're on Prime8!
pwd
# Output: /home/tobe
# (This is Prime8's filesystem, not your laptop's)
```

Anything you type now runs on Prime8 until you disconnect.

## Disconnecting

To close the connection and go back to your laptop:

```bash
exit
# or
logout
# or press Ctrl+D
```

## Multi-Hop SSH (Gateway → Prime8)

If there's an approved gateway between your laptop and Prime8:

```bash
# Option 1: Connect in two steps
# Step 1: SSH to gateway
ssh username@approved-gateway.address

# Step 2: From gateway, SSH to Prime8
ssh username@prime8

# Option 2: SSH through gateway in one command
ssh -J username@gateway username@prime8
```

Your mentors will tell you if you need multi-hop access.

## Common SSH Issues & Fixes

| Problem | Solution |
|---------|----------|
| "Permission denied (publickey)" | Check key file path, permissions; key might not be added to Prime8 |
| "Connection refused" | Remote host might be down; check hostname; try again |
| "ssh: command not found" | Windows: Use PuTTY instead, or install OpenSSH |
| "Permissions too open" key file | Key file should be readable only by you: `chmod 600 ~/.ssh/key.pem` |

## Security Best Practices

✅ **Do:**
- Keep private SSH keys in `~/.ssh/` directory
- Set permissions: `chmod 600 ~/.ssh/key.pem`
- Log out when done
- Use SSH keys instead of passwords
- Report suspicious login attempts to mentors

❌ **Don't:**
- Share your private SSH key with anyone
- Copy private keys to insecure locations
- Leave terminal session logged in and unattended
- Run `sudo` casually (you'll need it, but use carefully)
- Store passwords in files (use SSH keys instead)

## SSH Config File (Optional)

Create `~/.ssh/config` to simplify connections:

```
Host gateway
    HostName approved-gateway.address
    User tobe
    IdentityFile ~/.ssh/prime8_key.pem

Host prime8
    HostName prime8.internal
    User tobe
    IdentityFile ~/.ssh/prime8_key.pem
    ProxyJump gateway
```

Then just type:
```bash
ssh prime8
# It handles the rest!
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

1. Verify your SSH key is set up (mentor will confirm)
2. Connect to Prime8:
   ```bash
   ssh -i ~/.ssh/key.pem your_username@prime8
   ```
3. Check you're on remote system:
   ```bash
   pwd
   whoami
   hostname
   ```
4. Create a small test file:
   ```bash
   echo "Hello from Prime8" > test.txt
   cat test.txt
   ```
5. Download the file to your laptop:
   ```bash
   exit  # Log out first
   scp -i ~/.ssh/key.pem your_username@prime8:~/test.txt ~/test.txt
   cat ~/test.txt  # Verify it worked
   ```

## Next Steps

- Get SSH key from your mentors or generate one (Week 02)
- Test connection to Prime8
- Practice with the exercises above
- Ask if anything is unclear

## Additional Resources

- [SSH Manual](https://linux.die.net/man/1/ssh)
- [OpenSSH Best Practices](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
- [SSH Config Guide](https://linux.die.net/man/5/ssh_config)

---

**Remember:** SSH is how you access powerful remote computers. Secure it, and you're ready for research computing.

