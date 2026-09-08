#!/usr/bin/env python3
"""Build content/pretrip.en.json — the single source of truth for the game.

Every inspection item carries:
  script    : the model verbalisation (what a perfect student says)
  concepts  : the scoreable ideas inside that script, with accepted synonyms.
              Used by BOTH the offline keyword grader and the AI grader.
  action    : what the student physically does (name / point / touch / operate)
  auto_fail : whether missing this ends the test immediately

Source: "NEW MATERIAL PRE TRIP" (Fenix Truck School, 36pp) + "AIR BRAKES TEST"
handout + the official Class A Vehicle Inspection checklist (§11M).
"""
import json, os

ROOT = os.path.expanduser("~/Projects/PreTripCoach")
IMG  = "assets/reference/curated"

# ── reusable concept builders ────────────────────────────────────────────────
def c(cid, label, accept, required=True):
    return {"id": cid, "label": label, "accept": accept, "required": required}

SECURE   = lambda: c("secure", "Tight and securely mounted",
                     ["tight", "secure", "securely mounted", "properly mounted", "firmly mounted", "not loose"])
NO_CRACK = lambda: c("no_cracks", "No cracks",
                     ["no cracks", "not cracked", "no crack", "uncracked"])
NO_BREAK = lambda: c("not_broken", "Not bent, broken or twisted",
                     ["not broken", "not bent", "not twisted", "no breaks", "unbroken"])
NO_LEAK  = lambda: c("no_leaks", "No leaks",
                     ["no leaks", "not leaking", "no leak", "no air leaks", "no oil leaks"])
NO_WELD  = lambda: c("no_illegal_welds", "No illegal welds",
                     ["no illegal welding", "no illegal welds", "no welds", "no illegal weldings"])
CLEAN    = lambda: c("clean", "Clean", ["clean", "not dirty"])
COLOR    = lambda: c("proper_color", "Proper color",
                     ["proper color", "correct color", "amber", "red", "right color"])
HARDWARE = lambda: c("hardware", "All hardware present",
                     ["all hardware present", "hardware is present", "nothing missing",
                      "no missing bolts", "all bolts present"])
GREASED  = lambda: c("greased", "Properly greased",
                     ["greased", "properly greased", "fully greased", "lubricated"])
WORKS    = lambda: c("operational", "Demonstrated working",
                     ["works", "working", "operational", "functions", "operates"])

def item(iid, label, script, concepts, image=None, action="name_point_explain",
         auto_fail=False, tips=None, errors=None, demo=None):
    return {
        "id": iid, "label": label, "action": action,
        "image": f"{IMG}/{image}.png" if image else None,
        "script": script,
        "concepts": concepts,
        "auto_fail": auto_fail,
        "demonstrate": demo,
        "coach_tip": tips,
        "common_errors": errors or [],
    }

S = []  # sections

# ── 1. IN-CAB / ENGINE START ─────────────────────────────────────────────────
S.append({
 "id": "in_cab_engine_start", "order": 1,
 "title": "In-Cab / Engine Start",
 "checklist_category": "In-Vehicle/Engine Start",
 "book_pages": [7],
 "location": "driver_seat",
 "items": [
  item("seat_belt", "Seat Belt",
       "My seat belt is tight and secure at the top and the bottom, no cuts, no fraying, "
       "and it latches and releases properly.",
       [SECURE(), c("no_cuts","No cuts or fraying",["no cuts","no fraying","no frays","not torn","no rips"]),
        c("latches","Latches and releases properly",["latches","buckles","clicks","releases properly","opens and closes"])],
       image="01_incab_engine_start/seatbelt",
       tips="Physically tug the belt while you say it. Examiners want to see the check, not just hear it."),

  item("valves_up", "Air Valves — Set",
       "Both air valves are activated in the up position — the yellow parking brake valve "
       "and the red trailer air supply valve are pulled out.",
       [c("both_valves","Names both valves",["yellow","parking brake","red","trailer air supply","trailer supply"]),
        c("up_position","Valves are up / pulled out",["up position","pulled out","activated","set","out"])],
       image="01_incab_engine_start/valves_up", action="point_and_operate",
       tips="Yellow = tractor parking brake. Red = trailer air supply. Up/out means APPLIED."),

  item("gearshift_neutral", "Gear Shift",
       "My gear shift lever is in neutral.",
       [c("neutral","Shifter in neutral",["neutral","in neutral","ponto morto","neutro"])],
       image="01_incab_engine_start/gearshift_neutral", action="point_and_operate"),

  item("safe_start", "Safe Start",
       "I will safely start the engine: brakes are set, shifter is in neutral. Key to the on "
       "position — I check that my ABS and DEF lights come on and go off — then I start the motor.",
       [c("brakes_set","Brakes set before start",["brakes set","brakes are set","parking brake on","valves up"]),
        c("neutral","Shifter in neutral",["neutral","in neutral"]),
        c("abs_def","ABS and DEF lights come on and go off",["abs","def","warning lights come on","lights go off"]),
        c("start","Starts the engine",["start the motor","start the engine","crank"])],
       image="01_incab_engine_start/ignition_key", action="operate",
       tips="If the ABS light stays on, that is a defect — say so out loud.",
       errors=["Starting in gear","Forgetting to call out the ABS/DEF lamp check"]),
 ]})

