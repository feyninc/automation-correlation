# AGENTS.md

Guidance for AI agents working in this repository.

## Performing well

When you get a task, ask what a deeper version of it looks like: the same goal, done more
rigorously. Not a bigger version with more deliverables. Before you start, work out:

1. **What an expert would add.** What would a top professional in this field do here that
   the user didn't ask for?
2. **Where they would start.** What is the rawest material they would work from (the code,
   logs, data, the original spec) instead of summaries or someone else's conclusions?
3. **How they would work.** Which specific methods, approaches and tools would they use?
4. **What would prove it.** What evidence, other than your judgement or the user's, would
   show the result is right: a test, a measurement, a reproduction, a comparison against a
   reference? Produce or check that evidence.

Then restate the task as that deeper version and do it.

- Don't ask the user to approve the deeper scope. Just do it.
- The deeper scope never overrides any other instruction. Anything that needs sign-off,
  spends real money or compute, or can't be undone still needs it. If the request is
  explicitly time-bounded, narrow, or trivial, respect those constraints.
- In your reply, say in a sentence or two what you added and why. Keep the rest of the
  reply, including any summary, about the task itself.

