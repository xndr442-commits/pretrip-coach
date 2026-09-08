#!/usr/bin/env python3
"""Compute the full 3D layout: every inspectable part's primitive, size, position,
colour and camera station. Emits content/truck_layout.json.

This is the credit-expensive part of a 3D build -- working out where 53 parts sit
on a Class 8 tractor-trailer. Doing it deterministically here means the builder
runs a loop instead of iterating on geometry.

Coordinates: origin at the tractor's front bumper centre, ground level.
             +X rearward, +Y toward the driver side (left), +Z up. Metres.
"""
import json, os

R = os.path.expanduser("~/Projects/PreTripCoach")

# ---- reference dimensions (US Class 8) -------------------------------------
W, HW      = 2.60, 1.30          # width, half-width
STEER_X    = 1.35
WB         = 4.50
DRIVE_X    = STEER_X + WB        # 5.85 tandem centre
DRIVE_A    = DRIVE_X - 0.68      # 5.17
DRIVE_B    = DRIVE_X + 0.68      # 6.53
FRAME_TOP  = 1.10
FIFTH_X    = DRIVE_X - 0.30      # 5.55
FIFTH_Z    = 1.25
HOOD_END   = 2.10
CAB_END    = 5.60
TIRE_R     = 0.535
CAB_FLOOR  = 1.45

TRL_NOSE   = FIFTH_X - 0.90      # 4.65
TRL_LEN    = 16.15
TRL_END    = TRL_NOSE + TRL_LEN  # 20.80
TRL_FLOOR  = 1.25
TRL_TOP    = TRL_FLOOR + 2.90    # 4.15
LG_X       = TRL_NOSE + 2.40     # 7.05
TAND_A     = TRL_END - 2.80      # 18.00
TAND_B     = TRL_END - 1.50      # 19.30

C = dict(steel="#8A8F98", dark="#2B2F36", tyre="#1A1C1F", chrome="#C7CCD4",
         yellow="#F2C200", red="#D32F2F", blue="#1E6FD9", green="#2E9E4F",
         amber="#FF9E19", white="#F2F2F0", glass="#9FC6E0", rubber="#3A3D42",
         alu="#B9BEC6", copper="#B87333")

P = []
def part(pid, station, prim, pos, size, color, note, rot=(0, 0, 0), mirror=False):
    P.append({"id": f"part_{pid}", "station": station, "primitive": prim,
              "position": [round(v, 3) for v in pos],
              "size": [round(v, 3) for v in size],
              "rotation_deg": list(rot), "color": color,
              "mirror_y": mirror, "note": note})

def ctrl(cid, pos, size, color, note, prim="box"):
    P.append({"id": f"ctrl_{cid}", "station": "driver_seat", "primitive": prim,
              "position": [round(v, 3) for v in pos], "size": [round(v, 3) for v in size],
              "rotation_deg": [0, 0, 0], "color": color, "mirror_y": False, "note": note})

# ── FRONT OF TRUCK ──────────────────────────────────────────────────────────
part("truck_leveled","front_of_truck","box",(-0.35,0,2.0),(0.15,W,4.0),C["steel"],
     "Whole-vehicle proxy plate in front of the bumper; tap target for 'truck is level, no leaks'")
part("headlights","front_of_truck","box",(0.06,0.85,1.05),(0.10,0.42,0.26),C["white"],
     "Headlight housing, both sides", mirror=True)
part("front_lenses","front_of_truck","box",(0.06,1.15,1.32),(0.08,0.16,0.10),C["amber"],
     "Front clearance / marker lenses", mirror=True)
part("coolant","front_of_truck","cylinder",(1.05,0.50,1.42),(0.16,0.34),C["white"],
     "Coolant surge tank, engine bay")
part("oil","front_of_truck","cylinder",(1.30,-0.42,1.30),(0.03,0.44),C["chrome"],
     "Oil dipstick", rot=(0,18,0))
part("power_steering","front_of_truck","cylinder",(0.92,0.62,1.44),(0.11,0.26),C["dark"],
     "Power steering reservoir")
part("fluid_air_leaks","front_of_truck","box",(1.30,0,0.42),(1.60,1.10,0.06),C["dark"],
     "Ground-plane proxy under the engine for the leak check")
part("steering_gear_box","front_of_truck","box",(1.62,0.56,0.96),(0.26,0.22,0.30),C["steel"],
     "Steering gear box on the frame rail")
part("pitman_arm","front_of_truck","box",(1.70,0.62,0.80),(0.10,0.08,0.34),C["steel"],
     "Pitman arm, drops from the gear box", rot=(0,0,12))
part("drag_link","front_of_truck","cylinder",(1.55,0.82,0.74),(0.035,0.52),C["steel"],
     "Drag link, pitman arm to steering arm", rot=(0,90,20))