# ── 2. IN-CAB BRAKE CHECK (AUTO-FAIL SECTION) ────────────────────────────────
S.append({
 "id": "in_cab_brake_check", "order": 2,
 "title": "In-Cab Air Brake Check",
 "checklist_category": "air or hydraulic brake check",
 "book_pages": [8, 9],
 "location": "driver_seat",
 "auto_fail_section": True,
 "note": "Marked on the official checklist as automatic failure if not performed correctly.",
 "items": [
  item("air_compressor_governor", "Air Compressor — Governor Cut-Out",
       "With the engine on I fast-idle the truck up to between 120 and 140 psi, at which point "
       "the governor cut-out should occur. I'll hear the air release after the cut-out. "
       "My needle stopped at ___ psi — cut-out works.",
       [c("range","120–140 psi range",["120","140","one twenty","one forty","full pressure"]),
        c("governor","Governor cut-out",["governor","cut out","cutout","cut-out"]),
        c("reading","States the actual reading",["psi","pounds","pressure is"]),
        c("air_release","Hears the air release",["air release","hear the air","pop","exhaust"])],
       image="02_incab_brake_check/air_gauges", action="operate_and_report",
       auto_fail=True,
       demo={"type":"gauge_reading","target_min":120,"target_max":140,"unit":"psi"},
       tips="Say the number you actually see. The grader wants a real reading, not a range."),

  item("air_leak_test", "Static Air Leak Test",
       "Engine off, key on, air valves pushed in. I depress and hold the brake pedal, wait for "
       "the gauge to stabilize, and start my timer. In one minute I cannot lose more than "
       "{{leak_limit_applied_psi_per_min}} psi. Starting at ___ psi — it's been one minute and I lost only "
       "___ psi. I did not lose more than {{leak_limit_applied_psi_per_min}} psi.",
       [c("engine_off","Engine off, key on",["engine off","key on","motor off","shut the engine off"]),
        c("valves_in","Valves pushed in",["pushed in","valves in","push in the valves"]),
        c("hold_pedal","Holds the brake pedal",["hold the brake","depress the brake","press the pedal","90 pounds"]),
        c("one_minute","Times a full minute",["one minute","60 seconds","sixty seconds","timer"]),
        c("limit","States the allowable loss",["psi in one minute","cannot lose more than","no more than"]),
        c("result","Reports the actual result",["i did not lose","no air leaks","still","lost only"])],
       image="02_incab_brake_check/air_gauges", action="operate_and_report",
       auto_fail=True,
       demo={"type":"timer","seconds":60,"max_loss_psi":"{{leak_limit_applied_psi_per_min}}"},
       tips="You must actually let 60 seconds run. Rushing the timer is a fail."),

  item("low_air_warning", "Low Air Warning — Light and Buzzer",
       "Engine off, key on, valves pushed in. I fan the brake pedal down. The low air warning "
       "light and buzzer must come on at or above 55 psi. It came on at ___ psi — my low air "
       "warning works.",
       [c("fan","Fans the brake pedal down",["fan","fanning","pump the brake","pump it down"]),
        c("threshold","At or above 55 psi",["55","fifty five","at or above 55"]),
        c("both","Light AND buzzer",["light","buzzer","alarm","sound"]),
        c("reading","Reports where it came on",["it came on at","psi"])],
       image="02_incab_brake_check/low_air_warning", action="operate_and_report",
       auto_fail=True,
       demo={"type":"gauge_reading","target_min":55,"target_max":75,"unit":"psi"}),

  item("spring_brakes_popout", "Spring Brakes — Pop-Out",
       "I continue fanning the brakes down. Between 45 and 20 psi both brake valves must pop out "
       "on their own. I'm looking at the valves, not the gauge — I do not pull the valves. "
       "They popped out at ___ psi — my spring brakes work.",
       [c("range","Between 45 and 20 psi",["45","20","forty five","twenty"]),
        c("both_pop","Both valves pop out",["both","pop out","popped out","both buttons"]),
        c("no_pull","Does not pull the valves",["do not pull","don't pull","did not pull","on their own","by themselves"]),
        c("reading","Reports the pop-out pressure",["they came on at","popped at","psi"])],
       image="02_incab_brake_check/valves_popped_out", action="operate_and_report",
       auto_fail=True,
       demo={"type":"gauge_reading","target_min":20,"target_max":45,"unit":"psi"},
       tips="Tell the examiner as EACH valve pops. If only one pops, keep fanning until the second pops.",
       errors=["Pulling the valves by hand — automatic fail",
               "Watching the gauge instead of the valves"]),

  item("rate_of_buildup", "Air Pressure Build-Up Rate",
       "Parking brakes on, shifter in neutral, I safely start the engine and hold 1500 rpm. "
       "First my low air warning must shut off at or above 55 psi. Then I time from 85 to 100 psi "
       "at idle — it must take 45 seconds or less. It took ___ seconds.",
       [c("rpm","Holds engine rpm",["1500","fifteen hundred","rpm","1200","1400"]),
        c("alarm_off","Warning shuts off at or above 55",["shuts off","goes off","55","fifty five"]),
        c("window","Times 85 to 100 psi",["85","100","eighty five","one hundred"]),
        c("limit","45 seconds or less",["45 seconds","forty five seconds","or less"]),
        c("reading","Reports actual seconds",["it took","seconds"])],
       image="02_incab_brake_check/air_gauges", action="operate_and_report",
       demo={"type":"timer","seconds":45,"window_psi":[85,100]},
       tips="Optional in some states, required in others. Check your examiner's sheet.",
       ),

  item("parking_brake_check", "Tractor Parking Brake Check",
       "I release the trailer brake — push the red valve in — put the truck in gear and try to "
       "move it lightly. The truck does not move, which means my tractor parking brakes hold.",
       [c("red_in","Red valve pushed in",["red valve","push the red","trailer brake released"]),
        c("in_gear","Puts it in gear and tries to move",["in gear","first gear","try to move","let up on the clutch"]),
        c("result","States the truck did not move",["did not move","doesn't move","truck stayed","holds"])],
       image="02_incab_brake_check/valves_popped_out", action="operate_and_report",
       auto_fail=True),

  item("trailer_brake_check", "Trailer Brake Check",
       "I release the tractor parking brake — push the yellow valve in — and leave the red valve "
       "out. I put the truck in gear and try to move it lightly. The truck does not move, which "
       "means my trailer brakes hold and the trailer stayed connected.",
       [c("yellow_in","Yellow valve pushed in",["yellow valve","push the yellow","parking brake released"]),
        c("red_out","Red valve stays out",["red valve out","leave the red out","trailer air supply out"]),
        c("in_gear","Puts it in gear and tries to move",["in gear","first gear","try to move","let up on the clutch"]),
        c("result","States the truck did not move",["did not move","doesn't move","trailer brakes work","fifth wheel is secure"])],
       image="02_incab_brake_check/valves_popped_out", action="operate_and_report",
       auto_fail=True),

  item("service_brake_check", "Service Brake Check",
       "I release both parking and trailer brakes — both valves in. I put the truck in gear and "
       "move forward between 5 and 10 mph, then apply the service brake. The truck stops straight: "
       "no pulling to the left or right, no unusual feel to the pedal, no delay in stopping, "
       "no chatter, no unusual sounds or smells.",
       [c("both_in","Both valves in",["both valves in","release both","both brakes off"]),
        c("speed","Rolls 5 to 10 mph",["5","10","five","ten","mph","miles per hour"]),
        c("apply","Applies the service brake",["apply the service brake","press the brake","service brake"]),
        c("no_pull","Does not pull left or right",["does not pull","doesn't pull","no pull","stops straight","left or right"]),
        c("feel","No unusual feel, delay, chatter or noise",["no delay","no chatter","no unusual","normal feel"], required=False)],
       image="02_incab_brake_check/service_brake_pedal", action="operate_and_report",
       auto_fail=True),
 ]})

