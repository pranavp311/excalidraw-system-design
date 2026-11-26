---
name: excalidraw-system-design
description: "Draw a system design board in Excalidraw. Use for excalidraw sys design, system design in excalidraw, architecture diagrams or whiteboards, mapping how an existing system works, or laying out options for a technical decision. Picks one of four board formats, draws it, checks the render and opens it on excalidraw.com."
---

# Excalidraw system design

Make a board someone new to the project can read in two minutes. You hand back an editable `.excalidraw` file and a PNG.

## 1. Pick the format

Every board uses one of these four formats. Each one has a banner under the title: a row of boxes joined by arrows, one per section, each with a mint numbered circle. Every section below starts with the same numbered circle. Don't invent a fifth. If a request seems to need two, pick the main one and fit the other inside a section.

| The person wants to | Format | Banner |
| --- | --- | --- |
| Design a new product or app | Product | Requirements → Core entities → API → High-level design → Deep dives |
| Design a new backend part (queue, pipeline, rate limiter) | Infrastructure | Requirements → Inputs and outputs → High-level design → Deep dives |
| Understand or fix a system that already exists | Existing system | What it does → How it works today → What's wrong → Fixes |
| Choose between ways to build something | Decision | The question → What we have → Options → How the pick works → Risks → Next steps |

[references/frameworks.md](references/frameworks.md) says what goes in each section. Say which format you picked in one line before drawing.

## 2. Gather facts and plan

- For an existing codebase, read the code. Don't label anything as built unless you saw it in the source.
- For a new design, mark guesses as assumptions.
- Open the closest example in [references/examples.md](references/examples.md) and copy its layout, not its content.
- Before drawing, list the sections, the main flow you'll trace and two or three deep dives. Only ask the person a question if the answer changes the design. If they asked to design it "with me", agree the requirements with them before drawing the rest.

## 3. Write in plain words

People who don't know the code will read this board. Most past complaints were about wording, so treat this as a hard rule.

- **Boxes.** A name, then up to five words on what it does. "Publish worker / posts every minute", not "PublishJobProcessor (lease-based)".
- **Use names people already use.** Never invent a component name like "question router". If nothing has a name yet, describe what it does.
- **No jargon.** Drop terms like RLS, lease, idempotent, fan-out or SECURITY DEFINER unless the reader is an engineer and the term matters. If the board needs a special word, define it in a small "Words used" box.
- **Arrows.** One to three words saying what moves: "posts", "failures", "nightly sync".
- **Notes.** One idea per line, about twelve words at most, and no more than five lines under any section. Cut any note that repeats a box.
- **Reread as an outsider.** Before finishing, read every label as someone new to the project would. Rewrite anything they'd have to ask about.

## 4. Draw it

- White background, hand-drawn font, mint (`#299a8d`) numbered markers that match the banner. An extra step like 3b gets its own banner box.
- Give the main diagram the most space and put the other sections around it.
- Colour-code the board wherever a colour can carry meaning, and add a legend that says what each colour means. Use Excalidraw's light fills with dark strokes so text stays readable:
  - **By kind** on Product, Infrastructure and Decision boards: blue `#a5d8ff` for apps and clients, green `#b2f2bb` for your services, yellow `#ffec99` for databases and queues, violet `#d0bfff` for outside services, grey `#e9ecef` for notes and requirements.
  - **By status** on Existing system boards: green for built, yellow for partly built, grey dashed for planned.
  - Red `#ffc9c9` always means a failure or problem, on any board. On Decision boards, give your pick a mint (`#299a8d`) outline.
  - The same thing gets the same colour everywhere on the board. Don't colour a box just to decorate it.
- Dashed outlines for later or proposed parts.
- Solid arrows for direct calls, dashed for background work.
- Keep the person's existing drawings. Never clear a canvas you didn't create.

[references/canvas.md](references/canvas.md) covers setting up the canvas, loading scenes and exporting.

## 5. Check the render

Look at the real PNG, not the JSON. Zoom into each section and fix:

- text cut off at the edge of its box (the hand-drawn font is wider than it looks)
- labels sitting on arrows or on other labels
- arrows crossing boxes they don't connect to
- stray or leftover elements

Then trace one full flow end to end and check that each deep dive answers a requirement. Re-render after fixes. If you couldn't render, say the board is unchecked.

## 6. Hand it over

1. Export the `.excalidraw` and the PNG. For big boards, also export one PNG per section.
2. Open the board on excalidraw.com in the person's browser. This backs up whatever drawing they had there first. Steps are in [references/canvas.md](references/canvas.md#open-the-finished-board-on-excalidrawcom).
3. Stop any local canvas server you started.
4. Reply in a few lines: the file paths, any assumptions, the backup key if one was made, and on a Decision board your pick and why.

Don't create share links unless asked. Edits made on excalidraw.com stay in that browser until the person exports them.
