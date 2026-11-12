# Guide to Writing Specific Aims

This guide teaches you how to develop and write a research proposal in the NIH Specific Aims format. This is a standard, learnable format used in scientific research.

## What are Specific Aims?

Specific Aims is a **one-page document** that clearly articulates:
- What scientific problem you're investigating
- Why it matters
- What you will do to solve it
- What you expect to discover

It's the "executive summary" of a research proposal.

## Structure

A typical Specific Aims page has these sections:

### 1. Overall Objective (2-3 sentences)

State your big-picture goal in language an educated non-specialist can understand.

**Example:** "The overall objective is to develop machine learning approaches for automatically detecting and classifying cell types in testis microscopy images, enabling high-throughput analysis of tissue organization."

### 2. Research Problem & Significance (1/2 page)

Explain the problem you're solving and why it matters.

**Structure:**
- What is currently known? (background)
- What is NOT known? (the gap)
- Why does this matter? (significance)
- Who cares? (impact)

**Example:** 
"Testis tissue is composed of multiple cell types organized in specialized structures. Current manual analysis methods are labor-intensive and subjective. While deep learning has shown promise in medical image analysis, applying these methods to testis histology remains unexplored. Automated analysis would accelerate reproductive biology research and enable large-scale tissue characterization."

### 3. Central Hypothesis (1-2 sentences)

State what you believe to be true and will test.

**Example:** "We hypothesize that convolutional neural networks trained on annotated testis images can accurately classify cell types and identify tissue structures with performance approaching expert human analysis."

### 4. Specific Aim 1 (3-4 sentences each)

Write 2-3 specific aims. Each aim should:
- Start with an action verb ("To determine...", "To develop...", "To validate...")
- State what you'll do
- Explain how you'll do it
- Describe expected outcomes

**Example Aim 1:** "To determine the optimal deep learning architecture for classifying Sertoli cells and germ cells in testis microscopy images. We will train and evaluate convolutional neural networks with different architectures (ResNet, DenseNet, Vision Transformer) using annotated images. Success is defined as achieving >95% classification accuracy on held-out test images."

**Example Aim 2:** "To validate that Python-implemented models reproduce the results of established MATLAB-based approaches. We will compare outputs from our Python implementation against reference MATLAB implementations using quantitative metrics and visual inspection. Models will be considered validated if numerical results agree within acceptable biological variation."

**Example Aim 3:** "To explore alternative machine learning approaches for future research. We will investigate unsupervised learning and representation learning approaches and compare their data requirements, computational costs, and performance. This exploration will inform next-phase research directions."

### 5. Feasibility & Timeline (1/4 page)

Briefly explain how you'll accomplish this and on what timeline.

**Example:** "This project is feasible because reference datasets are available, mentors have expertise in both machine learning and testis biology, and computational resources (Prime8 with 1TB RAM) are sufficient. Timeline: Weeks 1-3 for onboarding, Weeks 5-6 for SATINN study and reproducibility, Weeks 7-10 for Python development, Weeks 11-12 for validation and next-phase planning."

## Tips for Writing Effective Specific Aims

✅ **Do:**
- Use clear, direct language (avoid jargon where possible; define terms you must use)
- Be specific ("determine which cell types are misclassified" is better than "improve performance")
- Focus on what you'll discover, not just what you'll do
- Make it testable (could someone check if you succeeded?)
- Align with available resources and timeframe

❌ **Don't:**
- Overclaim ("prove with 100% certainty")
- Use complicated sentences
- Propose things that are impossible with available resources
- Focus on methods instead of scientific questions
- Make it longer than one page

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too vague ("improve the system") | Be specific: "improve segmentation accuracy by 5% using data augmentation" |
| Too ambitious ("solve testis biology") | Narrow scope: "classify two major cell types in histological images" |
| Method-focused ("write Python code") | Outcome-focused: "determine if Python implementation reproduces MATLAB results" |
| No feasibility discussion | Briefly explain how it's achievable with available resources |

## The One-Page Limit

Everything must fit on ONE page. Use:
- 11-12 point font
- Single spacing
- Narrow margins (0.5 inches)
- Minimal graphics (focus is text)

**Ruthlessly cut:** If it doesn't directly support your aims, remove it.

## Developing Your Own Proposal (Weeks 7-8)

1. **Identify a research question** (Weeks 3-4)
   - What biological or computational problem interests you?
   - What would you want to know more about?

2. **Do a literature review** (Weeks 5-6)
   - What's already known?
   - What gaps exist?
   - What's not been tried?

3. **Draft your aims** (Weeks 7-8)
   - Write freely; editing comes later
   - Aim for clarity over perfection

4. **Get mentor feedback** (Weeks 9-10)
   - Eisa and Don will help refine
   - Iterate until clear and feasible

5. **Polish and present** (Weeks 11-12)
   - Create final version
   - Practice your presentation

## Real Examples

Your mentors will share real Specific Aims pages from:
- Published research proposals
- Successful grant applications
- Prior student work

Study these to understand the standard format.

## Next Steps

- Week 3: Develop your research question
- Week 5: Complete literature review
- Week 7: Draft your Specific Aims
- Week 9: Revise with mentor feedback
- Week 12: Present your final proposal

---

**Remember:** Specific Aims is a skill. It takes practice. Your first draft won't be perfect, and that's fine. Each iteration gets better.

See also: [docs/templates/specific-aims-outline.md](../templates/specific-aims-outline.md)