# ── 3. IN-CAB EQUIPMENT & INDICATORS ─────────────────────────────────────────
S.append({
 "id": "in_cab_equipment", "order": 3,
 "title": "Lighting Indicators & Emergency Equipment",
 "checklist_category": "lighting indicators / emergency equipment",
 "book_pages": [10],
 "location": "driver_seat",
 "items": [
  item("light_indicators", "Dashboard Light Indicators",
       "With my lights on I check my dashboard indicators: high beams show a blue light, my right "
       "and left turn signals show flashing green arrows, and my four-way flashers show both green "
       "arrows flashing together.",
       [c("high_beam","High beam blue indicator",["blue","high beam","brights"]),
        c("turn","Left and right turn indicators",["green arrow","turn signal","left","right","flashing green"]),
        c("four_way","Four-way flashers",["four way","4-way","hazards","both arrows"])],
       image="04_incab_visibility/heater_defroster", action="operate_and_report"),

  item("fire_extinguisher", "Fire Extinguisher",
       "My fire extinguisher is tight and secure, fully charged in the green, up to date, and the "
       "pin is present and secure.",
       [SECURE(), c("charged","Fully charged / in the green",["full","charged","in the green","gauge"]),
        c("current","Up to date",["up to date","not expired","current","inspection date"]),
        c("pin","Pin present and secure",["pin","seal"])],
       image="03_incab_equipment/fire_extinguisher"),

  item("triangles", "Reflective Triangles",
       "I have three reflective warning triangles, tight and secure, no damage, and clean.",
       [c("three","Three triangles",["three","3","3 pieces"]), SECURE(),
        c("no_damage","No damage",["no damage","not damaged","not broken"]), CLEAN()],
       image="03_incab_equipment/reflective_triangles"),

  item("spare_fuses", "Spare Fuses",
       "I carry one box of extra fuses and relays — at least six spare fuses.",
       [c("present","Spare fuses present",["spare fuses","extra fuses","fuse box","relays"]),
        c("count","At least six",["six","6","at least six"])],
       image="03_incab_equipment/spare_fuses",
       tips="Not required if the vehicle has no fuses — say that instead if it's all breakers."),
 ]})

# ── 4. VISIBILITY & CONTROLS ─────────────────────────────────────────────────
S.append({
 "id": "in_cab_visibility", "order": 4,
 "title": "Windshield, Mirrors, Wipers, Heater & Horns",
 "checklist_category": "windshield & traffic monitoring devices / wipers & washers / heater & defroster / horn(s)",
 "book_pages": [11],
 "location": "driver_seat",
 "items": [
  item("windshield", "Windshield",
       "My windshield is tight and secure, no cracks, no illegal stickers, clean, and nothing is "
       "blocking my view.",
       [SECURE(), NO_CRACK(), c("no_stickers","No illegal stickers",["no illegal stickers","no stickers"]),
        CLEAN(), c("view","Nothing blocking the view",["nothing blocking","clear view","unobstructed"])],
       image="04_incab_visibility/windshield"),

  item("mirrors", "Mirrors",
       "My mirrors are adjusted to me, tight and secure, no cracks, not broken, clean, no illegal "
       "stickers, and nothing is blocking my view.",
       [c("adjusted","Adjusted to the driver",["adjusted","adjusted to me","set for me"]),
        SECURE(), NO_CRACK(), CLEAN(),
        c("view","Nothing blocking the view",["nothing blocking","clear view"])],
       image="04_incab_visibility/mirrors"),

  item("wipers", "Windshield Wipers",
       "My wipers are properly mounted with no missing bolts, not broken, blades have no splits or "
       "cuts, and they sit even with the windshield.",
       [SECURE(), HARDWARE(), NO_BREAK(),
        c("blades","Blades not split or cut",["no splits","no cuts","blades","not torn"]),
        c("contact","Even with the windshield",["even","flush","makes contact","against the glass"])],
       image="04_incab_visibility/wipers_blade"),

  item("washer_fluid", "Washer Fluid",
       "Washer fluid is present, and the wipers and washer are working properly.",
       [c("present","Fluid present",["present","fluid","full","has fluid"]), WORKS()],
       image="04_incab_visibility/washer_fluid_spray", action="operate_and_report"),

  item("heater_defroster", "Heater / Defroster",
       "I demonstrate that both my heater and my defroster are operational.",
       [c("both","Both heater and defroster",["heater","defroster","defrost"]), WORKS()],
       image="04_incab_visibility/heater_defroster", action="operate_and_report"),

  item("horns", "Horns",
       "I ensure both horns are operational — my city horn and my highway air horn.",
       [c("both","Both horns",["city horn","air horn","highway horn","both horns"]), WORKS()],
       image="04_incab_visibility/horn", action="operate_and_report"),
 ]})

