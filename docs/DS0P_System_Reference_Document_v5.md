# DS0P System Reference Document (DS0P-SRD) v5

The Darker Side of Passion (DS0P) creative engine operates as a post-tool symbiotic ecosystem, translating complex conceptual intent into high-fidelity digital media, structured metadata, and multi-platform distribution feeds. This System Reference Document (SRD) establishes the master specification for brand identity, audience strategy, SEO taxonomies, three-domain pipeline isolation (Harvest, Trend, Publish), Wǔxíng (五行) Moore state machine execution, Shǔmíng (署名) attribution schemas, polymorphic projection adapters, publish mandates, and runtime sidecar contracts. By consolidating all governance contracts into this unified v5 specification, the system ensures that AI agents, daemonic execution proxies, and automated build pipelines operate under deterministic law while preserving total brand integrity.

---

## 1. Paradigm & Sancai System Architecture

The studio architecture transcends traditional tool-based software paradigms, moving from passive command-and-control interfaces to a dynamic, hypersemantic feedback loop. In traditional digital media, intent is downsampled into finite color spaces and rigid graphical user interfaces, bounding expression within static constraints. In contrast, the DS0P framework treats artificial intelligence as a co-creative interface operating across continuous, unbounded vector fields.

Mathematically, traditional pixel space forces high-dimensional intent into bounded color gamuts:

$$\text{Pixel Space} = 64 \times 64 \times 3 \implies 12,288 \text{ dimensions bounded by } [0, 255]$$

Whereas continuous latent spaces unlock infinite vector precision:

$$\text{Latent Space} = 8 \times 8 \times 4 \implies 256 \text{ dimensions of unbounded continuous vectors}$$

To govern this high-gamut creative process without cognitive friction or data bloat, the operating system is structured around the ancient **Sancai (三才)** triad—balancing conceptual intent, conscious steering, and deterministic execution.

The systemic division of labor across the Sancai layers defines how state, momentum, and execution flow through the pipeline:

| Layer | Domain | Primary State & Storage | Operational Responsibility |
| :--- | :--- | :--- | :--- |
| **天 (Tian - Heaven)** | Conceptual Vector Space | Continuous Latent Matrices (`.npy`), Yijing Gua States | Maps overarching creative intent, tracks project velocity, and predicts pipeline friction using mutating hexagram dynamics. |
| **人 (Ren - Humanity)** | Conscious Direction & Mandates | Master Brand Knowledge Base, *Shǔmíng* Contracts | Sets strategic constraints, defines brand voice, establishes attribution rules, and oversees the Director loop (Alex Ledante). |
| **地 (Di - Earth)** | Deterministic Execution | SQLite Databases (`staging_harvest.sql`, `taxonomy.db`), Sidecar Files (`sidecar.yml`), Rust FSM | Executes script-as-law automation, parses payloads, enforces state transitions via Rust/MCP FSM, and triggers audio-visual telemetry cues. |

Orchestration across these layers is driven by a **Mixture of Experts (MoE)** agentic architecture. The central conductor, designated as **Domina**, acts as the stateful interface and scheduler. Specialized sub-agent daemons—such as **Bear Mode** for trend vector analysis, and **Maestro** for audio-visual asset pipelines—operate strictly within their functional domains. All state machines and state transitions are implemented via zero-overhead Rust FSMs over Model Context Protocol (MCP), while file manipulation and string parsing are offloaded to lightweight scripts.

---

## 2. Core Brand Identity, Voice, & Target Demographics

The identity of **Darker Side of Passion (DS0P)** / **Alex Ledante** is rooted in philosophical exploration, cosmic dread, and technical mastery. The brand serves an audience seeking intellectually challenging, surreal narrative experiences that probe the boundaries of human existence, mythos, and technological evolution.

### Strategic Identity Specifications

| Identity Dimension | Structural Specification | Implementation Standard |
| :--- | :--- | :--- |
| **Brand Name & Umbrella** | **Darker Side of Passion (DS0P)** | Root umbrella brand, governing philosophy, and master specification. |
| **Mission Statement** | Explore the unsettling and philosophical depths of human existence, mythos, and the unknown through AI-driven digital art. | High-fidelity 4K 60fps animations, atmospheric soundscapes, and Lovecraftian mythos storytelling. |
| **Brand Motto** | *"The shadows contain truths too profound for the light."* | Injected into official documentation, video outros, and high-level brand summaries. |
| **Brand Persona** | Knowledgeable Curator & Philosophical Guide | Authoritative, mysterious, contemplative, and evocative voice; avoids sensationalism or jump scares. |
| **Core Philosophy** | **"Pure, Unadulterated Creation"** | Achieved through post-tool symbiosis, where human vision steers generative silicon neural networks. |

