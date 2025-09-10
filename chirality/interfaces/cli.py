"""
New CLI for Chirality Framework v19.1.0.

Implements the two-phase architecture with proper command separation.
"""

import argparse
import sys
from pathlib import Path

from ..application.phase1.dialogue_run import DialogueOrchestrator
from ..application.phase1.snapshotter import SnapshotGenerator
from ..infrastructure.lenses.derive import derive_all_lenses
from ..infrastructure.lenses.build import build_lens_catalog
from ..application.phase2.tensor_engine import TensorEngine
from ..infrastructure.export.neo4j_loader import load_artifacts_to_neo4j
from ..infrastructure.prompts.registry import get_registry
from ..domain.budgets import BudgetConfig
from ..application.lenses import LensCatalogManager, LensResolver
from ..lib.logging import log_info, log_error, log_success, log_progress, output_data


def cmd_assets_hash(args):
    """Print current kernel hash."""
    registry = get_registry()
    kernel_hash = registry.compute_kernel_hash()
    output_data(kernel_hash)  # Data output to stdout


def cmd_assets_verify(args):
    """Verify and create asset manifest."""
    registry = get_registry()
    result = registry.create_manifest(Path("artifacts/prompts_assets.manifest.yaml"))
    log_success(
        f"Manifest created: kernel_hash={result['kernel_hash']}, assets={result['asset_count']}"
    )


def cmd_phase1_dialogue_run(args):
    """Run Phase 1 dialogue."""
    # Setup budget config if provided
    budget_config = None
    if args.token_budget or args.cost_budget or args.time_budget:
        budget_config = BudgetConfig(
            token_budget=args.token_budget,
            cost_budget=args.cost_budget,
            time_budget=args.time_budget,
        )

    orchestrator = DialogueOrchestrator(
        budget_config=budget_config,
        lens_mode=args.lens_mode,
        write_catalog=args.write_catalog,
        model=args.model,
        reasoning_effort=getattr(args, 'reasoning_effort', None),
    )

    log_progress("Running Phase 1 dialogue...")
    if budget_config:
        log_info(
            f"  Budget limits: tokens={args.token_budget}, cost=${args.cost_budget}, time={args.time_budget}s"
        )

    # Save dialogue and output
    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle lens regeneration if requested
    if args.regen_lenses:
        log_info("Regenerating lens catalog from normative_spec...")
        orchestrator.regenerate_full_catalog(output_dir)
    
    final_output = orchestrator.run_dialogue(output_dir)
    orchestrator.save_dialogue(output_dir / "phase1_dialogue.jsonl")
    validated_output = orchestrator.save_output(final_output, output_dir)

    log_success(f"Phase 1 complete: {output_dir}/phase1_output.json")
    log_info(f"  - Kernel hash: {validated_output.meta.kernel_hash}")
    log_info(f"  - Matrices: {len(validated_output.matrices)}")
    log_info(f"  - Tokens: {validated_output.meta.token_count}")

    # Print budget status if tracking was enabled
    if budget_config and hasattr(orchestrator, "get_budget_status"):
        budget_status = orchestrator.get_budget_status()
        if budget_status:
            log_info(f"  - Budget used: {budget_status['cost']['spent']:.4f} USD")


def cmd_phase1_snapshot(args):
    """Generate Phase 1 snapshot."""
    dialogue_path = Path(args.dialogue)
    output_path = Path(args.out)

    # Load phase1_output.json from same directory
    phase1_output_path = dialogue_path.parent / "phase1_output.json"
    if not phase1_output_path.exists():
        log_error(f"phase1_output.json not found at {phase1_output_path}")
        sys.exit(1)

    import json

    with open(phase1_output_path, "r") as f:
        phase1_output = json.load(f)

    log_progress("Generating snapshot...")
    snapshotter = SnapshotGenerator()
    snapshot_hash = snapshotter.generate_snapshot(dialogue_path, output_path, phase1_output)

    log_success(f"Snapshot created: {output_path}")
    log_info(f"  - Snapshot hash: {snapshot_hash}")


