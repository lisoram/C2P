# C2P: Context File for AI Assistants

**Read this whole file before doing anything.** It is the handoff
document for any AI assistant (Antigravity, Claude Code, or any other)
working on this project. If you are a new assistant picking up work,
this file plus `docs/` should be enough to understand the project and
continue safely.

------------------------------------------------------------------------

## 1. Working Rules (most important section)

### Don't assume. Check first, then reply.

Look before you say. Read the file, run the command, query the data, and
only then answer.

-   **Facts:** never state something about the code, the database, or
    how a feature behaves unless you have checked it in this session. If
    you haven't checked, say "I haven't checked this" instead of
    presenting a guess as fact.
-   **Worries:** never raise a risk, a problem, or a decision unless you
    have confirmed it is real. First check whether it already exists, is
    already handled, or is actually likely to happen. If it isn't a real
    issue, leave it out.
-   **When unsure:** say what you know, what you don't, and check the
    rest before continuing.

### Don't hallucinate

-   Do not invent file names, function names, library APIs, endpoints,
    table names, environment variables, or config options. Open the file
    or read the library's docs/installed source to confirm they exist.
-   Do not invent requirements. If this file or `docs/` doesn't specify
    something, it is **undecided**, not "probably X". See Section 6 for
    the known undecided items.
-   If you are not sure a package or API version behaves a certain way,
    check the installed version in this repo before using it.

### Ask us before every decision

We want to stay in control of the design. **Stop and ask before:**

-   choosing between two reasonable approaches (libraries, patterns,
    structure)
-   adding a new dependency or tool
-   changing a database schema, an API endpoint shape, or a
    request/response format
-   changing anything that mentioned for Tech Stack 
-   deleting or renaming files, or restructuring folders
-   touching files that belong to another module 
-   anything that costs money, calls an external paid API in a new way,
    or handles secrets

When you ask, give **2 to 3 options**, a one-line trade-off for each,
and your recommendation. Wait for our answer before proceeding. Don't
ask about things the code or this file already settles.

### Stay in scope

-   Do only what the current task asks. No drive-by refactors, no "while
    I was here" changes, no extra features.
-   Build the **current module only**. Do not start Ballooning or
    Budgeting (future scope).
-   Prefer the smallest change that works. Small, reviewable changes are
    better than large rewrites.

### Explain in plain English

Some of us are still learning the architecture and need to understand it
well enough to direct the next prompt. After each task, tell us:

1.  what you changed, and **which files**
2.  **why** you did it that way (a short plain-English reason, an
    analogy if it helps)
3.  how to run or test it
4.  anything you did **not** do or couldn't verify

### Verify your work

Run the code, tests, or the endpoint before saying it works. If you
couldn't run it, say so plainly. Never claim something is tested when it
isn't.

### Never do these

-   Never commit `.env`, API keys, or any secret. Only `.env.example`
    with placeholder values is committed.
-   Never push to `main` or `develop` directly. Work on a feature branch
    .
-   Never edit the database schema by hand. Schema changes go through
    Alembic migrations.
-   Never use `git push --force`, `git reset --hard`, or delete branches
    unless we explicitly ask.

------------------------------------------------------------------------

## 2. What the Project Is

**C2P = Computer-Aided Process Planning.** An AI-powered platform for
engineering drawing intelligence.

**Problem:** In manufacturing, converting a CAED (Computer-Aided
Engineering Drawing) into a precise, cost-effective manufacturing
process plan takes significant manual engineering expertise, time, and
effort. Engineers must manually interpret drawings, identify
manufacturing features and tolerances, and select suitable machines,
tools, workholding, machining sequences, and inspection methods, while
ensuring quality and minimizing cost and time.

**Solution:** C2P uses AI and manufacturing ontology to turn engineering
drawings into structured, explainable, quality-oriented manufacturing
process plans and engineering reports, with a **human in the loop** at
every verification step.

**Pipeline (current build scope):** Upload drawing → extract data (AI) →
human verifies/edits (AI bot assists) → select CNC tools → generate
process plan (AI + bot edits) → save versioned plan with source drawing.