# ── 5. LIGHTS OPERATIONS (sequence drill) ────────────────────────────────────
S.append({
 "id": "lights_operations", "order": 5,
 "title": "Lights Operations Check",
 "checklist_category": "all external lights",
 "book_pages": [13],
 "location": "walk_around",
 "type": "light_sequence",
 "strategy": "Group similar lights together (headlights + high beams; turn signals + 4-way "
             "flashers; brake lights + tail lights). Four sides of the truck, four sides of the "
             "trailer — follow the flow and you won't miss any.",
 "sequence": [
  {"zone": "truck_front",   "label": "Front of Truck",
   "lights": ["clearance lights", "headlights", "high beams", "left turn", "right turn", "4-way flashers"],
   "image": f"{IMG}/05_lights_operations/tractor_studio.png"},
  {"zone": "truck_left",    "label": "Left Side of Truck",
   "lights": ["clearance light", "left turn", "4-way flasher"],
   "image": f"{IMG}/08_side_of_vehicle/tractor_side_a.png"},
  {"zone": "truck_rear",    "label": "Rear of Truck",
   "lights": ["tail lights", "brake lights", "left turn", "right turn", "4-way flasher"],
   "image": f"{IMG}/05_lights_operations/marker_light_amber.png"},
  {"zone": "truck_right",   "label": "Right Side of Truck",
   "lights": ["clearance light", "right turn", "4-way flasher"],
   "image": f"{IMG}/08_side_of_vehicle/tractor_side_c.png"},
  {"zone": "trailer_front", "label": "Front of Trailer",
   "lights": ["clearance lights"],
   "image": f"{IMG}/05_lights_operations/trailer_front_reefer.png"},
  {"zone": "trailer_left",  "label": "Left Side of Trailer",
   "lights": ["clearance light", "left turn", "4-way flasher"],
   "image": f"{IMG}/05_lights_operations/trailer_side_id.png"},
  {"zone": "trailer_rear",  "label": "Rear of Trailer",
   "lights": ["clearance lights", "tail lights", "brake lights", "left turn", "right turn", "4-way flasher"],
   "image": f"{IMG}/05_lights_operations/trailer_rear_lit.png"},
  {"zone": "trailer_right", "label": "Right Side of Trailer",
   "lights": ["clearance light", "right turn", "4-way flasher"],
   "image": f"{IMG}/05_lights_operations/marker_light_amber_alt.png"},
 ]})

# ── 6. FRONT OF VEHICLE / ENGINE AREA ────────────────────────────────────────
S.append({
 "id": "front_operations", "order": 6,
 "title": "Front of Vehicle / Engine Area",
 "checklist_category": "lenses / fluid levels / fluid & air leaks / steering systems",
 "book_pages": [15, 16, 17, 18],
 "location": "front_of_truck",
 "items": [
  item("truck_leveled", "Truck Leveled",
       "My truck is leveled and there are no leaks underneath — no oil, no grease, no coolant.",
       [c("level","Truck is level",["leveled","level","sitting level"]),
        c("no_puddles","No leaks underneath",["no leaks","no oil","no grease","no coolant","nothing on the ground"])],
       image="05_lights_operations/tractor_studio"),

  item("front_lenses", "Clearance, Flasher & Signal Lights",
       "My clearance, flasher and signal lights are tight and secure, no cracks, and the proper color.",
       [SECURE(), NO_CRACK(), COLOR()],
       image="05_lights_operations/marker_light_amber"),

  item("headlights", "Headlights — High and Low Beam",
       "My headlights, high beam and low beam, are tight and secure, no cracks, clean, and the "
       "proper color.",
       [SECURE(), NO_CRACK(), CLEAN(), COLOR(),
        c("both_beams","High and low beam",["high beam","low beam","both beams"])],
       image="05_lights_operations/tractor_studio"),

  item("coolant", "Coolant",
       "I verify the coolant is at the proper level through the sight glass or dipstick. The "
       "reservoir is properly mounted and not cracked, and the hoses have no splits or cuts and "
       "are securely mounted at both ends.",
       [c("level","Proper level",["proper level","correct level","full","at the line"]),
        c("how","Sight glass or dipstick",["sight glass","dipstick","reservoir"]),
        SECURE(), NO_CRACK(),
        c("hoses","Hoses no splits or cuts, secure both ends",["hoses","no splits","no cuts","both ends"])],
       image="06_front_operations/coolant_reservoir"),

  item("oil", "Engine Oil",
       "I indicate where my dipstick is located and that the oil is at the proper level.",
       [c("dipstick","Points out the dipstick",["dipstick","stick"]),
        c("level","Proper level",["proper level","correct level","full","between the marks"])],
       image="06_front_operations/engine_fluids_wide"),

  item("power_steering", "Power Steering Fluid",
       "I verify the power steering fluid is at the proper level through the sight glass or "
       "dipstick. The reservoir is securely mounted and not cracked, and the hoses have no splits "
       "or cuts and are securely mounted at both ends.",
       [c("level","Proper level",["proper level","correct level","full"]),
        c("how","Sight glass or dipstick",["sight glass","dipstick","reservoir"]),
        SECURE(), NO_CRACK(),
        c("hoses","Hoses no splits or cuts, secure both ends",["hoses","no splits","no cuts","both ends"])],
       image="06_front_operations/power_steering_reservoir"),

  item("fluid_air_leaks", "Fluid & Air Leaks",
       "Standing in front of the truck, I ensure there are no leaks underneath the engine "
       "compartment. I verify all the hoses in the engine compartment — no cuts, no bubbles, no leaks.",
       [c("under","Checks underneath the engine",["underneath","under the engine","below"]),
        NO_LEAK(),
        c("hoses","All hoses — no cuts, bubbles or leaks",["hoses","no cuts","no bubbles","no leaks"])],
       image="06_front_operations/engine_hoses"),

  item("steering_gear_box", "Steering Gear Box",
       "My steering gear box is properly mounted to the frame, not cracked, not leaking, all "
       "hardware is present, and the hose has no leaks and is properly mounted at both ends.",
       [SECURE(), NO_CRACK(), NO_LEAK(), HARDWARE()],
       image="06_front_operations/steering_gearbox"),

  item("pitman_arm", "Pitman Arm",
       "My pitman arm is not cracked and securely mounted, all hardware is present, and the castle "
       "nuts and cotter pins are in place.",
       [NO_CRACK(), SECURE(), HARDWARE(),
        c("cotter","Castle nuts and cotter pins in place",["castle nut","cotter pin","cotter pins"])],
       image="06_front_operations/steering_gearbox"),

  item("drag_link", "Drag Link",
       "My drag link is properly mounted at both ends, all hardware is present, and the rubber "
       "bushings are not split or cut and are properly greased.",
       [SECURE(), HARDWARE(),
        c("bushings","Rubber bushings not split or cut",["bushings","rubber","no splits","not cut"]),
        GREASED()],
       image="06_front_operations/steering_gearbox"),

  item("control_arms", "Upper & Lower Control Arms",
       "My upper and lower control arms are not broken and securely mounted, all hardware present.",
       [NO_BREAK(), SECURE(), HARDWARE()],
       image="06_front_operations/steering_gearbox"),

  item("tie_rod", "Tie Rod",
       "My tie rod is not broken and securely mounted, all hardware present, castle nuts and "
       "cotter pins in place.",
       [NO_BREAK(), SECURE(), HARDWARE(),
        c("cotter","Castle nuts and cotter pins",["castle nut","cotter pin","cotter pins"], required=False)],
       image="06_front_operations/steering_gearbox"),
 ]})

