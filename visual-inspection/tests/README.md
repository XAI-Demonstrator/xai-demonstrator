# TCAV Batch Test Runner

This folder contains a small, reproducible TCAV test harness for the visual inspection demo.
It was created to make TCAV runs easy to execute locally, easy to inspect afterwards, and easy to share with other developers.

The most important entry point is [`run_tcav_example.py`](./run_tcav_example.py).
It processes every supported image in [`assets/`](./assets), runs TCAV for each image, and writes a dedicated result folder under [`test_results/`](./test_results).

## What this setup does

For every image in `assets/`, the runner now:

1. loads the demo model,
2. preprocesses the image in the same way as the backend pipeline,
3. loads the precomputed TCAV CAVs from the backend,
4. computes concept scores,
5. renders a **standalone TCAV score visualization**,
6. copies the original input image into the result folder,
7. writes a structured `result.json` containing the TCAV output.

This is intentionally **not** a spatial heatmap overlay.
TCAV in this project measures how strongly the model responds to concepts such as `round`, `has_handle`, or `has_lens`.
That means the output is a **concept score visualization**, not a pixel-wise explanation of where the model “sees” those concepts.

## Data flow

The complete flow looks like this:

`assets/` → `run_tcav_example.py` → backend model + preprocessing → `tcav_.py` → `tcav_loading.py` → `tcav_scoring.py` → `tcav_render.py` → `test_results/<image>/`

In more detail:

- `run_tcav_example.py` iterates over all images in `assets/`.
- The script loads the configured model from the backend and uses the normal preprocessing pipeline.
- `inspection-backend/inspection/explainer/explainers/tcav_.py` exposes the TCAV analysis logic.
- `tcav_loading.py` loads the CAV files from `cavs/` and reads `cav_manifest.json` when available.
- `tcav_scoring.py` turns model activations and CAV vectors into concept scores.
- `tcav_render.py` renders the concept scores into a separate visual artifact.
- The runner stores the artifacts per image in `test_results/`.

## Relevant backend files

### `inspection-backend/inspection/explainer/explainers/tcav_.py`

This is the high-level TCAV integration used by the backend.
It contains two important pieces:

- `compute_tcav_analysis(...)`
- `tcav_explanation(...)`

`compute_tcav_analysis(...)` is the most important function for the batch runner.
It computes and returns a structured TCAV result object containing:

- `concept_scores`: one score per concept
- `ranked_concept_scores`: the same concepts sorted by score strength

`tcav_explanation(...)` is still available for the normal backend explanation flow.
It returns an image-based explanation when TCAV is used through the regular backend API.

### `inspection-backend/inspection/explainer/explainers/tcav/tcav_models.py`

Defines the Pydantic configuration models for TCAV:

- `TCAVExplainerConfiguration`
- `TCAVRendererConfiguration`
- `TCAVConfiguration`
- `CAVLoadEntry`

These models describe what the TCAV pipeline needs:

- which concepts to use,
- where the CAV files are stored,
- which bottleneck layer to analyze,
- how many top concepts should be highlighted.

### `inspection-backend/inspection/explainer/explainers/tcav/tcav_loading.py`

Loads the actual CAV data from disk.
It supports two paths:

1. **manifest-based loading** via `cav_manifest.json`
2. **fallback loading** by discovering the concept folders on disk

This file is responsible for connecting the configured concepts to the actual `.npz` CAV files.
If no CAVs are available, the TCAV run fails early.

### `inspection-backend/inspection/explainer/explainers/tcav/tcav_scoring.py`

Turns model activations into concept scores.
The scoring logic computes a normalized similarity between the activation vector and each CAV.
Scores are then ranked so the strongest concepts appear first.

The output of this module is the core of what the JSON files contain.

### `inspection-backend/inspection/explainer/explainers/tcav/tcav_render.py`

Creates the score visualization image.
This project now uses a **standalone score panel** instead of drawing on top of the input image.
That makes the original image easier to inspect and keeps the explanation artifact visually separate.