### Brand Guidelines and Prohibited Conventions

Content generation across all sub-agents and automated scripts must strictly adhere to the tri-tone voice matrix while enforcing negative constraints:

*   **Primary Tone**: Authoritative & Mysterious.
*   **Secondary Tone**: Contemplative & Philosophical.
*   **Tertiary Tone**: Evocative & Dread-Filled.
*   **Prohibited Voice Conventions (`avoid`)**:
    1. *Sensationalism*: Avoid cheap clickbait, hyperbolic punctuation, or superficial shock tactics.
    2. *Overtly Humorous / Lighthearted Language*: Banned from all official channels to preserve atmospheric tension.
    3. *Trivialization of Themes*: Existential, cosmic, and technical topics must be treated with philosophical gravity.

### Target Audience Profile

The strategy targets a global, intellectually engaged audience defined by clear demographic and psychographic vectors:

*   **Demographics**: Adults aged 25–45, globally distributed, gender-neutral.
*   **Psychographics**:
    *   Intellectually curious and drawn to dark, complex, philosophical themes.
    *   Aficionados of cosmic horror literature (H.P. Lovecraft, weird fiction) and philosophical sci-fi.
    *   Enthusiasts operating at the intersection of technology and art, including AI workflows and generative media.
    *   Seekers of thought-provoking, emotionally resonant content over passive entertainment.

---

## 3. Three-Domain Segregated Pipeline Architecture

To eliminate architectural friction and prevent mode contamination across system layers, the DS0P execution pipeline strictly segregates operations into three isolated domains: **Harvest (Domain 1)**, **Trend / Bear Mode (Domain 2)**, and **Publish / Mianzi Engine (Domain 3)**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. HARVEST DOMAIN (Raw Signal Ingestion / Scrapers)                     │
│    - Role: Sweeps external outposts (Mythos, AI, OSS).                  │
│    - Strict Rule: Zero vector analysis, zero Gua math, zero Mianzi.     │
│    - Output: Raw text candidates & metadata into staging storage.       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Raw Text Candidates)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. TREND DOMAIN (Bear Mode / Wǔxíng Vector Engine)                       │
│    - Role: Embeds vectors (.npy), samples tension, mutates Gua states.  │
│    - Strict Rule: Zero web scraping, zero formatting, zero Mianzi.       │
│    - Output: Rated, tension-sampled candidate vectors & nowcast rank.   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Selected Candidate)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. PUBLISH DOMAIN (Payload Compiler & Mianzi Attribution)               │
│    - Role: Wraps payload in atomic_text, checks headroom, orders tags.  │
│    - Strict Rule: Zero web scraping, zero trend calculation.            │
│    - Output: Platform-ready post payload (atomic_text + attachments).   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Functional Responsibilities Across Domains

| Domain Phase | Core Responsibility | Primary State & Storage | Strict Isolation Guarantee |
| :--- | :--- | :--- | :--- |
| **1. Harvest Domain** | Outpost Sweeping & Raw Text Ingestion | SQLite Staging (`staging_harvest.sql`) | Gathers raw text titles, URIs, and alt-text without performing vector math or attribution logic. |
| **2. Trend Domain (Bear Mode)** | Latent Embedding, 3D Cube Filtering & Gua Mutation | Continuous Vector Space (`.npy`), Rust Wǔxíng FSM | Internal analytical engine only; executes vector operations without scraping external web APIs or formatting post text. |
| **3. Publish Domain** | Post Assembly, Partner Attribution & Sidecar Headroom | Payload Compiler (`publish_compiler-v2.py`), Sidecar (`sidecar.yml`) | Deterministic payload compiler; constructs `atomic_text` envelopes and computes real-time character quotas without calculating trend scores. |

---

## 4. Domain 1: Harvest Domain Specification (`staging_harvest.sql`)

The **Harvest Domain** serves as the initial landing buffer for raw text candidates gathered across three primary outpost axes: **Mythos**, **AI Mechanics**, and **OSS Tooling**.

### Technical Requirements & Storage Directives

1.  **Text-Only Metadata Guarantee**: The staging buffer stores raw text titles, body abstracts, credit URIs, and alt-text descriptions. Binary media assets (images, videos) are never stored in SQL.
2.  **Audit Traceability**: Every candidate is linked to an explicit harvest execution run ID (`run_id`).
3.  **Unique Deduplication**: Hashed permalinks or URL slugs (`sample_uid`) enforce single-ingestion guarantees across scraping sweeps.