def cmd_lenses_derive(args):
    """Derive lens triples."""
    phase1_path = Path(args.phase1)
    spec_path = Path(args.spec)
    output_path = Path(args.out)

    # Get kernel hash for lens derivation
    registry = get_registry()
    kernel_hash = registry.compute_kernel_hash()

    log_progress("Deriving lens triples...")
    count = derive_all_lenses(phase1_path, spec_path, kernel_hash, "gpt-4o-mini", output_path)

    log_success(f"Lens triples derived: {output_path}")
    log_info(f"  - Unique lenses: {count}")


def cmd_lenses_build(args):
    """Build lens catalog."""
    triples_path = Path(args.triples)
    output_path = Path(args.out)

    log_progress("Building lens catalog...")
    count = build_lens_catalog(triples_path, output_path)

    log_success(f"Lens catalog built: {output_path}")
    log_info(f"  - Lenses generated: {count}")


def cmd_lenses_ensure(args):
    """Ensure lens catalog exists and is valid (idempotent)."""
    catalog_path = Path(args.out) if args.out else None
    manager = LensCatalogManager(catalog_path)
    
    log_progress("Checking lens catalog...")
    catalog = manager.ensure_catalog()
    
    meta = catalog["meta"]
    log_success("Lens catalog is ready")
    log_info(f"  - Stations: {len(meta['stations'])}")
    log_info(f"  - Generated: {meta['generated_at']}")
    log_info(f"  - System SHA: {meta['system_sha']}")


def cmd_lenses_refresh(args):
    """Force regeneration of lens catalog."""
    catalog_path = Path(args.out) if args.out else None
    manager = LensCatalogManager(catalog_path)
    
    log_progress("Regenerating lens catalog...")
    catalog = manager.ensure_catalog(force_refresh=True)
    
    meta = catalog["meta"]
    log_success("Lens catalog regenerated")
    log_info(f"  - Stations: {len(meta['stations'])}")
    log_info(f"  - Generated: {meta['generated_at']}")


def cmd_lenses_show(args):
    """Show lens catalog information."""
    catalog_path = Path(args.catalog) if args.catalog else None
    manager = LensCatalogManager(catalog_path)
    
    if args.station:
        # Show specific station
        try:
            info = manager.show_station_info(args.station)
            log_info(f"Station: {info['station']}")
            log_info(f"  - Matrix: {info['matrix_id']} ({info['dimensions']})")
            log_info(f"  - Rows: {info['rows']}")
            log_info(f"  - Cols: {info['cols']}")
            log_info(f"  - Lenses: {info['lens_count']}")
            log_info(f"  - Generated: {info['generated_at']}")
            log_info(f"  - Context hash: {info['context_hash']}")
        except (FileNotFoundError, ValueError) as e:
            log_error(f"Error: {e}")
            sys.exit(1)
    else:
        # Show all stations
        try:
            stations = manager.list_stations()
            meta = manager.get_catalog_meta()
            
            log_info("Lens catalog overview:")
            log_info(f"  - Generated: {meta['generated_at']}")
            log_info(f"  - Model: {meta['model']}")
            log_info(f"  - System SHA: {meta['system_sha']}")
            log_info(f"  - Normative SHA: {meta['normative_sha']}")
            log_info(f"  - Stations: {', '.join(stations)}")
            
        except FileNotFoundError as e:
            log_error(f"Error: {e}")
            log_info("Run 'chirality lenses ensure' to create catalog")
            sys.exit(1)


def cmd_lenses_meta(args):
    """Show lens catalog metadata."""
    catalog_path = Path(args.catalog) if args.catalog else None
    manager = LensCatalogManager(catalog_path)
    
    try:
        meta = manager.get_catalog_meta()
        
        log_info("Lens catalog metadata:")
        for key, value in meta.items():
            log_info(f"  - {key}: {value}")
            
    except FileNotFoundError as e:
        log_error(f"Error: {e}")
        log_info("Run 'chirality lenses ensure' to create catalog")
        sys.exit(1)