### `inspection-backend/inspection/explainer/explainers/tcav/tcav_render.py` vs. `tcav_explanation(...)`

There are two visual styles in the codebase:

- the backend explainer can still return an image-based explanation,
- the batch runner produces a dedicated score visualization image.

For the batch runner, the score panel is the preferred output because it is clearer and does not modify the original image.

## Runner file

### `run_tcav_example.py`

This script is the main test harness.
It does the following for every supported image in `assets/`:

- copies the original image into the result folder,
- computes TCAV concept scores,
- generates `tcav_scores.png`,
- writes `result.json`.

It also creates a separate result folder per image.
The folder name is derived from the image name and extension, for example:

- `example_camera.png` → `example_camera_png/`
- `example_coffe-cup.png` → `example_coffe-cup_png/`

## Output structure

A successful run produces a structure like this:

```text
visual-inspection/tests/test_results/
└── example_camera_png/
    ├── input.png
    ├── tcav_scores.png
    └── result.json
```

### Files in each result folder

- `input.png`
  - a copy of the original input image
  - unchanged, for easy comparison and traceability

- `tcav_scores.png`
  - the standalone TCAV concept score visualization
  - this is **not** a pixel heatmap overlay

- `result.json`
  - structured TCAV output for the image
  - contains the concept scores and the sorted ranking

## JSON schema

The current JSON format is intentionally compact and focused on the TCAV result itself.

Example:

```json
{
  "schema_version": 1,
  "image_name": "example_camera.png",
  "generated_at_utc": "2026-04-13T21:49:15.749779+00:00",
  "concept_scores": {
    "feature_concepts/has_lens": 0.2718199380880417
  },
  "ranked_concept_scores": [
    {
      "concept": "feature_concepts/has_lens",
      "score": 0.2718199380880417
    }
  ]
}
```

### Fields

- `schema_version`
  - version of the result format
  - currently `1`

- `image_name`
  - original input filename

- `generated_at_utc`
  - timestamp in UTC when the result was created

- `concept_scores`
  - mapping of concept name to score
  - this is the most important machine-readable result

- `ranked_concept_scores`
  - ordered list of concept/score pairs
  - sorted by absolute strength, strongest first

## How the runner and backend fit together

The runner does **not** reimplement TCAV itself.
It reuses the backend implementation:

- the backend owns the model loading and TCAV analysis logic,
- the runner is only a thin batch layer that loops over assets,
- the runner serializes the result into files that are easy to inspect and archive.

That separation is intentional:

- backend code stays reusable for the app/API,
- the runner stays small and test-friendly,
- the result folders are self-contained and easy to review.

## Required inputs

Before running the batch script, the following must already exist:

- a working backend model configuration,
- precomputed TCAV CAV files in:
  `visual-inspection/inspection-backend/inspection/explainer/explainers/tcav/cavs/`
- a matching `cav_manifest.json` file, or a folder structure that allows fallback discovery,
- image files in `visual-inspection/tests/assets/`.

Supported image extensions:

- `.png`
- `.jpg`
- `.jpeg`

## How to run

From the repository root:

```powershell
python "visual-inspection/tests/run_tcav_example.py"
```

The script will process all supported images in `assets/` and write the results to `test_results/`.

## Validation notes

A good run should satisfy the following checks:

- every image in `assets/` has its own result folder,
- each result folder contains `input.png`, `tcav_scores.png`, and `result.json`,
- `result.json` contains non-empty concept scores when CAVs are available,
- the ranking is consistent with the raw scores,
- the score visualization is separate from the original image.

## Known limitation

TCAV does not provide a spatial explanation like Grad-CAM.
It answers a different question:

> Which concepts influence the model output most strongly?

So the visual output is best understood as a **score dashboard for concepts**, not as a heatmap showing exact image regions.

## Notes for developers

If you change any of the following, the README and/or the runner output should be updated together:

- concept folder structure in `concept_data/`
- the bottleneck layer
- the CAV manifest format
- the JSON result schema
- the rendering style of `tcav_scores.png`

That keeps the TCAV workflow understandable and reproducible for future contributors.

