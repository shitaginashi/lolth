//! Bear Mode Trend Engine - Wǔxíng (五行) Moore State Machine
//!
//! This is an executable scaffold. Candidate ingestion, real embeddings, domain-specific
//! filtering, ranking, and durable persistence still require production implementations.

use std::error::Error;

/// The 5 Wǔxíng States + Wují (Idle) Boundary.
#[derive(Debug, PartialEq, Clone)]
pub enum WuxingState {
    /// Wují (無極): Unmanifest waiting state.
    Wuji,
    /// Wood (木 - Ingestion): Raw candidates supplied by the caller.
    WoodIngested {
        run_id: String,
        candidates: Vec<StagedCandidate>,
    },
    /// Fire (火 - Embedding): Candidate vectors.
    FireEmbedded {
        run_id: String,
        embedded_batch: Vec<CandidateVector>,
    },
    /// Earth (土 - Filtering): Candidates passing configured magnitude thresholds.
    EarthFiltered {
        run_id: String,
        qualified_batch: Vec<CandidateVector>,
    },
    /// Metal (金 - Mutation): Trend scoring results.
    MetalMutated {
        run_id: String,
        mutated_batch: GuaMutatedBatch,
    },
    /// Water (水 - Persistence): Persistence result.
    WaterPersisted {
        run_id: String,
        processed_count: usize,
    },
    /// Errata: Error logging state that resets to Wují on the next step.
    Errata { code: String, message: String },
}

/// Raw candidate supplied by the ingestion domain.
#[derive(Debug, Clone, PartialEq)]
pub struct StagedCandidate {
    pub sample_uid: String,
    pub domain_category: String,
    pub title: String,
    pub raw_body: Option<String>,
    pub alt_text_description: Option<String>,
    pub credit_uri: String,
}

/// Continuous float vector representation.
#[derive(Debug, Clone, PartialEq)]
pub struct CandidateVector {
    pub sample_uid: String,
    pub domain_category: String,
    pub vector: Vec<f32>,
    pub credit_uri: String,
}

/// Minimum vector magnitude by candidate domain.
#[derive(Debug, Clone, PartialEq)]
pub struct CubeThresholds {
    pub mythos_min_distance: f32,
    pub ai_min_distance: f32,
    pub oss_min_distance: f32,
}

/// Trend-scoring result.
#[derive(Debug, Clone, PartialEq)]
pub struct GuaMutatedBatch {
    pub hexagram_code: String,
    pub trend_velocity: f32,
    pub ranked_candidates: Vec<CandidateVector>,
}