### SQLite Harvest Staging DDL

```sql
-- SQLite Harvest Domain Staging Schema (staging_harvest.sql)
-- Domain 1: Raw Ingestion & Outpost Sweeps (Mythos, AI, OSS)

CREATE TABLE IF NOT EXISTS harvest_runs (
    run_id TEXT PRIMARY KEY,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    targets_scraped INTEGER DEFAULT 0,
    candidates_ingested INTEGER DEFAULT 0,
    run_status TEXT NOT NULL CHECK (run_status IN ('running', 'completed', 'failed', 'partial'))
);

CREATE TABLE IF NOT EXISTS harvest_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_uid TEXT UNIQUE NOT NULL,           -- Unique hash or permalink slug key
    domain_category TEXT NOT NULL CHECK (domain_category IN ('mythos', 'ai_mechanics', 'oss_tooling')),
    source_platform TEXT NOT NULL,             -- e.g. 'reddit', 'arxiv', 'github', 'rss', 'huggingface'
    credit_uri TEXT NOT NULL,                  -- External source URL / permalink
    title TEXT NOT NULL,                       -- Raw title / headline
    raw_body TEXT,                             -- Text abstract, body snippet, or post body
    alt_text_description TEXT,                 -- Plain text description metadata (no binaries)
    author_handle TEXT,                        -- Author, repo owner, or channel handle
    run_id TEXT,                               -- Traceability to execution run
    harvested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processing_status TEXT DEFAULT 'pending' CHECK (processing_status IN ('pending', 'embedded', 'rejected', 'archived')),
    FOREIGN KEY (run_id) REFERENCES harvest_runs(run_id)
);

-- Performance Indexes for Bear Mode Vector Handshake
CREATE INDEX IF NOT EXISTS idx_harvest_status ON harvest_candidates (processing_status);
CREATE INDEX IF NOT EXISTS idx_harvest_domain ON harvest_candidates (domain_category);
```

---

## 5. Domain 2: Trend Domain & Wǔxíng Moore FSM (`bear_fsm.rs`)

The **Trend Domain (Bear Mode)** operates as an internal vector analysis engine, completely decoupled from external web scraping and post compilation. To keep the engine trend-agnostic, baseline trend anchors are maintained in an external configuration matrix (`trend_anchors.npy`), enabling dynamic swapping of keywords and model checkpoints without modifying core binary logic.

### Wǔxíng (五行) Moore State Machine Topology

The state machine maps its execution cycle to the 5 Wǔxíng phases, bounded by the unmanifest state **Wují (無極 / Idle)**. State transitions operate strictly as a generative (*Shēng* 生) forward cycle, short-circuiting back to Wují on errors or zero-candidate filters.

```
                       ┌────────────────────────┐
                       │   Wují (無極) / Idle   │  ◄── (Enter / Exit Boundary)
                       └───────────┬────────────┘
                                   │ Trigger: External Sweep Command (MCP)
                                   ▼
                       ┌────────────────────────┐
                       │  1. Wood (木) Ingested  │  (Fetch Pending Raw Candidates)
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  2. Fire (火) Embedded │  (Generate Dense Float .npy Vectors)
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  3. Earth (土) Filtered│  (3D Latent Cube Boundary Check)
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │  4. Metal (金) Mutated │  (Compute Velocity & Mutate Gua)
                       └───────────┬────────────┘
                                   │
                                   ▼
                       ┌────────────────────────┐
                       │ 5. Water (水) Persisted│  (Consolidate to SQL & .npy Storage)
                       └───────────┬────────────┘
                                   │ Complete
                                   └─────────────────► Return to Wují (Idle)
```

### Wǔxíng FSM State Mapping Table

| Wǔxíng Phase | Internal Enum State | Operation & Data Guarantee | Transition Target |
| :--- | :--- | :--- | :--- |
| **無極 (Wují)** | `BearState::Idle` | Listening state; awaits external RPC command from Domina over MCP. | `State::Wood` |
| **木 (Wood)** | `BearState::Ingested` | Fetches `pending` raw candidates from `staging_harvest.sql`. | `State::Fire` |
| **火 (Fire)** | `BearState::Embedded` | Computes dense float vector embeddings into continuous `.npy` scratch buffer. | `State::Earth` |
| **土 (Earth)** | `BearState::Filtered` | Evaluates cosine distance against 3D Latent Cube boundaries (*Mythos / AI / OSS*). Prunes noise. | `State::Metal` |
| **金 (Metal)** | `BearState::Mutated` | Computes trend tension velocity delta (+ acceleration %) and mutates local Yijing Gua state. | `State::Water` |
| **水 (Water)** | `BearState::Persisted` | Consolidates rated metadata to SQLite and appends vector matrix to continuous `.npy` storage. | `State::Wují` |

