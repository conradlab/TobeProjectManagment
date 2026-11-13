# Specific Aims Outline Template

**Purpose:** Template for Tobe to develop one-page research proposal (Weeks 3-12)

**Instructions:** 
- Fill in each section with your specific research question
- Keep to one page maximum (this is a constraint, not a goal)
- Use this template for each iteration as your ideas evolve
- Submit final version by end of Week 12

---

## [YOUR RESEARCH TITLE]

### Long-Term Goal

What is the broader context? Why is this research important in the field?

---

### Specific Research Question

State in one clear sentence. Example: "We hypothesize that [X phenomenon] [does/doesn't occur] under [conditions], resulting in [predicted outcome]."

---

### Specific Aims

List 2-3 specific, measurable aims. Use action verbs (determine, measure, characterize, test, compare).

**Aim 1:**

**Aim 2:**

**Aim 3:**

---

### Expected Outcomes

Briefly describe what results you anticipate and how they will answer your research question.

---

### Significance

Explain why your findings matter. How will they advance the field? What practical applications or insights could result?

---

## Example Completed Template

### Cellular Heterogeneity in Spermatogenic Stages

### Long-Term Goal
Our long-term goal is to understand how the testis maintains 
spermatogenesis across the lifespan. Spermatogenesis is organized 
into discrete developmental stages, yet little is known about whether 
cellular properties (morphology, gene expression) change across stages. 
We aim to develop methods to map cellular heterogeneity during 
normal spermatogenesis, which could illuminate both basic reproductive 
biology and factors that contribute to age-related male infertility.

### Specific Research Question
We hypothesize that germ cells and Sertoli cells exhibit stage-specific 
morphological and organizational patterns that reflect developmental 
demands at each stage of spermatogenesis.

### Specific Aims

**Aim 1:** Use automated image segmentation (SATINN) to identify and 
characterize cell nuclei across tissue samples representing all eight 
developmental stages. Extract morphological features (size, shape, 
eccentricity) for each cell type.

**Aim 2:** Quantify cell-type-specific morphological changes across 
developmental stages and identify which features best distinguish 
early from late stages.

**Aim 3:** Correlate morphological changes with known developmental 
events (e.g., meiosis transition) to establish functional relationships 
between cellular structure and developmental state.

### Expected Outcomes
We expect to find that germ cell nuclei progressively increase in size 
and irregularity as they differentiate through meiosis, while Sertoli 
cells maintain consistent size but change their spatial positioning. 
Identifying stage-specific cellular signatures would enable rapid 
assessment of spermatogenic status from tissue samples, with 
applications to fertility diagnosis and aging research.

### Significance
This work provides the first quantitative characterization of 
morphological heterogeneity in normal spermatogenesis, bridging 
cellular morphology and developmental stage. The methods are 
immediately applicable to identify architectural abnormalities 
associated with infertility or aging. Understanding normal variation 
is essential for developing therapies that restore function to 
damaged tissue.

---

## Length Guidelines

**One page = approximately:**
- 250-300 words (10-12 sentences)
- Long-Term Goal: 1-2 sentences
- Specific Research Question: 1 sentence
- Specific Aims: 1-2 sentences each (3 aims = 3-6 sentences)
- Expected Outcomes: 2-3 sentences
- Significance: 2-3 sentences

**Total: ~25-30 lines of text**

---

## Iterative Development

### Iteration 1 (Week 4): Initial Idea
- Broad, exploratory
- Likely to change significantly
- ~100 words

### Iteration 2 (Week 8): Refined Hypothesis
- More specific
- Feasible within timeline
- ~200 words

### Iteration 3 (Week 12): Final Proposal
- Precise and testable
- Includes preliminary data if available
- Exactly one page
- Ready for presentation or submission

---

## Common Pitfalls and How to Fix Them

### Pitfall 1: Too Vague
**Bad:** "We want to understand testis biology"
**Good:** "We hypothesize that Sertoli cell clustering varies across developmental stages and correlates with germ cell density"

### Pitfall 2: Too Ambitious
**Bad:** "We will characterize all genes expressed in testis cells at each stage"
**Good:** "We will measure spatial clustering of Sertoli cells across three developmental stages"

