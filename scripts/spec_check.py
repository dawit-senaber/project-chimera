#!/usr/bin/env python3
"""Lightweight spec-check script.

Performs a small contract verification between runtime skill metadata
and the API contract described in `specs/technical.md` (section 2.1).

This is intentionally small: it exercises a `fetch_interface()` helper on
the skill and ensures required properties are present.
"""
import sys
import json
from pathlib import Path

# Ensure repository root is discoverable for local imports when running from scripts/
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from skills.skill_trend_fetcher.logic import TrendFetcher
from skills.skill_media_generator.logic import MediaGenerator
from skills.skill_onchain_payment.logic import PaymentProcessor

try:
    import jsonschema
    from jsonschema import Draft7Validator
except Exception:
    jsonschema = None


def load_schema(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_skill_against_schema(instance, schema_path: Path, name: str):
    print(f"🧪 [SPEC-CHECK] Validating {name} against schema {schema_path.name}...")
    interface = instance.fetch_interface()
    schema = load_schema(schema_path)
    schema_props = schema.get("properties", {})
    missing = [key for key in schema.get("required", []) if key not in interface.get("properties", {})]

    if missing:
        print(f"❌ [SPEC-CHECK] FAILURE: Missing keys {missing} in {name} implementation.")
        sys.exit(1)

    # If jsonschema available, do a stronger check by validating a sample
    if jsonschema:
        def type_sample(prop_schema):
            t = prop_schema.get("type")
            if t == "string":
                # honor enums when present
                if "enum" in prop_schema:
                    enum = prop_schema.get("enum")
                    if isinstance(enum, list) and enum:
                        return enum[0]
                min_len = prop_schema.get("minLength", 1)
                # create a simple string that satisfies minLength
                return "x" * max(1, int(min_len))
            if t == "integer":
                return prop_schema.get("minimum", 1)
            if t == "number":
                return prop_schema.get("minimum", 1.0)
            if t == "array":
                # produce an example with a single default item if item type available
                items = prop_schema.get("items", {})
                item_sample = type_sample(items) if items else []
                return [item_sample]
            if t == "object":
                obj = {}
                for p, p_schema in prop_schema.get("properties", {}).items():
                    val = type_sample(p_schema)
                    if val is not None:
                        obj[p] = val
                return obj
            if t == "boolean":
                return True
            return None

        sample = {}
        for prop, prop_schema in schema.get("properties", {}).items():
            v = type_sample(prop_schema)
            if v is not None:
                sample[prop] = v

        try:
            Draft7Validator(schema).validate(sample)
        except Exception as e:
            print(f"❌ [SPEC-CHECK] Schema validation failed for {name}: {e}")
            sys.exit(1)

        # Compare declared types if available
        for prop, prop_schema in schema.get("properties", {}).items():
            schema_type = prop_schema.get("type")
            iface_prop = interface.get("properties", {}).get(prop, {})
            iface_type = iface_prop.get("type")
            if iface_type and schema_type and iface_type != schema_type:
                print(f"❌ [SPEC-CHECK] Type mismatch for '{prop}' in {name}: schema={schema_type}, interface={iface_type}")
                sys.exit(1)

    print(f"✅ [SPEC-CHECK] {name} aligns with API Contract.")


def verify_all():
    base = Path(__file__).resolve().parent.parent / "specs" / "schemas"

    verify_skill_against_schema(TrendFetcher(niche="_spec_check"), base / "trend_fetcher.json", "TrendFetcher")
    verify_skill_against_schema(MediaGenerator(), base / "media_generator.json", "MediaGenerator")
    verify_skill_against_schema(PaymentProcessor(), base / "payment_processor.json", "PaymentProcessor")


if __name__ == "__main__":
    verify_all()
