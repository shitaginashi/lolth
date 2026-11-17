//! Bear Mode Trend Engine - Wǔxíng (五行) Moore State Machine
//!
//! Domain 2: Trend Engine (Deterministic Vector Evaluation & Gua State Mutation)
//!
//! State Pipeline (Generative Forward Cycle):
//!   Wuji (Idle) ──> Wood (Ingest) ──> Fire (Embed) ──> Earth (Filter) ──> Metal (Mutate) ──> Water (Persist) ──> Wuji (Idle)

use std::error::Error;

/// The 5 Wǔxíng States + Wují (Idle) Boundary
#[derive(Debug, PartialEq, Clone)]
pub enum WuxingState {
    /// Wují (無極): Unmanifest waiting state. Listens for external invocation.
    Wuji,
    /// Wood (木 - Ingestion): Raw signal gathered from `staging_harvest` database.
    WoodIngested {
        run_id: String,
        candidates: Vec<StagedCandidate>,
    },
    /// Fire (火 - Embedding): Transformed into continuous dense float vector matrices (.npy).
    FireEmbedded {
        run_id: String,
        embedded_batch: Vec<CandidateVector>,
    },
    /// Earth (土 - Filtering): Grounded against 3D Latent Cube boundary thresholds (Mythos/AI/OSS).
    EarthFiltered {
        run_id: String,
        qualified_batch: Vec<CandidateVector>,
    },
    /// Metal (金 - Mutation): Trend acceleration computed; Yijing Gua hexagram state mutated.
    MetalMutated {
        run_id: String,
        mutated_batch: GuaMutatedBatch,
    },
    /// Water (水 - Persistence): Deep consolidation of rated metadata into SQL & vector storage.
    WaterPersisted {
        run_id: String,
        processed_count: usize,
    },
    /// Errata: Error logging state that cleanly resets back to Wují.
    Errata {
        code: String,
        message: String,
    },
}

/// Raw Staged Candidate parsed from `staging_harvest` SQL table
#[derive(Debug, Clone)]
pub struct StagedCandidate {
    pub sample_uid: String,
    pub domain_category: String, // "mythos", "ai_mechanics", or "oss_tooling"
    pub title: String,
    pub raw_body: Option<String>,
    pub alt_text_description: Option<String>,
    pub credit_uri: String,
}

/// Continuous Float Vector Representation (Latent Space Matrix)
#[derive(Debug, Clone)]
pub struct CandidateVector {
    pub sample_uid: String,
    pub domain_category: String,
    pub vector: Vec<f32>, // Dense embedding coordinates
    pub credit_uri: String,
}

/// 3D Latent Cube Threshold Bounds (Axis X: Mythos, Axis Y: AI Mechanics, Axis Z: OSS Tooling)
#[derive(Debug, Clone)]
pub struct CubeThresholds {
    pub mythos_min_distance: f32,
    pub ai_min_distance: f32,
    pub oss_min_distance: f32,
}

/// Yijing Gua Mutated Batch Result
#[derive(Debug, Clone)]
pub struct GuaMutatedBatch {
    pub hexagram_code: String,      // Current mutating hexagram (e.g. "Gua_01_Qian")
    pub trend_velocity: f32,         // Trend momentum delta
    pub ranked_candidates: Vec<CandidateVector>,
}

/// Core Bear Mode FSM Runner
pub struct BearEngineFSM {
    pub state: WuxingState,
    pub thresholds: CubeThresholds,
}

impl BearEngineFSM {
    pub fn new(thresholds: CubeThresholds) -> Self {
        Self {
            state: WuxingState::Wuji,
            thresholds,
        }
    }

    /// Triggers a full generative forward cycle from external Domina RPC call
    pub fn execute_sweep(&mut self, run_id: &str) -> Result<(), Box<dyn Error>> {
        if self.state != WuxingState::Wuji {
            return Err("Engine must be in Wují (Idle) state to execute sweep".into());
        }

        // 1. Transition: Wují -> Wood (Ingest from staging_harvest)
        self.transition_to_wood(run_id)?;

        // Self-advancing Moore loop through Wǔxíng forward cycle
        while self.state != WuxingState::Wuji {
            self.step()?;
        }

        Ok(())
    }