### Rust State Machine Implementation (`bear_fsm.rs`)

```rust
// Wǔxíng (五行) Moore State Machine Implementation (bear_fsm.rs)

pub enum BearState {
    WujiIdle,
    WoodIngested { candidates: Vec<RawCandidate> },
    FireEmbedded { candidate_id: String, vector: Vec<f32> },
    EarthFiltered { candidate_id: String, vector: Vec<f32>, similarity_score: f32 },
    MetalMutated { candidate_id: String, delta_velocity: f32, old_hexagram: u8, new_hexagram: u8 },
    WaterPersisted { candidate_id: String, rank: usize },
    Errata { code: String, message: String },
}

pub struct BearDaemon {
    pub state: BearState,
    pub min_similarity_threshold: f32,
}

impl BearDaemon {
    pub fn new() -> Self {
        Self {
            state: BearState::WujiIdle,
            min_similarity_threshold: 0.75,
        }
    }

    pub fn step(&mut self, staged_inputs: Option<Vec<RawCandidate>>) {
        match &self.state {
            BearState::WujiIdle => {
                if let Some(candidates) = staged_inputs {
                    if candidates.is_empty() {
                        self.state = BearState::WujiIdle;
                    } else {
                        self.state = BearState::WoodIngested { candidates };
                    }
                }
            }
            BearState::WoodIngested { candidates } => {
                if let Some(target) = candidates.first() {
                    let mock_vector = vec![0.042f32; 768];
                    self.state = BearState::FireEmbedded {
                        candidate_id: target.sample_uid.clone(),
                        vector: mock_vector,
                    };
                } else {
                    self.state = BearState::WujiIdle;
                }
            }
            BearState::FireEmbedded { candidate_id, vector } => {
                let similarity = 0.894f32; // Measured distance to Yuggoth/Mythos anchor
                if similarity >= self.min_similarity_threshold {
                    self.state = BearState::EarthFiltered {
                        candidate_id: candidate_id.clone(),
                        vector: vector.clone(),
                        similarity_score: similarity,
                    };
                } else {
                    self.state = BearState::WujiIdle;
                }
            }
            BearState::EarthFiltered { candidate_id, vector, similarity_score: _ } => {
                self.state = BearState::MetalMutated {
                    candidate_id: candidate_id.clone(),
                    delta_velocity: 0.142f32,
                    old_hexagram: 62, // Xiao Guo
                    new_hexagram: 56, // Lu (The Wanderer)
                };
            }
            BearState::MetalMutated { candidate_id, .. } => {
                self.state = BearState::WaterPersisted {
                    candidate_id: candidate_id.clone(),
                    rank: 1,
                };
            }
            BearState::WaterPersisted { .. } => {
                self.state = BearState::WujiIdle;
            }
            BearState::Errata { .. } => {
                self.state = BearState::WujiIdle;
            }
        }
    }
}
```

---

## 6. Domain 3: Publish Domain Specification & Payload Compiler (`publish_compiler-v2.py`)

The **Publish Domain** is responsible for compiling raw text candidates into platform-compliant output envelopes, applying Mianzi attribution rules, enforcing character headroom quotas, and attaching downstream media manifests.

### Unified Mianzi Attribution Engine & Expression Modes

Attribution is governed by a unified priority calculation engine that evaluates partner weights (`mianzi_weight`). While the priority math remains identical, the engine supports three distinct surface modes of expression:

1.  **Text Mode (`atomic_text` / Social Feeds)**: Operates in social micro-posts and markdown payloads. Controls tag ordering, URL retention, and character cap pruning. **Corporate logos are strictly banned in social text contexts.**
2.  **Visual Scale Mode (Video Outros)**: Maps partner weight directly to logo bounding box dimensions in rendered 4K video end cards (P0/P1 logos rendered larger than P2/P3).
3.  **Visual Chromatic Mode (Video Outros)**: Maps partner weight to color treatment in rendered video end cards (full-color logos for top-tier sponsors vs. monochrome/grayscale for utility scripts).