part("control_arms","front_of_truck","box",(1.35,0.86,0.66),(0.42,0.10,0.07),C["steel"],
     "Upper and lower control arms", mirror=True)
part("tie_rod","front_of_truck","cylinder",(1.16,0,0.60),(0.035,2.05),C["steel"],
     "Tie rod spanning the steer axle", rot=(90,0,0))

# ── STEER AXLE (driver side) ────────────────────────────────────────────────
part("front_tire","steer_axle","cylinder",(STEER_X,1.16,TIRE_R),(TIRE_R,0.295),C["tyre"],
     "Steer tire, driver side", rot=(90,0,0))
part("rims","steer_axle","cylinder",(STEER_X,1.20,TIRE_R),(0.286,0.20),C["alu"],
     "Wheel rim inside the tire", rot=(90,0,0))
part("lug_nuts","steer_axle","cylinder",(STEER_X,1.31,TIRE_R),(0.20,0.04),C["chrome"],
     "Lug nut ring on the hub face; model 10 small nuts on a 0.20 radius", rot=(90,0,0))
part("spring_mounts","steer_axle","box",(STEER_X-0.62,0.62,1.02),(0.16,0.14,0.22),C["steel"],
     "Forward spring hanger at the frame")
part("leaf_springs","steer_axle","box",(STEER_X,0.62,0.86),(1.42,0.11,0.09),C["steel"],
     "Leaf spring pack")
part("u_bolts","steer_axle","cylinder",(STEER_X,0.62,0.74),(0.022,0.30),C["steel"],
     "U-bolts clamping the spring to the axle", rot=(0,0,0))
part("shock_absorber","steer_axle","cylinder",(STEER_X+0.30,0.72,0.95),(0.045,0.42),C["red"],
     "Shock absorber", rot=(0,14,0))
part("brake_hose","steer_axle","cylinder",(STEER_X-0.10,0.95,0.78),(0.022,0.40),C["rubber"],
     "Air brake hose to the chamber", rot=(0,70,0))
part("air_chamber","steer_axle","cylinder",(STEER_X+0.16,0.80,0.80),(0.085,0.22),C["dark"],
     "Brake air chamber", rot=(0,90,0))
part("brake_contaminants","steer_axle","cylinder",(STEER_X,1.06,TIRE_R),(0.21,0.19),C["steel"],
     "Brake drum -- the 'no oil, grease or debris' check", rot=(90,0,0))

# ── DRIVER SIDE ─────────────────────────────────────────────────────────────
part("turn_signal_side","driver_side","box",(2.28,HW+0.01,1.88),(0.14,0.05,0.10),C["amber"],
     "Side turn signal / marker on the cab")
part("mirrors_side","driver_side","box",(2.46,HW+0.14,2.30),(0.09,0.06,0.52),C["dark"],
     "Driver-side mirror head on its arm")
part("fuel_tank","driver_side","cylinder",(3.60,1.24,0.94),(0.31,1.50),C["chrome"],
     "Fuel tank, driver side", rot=(0,90,0))
part("def_tank","driver_side","cylinder",(4.62,1.22,0.88),(0.20,0.52),C["white"],
     "DEF tank, behind the fuel tank", rot=(0,90,0))
part("battery","driver_side","box",(4.95,1.18,1.02),(0.62,0.42,0.34),C["dark"],
     "Battery box under the catwalk step")
part("frame","driver_side","box",(3.60,0.46,1.02),(6.60,0.09,0.24),C["steel"],
     "Frame rail, driver side")

# ── BEHIND CAB / COUPLING ───────────────────────────────────────────────────
part("electrical_line","behind_cab","cylinder",(5.15,0.28,1.82),(0.022,0.90),C["green"],
     "Green electrical cable, cab to trailer", rot=(0,58,0))
part("air_lines","behind_cab","cylinder",(5.15,0.02,1.80),(0.024,0.90),C["blue"],
     "Service (blue) and emergency (red) air lines -- model both, offset 0.09 in Y",
     rot=(0,58,0))
part("fifth_wheel_skid","behind_cab","cylinder",(FIFTH_X,0,FIFTH_Z),(0.50,0.07),C["steel"],
     "Fifth wheel skid plate")
part("king_pin","behind_cab","cylinder",(FIFTH_X,0,FIFTH_Z+0.04),(0.045,0.13),C["chrome"],
     "King pin engaged in the jaws")
part("locking_jaws","behind_cab","cylinder",(FIFTH_X,0,FIFTH_Z+0.01),(0.14,0.05),C["dark"],
     "Locking jaws closed around the king pin")
