#!/usr/bin/env python3
import subprocess

REPO = "conradlab/TobeProjectManagment"

# SATINN Research Epic
satinn_body = """# SATINN Research & Python Development Epic

This epic encompasses Weeks 5-12 of Tobe's research internship, focusing on understanding and reimplementing SATINN in Python.

## Overview

SATINN (Software for Analysis of Testis Images with Neural Networks) is a machine learning system for analyzing testicular tissue images. Tobe will:

1. Study the published SATINN papers and existing architecture
2. Reproduce results using existing code
3. Design a modular Python reimplementation
4. Implement and validate Python components
5. Explore alternative ML approaches

## Related Weekly Issues

- [Week 05: Understanding SATINN](../../issues/6)
- [Week 06: SATINN Reproducibility](../../issues/7)
- [Week 07: Design Modular Architecture](../../issues/8)
- [Week 08: First Python Components](../../issues/9)
- [Week 09: Model Interfaces & Baselines](../../issues/10)
- [Week 10: Validation & Scientific Comparison](../../issues/11)
- [Week 11: Alternative ML Approaches](../../issues/12)
- [Week 12: Presentation & Research Review](../../issues/13)

## Research Milestones

- [ ] **Week 5-6:** Understand SATINN architecture and reproduce reference results
- [ ] **Week 7:** Complete architecture design document with mentor review
- [ ] **Week 8:** Implement and test first Python component
- [ ] **Week 9:** Design model interfaces and implement baselines
- [ ] **Week 10:** Validate Python implementation against reference; prepare scientific report
- [ ] **Week 11:** Explore and document alternative ML approaches
- [ ] **Week 12:** Final presentation; plan next research phase

## Key Deliverables

1. **Literature Summary** (Week 5-6) - Summary of SATINN papers and software architecture
2. **Architecture Document** (Week 7) - Design of modular Python implementation
3. **Working Python Components** (Weeks 8-9) - Implemented and tested code
4. **Validation Report** (Week 10) - Scientific comparison of Python vs. reference
5. **Alternatives Analysis** (Week 11) - Feasibility of different ML approaches
6. **Research Presentation** (Week 12) - Final presentation of work

## Questions for Mentors

- [ ] Which SATINN source code version should Tobe use?
- [ ] Are there specific research papers to prioritize?
- [ ] What are the validation metrics for the reference implementation?
- [ ] Should Tobe implement the full SATINN pipeline or focus on specific components?
- [ ] What alternative ML approaches should be explored?

## Notes

This epic runs parallel to independent research (Epic #14) and builds on foundational skills from Weeks 1-4.
"""

# Independent Research Epic
independent_body = """# Independent Research Proposal Epic

This epic spans Weeks 3-12, enabling Tobe to develop an original scientific research proposal.

## Overview

Tobe will develop an independent scientific research idea from problem definition through proposal presentation. This runs parallel to the SATINN research track.

## Research Proposal Timeline

### Phase 1: Define Research Problem (Weeks 3-4)

- [ ] Identify a scientific question or problem
- [ ] Preliminary background research
- [ ] Initial mentor discussion

**Expected output:** Problem statement (1-2 paragraphs)

### Phase 2: Literature Review (Weeks 5-6)

- [ ] Systematic literature search
- [ ] Read 8-10 key papers
- [ ] Identify research gap

**Expected output:** Literature review (3-4 pages)

### Phase 3: Hypotheses & Specific Aims (Weeks 7-8)

- [ ] Formulate clear, testable hypotheses
- [ ] Write NIH Specific Aims (2-3 pages)
- [ ] Design preliminary experiments

**Expected output:** Specific Aims document with mentor review

### Phase 4: Feasibility & Refinement (Weeks 9-10)

- [ ] Refine experimental design
- [ ] Assess time/resource requirements
- [ ] Address feasibility concerns
- [ ] Revise Specific Aims based on feedback

**Expected output:** Refined proposal and feasibility assessment

### Phase 5: Presentation & Next Steps (Weeks 11-12)

- [ ] Prepare research presentation
- [ ] Present to Eisa and Don
- [ ] Discuss next research phase

**Expected output:** Final presentation and planning document

## Key Questions to Answer

1. What is your research question?
2. Why does it matter?
3. What has been done before?
4. What is novel about your approach?
5. How will you test your hypotheses?
6. What resources do you need?

## Integration with Other Tracks

- **Computational Foundations (Weeks 1-3):** Develop skills needed for research computing
- **SATINN Research (Weeks 5-12):** Potential overlap or inspiration for research ideas
- **Machine Learning (Week 4):** Foundation for ML-based research approaches

## Success Criteria

- [ ] Clear, well-defined research problem
- [ ] Comprehensive literature review
- [ ] Testable, specific hypotheses
- [ ] Feasible within 12-week timeframe (or realistic longer timeline)
- [ ] Mentor-approved proposal
- [ ] Professional research presentation

## Important Guidelines

- Do NOT invent preliminary results or data
- Do NOT claim novelty without literature support
- Do focus on hypothesis-driven research
- Do be realistic about timelines and resources
- Do ask questions early and often

---

**Mentors:** Provide feedback on research direction and feasibility.  
**Student:** Use this epic to track your proposal development.
"""

def create_epic(title, body, labels):
    """Create an epic (really just an Issue with epic label)"""
    cmd = ["gh", "issue", "create", 
           "--repo", REPO,
           "--title", title,
           "--body", body]
    
    for label in labels:
        cmd.extend(["--label", label])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        if "#" in result.stdout:
            issue_num = result.stdout.strip().split("#")[1].split(" ")[0]
            print(f"✓ Created Epic #{issue_num}: {title}")
        else:
            print(f"✓ Created Epic: {title}")
    else:
        print(f"✗ Failed to create Epic: {title}")
        print(f"  Error: {result.stderr}")

print("Creating Research Epics...")
print()

create_epic(
    "SATINN Research & Python Development Epic",
    satinn_body,
    ["track:satinn", "type:research"]
)

create_epic(
    "Independent Research Proposal Epic",
    independent_body,
    ["track:independent-research", "type:research"]
)

print()
print("✓ Epics created!")
