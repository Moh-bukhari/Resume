---
name: cold-outreach-pattern-interrupt
description: |
  Make an outreach message memorable and unmistakably personal by breaking
  the pattern every other cold message follows. Use when a draft reads as
  competent but forgettable, when writing LinkedIn connection notes and DMs,
  or when a contact deserves a message nobody else would write. Distilled
  from Moatt's linkedin-voicenote-pre-warm move (see Source), adapted from
  voice to written outreach.
license: unknown (source license not stated; this file is an original
  distillation with attribution, no verbatim copying)
metadata:
  version: "1.0.0"
  adapted_for: written outreach (connection notes, DMs, emails); the source
    move is a 30-45 second voice note, and its principles transfer directly
---

# Pattern interrupt: be the one message they remember

A hiring-team contact gets dozens of outreach messages that all follow
the same shape: greeting, compliment, self-introduction, proof list,
meeting ask. Readers stop reading that shape before the second line.
A pattern interrupt breaks the shape in the first sentence, with
something that could only have been written by someone who actually
looked. The goal is not to be loud or clever. It is to be specific in
a way that makes the reader pause.

## The principle, in one line

One verifiable fact about them, connected to one true thing about you,
plus one small ask. Everything else is cut.

## Fact priority ladder

Hunt facts in this order. Take the first one you can verify with a
source and a date. Stop there; do not collect more.

1. **Recent post or talk (within ~30 days):** their own words. The
   strongest fact, because it is theirs and it dates itself.
2. **Hiring signal (within ~30 days):** a role they posted, a team they
   are building, a "we are hiring" note.
3. **Company event (within ~90 days):** launch, partnership, migration,
   reorg, but only if it touches their seat.
4. **Talk or appearance (within ~90 days):** podcast, panel, conference.
5. **Stack or workflow change:** a tool adopted, a system replaced, a
   process described in their own words.
6. **Tenure milestone:** weakest. Use only when nothing else exists.

Every fact needs a source the writer can check before sending. If you
cannot verify it, do not use it. A wrong "personal" detail destroys
trust faster than a generic message.

## The memorable-message structure

1. **Observation (one sentence).** Their fact, in your words, with a
   detail only a reader would know. Not a summary of their bio. A
   moment: what they said, what they shipped, what they decided.
2. **Why it stuck (one sentence).** Your honest reaction or the
   consequence you draw. This is the sentence no template can produce,
   because it carries your judgment. Keep it plain; a forced clever
   line reads worse than a plain true one.
3. **One proof point (one sentence).** Yours, matched to their fact.
   Not your resume. The one thing you built that belongs in this
   conversation.
4. **One small ask (one sentence).** A question they can answer in a
   sentence, a name, or a read of the application. Never a meeting ask
   on first contact.

Total: four sentences for a DM, under 90 words for an email, under 280
characters for a connection note. If the message needs a fifth sentence,
one of the four is doing two jobs badly; rewrite it.

## What makes it unique

- **An angle nobody else uses.** Every applicant cites the company
  homepage and the job post. Almost nobody cites the hiring lead's own
  post about how they hire, or the deployments lead's own post about
  joining. The niche fact is the moat.
- **A point of view, not a compliment.** "Your post ranked experience
  last in hiring" plus "that is a bar I would rather be measured
  against" is a view. "Love what you are building" is noise.
- **Restraint.** One fact, one proof, one ask. The discipline is the
  signal: it tells the reader you value their time, which is exactly
  what a future colleague does.
- **Their vocabulary, not yours.** If they say "forward-deployed,"
  "deployments," or "internal AI," use their words. Matching their
  language proves you read them; importing yours proves you did not.

## Example (job-seeker voice; connection-note length)

> Hi Nicolaus. Your August post on joining as founding Deployment
> Strategist read like a hiring brief, not an announcement. I applied
> for that seat on Friday; at Tamara I built a recruiting CRM TA and
> the COO run on. Worth a look from the person who built the role?

And the same fact stretched to a DM:

> Hi Prabir. Your June post on the Grab deployment stuck with me:
> voice agents reaching more people without adding headcount is the
> whole promise, and also the whole hard part. I applied for Founders
> Initiatives on Friday. At Tamara I built a recruiting CRM on
> Greenhouse plus OpenAI search that TA and the COO run on, and at
> SCET a HubSpot workflow that cut 100K+ leads to 500 targets. What
> does the internal-AI side of your work actually need most right now?

## Banned phrases

These mark a message as templated on sight. Never use them:

- "I hope this finds you well" / "I hope you are doing well"
- "I came across your profile"
- "I noticed you are a {title}"
- "Love what you / your team are building" (without a detail)
- "Amazing" / "incredible" about their work
- "Just checking in" / "bumping this up"
- "Quick question" as a subject line
- "Let me know if you have 15 minutes" on first contact

## Anti-patterns

- **Pitch-slapping:** compliment, then pitch, in the same breath. The
  compliment is revealed as bait and the reader stops trusting the
  next sentence.
- **Cleverness for its own sake:** a joke, a pun, or a gimmick opener
  that has nothing to do with their work. Memorable for the wrong
  reason.
- **Three proof points:** the message becomes a resume. Pick the one
  proof that belongs to this fact and cut the rest.
- **Asking for time before earning it:** a meeting ask, a calendar
  link, or "can I pick your brain" in a first message.
- **Voice-note rules that still apply in writing:** do not send a
  long, breathless message; do not bunch sends; do not write to
  someone with no verifiable fact and pretend otherwise. If the fact
  does not exist, send a shorter, plainer message or skip the person.
- **Bulk thinking:** if a message could be sent to twenty people by
  changing a name, it is not a pattern interrupt. Rewrite it until it
  could only go to one.

## Quality bar (run on every message)

- Names one specific, verifiable fact with a detail only a reader
  would know. Reject otherwise.
- Contains exactly one proof point and exactly one ask.
- Could not be sent to anyone else at the company by changing the
  name. Reject otherwise.
- Reads like the writer in their own voice: terse, direct, no sales
  language. Run the repo humanizer skill as the final pass.

## Source

Distilled in original wording from Moatt's
`linkedin-voicenote-pre-warm` skill
(https://github.com/Moatt/moatt-skills, path
`skills/moves/linkedin-voicenote-pre-warm/SKILL.md`): the fact-priority
ladder, the five-element structure, the specificity quality bar, and
the banned-phrase and anti-pattern lists, adapted from a 30-45 second
voice note to written outreach. No text is copied verbatim. The source
repository's license was not stated on the page read; treat this file
as an original adaptation with attribution.