# ── 7. STEERING AXLE ─────────────────────────────────────────────────────────
S.append({
 "id": "steering_axle", "order": 7,
 "title": "Steering Axle",
 "checklist_category": "tires / rims / lug nuts / springs & mounts & shocks / brake lines & hoses / brake contaminates",
 "book_pages": [20, 21],
 "location": "steer_axle",
 "items": [
  item("front_tire", "Front Tire",
       "My steer tire is evenly worn with tread depth no less than four thirty-seconds. No cuts, "
       "no bulges, no bubbles, no air leaks, no recaps on the steer axle, and no flat spots. "
       "Properly inflated at around 100 psi.",
       [c("even_wear","Evenly worn",["evenly worn","even wear","uniform"]),
        c("tread","Tread depth at least 4/32",["4/32","four thirty second","four thirty-seconds","tread depth"]),
        c("no_damage","No cuts, bulges or bubbles",["no cuts","no bulges","no bubbles","no damage"]),
        c("no_leak","No air leaks",["no air leaks","not leaking"]),
        c("no_recap","No recaps on the steer axle",["no recap","no retread","not recapped"]),
        c("pressure","Properly inflated",["100 psi","properly inflated","proper pressure"])],
       image="07_steering_axle/front_tire",
       tips="Steer tires need 4/32\". Every other tire on the vehicle needs 2/32\". Never call a "
            "recap legal on the steer axle.",
       errors=["Saying 2/32 on the steer axle","Saying '4.32 inches' instead of 'four thirty-seconds'"]),

  item("rims", "Rims",
       "My rims are tight and secure, no cracks, no bends, not broken, no illegal welds, and no "
       "illegal holes.",
       [SECURE(), NO_CRACK(), NO_BREAK(), NO_WELD(),
        c("no_holes","No illegal holes",["no illegal holes","no holes"])],
       image="07_steering_axle/rim_lugnuts"),

  item("lug_nuts", "Lug Nuts",
       "My lug nuts are tight and secure, all present, no cracks, and no rust streaks — if I see "
       "rust they might be loose and they need to be tightened. No bolt holes elongated.",
       [SECURE(), c("all_present","All present",["all present","none missing","all there"]),
        NO_CRACK(),
        c("rust","No rust streaks (sign of looseness)",["no rust","rust","rust streaks","shiny threads"])],
       image="07_steering_axle/rim_lugnuts",
       tips="Explaining WHY rust matters — 'rust means it may be loose' — is what earns the credit."),

  item("spring_mounts", "Spring Mounts",
       "My spring mounts and hardware are not cracked or broken and are properly mounted to the frame.",
       [NO_CRACK(), NO_BREAK(), SECURE(), HARDWARE()],
       image="07_steering_axle/spring_mount"),

  item("leaf_springs", "Leaf Springs",
       "My leaf springs are not shifted or scissoring, no illegal welds, and they're properly "
       "mounted to the spring hangers.",
       [c("not_shifted","Not shifted or scissoring",["not shifted","no scissoring","not scissored","aligned"]),
        NO_WELD(), SECURE()],
       image="07_steering_axle/leaf_springs"),

  item("u_bolts", "U-Bolts",
       "My U-bolts are not cracked or broken, no loose parts, and no missing bolts.",
       [NO_CRACK(), NO_BREAK(), HARDWARE()],
       image="07_steering_axle/ubolts_shock"),

  item("shock_absorber", "Shock Absorber",
       "My shock absorber is not bent or broken and is mounted securely, no visible leaks, and the "
       "rubber bushings are not worn.",
       [NO_BREAK(), SECURE(), NO_LEAK(),
        c("bushings","Rubber bushings not worn",["bushings","rubber","not worn"])],
       image="07_steering_axle/ubolts_shock"),

  item("brake_hose", "Air Brake System Hose",
       "My air brake hose is tight and secure with fittings at both ends, no cracks, no air leaks, "
       "not worn, and no dry rot.",
       [SECURE(), c("fittings","Fittings at both ends",["fittings","both ends"]),
        NO_CRACK(), NO_LEAK(),
        c("no_rot","Not worn, no dry rot",["dry rot","not worn","no rot"])],
       image="07_steering_axle/air_brake_hose"),

  item("air_chamber", "Air Chamber",
       "My air chamber is properly mounted, tight and secure, no cracks, not broken, no air leaks, "
       "and the clamps are tight and not missing.",
       [SECURE(), NO_CRACK(), NO_BREAK(), NO_LEAK(),
        c("clamps","Clamps tight and present",["clamps","clamp","not missing"])],
       image="07_steering_axle/air_chamber"),

  item("brake_contaminants", "Brake Drums, Shoes & Linings",
       "My brake drum is not cracked and my shoes and linings are not worn thinner than a quarter "
       "inch. There are no contaminants — no oil, no grease, no debris between the brake drum and "
       "the brake shoes.",
       [c("drum","Drum not cracked",["drum","not cracked","no cracks"]),
        c("lining","Lining thickness",["quarter inch","1/4","not worn thin","thickness"], required=False),
        c("contaminants","No oil, grease or debris",["no oil","no grease","no debris","no contaminants"])],
       image="07_steering_axle/brake_drum_shoes",
       tips="'Brake contaminates' is its own line on the official checklist — say the words "
            "'no oil, no grease, no debris' explicitly."),
 ]})

