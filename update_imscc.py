#!/usr/bin/env python3
"""
Update the IMSCC file to include visualization pages for all concepts.
"""

import json
import xml.etree.ElementTree as ET
import zipfile
import os
import shutil
from pathlib import Path

# Define namespaces
NS = {
    '': 'http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1',
    'lom': 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource',
    'lomimscc': 'http://ltsc.ieee.org/xsd/imsccv1p1/LOM/manifest',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Register namespaces
for prefix, uri in NS.items():
    if prefix:
        ET.register_namespace(prefix, uri)
    else:
        ET.register_namespace('', uri)

def generate_id():
    """Generate a unique identifier"""
    import uuid
    return 'i' + uuid.uuid4().hex

def update_manifest(manifest_path, concepts):
    """Update the manifest XML to include visualization items"""

    # Parse the XML
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    # Find the organizations and resources sections
    orgs = root.find('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}organizations')
    org = orgs.find('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}organization')
    resources = root.find('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resources')

    # Process each concept
    for concept in concepts:
        concept_id = concept['id']
        concept_name = concept['name']

        # Find the concept's parent item in the organization
        # Look for items with title matching the concept name
        for item in org.findall('.//{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
            title_elem = item.find('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
            if title_elem is not None and title_elem.text == concept_name:
                # Check if visualization already exists
                viz_exists = False
                for child_item in item.findall('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item'):
                    child_title = child_item.find('{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
                    if child_title is not None and 'Visualization' in child_title.text:
                        viz_exists = True
                        break

                if not viz_exists:
                    # Add visualization item
                    viz_item_id = generate_id()
                    viz_resource_id = generate_id()

                    # Create the item element
                    viz_item = ET.SubElement(item, '{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}item')
                    viz_item.set('identifier', viz_item_id)
                    viz_item.set('identifierref', viz_resource_id)

                    viz_title = ET.SubElement(viz_item, '{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}title')
                    viz_title.text = f'Visualization: {concept_name}'

                    # Add resource
                    resource = ET.SubElement(resources, '{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}resource')
                    resource.set('identifier', viz_resource_id)
                    resource.set('type', 'webcontent')

                    file_elem = ET.SubElement(resource, '{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}file')
                    file_elem.set('href', f'wiki_content/{concept_id}-visualization.html')

                    print(f'  Added visualization for: {concept_name}')

                break

    # Write the updated XML
    tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
    print(f'\nUpdated manifest file: {manifest_path}')

def create_updated_imscc():
    """Create updated IMSCC file with visualization pages"""

    print('=' * 60)
    print('Updating IMSCC file with visualization pages')
    print('=' * 60)

    # Paths
    repo_path = Path('/home/user/pla-2026')
    imscc_path = repo_path / 'music_theory_course.imscc'
    extract_dir = Path('/tmp/imscc_extract')
    wiki_content_source = repo_path / 'canvas_music_theory_course' / 'wiki_content'

    # Load concepts
    concepts_file = repo_path / 'music-theory-concepts.json'
    with open(concepts_file, 'r') as f:
        data = json.load(f)
        concepts = data['concepts']

    print(f'\nLoaded {len(concepts)} concepts')

    # Extract existing IMSCC
    print(f'\nExtracting {imscc_path}...')
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(imscc_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Copy visualization files to wiki_content
    print(f'\nCopying visualization files...')
    wiki_dest = extract_dir / 'wiki_content'
    viz_count = 0

    for concept in concepts:
        concept_id = concept['id']
        viz_file = wiki_content_source / f'{concept_id}-visualization.html'

        if viz_file.exists():
            dest_file = wiki_dest / f'{concept_id}-visualization.html'
            shutil.copy2(viz_file, dest_file)
            viz_count += 1

    print(f'  Copied {viz_count} visualization files')

    # Update manifest
    print(f'\nUpdating manifest...')
    manifest_path = extract_dir / 'imsmanifest.xml'
    update_manifest(manifest_path, concepts)

    # Create new IMSCC file
    print(f'\nCreating updated IMSCC file...')
    new_imscc_path = repo_path / 'music_theory_course.imscc'

    # Remove old file
    if new_imscc_path.exists():
        new_imscc_path.unlink()

    # Create new ZIP
    with zipfile.ZipFile(new_imscc_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(extract_dir)
                zipf.write(file_path, arcname)

    # Verify
    print(f'\nVerifying updated IMSCC...')
    with zipfile.ZipFile(new_imscc_path, 'r') as zipf:
        files = zipf.namelist()
        wiki_files = [f for f in files if f.startswith('wiki_content/')]
        print(f'  Total files in IMSCC: {len(files)}')
        print(f'  Wiki content files: {len(wiki_files)}')

        viz_files = [f for f in wiki_files if '-visualization.html' in f]
        print(f'  Visualization files: {len(viz_files)}')

    print(f'\n' + '=' * 60)
    print(f'Successfully updated: {new_imscc_path}')
    print('=' * 60)

if __name__ == '__main__':
    create_updated_imscc()
