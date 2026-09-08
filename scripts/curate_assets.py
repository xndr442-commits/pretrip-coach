#!/usr/bin/env python3
"""Rename deduped photos extracted from the Fenix pre-trip booklet into a
named, section-organised reference library + manifest.json.

Run after extract_assets.py. Idempotent.
"""
import os, json, shutil
from PIL import Image

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
UNIQ = f"{ROOT}/assets/reference/extracted/unique"
CUR  = f"{ROOT}/assets/reference/curated"

# index -> (section_dir, filename, human caption)
MAP = {
 0:  ("00_brand", "cover_student_tire_inspection", "Student inspecting a steer tire (booklet cover)"),
 1:  ("00_brand", "cover_driver_in_cab",           "Driver at the wheel (booklet cover)"),
 3:  ("00_brand", "ceo_signature",                 "CEO signature mark"),
 4:  ("01_incab_engine_start", "seatbelt",         "Seat belt latched — top and bottom, no cuts or fraying"),
 5:  ("01_incab_engine_start", "valves_up",        "Yellow parking-brake and red trailer-air-supply valves, pulled up"),
 6:  ("01_incab_engine_start", "gearshift_neutral","Gear shift lever in neutral"),
 7:  ("01_incab_engine_start", "ignition_key",     "Hand turning the key to the ON position"),
 8:  ("02_incab_brake_check", "air_gauges",        "Dual air pressure gauges (primary + secondary)"),
 9:  ("02_incab_brake_check", "low_air_warning",   "Dash cluster with low-air warning light illuminated"),
 10: ("02_incab_brake_check", "valves_popped_out", "Yellow and red valves popped OUT (spring brakes applied)"),
 11: ("02_incab_brake_check", "service_brake_pedal","Foot on the service brake pedal"),
 12: ("03_incab_equipment", "reflective_triangles","Reflective warning triangle deployed"),
 13: ("03_incab_equipment", "fire_extinguisher",   "Fire extinguisher, mounted, charged, pin present"),
 14: ("03_incab_equipment", "spare_fuses",         "Spare fuse and relay box"),
 15: ("04_incab_visibility", "windshield",         "Windshield viewed from the driver's seat"),
 16: ("04_incab_visibility", "mirrors",            "Driver-side mirror assembly"),
 17: ("04_incab_visibility", "wipers_blade",       "Wiper blade resting on the windshield"),
 18: ("04_incab_visibility", "wipers_operating",   "Wipers sweeping the windshield"),
 19: ("04_incab_visibility", "heater_defroster",   "Heater / defroster control panel"),
 20: ("04_incab_visibility", "washer_fluid_spray", "Washer fluid spraying, wipers clearing"),
 21: ("04_incab_visibility", "horn",               "Steering wheel — city horn"),
 22: ("05_lights_operations", "tractor_studio",    "Day-cab tractor, three-quarter studio view"),
 23: ("05_lights_operations", "trailer_rear_doors","Trailer rear doors, studio view"),
 24: ("05_lights_operations", "trailer_front_reefer","Trailer nose / reefer unit"),
 25: ("05_lights_operations", "trailer_side_id",   "Trailer side with unit number"),
 26: ("05_lights_operations", "trailer_rear_lit",  "Trailer rear with all lights illuminated"),
 27: ("05_lights_operations", "marker_light_amber","Amber side marker light strip"),
 28: ("05_lights_operations", "marker_light_amber_alt","Amber side marker light strip (alt angle)"),
 29: ("06_front_operations", "coolant_reservoir",  "Coolant reservoir and sight glass"),
 30: ("06_front_operations", "power_steering_reservoir","Power steering reservoir"),
 31: ("06_front_operations", "engine_hoses",       "Engine compartment hoses — checking for cuts, bubbles, leaks"),
 32: ("06_front_operations", "engine_fluids_wide", "Engine compartment, fluid reservoirs, wide view"),
 33: ("06_front_operations", "steering_gearbox",   "Steering gear box and pitman arm"),
 34: ("07_steering_axle", "front_tire",            "Steer tire tread and sidewall"),
 35: ("07_steering_axle", "rim_lugnuts",           "Steer wheel rim, hub and lug nuts"),
 36: ("07_steering_axle", "spring_mount",          "Spring mount / hanger at the frame"),
 37: ("07_steering_axle", "leaf_springs",          "Leaf spring pack"),
 38: ("07_steering_axle", "ubolts_shock",          "U-bolts (4) and shock absorber (3)"),
 39: ("07_steering_axle", "air_brake_hose",        "Air brake hose with fittings at both ends"),
 40: ("07_steering_axle", "brake_drum_shoes",      "Brake drum, shoes and lining — checking for contaminants"),
 41: ("07_steering_axle", "air_chamber",           "Air chamber and clamps"),
 42: ("08_side_of_vehicle", "frame",               "Frame rail"),
 43: ("08_side_of_vehicle", "tractor_side_a",      "Tractor side — turn signal and mirror"),
 44: ("08_side_of_vehicle", "tractor_side_b",      "Tractor side view (alt)"),
 45: ("08_side_of_vehicle", "battery_box",         "Battery box, cover open, connectors and cables"),
 46: ("08_side_of_vehicle", "fuel_def_tank",       "Fuel tank cap / DEF tank"),
 47: ("08_side_of_vehicle", "tractor_side_c",      "Tractor side view (alt 2)"),
 48: ("08_side_of_vehicle", "battery_box_steps",   "Battery box beneath the catwalk steps"),
 49: ("09_combination", "air_electrical_lines",    "Electrical (green) line and service/emergency air lines at the catwalk"),
 50: ("09_combination", "kingpin_apron",           "King pin and apron, viewed from underneath"),
 51: ("09_combination", "fifth_wheel_skid_plate",  "Fifth wheel skid plate, greased"),
 52: ("09_combination", "release_handle_pins",     "Fifth wheel release handle and mounting pins"),
 53: ("09_combination", "locking_jaws",            "Locking jaws closed around the king pin"),
 54: ("10_trailer_only", "landing_gear",           "Landing gear raised, crank handle secured"),
 55: ("10_trailer_only", "dot_tape",               "DOT conspicuity tape along the trailer side"),
 56: ("11_rear_of_trailer", "clearance_lights",    "Trailer rear clearance lights"),
 57: ("11_rear_of_trailer", "lenses_reflectors",   "Tail, brake and turn lenses illuminated"),
 58: ("12_railroad_crossing", "crossing_sign",     "Railroad crossing — crossbuck, signals, 2 TRACKS sign"),
 59: ("13_emergency_stop", "triangles_placed",     "Warning triangles placed behind a stopped rig"),
}
SKIP = {2}  # background texture

def main():
    rows = json.load(open(f"{UNIQ}/_index.json"))
    manifest = []
    for i, r in enumerate(rows):
        if i in SKIP or i not in MAP:
            continue
        sec, name, cap = MAP[i]
        d = f"{CUR}/{sec}"
        os.makedirs(d, exist_ok=True)
        dst = f"{d}/{name}.png"
        shutil.copy(f"{UNIQ}/{r['file']}", dst)
        w, h = Image.open(dst).size
        manifest.append({
            "id": f"{sec.split('_',1)[1]}/{name}",
            "file": f"assets/reference/curated/{sec}/{name}.png",
            "section": sec,
            "caption": cap,
            "width": w, "height": h,
            "source": "NEW MATERIAL PRE TRIP.pdf",
            "source_pages": sorted(set(r["pages"])),
            "rights": "Fenix Truck School — owned material, cleared for in-app use",
        })
    json.dump({"generated_from": "Fenix pre-trip booklet, 36pp",
               "count": len(manifest), "images": manifest},
              open(f"{CUR}/manifest.json", "w"), indent=2)
    print(f"curated {len(manifest)} photos into {CUR}")

if __name__ == "__main__":
    main()
