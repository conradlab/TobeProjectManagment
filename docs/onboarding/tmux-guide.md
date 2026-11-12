# Terminal Multiplexing with tmux

tmux lets you create multiple terminal windows and panes within a single SSH connection. It's essential for research computing.

## Why tmux?

When you SSH to Prime8, one SSH session = one window. If your connection drops, your programs stop.

tmux solves this:
- Multiple windows/panes in one session
- Detach and reattach (disconnect laptop, SSH back, resume work)
- Long-running programs keep running even if SSH disconnects
- Easy multitasking on remote server

## Basic tmux Concepts

**Session:** A collection of windows (your entire work session)
**Window:** Like a tab (each window has one or more panes)
**Pane:** A rectangular area showing output (split screen)

```
Session "learning"
├── Window 0: editing
│   ├── Pane (left): $
│   └── Pane (right): $
└── Window 1: running_job
    └── Pane: Output from a Python script
```

## Creating and Managing Sessions

```bash
# Create a new session named "learning"
tmux new-session -s learning
# Or shorthand:
tmux new -s learning

# List all sessions
tmux ls

# Attach to an existing session
tmux attach -t learning

# Detach from current session (keep it running)
# Press: Ctrl+B then D

# Kill a session (stop it)
tmux kill-session -t learning
```

## Within a tmux Session

Once inside tmux, your prefix key is `Ctrl+B`. All tmux commands start with this.

### Windows (tabs)

```bash
# Create new window
Ctrl+B C

# Switch to next window
Ctrl+B N

# Switch to previous window
Ctrl+B P

# List windows and select
Ctrl+B W

# Rename current window
Ctrl+B ,

# Kill current window
Ctrl+B X
```

### Panes (split screen)

```bash
# Split pane horizontally (left-right)
Ctrl+B %

# Split pane vertically (top-bottom)
Ctrl+B "

# Switch to next pane
Ctrl+B O

# Kill current pane
Ctrl+B X
```

### Scrolling

```bash
# Enter copy mode (scroll/search)
Ctrl+B [

# Navigate with arrow keys
# Press Q to exit copy mode
```

## Practical Workflow

### Example: Long-running experiment

```bash
# 1. SSH to Prime8
ssh -i ~/.ssh/key.pem tobe@prime8

# 2. Create a tmux session
tmux new -s experiment

# 3. Start a long Python job
python train_model.py  # runs for hours...

# 4. Detach (Ctrl+B then D)
# Connection closes, but job keeps running!

# 5. Next day, SSH back
ssh -i ~/.ssh/key.pem tobe@prime8

# 6. Reattach to session
tmux attach -t experiment

# 7. Check if training finished!
```

### Example: Multiple tasks at once

```bash
# 1. Create session
tmux new -s work

# 2. Create and switch to Window 0: Editing
# You're in window 0 by default

# 3. Edit code
nano script.py
# (Edit, then Ctrl+X to save)

# 4. Create Window 1: Testing
Ctrl+B C

# 5. Run the script
python script.py

# 6. Switch back to window 0 (editing)
Ctrl+B 0

# 7. Make changes to script
nano script.py

# 8. Switch to window 1 and run again
Ctrl+B 1
python script.py
```

## Common Scenarios

### Session Drops / SSH Connection Lost

```bash
# On your laptop, reconnect
ssh -i ~/.ssh/key.pem tobe@prime8

# Reattach to your work
tmux attach -t experiment

# Everything still running!
```

### Working with large output

```bash
# In tmux, enter copy mode
Ctrl+B [

# Use arrow keys to scroll
# Use / to search
# Press Q to exit

# Or just pipe to `less`
program_output | less
```

### Monitoring multiple jobs

```bash
# Create session
tmux new -s monitor

# Split into panes (top and bottom)
Ctrl+B "

# Top pane: top command
top

# Switch to bottom pane
Ctrl+B O

# Bottom pane: run something else
python job2.py
```

## tmux Cheat Sheet

| Action | Command |
|--------|---------|
| New session | `tmux new -s name` |
| List sessions | `tmux ls` |
| Attach session | `tmux attach -t name` |
| Kill session | `tmux kill-session -t name` |
| New window | `Ctrl+B C` |
| Next window | `Ctrl+B N` |
| Previous window | `Ctrl+B P` |
| Split pane (H) | `Ctrl+B %` |
| Split pane (V) | `Ctrl+B "` |
| Next pane | `Ctrl+B O` |
| Detach | `Ctrl+B D` |
| List windows | `Ctrl+B W` |

## Best Practices

✅ **Do:**
- Use named sessions: `tmux new -s analysis` (easier to remember)
- Detach before logging out
- Keep one session per project
- Use windows to organize different tasks
- Check `tmux ls` before connecting to Prime8

❌ **Don't:**
- Forget to detach (close the window instead)
- Create dozens of tiny sessions
- Leave sensitive data visible on screen
- Run `exit` when you mean to detach

## Practice Exercise (Week 02)

```bash
# On Prime8 (via SSH)

# 1. Create a session
tmux new -s learning

# 2. Create a file
echo "print('Hello from tmux')" > hello.py

# 3. Create a new window
Ctrl+B C

# 4. In the new window, run Python
python hello.py

# 5. Create another window
Ctrl+B C

# 6. Monitor system
top

# 7. Detach from everything
Ctrl+B D

# 8. Close SSH
exit

# 9. SSH back
ssh -i ~/.ssh/key.pem tobe@prime8

# 10. Check sessions
tmux ls

# 11. Reattach
tmux attach -t learning

# 12. All three windows still there! Switch between them:
Ctrl+B 0   # First window
Ctrl+B 1   # Second window
Ctrl+B 2   # Third window (top)
```

## Next Steps

- Practice tmux on Prime8 (Week 02)
- Use it for all your long-running jobs
- Experiment with windows and panes
- Build muscle memory for Ctrl+B commands

## Additional Resources

- [tmux Manual](https://man7.org/linux/man-pages/man1/tmux.1.html)
- [tmux Tutorial](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)
- [tmux Cheat Sheet](https://tmuxcheatsheet.com/)

---

**Key Takeaway:** tmux is your safety net for remote computing. Use it for any job that takes more than a few seconds.