# ── 8. SIDE OF VEHICLE ───────────────────────────────────────────────────────
S.append({
 "id": "side_of_vehicle", "order": 8,
 "title": "Side of Vehicle",
 "checklist_category": "lenses & reflectors / traffic monitoring devices / battery / fuel & DEF tanks / frame",
 "book_pages": [23],
 "location": "driver_side",
 "items": [
  item("turn_signal_side", "Turn Signal Light & Reflectors",
       "My turn signal light is tight and secure, no cracks, clean, proper amber color, and it "
       "works as a signal light and as an emergency light. My reflectors are amber at the front "
       "and red at the back.",
       [SECURE(), NO_CRACK(), CLEAN(), COLOR(),
        c("reflectors","Amber front, red rear",["amber","red","front","back","reflectors"])],
       image="08_side_of_vehicle/tractor_side_a"),

  item("mirrors_side", "Mirrors (Traffic Monitoring Devices)",
       "My mirrors are tight and secure to the door, no cracks, not broken, clean, and no illegal "
       "stickers blocking my view.",
       [SECURE(), NO_CRACK(), NO_BREAK(), CLEAN(),
        c("view","Nothing blocking the view",["nothing blocking","no stickers","clear view"])],
       image="08_side_of_vehicle/tractor_side_b"),

  item("fuel_tank", "Fuel Tank",
       "My fuel tank is tight and secure, no cracks, not bent, no leaks. The cap is present, tight "
       "and secure. The straps are secure and not cracked.",
       [SECURE(), NO_CRACK(), NO_BREAK(), NO_LEAK(),
        c("cap","Cap present and tight",["cap","cap is present","cap is tight"]),
        c("straps","Straps secure",["straps","mounting straps"], required=False)],
       image="08_side_of_vehicle/fuel_def_tank"),

  item("def_tank", "DEF Tank",
       "My DEF tank is tight and secure, no cracks, not bent, no leaks. The cap is present, tight "
       "and secure, no cracks or leaks.",
       [SECURE(), NO_CRACK(), NO_BREAK(), NO_LEAK(),
        c("cap","Cap present and tight",["cap","cap is present","cap is tight"])],
       image="08_side_of_vehicle/fuel_def_tank"),

  item("battery", "Battery",
       "My battery box and cover are secured, no cracks, no broken welds, and the battery "
       "connectors are secured. The cables and wires are not exposed, corroded, ripped or torn.",
       [SECURE(), NO_CRACK(),
        c("welds","No broken welds",["no broken welds","welds"]),
        c("connectors","Connectors secured",["connectors","terminals","secured"]),
        c("cables","Cables not exposed, corroded or torn",["not exposed","no corrosion","not corroded","not torn","not ripped"])],
       image="08_side_of_vehicle/battery_box"),

  item("frame", "Frame",
       "My frame has no cracks, is not bent, twisted or broken, no illegal welding, and no rust "
       "through.",
       [NO_CRACK(), NO_BREAK(), NO_WELD(),
        c("rust","No rust through",["no rust","not rusted"])],
       image="08_side_of_vehicle/frame"),
 ]})

# ── 9. COMBINATION VEHICLES ONLY ─────────────────────────────────────────────
S.append({
 "id": "combination_vehicle", "order": 9,
 "title": "Combination Vehicles Only",
 "checklist_category": "air & electric lines & connectors / fifth wheel / kingpin & apron & gap / locking & safety devices",
 "book_pages": [25],
 "location": "behind_cab",
 "applies_to": ["class_a"],
 "items": [
  item("electrical_line", "Electrical Line",
       "My electrical line — the green cable — is flexible and doesn't touch the frame, catwalk, "
       "tractor or trailer. No exposed wires and no illegal taping. It's tight and secure to my "
       "tractor with the seven pins and to my trailer's electrical box with the seven pins. The "
       "pins are not bent or broken, no debris, and all seven are present.",
       [c("flexible","Flexible, not rubbing",["flexible","doesn't touch","not rubbing","no chafing"]),
        c("no_exposed","No exposed wires or illegal tape",["no exposed wires","no illegal taping","not taped"]),
        SECURE(),
        c("pins","All seven pins present, not bent",["seven pins","7 pins","all seven","not bent"])],
       image="09_combination/air_electrical_lines"),

  item("air_lines", "Air Lines — Service & Emergency",
       "My service line is the blue hose and my emergency line is the red hose. They don't touch "
       "the tractor, trailer or catwalk, they're flexible, no cuts, no bubbles, no leaks. They're "
       "tight and secure to my tractor with the fittings and to my trailer with the glad hands, "
       "and the glad hand rubber seals are not worn.",
       [c("colors","Blue service, red emergency",["blue","red","service line","emergency line"]),
        c("flexible","Flexible, not rubbing",["flexible","doesn't touch","not rubbing"]),
        c("no_damage","No cuts, bubbles or leaks",["no cuts","no bubbles","no leaks"]),
        c("gladhands","Glad hands secure, seals not worn",["glad hand","gladhands","rubber seal","not worn"])],
       image="09_combination/air_electrical_lines"),

  item("fifth_wheel_skid", "Fifth Wheel Skid Plate",
       "My fifth wheel skid plate is tight and secure to the platform, no cracks, not broken, no "
       "illegal welding, and properly greased. There is no space between the skid plate and the apron.",
       [SECURE(), NO_CRACK(), NO_BREAK(), NO_WELD(), GREASED(),
        c("no_gap","No gap between skid plate and apron",["no space","no gap","flush","no daylight"])],
       image="09_combination/fifth_wheel_skid_plate",
       tips="'No gap' is the safety-critical part — a visible gap means the trailer can separate."),

  item("king_pin", "King Pin & Apron",
       "My king pin is securely mounted, not bent or cracked, no illegal welding, and fully "
       "greased. My apron is securely mounted to the trailer, not cracked or broken, and has no "
       "illegal holes or welds.",
       [SECURE(), NO_BREAK(), NO_CRACK(), NO_WELD(), GREASED(),
        c("apron","Apron secure and sound",["apron","securely mounted to the trailer"])],
       image="09_combination/kingpin_apron"),

  item("locking_jaws", "Locking Jaws",
       "My locking jaw is securely mounted, no cracks, no illegal welds, fully greased, and it's "
       "in the locked position all the way around the king pin.",
       [SECURE(), NO_CRACK(), NO_WELD(), GREASED(),
        c("locked","Closed all the way around the king pin",["locked position","all the way around","closed around","engaged"])],
       image="09_combination/locking_jaws"),

  item("locking_pins", "Mounting Pins, Release Handle & Pivot Pins",
       "My mounting pins are present, fully engaged and in the locked position. My release handle "
       "is not broken and is in the locked position all the way in. My pivot pins are present, not "
       "cracked or broken.",
       [c("pins","Mounting pins present and engaged",["pins are present","fully engaged","locked position"]),
        c("handle","Release handle locked, not broken",["release handle","not broken","all the way in"]),
        c("pivot","Pivot pins present, not cracked",["pivot pins","not cracked","not broken"])],
       image="09_combination/release_handle_pins"),
 ]})