def cmd_lenses_source(args):
    """Show lens source precedence for stations."""
    lens_mode = args.mode or "catalog"
    resolver = LensResolver(lens_mode=lens_mode)
    
    if args.station:
        # Show specific station
        try:
            source = resolver.get_lens_source(args.station)
            log_info(f"Station '{args.station}': {source}")
        except Exception as e:
            log_error(f"Error: {e}")
            sys.exit(1)
    else:
        # Show all stations
        station_matrices = {
            "Problem Statement": "C",
            "Requirements": "F", 
            "Objectives": "D",
            "Verification": "X",
            "Validation": "Z",
            "Evaluation": "E"
        }
        
        log_info(f"Lens sources (mode: {lens_mode}):")
        for station in station_matrices.keys():
            try:
                source = resolver.get_lens_source(station)
                log_info(f"  - {station}: {source}")
            except Exception as e:
                log_info(f"  - {station}: ERROR - {e}")


def cmd_lenses_clear_overrides(args):
    """Clear lens overrides."""
    resolver = LensResolver()
    
    if args.station:
        # Clear specific station
        success = resolver.clear_station_override(args.station)
        if success:
            log_success(f"Override cleared for station '{args.station}'")
        else:
            log_info(f"No override found for station '{args.station}'")
    else:
        # Clear all overrides
        count = resolver.clear_all_overrides()
        if count > 0:
            log_success(f"Cleared {count} overrides")
        else:
            log_info("No overrides to clear")


def cmd_phase2_run(args):
    """Run Phase 2 tensor computation."""
    tensor_spec_path = Path(args.tensor_spec)
    snapshot_path = Path(args.snapshot)
    artifacts_dir = Path(args.out)

    # Load inputs
    import json

    with open(tensor_spec_path, "r") as f:
        tensor_spec = json.load(f)

    # Load phase1_output from same directory as snapshot
    phase1_output_path = snapshot_path.parent / "phase1_output.json"
    with open(phase1_output_path, "r") as f:
        phase1_output = json.load(f)

    # Setup lens catalog path
    lens_catalog_path = snapshot_path.parent / "lens_catalog.jsonl"

    # Setup budget config if provided
    budget_config = None
    if args.token_budget or args.cost_budget or args.time_budget:
        budget_config = BudgetConfig(
            token_budget=args.token_budget,
            cost_budget=args.cost_budget,
            time_budget=args.time_budget,
        )

    log_progress(f"Running Phase 2 with {args.parallel} parallel workers...")
    if budget_config:
        log_info(
            f"  Budget limits: tokens={args.token_budget}, cost=${args.cost_budget}, time={args.time_budget}s"
        )
    if args.resume:
        log_info("  Resume mode: enabled")
    log_info(f"  Cache: {'enabled' if args.cache else 'disabled'}")
    log_info(
        f"  Model: {args.model} (temp={args.temperature}, top_p={getattr(args, 'top_p', args.__dict__.get('top_p', 0.9))})"
    )

    engine = TensorEngine(
        snapshot_path=snapshot_path,
        phase1_output=phase1_output,
        lens_catalog_path=lens_catalog_path if lens_catalog_path.exists() else None,
        model=args.model,
        temperature=args.temperature,
        top_p=getattr(args, "top_p", args.__dict__.get("top_p", 0.9)),
        budget_config=budget_config,
        parallel=args.parallel,
        artifacts_dir=artifacts_dir,
        cache_enabled=args.cache,
        resume=args.resume,
    )

    # Run tensors from spec
    for tensor_spec_item in tensor_spec.get("tensors", []):
        log_progress(f"Computing tensor {tensor_spec_item.get('name', 'unknown')}...")
        try:
            result = engine.compute_tensor(tensor_spec_item)
            stats = result.get("stats", {})
            log_success(f"Tensor {result['name']} complete:")
            log_info(f"  - Total cells: {stats.get('total_cells', 0)}")
            log_info(f"  - Computed: {stats.get('cells_computed', 0)}")
            log_info(f"  - From cache: {stats.get('cells_from_cache', 0)}")
            log_info(f"  - From resume: {stats.get('cells_from_resume', 0)}")
        except Exception as e:
            log_error(f"Tensor computation failed: {e}")
            if budget_config:
                budget_status = engine.get_budget_status()
                if budget_status:
                    log_info(
                        f"  Budget status: {budget_status['tokens']['total']:,} tokens, ${budget_status['cost']['spent']:.4f}"
                    )
            raise

    # Save budget status
    if budget_config:
        engine.save_budget_status()
        budget_status = engine.get_budget_status()
        log_success(
            f"Budget status: {budget_status['tokens']['total']:,} tokens, ${budget_status['cost']['spent']:.4f} USD"
        )

    log_success(f"Phase 2 complete: results in {artifacts_dir}")


