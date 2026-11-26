# Board formats

Each format lists its sections in banner order. Number the sections on the board to match.

## Product

For apps people use: ticket booking, ride matching, file sharing. Example: `product.excalidraw` (Ticketmaster).

1. **Requirements.** What users can do, what's out of scope, rough scale, and the few limits that matter (speed, uptime, no double booking). Mark assumptions.
2. **Core entities.** The main things the system stores and how they link. Not a full schema.
3. **API.** The calls that make the requirements work, with key inputs and outputs. REST is fine but not required.
4. **High-level design.** The main user actions traced through apps, services, databases and outside systems. Say which store holds the truth and what runs in the background.
5. **Deep dives.** Two or three hard problems from the requirements, each with how it's solved and what it costs.

Add a **Data flow** step between API and High-level design (numbered 3b) only when one lifecycle needs its own picture, like a post going from draft to published.

## Infrastructure

For backend parts: queues, pipelines, crawlers, aggregators, rate limiters. Example: `infrastructure.excalidraw` (ad click aggregator). Ignore the crossed-out section in that file; it was a teaching note.

1. **Requirements.** What it must do, who uses it, scale, and limits on speed, ordering, data loss and uptime.
2. **Inputs and outputs.** What comes in, what goes out, what each record looks like, and the steps in between.
3. **High-level design.** The main path, where data is stored, the workers, and what happens when work piles up.
4. **Deep dives.** How it handles retries, duplicates, recovery, hot spots or memory limits.

## Existing system

For explaining or fixing something that's already built. Example: `detailed.excalidraw`, for its status colours and grouping only.

1. **What it does.** Two or three lines on its purpose and who uses it.
2. **How it works today.** The main flow through the real components, grouped by team or service. Colour each part built, partly built or planned, with a legend. Put the repo and commit you read in a small note under the title.
3. **What's wrong.** Each problem pinned next to the part it affects, in plain words, with how you know.
4. **Fixes.** One fix per problem, with its rough size and anything it depends on.

## Decision

For choosing between ways to build something.

1. **The question.** The decision in one sentence, plus what each person involved wants.
2. **What we have.** Today's setup, only the parts that affect the choice.
3. **Options.** Two to four side by side. Each gets a plain title, a three-box sketch, good and bad points, and a one-line verdict. Mark your pick.
4. **How the pick works.** A diagram of the recommended option.
5. **Risks.** Where the pick could go wrong, and the fix for each.
6. **Next steps.** The build order, and open questions for the people deciding.