# ── 10. TRAILER ONLY ─────────────────────────────────────────────────────────
S.append({
 "id": "trailer_only", "order": 10,
 "title": "Trailer Only",
 "checklist_category": "landing gear & clearance / reflective tape",
 "book_pages": [27],
 "location": "trailer_side",
 "applies_to": ["class_a"],
 "items": [
  item("landing_gear", "Landing Gear",
       "My landing gear is fully raised, properly mounted, not broken, no illegal welding. The "
       "crank handle is present, not broken, secured in its holder, and it's operational.",
       [c("raised","Fully raised",["raised","up","fully raised","cranked up"]),
        SECURE(), NO_BREAK(), NO_WELD(),
        c("handle","Crank handle present and secured",["handle","crank","present","secured"])],
       image="10_trailer_only/landing_gear"),

  item("trailer_clearance_lights", "Trailer Clearance Lights",
       "My trailer clearance lights are tight and secure, clean, not cracked, proper amber color "
       "on the front and red on the back.",
       [SECURE(), CLEAN(), NO_CRACK(), COLOR()],
       image="11_rear_of_trailer/clearance_lights"),

  item("dot_tape", "DOT Reflective Tape",
       "My DOT tape is present, properly fastened, not dirty, and covers at least fifty percent of "
       "the side of my trailer. Proper red and clear color.",
       [c("present","Present and fastened",["present","properly fastened","attached"]),
        CLEAN(),
        c("coverage","At least 50% coverage",["50","fifty percent","half"]),
        c("color","Red and white/clear",["red","clear","white"])],
       image="10_trailer_only/dot_tape"),
 ]})

# ── 11. REAR OF TRAILER ──────────────────────────────────────────────────────
S.append({
 "id": "rear_of_trailer", "order": 11,
 "title": "Rear of Trailer",
 "checklist_category": "lenses & reflectors",
 "book_pages": [29],
 "location": "trailer_rear",
 "applies_to": ["class_a"],
 "items": [
  item("rear_lenses", "Lenses & Reflectors",
       "My lenses and reflectors are not cracked, broken or loose, they're clean and the proper "
       "color. They function as turn signals, emergency lights, brake lights, markers and reflectors.",
       [NO_CRACK(), NO_BREAK(), SECURE(), CLEAN(), COLOR(),
        c("functions","Names the functions",["turn signal","brake light","emergency","marker","reflector"])],
       image="11_rear_of_trailer/lenses_reflectors"),

  item("rear_clearance", "Clearance Lights",
       "My clearance lights are tight, secure, no cracks, proper color, clean and working.",
       [SECURE(), NO_CRACK(), COLOR(), CLEAN(), WORKS()],
       image="11_rear_of_trailer/clearance_lights"),

  item("rear_lights", "Turn, Brake, Clearance & Flasher Lights",
       "My turn signals, brake lights, clearance lights and flasher lights are tight, secure, no "
       "cracks, proper color and working.",
       [SECURE(), NO_CRACK(), COLOR(), WORKS()],
       image="11_rear_of_trailer/lenses_reflectors"),
 ]})

# ── 12. RAILROAD CROSSING (procedure) ────────────────────────────────────────
S.append({
 "id": "railroad_crossing", "order": 12,
 "title": "Railroad Crossing",
 "checklist_category": "road test — railroad crossing",
 "book_pages": [30],
 "location": "on_road",
 "type": "procedure",
 "items": [
  item("rr_procedure", "Railroad Crossing Procedure",
       "At two hundred feet I turn my flashers on and check for traffic. I move forward between "
       "fifteen and fifty feet from the tracks. I stop, lower my window, look and listen for a "
       "train. I don't see or hear a train — it's safe. I have space on the other side to clear the "
       "tracks completely. I stay to my right. I move forward without changing gears. Once the "
       "trailer passes the tracks I turn my flashers off, check my traffic and accelerate.",
       [c("flashers_on","Flashers on at 200 ft",["200 feet","two hundred feet","flashers on"]),
        c("stop_distance","Stops 15–50 ft from the tracks",["15","50","fifteen","fifty","feet"]),
        c("window","Lowers window, looks and listens",["window","lower my window","look","listen"]),
        c("clear","Has room to clear the far side",["space","room","clear the tracks","other side"]),
        c("no_shift","No gear change on the tracks",["without changing gear","no shifting","don't shift"]),
        c("flashers_off","Flashers off after clearing",["flashers off","turn off my flashers"])],
       action="narrate_procedure",
       image="12_railroad_crossing/crossing_sign",
       tips="Never shift on the tracks. Never stop on the tracks. Both are instant fails.",
       errors=["Shifting gears while on the tracks","Stopping with any part of the rig on the tracks",
               "Forgetting to turn the flashers back off"]),
 ]})

# ── 13. EMERGENCY STOP (procedure) ───────────────────────────────────────────
S.append({
 "id": "emergency_stop", "order": 13,
 "title": "Emergency Stop",
 "checklist_category": "road test — emergency stop",
 "book_pages": [31],
 "location": "on_road",
 "type": "procedure",
 "items": [
  item("emergency_procedure", "Emergency Stop Procedure",
       "I will pull to the side of the road, put my brake valves up, put my truck in neutral, turn "
       "on my four-way flashers, and place my three reflective triangles. Then I check for traffic "
       "before I get back in and accelerate.",
       [c("pull_over","Pulls fully off the road",["pull to the side","pull over","off the road","shoulder"]),
        c("valves_up","Brake valves up",["valves up","set the brakes","parking brake"]),
        c("neutral","Transmission in neutral",["neutral"]),
        c("flashers","Four-way flashers on",["four way","4-way","flashers","hazards"]),
        c("triangles","Places three triangles",["three triangles","3 triangles","reflective triangles","warning devices"]),
        c("traffic","Checks traffic before moving",["check for traffic","check traffic"])],
       action="narrate_procedure",
       image="13_emergency_stop/triangles_placed",
       tips="Triangle placement: 10 ft behind, 100 ft behind, and 100 ft ahead on a two-lane road."),
 ]})

