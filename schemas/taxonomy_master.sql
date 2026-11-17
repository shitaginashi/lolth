-- DS0P Master Attribution Taxonomy DDL & Seed Script (taxonomy.db) v2
-- Corrected: Symbolic Unique Text Identifiers for P3 Anchors
-- Corrected: Mianzi Weights set to baseline NULL/placeholder pending model definition

PRAGMA foreign_keys = ON;

-- 1. Tier Definitions
CREATE TABLE IF NOT EXISTS tiers (
    id TEXT PRIMARY KEY,
    weight_min INTEGER,
    weight_max INTEGER,
    description TEXT NOT NULL
);

INSERT INTO tiers (id, weight_min, weight_max, description) VALUES
('P0', NULL, NULL, 'Primary Compute Engines & Timeline Compositors'),
('P1', NULL, NULL, 'Operating Systems & Tensor Hardware Acceleration'),
('P2', NULL, NULL, 'Specialized Protocols, Custom Nodes & Frameworks'),
('P3', NULL, NULL, 'Local Notebook Ecosystem & Project Context Anchors');

-- 2. Category Taxonomy
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO categories (id, name) VALUES
('node_compositor', 'Node-Based Generative Compositors'),
('neural_runtime', 'Video & Image Neural Runtimes'),
('nle_editor', 'Non-Linear Editors & Compositing Suites'),
('3d_engine', '3D Scene & Motion Graphics Engines'),
('host_os', 'Operating System Runtimes'),
('compute_hardware', 'Tensor Compute & Acceleration Hardware'),
('script_runtime', 'Execution Environments & Language Runtimes'),
('mcp_protocol', 'Model Context Protocol & Daemonic Harnesses'),
('audio_engine', 'Acoustic Processing & Fairlight Engines'),
('local_notebook', 'Local Project Notebooks & Domain Context');

-- 3. Tools & Assets Schema
CREATE TABLE IF NOT EXISTS tools (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tier_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    role_description TEXT NOT NULL,
    mianzi_weight INTEGER,              -- Placeholder: Weight hierarchy TBD
    logo_ref TEXT,                     -- Optional visual ref
    credit_uri TEXT,                   -- Unique text identifier handle (replaced manually when target exists)
    FOREIGN KEY(tier_id) REFERENCES tiers(id),
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

-- Seed P0: Primary Compute & Timeline Editors
INSERT INTO tools (id, name, tier_id, category_id, role_description, mianzi_weight, logo_ref, credit_uri) VALUES
('comfyui', 'ComfyUI Core', 'P0', 'node_compositor', 'Primary node-based neural generation graph harness', NULL, 'assets/logos/comfyui.svg', 'P3_ANCHOR_COMFYUI_CORE'),
('davinci_resolve', 'DaVinci Resolve Studio', 'P0', 'nle_editor', 'Master 4K 60fps timeline composition and color grading', NULL, 'assets/logos/davinci.svg', 'P3_ANCHOR_DAVINCI_RESOLVE'),
('blender', 'Blender 3D Suite', 'P0', '3d_engine', 'Spatial geometry generation and motion tracking', NULL, 'assets/logos/blender.svg', 'P3_ANCHOR_BLENDER_SUITE');

-- Seed P1: Execution Environment & Hardware Acceleration
INSERT INTO tools (id, name, tier_id, category_id, role_description, mianzi_weight, logo_ref, credit_uri) VALUES
('ubuntu_lts', 'Ubuntu Linux Enterprise', 'P1', 'host_os', 'Host operating system runtime environment', NULL, 'assets/logos/ubuntu.svg', 'P3_ANCHOR_UBUNTU_LTS'),
('nvidia_rtx', 'NVIDIA Tensor Compute', 'P1', 'compute_hardware', 'CUDA & Tensor Core neural acceleration hardware', NULL, 'assets/logos/nvidia.svg', 'P3_ANCHOR_NVIDIA_RTX'),
('python_runtime', 'Python 3.12 Engine', 'P1', 'script_runtime', 'Script-as-law orchestration runtime', NULL, 'assets/logos/python.svg', 'P3_ANCHOR_PYTHON_RUNTIME');

-- Seed P2: Specialized Protocols & Custom Harnesses
INSERT INTO tools (id, name, tier_id, category_id, role_description, mianzi_weight, logo_ref, credit_uri) VALUES
('mcp_harness', 'Model Context Protocol (MCP)', 'P2', 'mcp_protocol', 'Daemonic state machine & agent orchestration protocol', NULL, 'assets/logos/mcp.svg', 'P3_ANCHOR_MCP_HARNESS'),
('fairlight_audio', 'Fairlight Audio Suite', 'P2', 'audio_engine', 'Acoustic soundscape mastering & spectral spatialization', NULL, 'assets/logos/fairlight.svg', 'P3_ANCHOR_FAIRLIGHT_AUDIO');

-- Seed P3: Local Notebook Ecosystem & Project Context Anchors
-- credit_uri stores unique text identifiers to be manually replaced when target exists
INSERT INTO tools (id, name, tier_id, category_id, role_description, mianzi_weight, logo_ref, credit_uri) VALUES
('nb_branding', 'Notebook: Branding & SRD', 'P3', 'local_notebook', 'Master strategic brand identity, Sancai rules, and Shǔmíng contracts', NULL, NULL, 'P3_ANCHOR_BRANDING'),
('nb_video_pipeline', 'Notebook: Video & Render Pipelines', 'P3', 'local_notebook', 'Render configurations, CUDA precision, and LUT paths', NULL, NULL, 'P3_ANCHOR_VIDEO_PIPELINE'),
('nb_seo_hardware', 'Notebook: SEO & Server Hardware', 'P3', 'local_notebook', 'Server hardware specifications and Bear Mode scraper heuristics', NULL, NULL, 'P3_ANCHOR_SEO_HARDWARE'),
('nb_python_automation', 'Notebook: Python Automation', 'P3', 'local_notebook', 'Automation scripts, JSON schema fallbacks, and maintenance daemons', NULL, NULL, 'P3_ANCHOR_PYTHON_AUTOMATION'),
('nb_sancai_pedagogy', 'Notebook: Sancai Pedagogy Engine', 'P3', 'local_notebook', 'Yijing 3D vector math, Gua states, and pedagogy architecture', NULL, NULL, 'P3_ANCHOR_SANCAI_PEDAGOGY');