/// Core Bear Mode FSM runner.
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

    /// Run one complete cycle using candidates supplied by the caller.
    pub fn execute_sweep(
        &mut self,
        run_id: &str,
        candidates: Vec<StagedCandidate>,
    ) -> Result<(), Box<dyn Error>> {
        if !matches!(self.state, WuxingState::Wuji) {
            return Err("Engine must be in Wují (Idle) state to execute sweep".into());
        }

        self.transition_to_wood(run_id, candidates)?;
        while !matches!(self.state, WuxingState::Wuji) {
            self.step()?;
        }
        Ok(())
    }

    /// Advance the machine by one state transition.
    pub fn step(&mut self) -> Result<(), Box<dyn Error>> {
        match self.state.clone() {
            WuxingState::Wuji => {}
            WuxingState::WoodIngested { run_id, candidates } => {
                if candidates.is_empty() {
                    self.state = WuxingState::Wuji;
                } else {
                    let embedded = self.embed_candidates(&candidates)?;
                    self.state = WuxingState::FireEmbedded {
                        run_id,
                        embedded_batch: embedded,
                    };
                }
            }
            WuxingState::FireEmbedded {
                run_id,
                embedded_batch,
            } => {
                let qualified = self.filter_3d_cube(&embedded_batch);
                if qualified.is_empty() {
                    self.state = WuxingState::Wuji;
                } else {
                    self.state = WuxingState::EarthFiltered {
                        run_id,
                        qualified_batch: qualified,
                    };
                }
            }
            WuxingState::EarthFiltered {
                run_id,
                qualified_batch,
            } => {
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
                println!(
                    "[Cycle Complete] Run {}: {} candidates consolidated.",
                    run_id, processed_count
                );
                self.state = WuxingState::Wuji;
            }
            WuxingState::Errata { code, message } => {
                eprintln!("[Errata Log] Code: {}, Message: {}", code, message);
                self.state = WuxingState::Wuji;
            }
        }
        Ok(())
    }

    fn transition_to_wood(
        &mut self,
        run_id: &str,
        candidates: Vec<StagedCandidate>,
    ) -> Result<(), Box<dyn Error>> {
        self.state = WuxingState::WoodIngested {
            run_id: run_id.to_string(),
            candidates,
        };
        Ok(())
    }

    fn embed_candidates(
        &self,
        candidates: &[StagedCandidate],
    ) -> Result<Vec<CandidateVector>, Box<dyn Error>> {
        // Placeholder embedding. Replace with the configured embedding model before production use.
        Ok(candidates
            .iter()
            .map(|candidate| CandidateVector {
                sample_uid: candidate.sample_uid.clone(),
                domain_category: candidate.domain_category.clone(),
                vector: vec![0.12, 0.84, 0.45],
                credit_uri: candidate.credit_uri.clone(),
            })
            .collect())
    }

    fn filter_3d_cube(&self, batch: &[CandidateVector]) -> Vec<CandidateVector> {
        batch
            .iter()
            .filter(|candidate| {
                let threshold = match candidate.domain_category.as_str() {
                    "mythos" => self.thresholds.mythos_min_distance,
                    "ai_mechanics" => self.thresholds.ai_min_distance,
                    "oss_tooling" => self.thresholds.oss_min_distance,
                    _ => return false,
                };
                let magnitude = candidate
                    .vector
                    .iter()
                    .map(|value| value * value)
                    .sum::<f32>()
                    .sqrt();
                magnitude >= threshold
            })
            .cloned()
            .collect()
    }

    fn mutate_hexagram_state(
        &self,
        batch: &[CandidateVector],
    ) -> Result<GuaMutatedBatch, Box<dyn Error>> {
        let trend_velocity = batch
            .iter()
            .map(|candidate| {
                candidate.vector.iter().map(|value| value * value).sum::<f32>().sqrt()
            })
            .sum::<f32>()
            / batch.len() as f32;

        Ok(GuaMutatedBatch {
            hexagram_code: "Gua_01_Qian".to_string(),
            trend_velocity,
            ranked_candidates: batch.to_vec(),
        })
    }

    // Persistence remains a scaffold; this currently reports the batch size only.
    fn persist_to_storage(
        &self,
        _run_id: &str,
        batch: &GuaMutatedBatch,
    ) -> Result<usize, Box<dyn Error>> {
        Ok(batch.ranked_candidates.len())
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let thresholds = CubeThresholds {
        mythos_min_distance: 0.0,
        ai_min_distance: 0.0,
        oss_min_distance: 0.0,
    };
    let mut engine = BearEngineFSM::new(thresholds);
    // The executable demonstrates an empty run. Integrators should pass candidates from harvest.
    engine.execute_sweep("demo-run", Vec::new())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn engine() -> BearEngineFSM {
        BearEngineFSM::new(CubeThresholds {
            mythos_min_distance: 0.5,
            ai_min_distance: 0.5,
            oss_min_distance: 0.5,
        })
    }

    fn candidate(category: &str) -> StagedCandidate {
        StagedCandidate {
            sample_uid: "candidate-1".to_string(),
            domain_category: category.to_string(),
            title: "Candidate".to_string(),
            raw_body: None,
            alt_text_description: None,
            credit_uri: "https://example.invalid/candidate".to_string(),
        }
    }

    #[test]
    fn empty_sweep_returns_to_idle() {
        let mut engine = engine();
        engine.execute_sweep("empty", Vec::new()).unwrap();
        assert_eq!(engine.state, WuxingState::Wuji);
    }

    #[test]
    fn supplied_candidate_flows_through_the_pipeline() {
        let mut engine = engine();
        engine.execute_sweep("test", vec![candidate("mythos")]).unwrap();
        assert_eq!(engine.state, WuxingState::Wuji);
    }

    #[test]
    fn unknown_domain_is_filtered_out() {
        let mut engine = engine();
        engine.execute_sweep("test", vec![candidate("unknown")]).unwrap();
        assert_eq!(engine.state, WuxingState::Wuji);
    }
}