### Pitfall 3: Too Technical
**Bad:** "We will compute eigenvectors of the spatial covariance matrix using principal component analysis"
**Good:** "We will measure how tightly Sertoli cells are clustered together using nearest-neighbor distance"

### Pitfall 4: Missing Significance
**Bad:** "We will measure morphological features of cells"
**Good:** "We will identify morphological features that distinguish fertile from subfertile tissue, enabling non-invasive diagnosis of male infertility"

### Pitfall 5: Exceeds One Page
**Solution:** Cut ruthlessly
- Remove jargon
- Combine related sentences
- Use specific numbers instead of prose ("20% increase" vs. "a substantial increase")
- Eliminate qualifiers ("arguably," "likely," "possibly")

---

## Self-Review Checklist

Before submitting your final Specific Aims:

- [ ] **Clarity:** Could someone unfamiliar with the project understand my question?
- [ ] **Specificity:** Are my aims concrete and measurable (not vague)?
- [ ] **Feasibility:** Can I realistically complete this by end of Week 12?
- [ ] **Significance:** Why should anyone care? What's the broader impact?
- [ ] **Length:** Exactly one page? (Trim if longer!)
- [ ] **Grammar:** Proofread for spelling and clarity
- [ ] **Alignment:** Aims directly address the research question?
- [ ] **Independence:** Does this go beyond SATINN reimplementation?
- [ ] **Methods:** Are methods sound and appropriate?

---

## Key Questions to Answer in Your Proposal

If you can clearly answer these, your Specific Aims are ready:

1. **What is the central question?** (Write one sentence)
2. **Why is it important?** (One sentence)
3. **What will you do?** (Specific Aims, 3 bullets)
4. **What do you expect to find?** (One sentence)
5. **How will that advance the field?** (One sentence)

---

## Integration with SATINN

Your independent research should leverage SATINN outputs:

```
SATINN Pipeline
    ↓ Produces
Segmented cells + extracted features
    ↓ You apply
Your analysis method (clustering, statistics, visualization)
    ↓ To answer
Your independent research question
```

**Example workflow:**
```
Week 7: SATINN provides cell segmentations for tissues 
        from all developmental stages

Week 9: You extract Sertoli cell locations from each segmentation

Week 10: You compute nearest-neighbor distances to assess clustering

Week 12: You compare clustering across stages and interpret results
```

---

## Mentor Feedback Template

When you submit your Specific Aims for feedback:

**To Your Mentor:**
```
I've developed a research proposal to extend the SATINN work. 
My question is: [one sentence]

Here's my one-page Specific Aims document. I'm looking for feedback on:
1. Is the research question clear and specific?
2. Are the aims feasible in the timeline?
3. Is the approach scientifically sound?
4. What should I revise before Week 12?
```

**From Your Mentor:**
```
Feedback on [Your Name]'s Specific Aims:

Strengths:
- [Clear question / specific aims / feasible approach]

Areas for revision:
- [Aim is too vague / timeline is too ambitious / methods unclear]

Suggestions:
- [Reframe question as / simplify approach to / clarify methods]

Status: [Approved to proceed / Needs revision / Discuss further]
```

---

## References and Further Reading

- **Specific Aims guide:** https://grants.nih.gov/grants/how-to-apply-application-guide/format-and-write/format-attachments.htm
- **Research question examples:** https://www.cdc.gov/csels/dsepd/ss1000/lesson1/index.html
- **Hypothesis formulation:** https://en.wikipedia.org/wiki/Hypothesis#Characteristics
- **Feasibility assessment:** https://libguides.uoregon.edu/c.php?g=119878

---

## How to Submit Your Final Specific Aims

**By end of Week 12:**
1. Create final 1-page document (PDF or Google Doc)
2. Submit to mentor with cover email
3. Include: title, your name, date, one-page Specific Aims
4. Optional: brief (5-minute) verbal summary at lab meeting

**Final checklist:**
- [ ] One page (no more, no less)
- [ ] All sections completed
- [ ] Mentor has approved (or provided feedback addressed)
- [ ] Proofread for grammar
- [ ] Ready to present or publish