# ── standards / thresholds (configurable per state) ──────────────────────────
STANDARDS = {
  "_note": "Thresholds are configuration, never hardcoded in components. The static leak limit was "
           "disputed between the booklet (4 psi/min Class A) and the air-brake handout (3 released / "
           "4 applied); RESOLVED 2026-09-08 by Alexandre in favour of the handout, for both FL and MA. "
           "The booklet's figure is retained below as leak_limit_booklet_psi_per_min for reference only "
           "and is NOT used for grading.",
  "_leak_limit_resolved": {
    "decision": "handout", "released_psi_per_min": 3, "applied_psi_per_min": 4,
    "decided_by": "Alexandre Felix", "decided_on": "2026-09-08",
    "applies_to": ["us_fl", "us_ma"], "confirmed": True
  },
  "class_a_combination": {
    "governor_cutout_psi": [120, 140],
    "governor_cutin_psi": [85, 100],
    "leak_limit_released_psi_per_min": 3,
    "leak_limit_applied_psi_per_min": 4,
    "leak_limit_booklet_psi_per_min": 4,
    "leak_limit_source": "AIR BRAKES TEST handout (confirmed 2026-09-08)",
    "low_air_warning_psi_min": 55,
    "spring_brake_popout_psi": [20, 45],
    "buildup_85_to_100_max_seconds": 45,
    "service_brake_test_speed_mph": [5, 10],
    "steer_tire_tread_32nds": 4,
    "other_tire_tread_32nds": 2,
    "steer_tire_pressure_psi": 100,
    "brake_lining_min_inches": 0.25
  },
  "class_b_straight": {
    "governor_cutout_psi": [120, 140],
    "leak_limit_released_psi_per_min": 2,
    "leak_limit_applied_psi_per_min": 3,
    "leak_limit_booklet_psi_per_min": 3,
    "low_air_warning_psi_min": 55,
    "spring_brake_popout_psi": [20, 45],
    "buildup_85_to_100_max_seconds": 45,
    "steer_tire_tread_32nds": 4,
    "other_tire_tread_32nds": 2
  }
}


# ── jurisdictions (per school / per state) ───────────────────────────────────
JURISDICTIONS = {
  "_note": "The app ships to two schools in two states. Each student is assigned a "
           "jurisdiction once; all checklist wording and any threshold overrides come "
           "from here. Overrides are deliberately empty until confirmed against each "
           "state's current examiner sheet — see docs/06_OPEN_QUESTIONS.md Q1.",
  "us_fl": {
    "label": "Florida",
    "school": "Fenix Truck School — Jacksonville, FL",
    "checklist_reference": "FL CDL Vehicle Inspection checklist — TO BE CONFIRMED",
    "checklist_confirmed": False,
    "_todo": "Alexandre to supply the Florida examiner sheet; thresholds already confirmed.",
    "threshold_overrides": {}
  },
  "us_ma": {
    "label": "Massachusetts",
    "school": "Moov — Boston, MA",
    "checklist_reference": "MA RMV CDL Manual Section 11M, version 2022-09-09",
    "checklist_confirmed": True,
    "threshold_overrides": {}
  }
}

doc = {
  "schema_version": "1.0.0",
  "content_version": "2026.09.08",
  "title": "CDL Pre-Trip Inspection & Air Brake Test",
  "publisher": "Fenix Truck School",
  "source_documents": [
    "NEW MATERIAL PRE TRIP.pdf (36 pp)",
    "AIR BRAKES TEST handout",
    "Class A Vehicle Inspection checklist §11M (rev. 2022-09-09)"
  ],
  "languages": ["en", "es", "pt"],
  "vehicle_classes_supported": ["class_a_combination"],
  "default_vehicle_class": "class_a_combination",
  "jurisdictions": JURISDICTIONS,
  "default_jurisdiction": "us_fl",
  "transmissions": ["manual", "automatic"],
  "tenancy": {
    "mode": "single_org",
    "_note": "Built school-only but tenant-ready: every run, progress and leaderboard "
             "row carries an org_id from day one so multi-school can be switched on "
             "later without a data migration. See BUILD_SPEC.md."
  },
  "standards": STANDARDS,
  "grading": {
    "credit_rule": "You MUST name, point to and/or touch, and fully explain what you are "
                   "inspecting each safety-critical item for. If you do not, you get no credit.",
    "pass_threshold_pct": 80,
    "auto_fail_sections": ["in_cab_brake_check"],
    "auto_fail_behaviour": "Missing any auto_fail item ends the run immediately with a FAIL and a "
                           "written explanation of what was missed."
  },
  "sections": S,
}

# integrity checks
ids = [it["id"] for sec in S for it in sec.get("items", [])]
assert len(ids) == len(set(ids)), f"duplicate item ids: {[i for i in ids if ids.count(i)>1]}"
for sec in S:
    for it in sec.get("items", []):
        assert it["script"], it["id"]
        assert it["concepts"], it["id"]

out = f"{ROOT}/content/pretrip.en.json"
json.dump(doc, open(out, "w"), indent=2, ensure_ascii=False)
n_items = len(ids)
n_concepts = sum(len(it["concepts"]) for sec in S for it in sec.get("items", []))
n_af = sum(1 for sec in S for it in sec.get("items", []) if it["auto_fail"])
print(f"wrote {out}")
print(f"  sections        : {len(S)}")
print(f"  graded items    : {n_items}")
print(f"  scoreable concepts: {n_concepts}")
print(f"  auto-fail items : {n_af}")
print(f"  light sequence  : {sum(len(z['lights']) for z in S[4]['sequence'])} lights across 8 zones")
