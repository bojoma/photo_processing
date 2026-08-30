import json
import os
import csv

PROJECTS_DIRECTORY = "/Users/margofarley/Desktop/thesis/hurricane_hole/surveys/photo_processing/taglab_projects/"
OUTPUT_CSV = "/Users/margofarley/Desktop/thesis/hurricane_hole/surveys/photo_processing/data/master_taglab_data.csv"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

master_data = []

for root, dirs, files in os.walk(PROJECTS_DIRECTORY):
    for file in files:
        if file.endswith(".json") and "template" not in file.lower() and "dictionary" not in file.lower():
            filepath = os.path.join(root, file)
            project_name = os.path.basename(root)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    project = json.load(f)
            except Exception:
                continue

            images = project.get('images', [])
            
            for img in images:
                photo_name = img.get('name', os.path.basename(filepath))
                px_to_mm = float(img.get('map_px_to_mm_factor', 1.0))
                
                ann_dict = img.get('annotations', {})
                regions = ann_dict.get('regions', [])
                points = ann_dict.get('points', [])
                
                # Process regions
                for ann in regions:
                    if not isinstance(ann, dict): continue
                    
                    class_name = ann.get('class name', '')  # Regions use 'class name'
                    substrate = ann.get('note', '')  # Regions use 'note'
                    
                    area_px = ann.get('area', 0)
                    perim_px = ann.get('perimeter', 0)
                    area_cm2 = (float(area_px) * (px_to_mm ** 2)) / 100.0 if area_px else 0.0
                    perim_cm = (float(perim_px) * px_to_mm) / 10.0 if perim_px else 0.0
                    
                    bbox = ann.get('bbox', [])
                    length_cm = 0.0
                    width_cm = 0.0
                    if len(bbox) == 4:
                        w_px = bbox[2]
                        h_px = bbox[3]
                        length_cm = (max(w_px, h_px) * px_to_mm) / 10.0
                        width_cm = (min(w_px, h_px) * px_to_mm) / 10.0
                    
                    master_data.append({
                        'project_folder': project_name,
                        'photo_filename': photo_name,
                        'colony_id': ann.get('id', ''),
                        'class': class_name,
                        'substrate': str(substrate).strip(),
                        'area_cm2': round(area_cm2, 3),
                        'perimeter_cm': round(perim_cm, 3),
                        'length_cm': round(length_cm, 3),
                        'width_cm': round(width_cm, 3)
                    })
                
                # Process points
                for pt in points:
                    if not isinstance(pt, dict): continue
                    
                    class_name = pt.get('Class', '')  # Points use 'Class' (capital C)
                    substrate = pt.get('Note', '')  # Points use 'Note' (capital N)
                    colony_id = pt.get('Id', '')  # Points use 'Id' (capital I)
                    
                    master_data.append({
                        'project_folder': project_name,
                        'photo_filename': photo_name,
                        'colony_id': colony_id,
                        'class': class_name,
                        'substrate': str(substrate).strip(),
                        'area_cm2': 0.0,
                        'perimeter_cm': 0.0,
                        'length_cm': 0.0,
                        'width_cm': 0.0
                    })

if master_data:
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['project_folder', 'photo_filename', 'colony_id', 'class', 'substrate', 'area_cm2', 'perimeter_cm', 'length_cm', 'width_cm']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master_data)
    
    print(f"\nSUCCESS!")
    print(f"Exported {len(master_data)} total annotations.")
    print(f"Saved to: {OUTPUT_CSV}")
else:
    print("\nNo data exported.")