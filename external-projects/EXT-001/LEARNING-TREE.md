# EXT-001 — technical learning tree

[Final selected idea and project history](../../EXTERNAL-PROJECTS.md#latest-concept)

**Updated:** October 24, 2026 (America/Los_Angeles)

**Direction:** EXT-001, V10 — a connected-workforce operating system for
physical work. People and AI agents share task context, confirmed progress,
dependencies, and relevant updates. Wearables provide one interface; future
robot integrations could participate in the same work model.

“Operating system” describes the product's role in coordinating work. It does
not require writing a device operating system or manufacturing new glasses.
This is an implementation learning plan, not evidence that a prototype exists.
The first market, detailed scope, technology stack, and production hardware
access remain to be validated.

Build a working understanding across these areas, then deepen the parts the
first workflow depends on. The priorities below are proposed sequencing:

- **NOW:** needed for a first useful, testable version.
- **NEXT:** needed as it enters real workplace conditions or gains integrations.
- **LATER:** advanced capabilities and mission-specific expansion.

## Learning tree

```text
CONNECTED-WORKFORCE OPERATING SYSTEM
│
├── 1. Understand the work [NOW]
│   ├── Map assignment → preparation → execution → review → handoff
│   ├── Identify workers, supervisors, contractors, and approvers
│   ├── Understand prerequisites, dependencies, and shared resources
│   ├── Separate reported progress from authorized approval
│   ├── Find the current source for tasks, procedures, and equipment status
│   └── Measure delays, rework, missing information, and reporting effort
│
├── 2. Hardware and sensing [BASICS NOW; DEEPER NEXT]
│   ├── Cameras
│   │   ├── Field of view, focus, resolution, and frame rate
│   │   ├── Exposure, lighting, motion blur, and blocked views
│   │   └── Image/video compression, bandwidth, and processing cost
│   ├── Microphones and audio
│   │   ├── Sampling, capture, microphone placement, and activation
│   │   ├── Noise, wind, echo, overlapping speech, and hearing protection
│   │   └── Headsets, speakers, and intelligible spoken feedback
│   ├── Embedded computers
│   │   ├── Raspberry Pi: Linux, processes, permissions, and services
│   │   ├── USB/UVC cameras versus CSI ribbon-cable cameras
│   │   └── Power, storage, heat, and recovery after a restart
│   └── Wearable constraints
│       ├── Battery life, comfort, weight, durability, and fit
│       ├── Available sensors and supported vendor SDK functions
│       └── Compatibility with actual workplace equipment and conditions
│
├── 3. Connect devices [NEXT]
│   ├── Phone as the bridge between glasses and application services
│   ├── Camera/audio SDK access, supported models, and publishing terms
│   ├── Bluetooth audio versus Bluetooth Low Energy control/data
│   ├── Actual video transport: verify the vendor's supported route
│   ├── Wi-Fi/cellular connections, HTTPS, and real-time channels
│   ├── Pairing, user permissions, and mobile background behavior
│   └── Time-stamping, buffering, reconnection, and dropped data
│
├── 4. Software foundations and backend [NOW]
│   ├── One main backend language: Python or TypeScript
│   ├── Git, debugging, dependencies, configuration, and secrets
│   ├── HTTP, JSON, APIs, schemas, and input validation
│   ├── Authentication: identify the person or agent making a request
│   ├── Authorization: check the actions and records they may access
│   ├── Background jobs for processing and notification delivery
│   └── Deployment, logs, monitoring, backups, and recovery
│
├── 5. Data layers [CORE EXPERTISE]
│   ├── Operational database [NOW]
│   │   ├── People, agents, teams, projects, and responsibilities
│   │   ├── Tasks, equipment, dependencies, blockers, and permissions
│   │   └── SQL, relationships, constraints, indexes, and transactions
│   ├── Change history [NOW]
│   │   ├── Who reported what, when, and about which task
│   │   ├── AI proposal → user confirmation → authorized approval
│   │   └── Corrections, provenance, and last-confirmed timestamps
│   ├── File storage [WHEN NEEDED]
│   │   ├── Photos, recordings, manuals, drawings, and test results
│   │   └── Versions, access controls, retention, and deletion
│   ├── Knowledge retrieval [FOR TUTORING]
│   │   ├── Extract text and structure from documents
│   │   ├── Match equipment configuration and procedure revision
│   │   ├── Keyword search, embeddings, and vector search
│   │   └── Return relevant sources with each explanation
│   ├── Offline data [NEXT]
│   │   ├── Local cache and queued updates
│   │   ├── Synchronization and duplicate prevention
│   │   └── Conflicting edits and visibly stale information
│   └── Analytics [NEXT]
│       ├── Delays, handoff quality, errors, and update effort
│       └── Trends derived from traceable operational records
│
├── 6. Integrations and work coordination [NOW → NEXT]
│   ├── Connect the customer's task, equipment, and document systems
│   ├── APIs, webhooks, access scopes, rate limits, and credentials
│   ├── Match people, equipment, and task IDs across systems
│   ├── Decide which system owns each field
│   ├── Handle retries, duplicate events, and conflicting updates
│   ├── Model prerequisites and permitted task transitions
│   ├── Give agents bounded jobs and explicit tool permissions
│   └── Route alerts using responsibilities and subscriptions
│
├── 7. AI capabilities [VOICE FIRST]
│   ├── Speech-to-text and text-to-speech
│   ├── Extract task, status, blocker, owner, and estimate from speech
│   ├── Validate structured model output in ordinary application code
│   ├── Resolve ambiguous people, equipment, and task names
│   ├── Ask for clarification and accept user corrections
│   ├── Retrieve approved material for grounded explanations
│   ├── Treat instructions inside retrieved content as untrusted data
│   └── Later: image understanding, temporal context, and action recognition
│
├── 8. User experience [NOW]
│   ├── Worker: contribute an update with minimal interruption
│   ├── Supervisor: see blockers and decisions needing attention
│   ├── Next shift: understand changes, decisions, and unfinished work
│   ├── Clear confirmation, correction, and cancellation
│   ├── Immediate alerts, summaries, and required acknowledgments
│   └── Noise, gloves, occupied hands, accessibility, and weak signal
│
├── 9. Reliability, security, and evaluation [NOW]
│   ├── Prevent unauthorized access across projects or organizations
│   ├── Protect credentials, recordings, and sensitive documents
│   ├── Test incorrect extraction and wrong-task attribution
│   ├── Test missed alerts, false alerts, and duplicate updates
│   ├── Preserve required technical and operational approvals
│   ├── Measure latency, running cost, and correction frequency
│   └── Test interruptions, disconnection, restart, and recovery
│
└── 10. Advanced capabilities [LATER]
    ├── Continuous recognition of physical actions
    ├── Personalized tutoring and demonstrated skill progression
    ├── Spatial tracking and guidance attached to objects
    ├── Robot and instrument-control interfaces
    │   ├── Capabilities, permitted commands, and task allocation
    │   ├── Acknowledgments, execution state, failure, and recovery
    │   └── Existing safety controls and human approval boundaries
    └── Space operations
        ├── Configuration control and traceable procedures
        ├── Human factors and interruption recovery
        ├── Local operation with delayed ground communication
        └── Mission-specific hardware and operational validation
```

## Understand the boundaries between data layers

| Layer | What belongs there | What to learn first |
| --- | --- | --- |
| Operational database | Confirmed task status, ownership, responsibilities, dependencies, and permissions. | Stable IDs, relational modeling, transactions, constraints, and authorized writes. |
| Change history | How a record changed, who supplied or approved the change, and the supporting source. | Append-only events, corrections, timestamps, provenance, and duplicate prevention. |
| File storage | Photos, recordings, manuals, drawings, and measurements. | Metadata, versioning, access checks, secure retrieval, and retention. |
| Search index | Searchable representations of permitted documents and records. | Retrieval quality, applicability, permissions, and refreshing derived indexes after corrections or deletion. |
| Offline cache | A local copy of needed information plus pending changes. | Reconnection, conflict handling, freshness, and distinguishing queued work from confirmed server changes. |
| Analytics | Aggregations for learning about workflow outcomes. | Definitions, data quality, denominators, and separation of observed results from estimates. |
| AI services | Interpretation, clarification, summarization, and proposed actions. | Evaluated prompts, structured outputs, bounded tools, and error handling. |

A search or vector index should not become the authority on whether a task is
complete. The operational record controls that status. If an existing customer
system already owns it, the integration must preserve that authority.

The learning goal is not to deploy seven databases. A relational database can
support task state, permissions, dependencies, and change history initially.
Add file storage or search infrastructure when the chosen workflow needs it.
A specialized graph database or distributed streaming platform is not an
initial prerequisite.

## First complete interaction to build

```text
Worker speaks into phone
        ↓
Speech becomes text
        ↓
AI proposes a structured task update
        ↓
Application validates identity, permissions, and proposed fields
        ↓
Worker confirms or corrects the update
        ↓
Database saves the authorized change and its history
        ↓
Routing rules identify the relevant teammate
        ↓
Teammate receives a useful notification
```

Confirmation of a progress report does not replace a separately required
technical approval. The first version should make this distinction visible.

Agents can initially retrieve the applicable procedure, identify missing
information, prepare a handoff, and propose routing. More consequential actions
need explicit permissions and appropriate approval. Robot integration follows
an actual customer workflow and supported device interface; it is not required
to demonstrate the human-and-agent coordination loop.

## Proposed learning and build sequence

These checkpoints describe useful future demonstrations, not checks already run.

| Step | Learn by building | Evidence of progress |
| --- | --- | --- |
| 1 | Model one real task and handoff with a worker and manager. | Named participants, information sources, dependencies, and approval rules agree with observed work. |
| 2 | Create a small task/status interface with authentication and history. | An authorized person can update the right task; an unauthorized person cannot; corrections preserve context. |
| 3 | Add voice transcription and structured update proposals. | Users can correct ambiguous names or wrong fields before the record changes. |
| 4 | Route a small set of relevant notifications. | Required recipients receive the change without duplicate alerts or unrelated recipients seeing restricted information. |
| 5 | Connect one existing work system. | Field ownership is clear and repeated events do not create duplicate changes. |
| 6 | Exercise outages, queued updates, and stale information. | Users can tell what is pending; reconnection preserves records and surfaces conflicts. |
| 7 | Compare phone interaction with supported glasses. | Observation establishes where wearables reduce effort and where they introduce friction. |
| 8 | Add a small reviewed procedure collection and optional visual context. | Answers use the applicable source and abstain or ask when evidence is insufficient. |

An illustrative starting stack is a phone/web interface, one Python or
TypeScript backend, PostgreSQL, and speech/model APIs. Add object storage for
media when needed. Add document retrieval for tutoring. These are suggestions,
not a final technology selection or a claim that API access is configured.

## Mohammed's hardware starting point

The established equipment is a **Raspberry Pi 5** and **Meta glasses**. The
glasses model, phone operating system, and current commercial SDK access remain
unknown. A camera had not been purchased in the earlier discussion.

- The phone can bridge the wearable interface and application services.
- The Pi could become a fixed camera or equipment gateway if that serves the
  selected workflow. It does not need to sit in every initial interaction.
- Ordinary Bluetooth pairing does not grant access to glasses cameras.
  Verify the actual vendor SDK, model, firmware, and permitted distribution route.
- Do not assume Bluetooth Low Energy can carry the required continuous video
  stream. Learn the platform's actual transport, compression, and power limits.
- A camera cannot establish hidden connections, torque, or electrical performance.
  Such claims require appropriate instrument evidence or authorized verification.

The earlier laundry experiment remains an explanation-only concept. This
learning plan does not turn it into a completed build or authorize control of
the washer.

## Continuing this guide

Keep the [selected concept](../../EXTERNAL-PROJECTS.md#latest-concept) as the
source for product direction. Update this guide when customer evidence changes
the required capabilities. Mark actual prototypes, evaluations, and remaining
unknowns explicitly; a completed reading exercise is not proof of a working
integration or a reliable product.