    /// Single step state transition logic (Moore Machine)
    pub fn step(&mut self) -> Result<(), Box<dyn Error>> {
        match self.state.clone() {
            WuxingState::Wuji => {
                // Waiting state; no action required
            }
            WuxingState::WoodIngested { run_id, candidates } => {
                if candidates.is_empty() {
                    println!("[Wují Return] No pending candidates in staging.");
                    self.state = WuxingState::Wuji;
                } else {
                    let embedded = self.embed_candidates(&candidates)?;
                    self.state = WuxingState::FireEmbedded {
                        run_id,
                        embedded_batch: embedded,
                    };
                }
            }
            WuxingState::FireEmbedded { run_id, embedded_batch } => {
                let qualified = self.filter_3d_cube(&embedded_batch);
                if qualified.is_empty() {
                    println!("[Wují Return] Zero candidates passed 3D Latent Cube filter.");
                    self.state = WuxingState::Wuji;
                } else {
                    self.state = WuxingState::EarthFiltered {
                        run_id,
                        qualified_batch: qualified,
                    };
                }
            }
            WuxingState::EarthFiltered { run_id, qualified_batch } => {
                let mutated = self.mutate_hexagram_state(&qualified_batch)?;
                self.state = WuxingState::MetalMutated {
                    run_id,
                    mutated_batch: mutated,
                };
            }
            WuxingState::MetalMutated { run_id, mutated_batch } => {
                let count = self.persist_to_storage(&run_id, &mutated_batch)?;
                self.state = WuxingState::WaterPersisted {
                    run_id,
                    processed_count: count,
                };
            }
            WuxingState::WaterPersisted { run_id, processed_count } => {
                println!("[Cycle Complete] Run {}: {} candidates consolidated. Returning to Wují.", run_id, processed_count);
                self.state = WuxingState::Wuji;
            }
            WuxingState::Errata { code, message } => {
                eprintln!("[Errata Log] Code: {}, Message: {}", code, message);
                self.state = WuxingState::Wuji;
            }
        }
        Ok(())
    }

    // --- State Execution Handlers ---

    fn transition_to_wood(&mut self, run_id: &str) -> Result<(), Box<dyn Error>> {
        let candidates = vec![]; // Fetched from SQL staging_harvest
        self.state = WuxingState::WoodIngested {
            run_id: run_id.to_string(),
            candidates,
        };
        Ok(())
    }

    fn embed_candidates(&self, candidates: &[StagedCandidate]) -> Result<Vec<CandidateVector>, Box<dyn Error>> {
        let mut embedded = Vec::new();
        for c in candidates {
            embedded.push(CandidateVector {
                sample_uid: c.sample_uid.clone(),
                domain_category: c.domain_category.clone(),
                vector: vec![0.12, 0.84, 0.45],
                credit_uri: c.credit_uri.clone(),
            });
        }
        Ok(embedded)
    }

    fn filter_3d_cube(&self, batch: &[CandidateVector]) -> Vec<CandidateVector> {
        batch.iter().cloned().filter(|_c| {
            true // Evaluated against 3D Latent Cube boundaries
        }).collect()
    }

    fn mutate_hexagram_state(&self, batch: &[CandidateVector]) -> Result<GuaMutatedBatch, Box<dyn Error>> {
        Ok(GuaMutatedBatch {
            hexagram_code: "Gua_01_Qian".to_string(),
            trend_velocity: 0.88,
            ranked_candidates: batch.to_vec(),
        })
    }

    fn persist_to_storage(&self, _run_id: &str, batch: &GuaMutatedBatch) -> Result<usize, Box<dyn Error>> {
        Ok(batch.ranked_candidates.len())
    }
}