### Mark 1 Text-Only Partner Attribution Heuristic

For social posts and text payloads, attribution is simplified to a lightweight, deterministic check:
*   **Solo Posts**: If no recognized partner IDs are present in candidate tags, partner attribution formatting is bypassed entirely.
*   **Partner Posts**: If partner tags are detected (e.g. `#NVIDIA`, `#JWST`, `#ComfyUI`), they are formatted at the top of the footer under a discrete `In collaboration with: #Partner` block, preceding primary and secondary hashtags.

### 3 Payload Attachment Tiers

Published outputs are constructed across three progressive payload tiers:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Tier 1: ATOMIC_TEXT (Base Universal Envelope)                            │
│  - Compulsory body text + domain link + Mark 1 partner tags + hashtag arrays│
│  - Real-time sidecar.yml headroom pruning                                │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ (+ Static Visual Asset)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Tier 2: ILLUSTRATED (Static Visual Attachment Envelope)                  │
│  - Inherits atomic_text base                                             │
│  - Attachments: Static Image URL, aspect ratio (16:9 / 1:1), alt-text,   │
│    color palette token, thumbnail manifest                               │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ (+ Rich Multi-Asset / Video Sequence)
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Tier 3: FANCY (Rich Media & Video Payload Envelope)                      │
│  - Inherits atomic_text base                                             │
│  - Attachments: Video MP4/WebM URL (e.g. YouTube pointer), audio stem ID, │
│    video outro Mianzi logo slots (P0-P3), frame rate, 4K resolution      │
└──────────────────────────────────────────────────────────────────────────┘
```

### Dynamic Headroom & Runtime Sidecar Manifest (`sidecar.yml`)

Platform character quotas are tracked dynamically via real-time headroom calculations:

$$\text{Headroom}_{\text{remaining}} = \text{Platform}_{\text{limit}} - \text{Length}(\text{Content}_{\text{body}})$$

If total content exceeds the platform cap, lower-priority hashtags are pruned in reverse order (boilerplate $\to$ secondary $\to$ primary). The results are emitted into a standardized runtime sidecar manifest (`sidecar.yml` / JSON).

```json
{
  "run_metadata": {
    "candidate_id": "pluto_yuggoth_01",
    "target_platform": "x_micro",
    "profile_applied": "micro_post",
    "attachment_tier": "fancy"
  },
  "budget_interface": {
    "platform_max_chars": 280,
    "content_body_chars": 150,
    "headroom_remaining": 130,
    "allocated_footer_chars": 106,
    "total_payload_chars": 256
  },
  "execution_status": {
    "superset_profile_applied": "micro_post",
    "quota_status": "optimal",
    "tags_retained": 6,
    "tags_pruned": 0
  },
  "attachment_status": {
    "tier": "fancy",
    "attached": true
  },
  "errata_audit_log": []
}
```

---

## 7. Shǔmíng Attribution Taxonomy & Model-Agnostic Schema

Attribution across the DS0P ecosystem is operationalized as a culturally anchored **Shǔmíng (署名)** taxonomy enforcing two key principles:

1.  ***Yǐnshuǐ Sīyuán* (饮水思源 - Remembering the Source)**: Establishes complete, un-truncated historical lineage tracking across every software framework, hardware environment, local notebook knowledge base, and utility script utilized in production.
2.  ***Mianzi* (面子 - Prestige & Weight)**: Assigns dynamic numeric weights (`mianzi_weight`) to determine visual prominence, logo scaling, color mode, and pruning order when platform delivery targets enforce strict character or token caps.

### Model-Agnostic Functional Tier Hierarchy

Specific neural model releases and checkpoint names carry short-lived trend value and become rapidly obsolete. To ensure long-term architectural durability, the functional tier hierarchy abstracts individual software models into general engine categories. Furthermore, **Tier P3 is re-anchored to Local Notebooks & Knowledge Bases**, grounding asset attribution directly in local project context files rather than ephemeral third-party repos.

| Tier Identifier | Category Name | Functional Scope | Structural Category Examples | Mianzi Weight Range |
| :--- | :--- | :--- | :--- | :--- |
| **P0** | `core_engine` | Primary Compute Engines & NLE Compositors | Node-Based Generative Compositors, Video Neural Runtimes, NLE Editors, 3D Engines | 90 – 100 |
| **P1** | `execution_env` | Host OS & Hardware Acceleration | Enterprise Linux Runtimes, Tensor Compute Acceleration, Python Runtimes | 70 – 89 |
| **P2** | `sub_pipeline` | Frameworks, Protocols & Nodes | Model Context Protocol (MCP), Fairlight, Custom Harnesses | 50 – 69 |
| **P3** | `local_notebook_ecosystem` | Local Notebooks, Knowledge Bases & Project Context | Domain Notebooks, Master Knowledge Bases, Project Manifests, Local Research Synthesis | 10 – 49 |

### Single Source of Truth DDL (`taxonomy.db`)

```sql
-- SQLite Master Taxonomy Schema DDL (taxonomy.db)

