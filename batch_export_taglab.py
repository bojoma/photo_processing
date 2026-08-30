import json
import os
import csv
import math

# -----------------------------
# YOUR SETTINGS
# -----------------------------
PROJECTS_DIRECTORY = "/Users/margofarley/Desktop/taglab_projects/"
OUTPUT_CSV = "/Users/margofarley/Desktop/Thesis/data/hh/master_taglab_data.csv"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def calculate_perimeter_px(vertices):
    """Calculates perimeter in pixels from vertices."""
    if not vertices or len(vertices) < 2: 
        return 0.0
    perimeter = 0.0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        dx = vertices[j][0] - vertices[i][0]
        dy = vertices[j][1] - vertices[i][1]
        perimeter += math.sqrt(dx*dx + dy*dy)
    return perimeter

# -----------------------------
# MAIN EXPORT LOGIC
# -----------------------------
print(" Scanning for TagLab projects...")
master_data = []
projects_processed = 0

for root, dirs, files in os.walk(PROJECTS_DIRECTORY):
    for file in files:
        if file.endswith(".json") and "template" not in file.lower() and "dictionary" not in file.lower():
            filepath = os.path.join(root, file)
            project_name = os.path.basename(root)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    project = json.load(f)
            except Exception as e:
                print(f"️ Could not read {file}: {e}")
                continue
                
            print(f"📂 Processing: {file}")
            projects_processed += 1
            
            images = project.get('images', [])
            
            for img in images:
                photo_name = img.get('name', os.path.basename(filepath))
                px_to_mm = float(img.get('map_px_to_mm_factor', 1.0))
                
                raw_anns = img.get('annotations', {})
                
                # Flatten annotations in case they are grouped in lists
                ann_list = []
                if isinstance(raw_anns, dict):
                    for val in raw_anns.values():
                        if isinstance(val, list):
                            ann_list.extend(val)
                        else:
                            ann_list.append(val)
                elif isinstance(raw_anns, list):
                    for item in raw_anns:
                        if isinstance(item, list):
                            ann_list.extend(item)
                        else:
                            ann_list.append(item)
                
                for ann in ann_list:
                    if not isinstance(ann, dict):
                        continue
                        
                    # 1. Extract ID
                    region_id = ann.get('id', '')
                    
                    # 2. Extract Class using the exact key from your JSON: 'class name'
                    class_name = ann.get('class name', ann.get('class', 'UNK'))
                    
                    # 3. Extract Substrate using the exact key: 'note'
                    substrate = ann.get('note', '')
                    
                    # 4. Extract Area and Perimeter (already in pixels in the JSON)
                    area_px = ann.get('area', 0)
                    perim_px = ann.get('perimeter', 0)
                    
                    # Convert to cm (assuming TagLab saved in mm)
                    area_cm2 = (float(area_px) * (px_to_mm ** 2)) / 100.0 if area_px else 0.0
                    perim_cm = (float(perim_px) * px_to_mm) / 10.0 if perim_px else 0.0
                    
                    # 5. Extract Length and Width from bbox [x, y, width, height]
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
                        'region_id': region_id,
                        'class': class_name,
                        'substrate': str(substrate).strip(),
                        'area_cm2': round(area_cm2, 3),
                        'perimeter_cm': round(perim_cm, 3),
                        'length_cm': round(length_cm, 3),
                        'width_cm': round(width_cm, 3)
                    })

# -----------------------------
# SAVE TO CSV
# -----------------------------
if master_data:
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'project_folder', 'photo_filename', 'region_id', 'class', 'substrate', 
            'area_cm2', 'perimeter_cm', 'length_cm', 'width_cm'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master_data)
    
    print("\n" + "="*60)
    print(f"🎉 SUCCESS!")
    print(f"Processed {projects_processed} projects.")
    print(f"Exported {len(master_data)} total coral annotations.")
    print(f"Saved to: {OUTPUT_CSV}")
    print("="*60)
else:
    print("\n❌ No data exported.")