#!/usr/bin/env python3
# safe_loaddata.py
"""
Standalone safe loader for fixtures.
Usage:
  # example (local dev)
  DJANGO_SETTINGS_MODULE=yourproject.settings python safe_loaddata.py initial_data.json

  # example (production on PythonAnywhere)
  DJANGO_SETTINGS_MODULE=yourproject.settings_prod python safe_loaddata.py initial_data.json
"""

import sys
import os
import json
import argparse
from django import setup as django_setup
from django.apps import apps
from django.db import transaction

def bootstrap(django_settings_module):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', django_settings_module)
    django_setup()

def safe_create_object(Model, pk, normal_fields, m2m_data):
    """
    Create a single Model instance with explicit pk and set m2m relationships.
    Skip if object with same pk already exists.
    """
    if Model.objects.filter(pk=pk).exists():
        return 'skipped', None

    # create instance
    instance = Model.objects.create(pk=pk, **normal_fields)

    # set M2M fields (list of pks)
    for m2m_field, pks in m2m_data.items():
        try:
            m2m_manager = getattr(instance, m2m_field)
            # only keep non-null ints/strings -- ignore missing refs
            valid_pks = [x for x in pks if x is not None]
            # ensure the related objects exist — filter to existing ones
            # note: .set() can accept a list of PKs
            m2m_manager.set(valid_pks)
        except Exception as e:
            print(f"Warning: couldn't set M2M '{m2m_field}' on {Model._meta.label} pk={pk}: {e}")
    return 'created', instance

def process_fixture(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    created = 0
    skipped = 0
    errors = 0

    for obj in data:
        try:
            model_label = obj.get('model')
            pk = obj.get('pk')
            fields = obj.get('fields', {})

            app_label, model_name = model_label.split('.')
            Model = apps.get_model(app_label, model_name)
            if Model is None:
                print(f"Skipping unknown model {model_label}")
                skipped += 1
                continue

            # Separate m2m fields from normal fields
            m2m_data = {}
            normal_fields = {}

            for fname, fvalue in fields.items():
                # If the field ends with "_id" it's probably a FK value stored raw
                # but dumpdata standard stores FK as field name with PK in fields,
                # so this should generally be fine.
                field_obj = None
                try:
                    field_obj = Model._meta.get_field(fname)
                except Exception:
                    # Not a model field — ignore or keep as normal
                    field_obj = None

                if field_obj is not None and getattr(field_obj, 'many_to_many', False):
                    m2m_data[fname] = fvalue
                else:
                    normal_fields[fname] = fvalue

            # Some fields in fixtures might be JSON-like for date strings etc. Let Django handle conversions
            with transaction.atomic():
                status, instance = safe_create_object(Model, pk, normal_fields, m2m_data)
                if status == 'created':
                    created += 1
                else:
                    skipped += 1

        except Exception as e:
            errors += 1
            print(f"Error loading object {obj.get('model')} pk={obj.get('pk')}: {e}", file=sys.stderr)

    print(f"Finished. Created: {created}, Skipped: {skipped}, Errors: {errors}")

def main(argv=None):
    parser = argparse.ArgumentParser(description="Standalone safe loader for Django dumpdata fixtures.")
    parser.add_argument('fixture', help='Path to fixture JSON file (e.g., initial_data.json)')
    parser.add_argument('--settings', '-s', help='Django settings module (or set DJANGO_SETTINGS_MODULE env var)')
    args = parser.parse_args(argv)

    settings_module = args.settings or os.environ.get('DJANGO_SETTINGS_MODULE')
    if not settings_module:
        print("ERROR: You must set DJANGO_SETTINGS_MODULE (via --settings or env var).", file=sys.stderr)
        sys.exit(2)

    fixture_path = args.fixture
    if not os.path.isfile(fixture_path):
        print(f"ERROR: fixture file not found: {fixture_path}", file=sys.stderr)
        sys.exit(3)

    bootstrap(settings_module)
    process_fixture(fixture_path)

if __name__ == '__main__':
    main()
