# Linux Basics

Linux is the operating system that runs Prime8 and most research computing environments. Understanding Linux fundamentals is essential for computational research.

## What is Linux?

Linux is a **free, open-source operating system** used on servers, supercomputers, and research systems worldwide. It's similar to macOS (which is also Unix-based) but with important differences.

**Why Linux for research?**
- Used on nearly all research computing systems
- Powerful command-line tools for data processing
- Free and open-source (no licensing costs)
- Highly configurable
- Excellent for automation and reproducibility

## The Command Line (Shell)

The command line is how you interact with Linux. Instead of clicking icons, you type commands and press Enter.

### Basic Navigation

```bash
pwd                    # Print working directory (where am I?)
ls                     # List files in current directory
ls -la                 # List with details (including hidden files)
cd folder_name         # Change directory (go into a folder)
cd ..                  # Go up one level
cd ~                   # Go to home directory
mkdir new_folder       # Make a new directory
```

### Understanding Directories

Linux organizes files in a hierarchical tree:

```
/                      # Root directory (top of the system)
├── home/              # User home directories
│   └── tobe/          # Your home directory (~)
├── tmp/               # Temporary files
├── usr/               # Programs and data
└── etc/               # Configuration files
```

Your home directory (`~`) is where you have write permissions and should store your personal work.

### File Operations

```bash
cat filename           # Display file contents
less filename          # View file (scroll with space/q to quit)
head filename          # Show first 10 lines
tail filename          # Show last 10 lines
cp source dest         # Copy file
mv source dest         # Move or rename file
rm filename            # Delete file (be careful—no undo!)
rm -r folder           # Delete folder and contents
```

**⚠️ Warning:** `rm` is permanent. There's no trash can. Always double-check before running `rm`.

## File Permissions

Linux controls who can read, write, and execute files:

```bash
ls -l                  # View permissions
chmod u+x script.py    # Make script executable (u=user)
chmod 755 script.py    # Another way to set permissions
```

**Permission bits:**
- `r` = read
- `w` = write
- `x` = execute

Example: `-rwxr-xr-x` means owner can do everything, others can only read/execute.

## Processes & System Monitoring

```bash
ps                     # List running processes
top                    # Interactive process monitor (q to quit)
htop                   # Better version of top (if available)
kill PID               # Terminate a process by ID
```

**Why check processes?**
- Verify your script is running
- Monitor CPU and memory use
- Stop stuck processes

## Environment Variables

Environment variables store configuration like PATH (where to find programs):

```bash
echo $HOME             # Print your home directory
echo $PATH             # Print where shell looks for programs
echo $USER             # Print your username
export VAR=value       # Set a variable (just for this session)
```

These are typically set in your shell configuration file (`.bashrc` or `.zshrc`).

## Useful Advanced Commands

```bash
find . -name "*.py"    # Find all Python files
grep "pattern" file    # Search for text in files
wc -l file             # Count lines in file
du -h folder           # Show disk usage
df -h                  # Show available disk space
which python           # Show where a program is located
man command            # Show the manual for a command
```

## Tips for Success

**1. Explore safely:** Use `ls` before `cd` or `rm` to see what you're doing
```bash
ls ~/folder_to_delete  # Check contents first
rm -r ~/folder_to_delete  # Then delete if sure
```

**2. Use tab completion:** Press Tab to auto-complete file names
```bash
cd /home/groups/Con[TAB]  # Completes to /home/groups/ConradLab/
```

**3. Check your location:** Run `pwd` if you're unsure where you are
```bash
pwd                    # "Oh, I'm in /home/groups/ConradLab/"
```

**4. Read error messages:** They tell you what went wrong
```bash
# Error: "No such file or directory"
# → You typed the path wrong, or file doesn't exist
```

**5. Use `man` for help:** Every command has a manual page
```bash
man ls                 # Read the manual for 'ls'
man grep               # Read the manual for 'grep'
q                      # Exit the manual
```

## Common Mistakes & How to Avoid Them

| Mistake | Problem | Solution |
|---------|---------|----------|
| `rm -r /` | Deletes entire system | Always check paths carefully |
| `cd /tmp` then create files | Files deleted on restart | Use `$HOME` or approved directories |
| `chmod 777 *` | Makes everything accessible | Use specific, restricted permissions |
| Running as root | Can break system | Don't use `sudo` casually |
| Ignoring disk space | Run out of storage | Monitor with `df -h` |

## Practice Exercise (Week 02)

Try these commands on Prime8:

```bash
# 1. Check where you are
pwd

# 2. Go to your home directory
cd ~

# 3. Create a practice folder
mkdir linux_practice

# 4. Go into it
cd linux_practice

# 5. Create a file
echo "Hello Linux" > hello.txt

# 6. View it
cat hello.txt

# 7. Check file details
ls -la

# 8. Go back up
cd ..

# 9. Delete the practice folder
rm -r linux_practice
```

## Next Steps

- Practice these commands on Prime8 (Week 02)
- Read the manual for commands you use: `man command`
- Don't worry about understanding everything—you'll learn by doing
- Ask your mentors if something doesn't make sense

## Additional Resources

- [Linux Journey](https://linuxjourney.com/) — Interactive Linux tutorial
- [Linux Manual Pages](https://man7.org/) — Official documentation
- [Bash Cheat Sheet](https://www.gnu.org/software/bash/manual/) — Quick reference

---

**Remember:** The best way to learn Linux is by doing. Experiment safely in your practice directory, and don't worry about mistakes.