def cmd_export_neo4j(args):
    """Export to Neo4j."""
    artifacts_dir = Path(args.artifacts)

    log_progress(f"Exporting to Neo4j at {args.uri}...")
    run_id = load_artifacts_to_neo4j(
        artifacts_dir=artifacts_dir,
        uri=args.uri,
        user=args.user,
        password=args.pwd,
        setup_constraints=True,
    )

    log_success(f"Export complete: run_id={run_id}")


from dotenv import load_dotenv


def main():
    """Main CLI entry point."""
    load_dotenv()
    parser = argparse.ArgumentParser(prog="chirality", description="Chirality Framework v19.3.0")
    subparsers = parser.add_subparsers(dest="cmd", required=True, help="Available commands")

    # Assets commands
    subparsers.add_parser("assets-hash", help="Print current kernel hash")
    subparsers.add_parser("assets-verify", help="Verify and create asset manifest")

    # Phase 1 commands
    p1_run = subparsers.add_parser("phase1-dialogue-run", help="Run Phase 1 dialogue")
    p1_run.add_argument("--spec", help="Problem specification (placeholder)")
    p1_run.add_argument("--out", default="artifacts/", help="Output directory")
    p1_run.add_argument("--token-budget", type=int, help="Maximum tokens to use")
    p1_run.add_argument("--cost-budget", type=float, help="Maximum cost in USD")
    p1_run.add_argument("--time-budget", type=int, help="Maximum time in seconds")
    p1_run.add_argument("--lens-mode", choices=["catalog", "generate", "auto"], default="catalog",
                       help="Where Stage-3 lenses come from: catalog=use existing catalog, auto=in-transcript generation (default: catalog)")
    p1_run.add_argument("--write-catalog", action="store_true", 
                       help="Persist generated lenses into artifacts/lens_catalog.json")
    p1_run.add_argument("--regen-lenses", action="store_true",
                       help="Regenerate the full catalog from normative_spec before running")
    p1_run.add_argument("--model", help="LLM model to use (uses global config if not specified)")
    p1_run.add_argument("--reasoning-effort", choices=["low", "medium", "high"], 
                       help="GPT-5 reasoning effort level")

    p1_snap = subparsers.add_parser("phase1-snapshot", help="Generate Phase 1 snapshot")
    p1_snap.add_argument(
        "--from", dest="dialogue", required=True, help="Path to phase1_dialogue.jsonl"
    )
    p1_snap.add_argument("--out", required=True, help="Output snapshot path")

    # Lens commands
    lens_derive = subparsers.add_parser("lenses-derive", help="Derive lens triples")
    lens_derive.add_argument("--phase1", required=True, help="Path to phase1_output.json")
    lens_derive.add_argument("--spec", required=True, help="Path to tensor_spec.json")
    lens_derive.add_argument("--out", required=True, help="Output triples path")

    lens_build = subparsers.add_parser("lenses-build", help="Build lens catalog")
    lens_build.add_argument("--triples", required=True, help="Path to lenses_triples.json")
    lens_build.add_argument("--out", required=True, help="Output catalog path")

    # New lens management commands
    lens_ensure = subparsers.add_parser("lenses-ensure", help="Ensure lens catalog exists and is valid")
    lens_ensure.add_argument("--out", help="Custom catalog path (default: artifacts/lens_catalog.json)")

    lens_refresh = subparsers.add_parser("lenses-refresh", help="Force regeneration of lens catalog")
    lens_refresh.add_argument("--out", help="Custom catalog path (default: artifacts/lens_catalog.json)")

    lens_show = subparsers.add_parser("lenses-show", help="Show lens catalog information")
    lens_show.add_argument("--station", help="Show specific station (e.g., 'Validation')")
    lens_show.add_argument("--catalog", help="Custom catalog path (default: artifacts/lens_catalog.json)")

    lens_meta = subparsers.add_parser("lenses-meta", help="Show lens catalog metadata")
    lens_meta.add_argument("--catalog", help="Custom catalog path (default: artifacts/lens_catalog.json)")

    lens_source = subparsers.add_parser("lenses-source", help="Show lens source precedence for stations")
    lens_source.add_argument("--station", help="Show specific station (e.g., 'Validation')")
    lens_source.add_argument("--mode", choices=["catalog", "auto"], default="catalog", help="Lens resolution mode")

    lens_clear = subparsers.add_parser("lenses-clear-overrides", help="Clear lens overrides")
    lens_clear.add_argument("--station", help="Clear specific station (default: clear all)")

    # Phase 2 commands
    p2_run = subparsers.add_parser("phase2-run", help="Run Phase 2 tensor computation")
    p2_run.add_argument("tensor_spec", help="Path to tensor_spec.json")
    p2_run.add_argument("--snapshot", required=True, help="Path to phase1_snapshot.md")
    p2_run.add_argument("--parallel", type=int, default=8, help="Parallel workers")
    p2_run.add_argument("--resume", action="store_true", help="Resume from previous incomplete run")
    p2_run.add_argument(
        "--out", default="artifacts/", help="Output directory for caching and resume"
    )
    p2_run.add_argument("--token-budget", type=int, help="Maximum tokens to use")
    p2_run.add_argument("--cost-budget", type=float, help="Maximum cost in USD")
    p2_run.add_argument("--time-budget", type=int, help="Maximum time in seconds")
    p2_run.add_argument("--model", default="gpt-5-nano", help="LLM model to use")
    p2_run.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    p2_run.add_argument("--top-p", type=float, default=0.9, help="Nucleus sampling parameter")
    p2_run.add_argument(
        "--cache", action="store_true", default=True, help="Enable caching (default: True)"
    )
    p2_run.add_argument("--no-cache", dest="cache", action="store_false", help="Disable caching")

    # Export commands
    export_neo4j = subparsers.add_parser("export-neo4j", help="Export to Neo4j")
    export_neo4j.add_argument("--uri", required=True, help="Neo4j URI")
    export_neo4j.add_argument("--user", required=True, help="Neo4j username")
    export_neo4j.add_argument("--pwd", required=True, help="Neo4j password")
    export_neo4j.add_argument("--artifacts", default="artifacts/", help="Artifacts directory")

    # Parse and dispatch
    args = parser.parse_args()

    # Command mapping
    commands = {
        "assets-hash": cmd_assets_hash,
        "assets-verify": cmd_assets_verify,
        "phase1-dialogue-run": cmd_phase1_dialogue_run,
        "phase1-snapshot": cmd_phase1_snapshot,
        "lenses-derive": cmd_lenses_derive,
        "lenses-build": cmd_lenses_build,
        "lenses-ensure": cmd_lenses_ensure,
        "lenses-refresh": cmd_lenses_refresh,
        "lenses-show": cmd_lenses_show,
        "lenses-meta": cmd_lenses_meta,
        "lenses-source": cmd_lenses_source,
        "lenses-clear-overrides": cmd_lenses_clear_overrides,
        "phase2-run": cmd_phase2_run,
        "export-neo4j": cmd_export_neo4j,
    }

    if args.cmd in commands:
        try:
            commands[args.cmd](args)
        except Exception as e:
            log_error(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