part("locking_pins","behind_cab","box",(FIFTH_X-0.34,0.40,FIFTH_Z-0.06),(0.20,0.06,0.06),C["steel"],
     "Release handle and mounting pins")

# ── TRAILER ─────────────────────────────────────────────────────────────────
part("landing_gear","trailer_side","box",(LG_X,1.02,0.62),(0.14,0.14,1.24),C["steel"],
     "Landing gear leg, raised; mirror to both sides", mirror=True)
part("trailer_clearance_lights","trailer_side","box",(TRL_NOSE+0.05,1.24,TRL_TOP-0.06),
     (0.10,0.14,0.08),C["amber"],"Trailer clearance lights, amber at the front", mirror=True)
part("dot_tape","trailer_side","box",(12.0,HW+0.005,1.42),(9.60,0.01,0.05),C["red"],
     "DOT conspicuity tape, alternating red/white along the side")
part("rear_lenses","trailer_rear","box",(TRL_END-0.03,0.92,1.06),(0.06,0.34,0.16),C["red"],
     "Rear lens cluster: tail, brake, turn", mirror=True)
part("rear_clearance","trailer_rear","box",(TRL_END-0.03,0,TRL_TOP-0.06),(0.06,0.16,0.08),C["red"],
     "Rear clearance lights across the top rail")
part("rear_lights","trailer_rear","box",(TRL_END-0.03,0.60,1.38),(0.06,0.20,0.12),C["red"],
     "Turn / brake / flasher lamps", mirror=True)

# ── CAB INTERIOR ────────────────────────────────────────────────────────────
DASH_X, DASH_Z = 2.55, CAB_FLOOR + 0.60
part("seat_belt","driver_seat","box",(3.05,0.62,CAB_FLOOR+0.42),(0.05,0.02,0.70),C["dark"],
     "Seat belt webbing across the driver's seat", rot=(0,12,0))
part("valves_up","driver_seat","box",(DASH_X,0.20,DASH_Z),(0.10,0.16,0.05),C["yellow"],
     "Valve pair panel -- yellow parking + red trailer air supply")
part("gearshift_neutral","driver_seat","cylinder",(2.95,0.30,CAB_FLOOR+0.28),(0.03,0.46),C["dark"],
     "Gear shift lever")
part("windshield","driver_seat","box",(2.18,0,CAB_FLOOR+0.86),(0.04,2.30,0.86),C["glass"],
     "Windshield glass", rot=(0,-14,0))
part("mirrors","driver_seat","box",(2.44,1.42,2.28),(0.08,0.05,0.48),C["dark"],
     "Mirror seen from the driver's seat", mirror=True)
part("wipers","driver_seat","cylinder",(2.24,0.45,CAB_FLOOR+0.44),(0.014,0.70),C["dark"],
     "Wiper arm on the glass", rot=(0,76,0), mirror=True)
part("washer_fluid","driver_seat","cylinder",(1.32,0.72,1.38),(0.10,0.24),C["white"],
     "Washer fluid bottle in the engine bay, referenced from the cab")
part("heater_defroster","driver_seat","box",(DASH_X,-0.10,DASH_Z-0.10),(0.09,0.24,0.10),C["dark"],
     "Heater / defroster control panel")
part("horns","driver_seat","cylinder",(2.86,0.55,CAB_FLOOR+0.52),(0.10,0.05),C["dark"],
     "Horn pad at the centre of the steering wheel", rot=(0,16,0))
part("light_indicators","driver_seat","box",(DASH_X-0.04,0.55,DASH_Z+0.06),(0.05,0.34,0.18),C["dark"],
     "Dash indicator cluster")
part("fire_extinguisher","driver_seat","cylinder",(3.35,0.95,CAB_FLOOR+0.16),(0.06,0.34),C["red"],
     "Fire extinguisher, bracketed behind the seat")
part("triangles","driver_seat","box",(3.45,1.05,CAB_FLOOR+0.06),(0.30,0.08,0.24),C["red"],
     "Reflective triangle case")
part("spare_fuses","driver_seat","box",(DASH_X+0.14,-0.55,DASH_Z-0.02),(0.14,0.18,0.08),C["dark"],
     "Spare fuse and relay box")

# ── shared cab controls (drive the air-brake procedures) ────────────────────
ctrl("air_gauge_primary",(DASH_X-0.03,0.42,DASH_Z+0.10),(0.03,0.11,0.11),C["white"],
     "Primary air pressure gauge -- needle must animate", prim="cylinder")
ctrl("air_gauge_secondary",(DASH_X-0.03,0.26,DASH_Z+0.10),(0.03,0.11,0.11),C["white"],
     "Secondary air pressure gauge -- needle must animate", prim="cylinder")