CREATE TABLE tiers (
    id TEXT PRIMARY KEY,
    weight_min INTEGER NOT NULL,
    weight_max INTEGER NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE tools (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tier_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    role_description TEXT NOT NULL,
    mianzi_weight INTEGER NOT NULL,
    logo_ref TEXT,                     -- Path/URI reference string only
    credit_uri TEXT,                   -- Local notebook URI or documentation handle
    FOREIGN KEY(tier_id) REFERENCES tiers(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

-- Seed Initial Tier Taxonomy
INSERT INTO tiers (id, weight_min, weight_max, description) VALUES
('P0', 90, 100, 'Primary Compute & Timeline Frameworks'),
('P1', 70, 89, 'Operating Systems & Hardware Acceleration'),
('P2', 50, 69, 'Specialized Protocols & Pipeline Nodes'),
('P3', 10, 49, 'Local Notebooks, Knowledge Bases & Project Context');
```

---

## 8. FanService Rank (FSR) & Post Mandates

Asset selection enforced during downstream assembly adheres to the **FanService Rank (`fsr.md`)** metadata star index:

*   **`*` (SFW / Tier 1)**: General distribution tier; safe for all platforms. (Universal baseline).
*   **`**` (Tier 2)**: Suggestive or artistic content tier.
*   **`***` (Tier 3)**: Restricted Content Level 1.
*   **`****` (Tier 4)**: Restricted Content Level 2.
*   **`*****` (Tier 5)**: Unrestricted internal archive tier.

*Gatekeeping Rule*: Each target channel enforces a preset FSR star ceiling. An asset is eligible for deployment only if its FanService star rank is less than or equal to the destination channel's preset ceiling.

### Publish Mandate & Tension-Based Selection

1.  **Tension Sampling (`sample NPY for most tension`)**: The engine queries local `.npy` continuous vector matrices to sample candidates exhibiting maximum semantic tension and resonance relative to active project momentum.
2.  **Hierarchical Scheduling (`attempt intersect with schedule/hierarchy`)**:
    *   *Hierarchy Class*: `scheduled` (planned drops), `forecast` (medium-term trends), `nowcast` (real-time trend captures), `awareness` (brand maintenance).
    *   *Post Schedule*: `iconic` (channel avatar/banner updates), `brand` (trend alignment & brand propagation), `promo` (content release & site updates).
3.  **Telemetry Delta Audit (`record delta [optimal score/post score]`)**: The system logs the delta between theoretical vector tension scores and real-world post performance metrics, feeding empirical telemetry back into the nowcasting vector space.

---

## 9. Notebook Governance & Migration Directive

To ensure optimal semantic retrieval and eliminate low-level code noise during branding queries, the **"branding"** notebook is locked to high-level strategic identity and taxonomy contracts.

### Notebook Allocation Matrix

| Notebook Destination | Source Selection & Allocation | Governance Scope |
| :--- | :--- | :--- |
| **`branding` (Current Notebook)** | **Keep 5 Core Branding Sources**: Art: Circuit of Creation, KJV Verses, Outro & Branding Pipeline, SEO Tags, Website Update Reorg. | Brand Bible, Sancai Framework, *Shǔmíng* Taxonomy, SQLite DB Schema, Superset Rules, Post Mode Spec, SEO Taxonomies. |
| **`video-pipeline-and-rendering`** | **Migrated Operational Sources** | Render pipelines, CUDA precision, LUT directory configs, quantization benchmarks. |
| **`seo-agent-and-hardware`** | **Migrated Operational Sources** | Server hardware mandates, SATA SSD IOPS, scraper algorithms, API credentials. |
| **`python-scripts-and-automation`** | **Migrated Automation Sources** | Python script maintenance, JSON schema fallbacks, command-line tool execution. |
| **`sancai-pedagogy-engine`** | **Migrated Architecture Sources** | Gua-chan visual sprites, 3-Yao health stack, 3D vector math, Mandarin voice recognition. |