ctrl("ignition_key",(DASH_X+0.02,0.70,DASH_Z-0.14),(0.02,0.04,0.04),C["chrome"],
     "Ignition key: OFF / ON / START", prim="cylinder")
ctrl("brake_pedal",(2.62,0.36,CAB_FLOOR+0.06),(0.22,0.12,0.03),C["dark"],
     "Service brake pedal -- travel drives the leak test")
ctrl("yellow_valve",(DASH_X-0.02,0.26,DASH_Z),(0.035,0.03),C["yellow"],
     "Yellow octagonal parking brake knob -- pull=set, push=release", prim="cylinder")
ctrl("red_valve",(DASH_X-0.02,0.14,DASH_Z),(0.035,0.03),C["red"],
     "Red octagonal trailer air supply knob -- pops out at 20-45 psi", prim="cylinder")
ctrl("low_air_light",(DASH_X-0.04,0.60,DASH_Z+0.16),(0.02,0.05,0.03),C["red"],
     "Low air warning lamp -- lights at or above 55 psi")

# ── stations ────────────────────────────────────────────────────────────────
STATIONS = [
 {"id":"driver_seat",    "camera":[3.05,0.62,CAB_FLOOR+0.72],"look_at":[2.30,0.30,CAB_FLOOR+0.55],"seated":True},
 {"id":"front_of_truck", "camera":[-1.60,0,1.60],            "look_at":[1.10,0,1.10]},
 {"id":"steer_axle",     "camera":[STEER_X,2.60,1.20],       "look_at":[STEER_X,1.10,0.70]},
 {"id":"driver_side",    "camera":[3.80,2.90,1.70],          "look_at":[3.80,1.20,1.10]},
 {"id":"behind_cab",     "camera":[FIFTH_X-0.60,2.10,1.95],  "look_at":[FIFTH_X,0.20,1.30]},
 {"id":"trailer_side",   "camera":[9.50,3.40,1.80],          "look_at":[9.50,1.25,1.40]},
 {"id":"trailer_rear",   "camera":[TRL_END+2.80,0,1.80],     "look_at":[TRL_END,0,1.90]},
]

doc = {
 "_README": ("Full 3D layout for the tractor-trailer. Every inspectable part with its "
             "primitive, size, position, colour and camera station, pre-computed so the "
             "builder runs a loop instead of iterating on geometry. Origin at the front "
             "bumper centre, ground level. +X rearward, +Y driver side, +Z up. Metres. "
             "'size' is [x,y,z] for a box and [radius,length] for a cylinder. "
             "'mirror_y': also emit a mirrored copy at -Y."),
 "units": "metres",
 "reference": {"tractor_length":7.2,"width":W,"wheelbase":WB,"steer_axle_x":STEER_X,
               "drive_axles_x":[DRIVE_A,DRIVE_B],"frame_top_z":FRAME_TOP,
               "fifth_wheel":[FIFTH_X,0,FIFTH_Z],"cab_floor_z":CAB_FLOOR,
               "trailer_nose_x":TRL_NOSE,"trailer_end_x":TRL_END,
               "trailer_floor_z":TRL_FLOOR,"trailer_top_z":TRL_TOP,
               "landing_gear_x":LG_X,"trailer_tandems_x":[TAND_A,TAND_B],
               "combination_length":round(TRL_END,2)},
 "procedures_no_geometry": [
   "safe_start","air_compressor_governor","air_leak_test","low_air_warning",
   "spring_brakes_popout","rate_of_buildup","parking_brake_check",
   "trailer_brake_check","service_brake_check","rr_procedure","emergency_procedure"],
 "stations": STATIONS,
 "parts": P,
}
json.dump(doc, open(f"{R}/content/truck_layout.json","w"), indent=1, ensure_ascii=False)

# ---- validate against the content -----------------------------------------
items = {i["id"] for s in json.load(open(f"{R}/content/pretrip.en.json"))["sections"]
         for i in s.get("items", [])}
laid  = {p["id"][5:] for p in P if p["id"].startswith("part_")}
procs = set(doc["procedures_no_geometry"])
missing = items - laid - procs
extra   = laid - items
print(f"parts with geometry : {len(laid)}")
print(f"cab controls        : {len([p for p in P if p['id'].startswith('ctrl_')])}")
print(f"procedures (no mesh): {len(procs)}")
print(f"stations            : {len(STATIONS)}")
print(f"coverage            : {len(laid)+len(procs)}/{len(items)} content items")
print(f"combination length  : {TRL_END:.2f} m")
if missing: print(f"MISSING: {sorted(missing)}")
if extra:   print(f"EXTRA:   {sorted(extra)}")
if not missing and not extra: print("\nOK — every content item is either laid out or declared procedure-only")
