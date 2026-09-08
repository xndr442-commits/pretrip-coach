#!/usr/bin/env python3
"""Build content/airbrakes.en.json — the standalone Air Brake Test module.

This is a TIMED, ORDERED, SPOKEN procedure. Unlike the pre-trip walkaround,
order matters and the student must announce live numeric readings. Source:
the "AIR BRAKES TEST" handout.
"""
import json, os
ROOT = os.path.expanduser("~/Projects/PreTripCoach")
IMG = "assets/reference/curated"

def step(sid, say, must, kind="say", **kw):
    d = {"id": sid, "kind": kind, "say": say, "must": must}
    d.update(kw); return d

PHASES = [
{"id":"setup","preconditions":['engine_off', 'shifter_neutral', 'parking_brakes_set'],"title":"Setup & Securement","order":1,
 "image":f"{IMG}/01_incab_engine_start/valves_up.png",
 "steps":[
  step("secure","Check the brakes are set and the shifter is in neutral.",
       ["brakes set","neutral"], kind="do"),
  step("start_1","Safely start the engine.",["start"],kind="do"),
  step("first_gear","Put the truck in first gear.",["first gear"],kind="do"),
  step("shutdown","Shut off the engine and take the key.",["shut off","take the key"],kind="do"),
  step("chock","Chock the wheels.",["chock"],kind="do"),
  step("return","Return to the truck maintaining three points of contact.",
       ["three points of contact"],kind="do",
       note="Three points of contact is scored on the road test too — build the habit here."),
  step("safe_start","\"I will safely start the engine: shifter in neutral, brakes set.\"",
       ["safely start","neutral","brakes set"]),
 ]},

{"id":"cut_in_cut_out","preconditions":['engine_on', 'valves_in', 'wheels_chocked'],"title":"Governor Cut-In and Cut-Out","order":2,
 "image":f"{IMG}/02_incab_brake_check/air_gauges.png",
 "steps":[
  step("release","After the engine is on, release the parking brakes.",["release"],kind="do"),
  step("build","\"I will build the air to full pressure between 120 and 140 psi.\"",
       ["120","140","full pressure"]),
  step("report_full","\"I am at full pressure, ___ psi.\"",["psi"],
       kind="report", reading={"type":"psi","min":120,"max":140}),
  step("fan_to_100","\"I will fan down to 100 and then stay at idle to check the cut-in.\"",
       ["fan down","100","cut in"]),
  step("cut_in","\"Needle is rising — the cut-in works.\"",["needle is rising","cut in works"]),
  step("rpm","\"I will raise the engine to between 1200 and 1400 rpm.\"",["1200","1400","rpm"]),
  step("build_again","\"I will bring the air pressure up to 120 to 140 psi to check the cut-out.\"",
       ["120","140","cut out"]),
  step("cut_out","\"Needle stopped at ___ psi. Cut-out works.\"",["needle stopped","cut out works"],
       kind="report", reading={"type":"psi","min":120,"max":140}),
  step("set_brakes","Set the brakes.",["set the brakes"],kind="do"),
 ]},

{"id":"air_loss_released","preconditions":['engine_off', 'key_on', 'brakes_released'],"title":"Air Loss Rate — Brakes Released","order":3,
 "image":f"{IMG}/02_incab_brake_check/air_gauges.png","auto_fail":True,
 "steps":[
  step("engine_off","Shut the engine off.",["shut the engine off"],kind="do"),
  step("key_on","Put the key in the ON position.",["key on"],kind="do"),
  step("declare","\"I will release the brakes. After an initial loss of about 5 to 15 pounds, I "
       "cannot lose more than {{leak_released}} pounds in 1 minute.\"",
       ["release the brakes","initial loss","cannot lose more than","one minute"]),
  step("start_psi","\"Starting at ___ psi.\"",["starting at"],
       kind="report", reading={"type":"psi","min":90,"max":140}),
  step("release_do","Release the brakes.",["release"],kind="do"),
  step("initial","\"Initial loss is ___ psi.\"",["initial loss"],
       kind="report", reading={"type":"psi_delta","max":15},
       note="If the initial loss is over 15 lbs, tell the examiner it's too much and ask if you may continue."),
  step("timer","Start timing 60 seconds.",["timing","60 seconds"],
       kind="timer", seconds=60),
  step("result","\"It's been one minute and air pressure is still ___ psi. No air leaks.\"",
       ["one minute","no air leaks"],
       kind="report", reading={"type":"psi_delta","max":"{{leak_released}}"}),
 ]},

{"id":"air_loss_applied","preconditions":['engine_off', 'key_on', 'brake_pedal_applied_90psi'],"title":"Air Loss Rate — Brakes Applied","order":4,
 "image":f"{IMG}/02_incab_brake_check/service_brake_pedal.png","auto_fail":True,
 "steps":[
  step("apply","\"I will put 90 pounds of pressure on the brake pedal.\"",["90 pounds","brake pedal"]),
  step("declare","\"After another initial loss of about 5 to 15 pounds, I cannot lose more than "
       "{{leak_applied}} pounds in 1 minute.\"",
       ["initial loss","cannot lose more than","one minute"]),
  step("start_psi","\"Starting at ___ psi, initial loss was ___ pounds. Starting timing 60 seconds.\"",
       ["starting at","initial loss","timing"],
       kind="report", reading={"type":"psi","min":80,"max":140}),
  step("timer","Time a full 60 seconds.",["60 seconds"],kind="timer",seconds=60),
  step("result","\"It's been one minute and I have no air loss — still ___ psi.\"",
       ["one minute","no air loss"],
       kind="report", reading={"type":"psi_delta","max":"{{leak_applied}}"}),
 ]},

{"id":"low_air_warning","preconditions":['engine_off', 'key_on', 'valves_in'],"title":"Low Air Warning Alarm","order":5,
 "image":f"{IMG}/02_incab_brake_check/low_air_warning.png","auto_fail":True,
 "steps":[
  step("fan","\"I will fan the brakes.\"",["fan the brakes"]),
  step("declare","\"The low air warning alarm must come on at or above 55 psi.\"",
       ["low air warning","55"]),
  step("report","\"It came on at ___ psi.\"",["it came on at"],
       kind="report", reading={"type":"psi","min":55,"max":90}),
  step("confirm","\"My low air warning alarm works.\"",["alarm works"]),
 ]},

{"id":"spring_brakes","preconditions":['engine_off', 'key_on', 'valves_in'],"title":"Spring Brakes","order":6,
 "image":f"{IMG}/02_incab_brake_check/valves_popped_out.png","auto_fail":True,
 "steps":[
  step("continue","\"I will continue fanning the brakes.\"",["continue fanning"]),
  step("declare","\"Between 45 and 20 psi the spring brakes must apply. I will know it because "
       "both buttons will pop out.\"",["45","20","both buttons","pop out"]),
  step("report","\"They came on at ___ psi.\"",["they came on at"],
       kind="report", reading={"type":"psi","min":20,"max":45},
       note="If only one button pops, keep fanning until the second pops too."),
  step("confirm","\"My spring brakes work.\"",["spring brakes work"]),
 ]},

{"id":"rate_of_buildup","preconditions":['engine_on', 'shifter_neutral', 'parking_brakes_set'],"title":"Rate of Air Build-Up","order":7,
 "image":f"{IMG}/02_incab_brake_check/air_gauges.png",
 "steps":[
  step("state","\"Parking brakes are on, shifter in neutral. I will safely start the engine.\"",
       ["parking brakes","neutral","safely start"]),
  step("rebuild","\"Rebuild air maintaining 1500 rpm.\"",["1500","rpm"]),
  step("alarm_check","\"First, I need to make sure the low air warning alarm shuts off at or above "
       "55 psi.\"",["shuts off","55"]),
  step("declare","\"I will time it from 85 to 100 psi, at idle, and it must take 45 seconds or less.\"",
       ["85","100","45 seconds"]),
  step("alarm_off","\"My alarm shut off above 55.\"",["shut off","55"]),
  step("to_idle","\"I am at 75 psi; I will bring it to idle.\"",["75","idle"]),
  step("timing","\"I am at 85 and timing now.\"",["85","timing"],kind="timer",seconds=45),
  step("result","\"I am at 100 psi and it took ___ seconds.\"",["100","it took","seconds"],
       kind="report", reading={"type":"seconds","max":45}),
  step("full","\"Now I will build up to full pressure.\"",["full pressure"]),
  step("secure","\"I will secure my truck and remove the chocks.\" Check brakes are set, put it in "
       "first gear, shut off the engine, take the key, remove the chock blocks and return to the truck.",
       ["secure","remove the chocks","first gear","take the key"]),
 ]},

{"id":"test_brakes","preconditions":['engine_on', 'shifter_neutral', 'full_air_pressure'],"title":"Brake Hold Tests","order":8,
 "image":f"{IMG}/02_incab_brake_check/valves_popped_out.png","auto_fail":True,
 "steps":[
  step("safe_start","\"I am going to safe-start the engine: parking brakes are on, shifter is in "
       "neutral.\"",["parking brakes","neutral"]),
  step("trailer_declare","\"First, I am going to test the trailer parking brake. I will release the "
       "tractor parking brake. In first gear I will let up on the clutch just until it starts to grab.\"",
       ["trailer parking brake","release the tractor","first gear","clutch"],
       variants={
         "manual": "\"First, I am going to test the trailer parking brake. I will release the tractor "
                   "parking brake. In first gear I will let up on the clutch just until it starts to grab.\"",
         "automatic": "\"First, I am going to test the trailer parking brake. I will release the tractor "
                      "parking brake. In drive I will gently apply throttle and try to move forward.\""
       },
       variant_must={
         "manual": ["trailer parking brake","release the tractor","first gear","clutch"],
         "automatic": ["trailer parking brake","release the tractor","drive","try to move"]
       }),
  step("trailer_result","\"Truck did not move — trailer brakes work. Trailer stayed connected and "
       "the fifth wheel is secure.\"",["did not move","trailer brakes work","fifth wheel"]),
  step("tractor_declare","\"Now I will test the tractor parking brake. I will reapply the tractor "
       "brake and release the trailer parking brake. In first gear I will let up on the clutch just "
       "until it starts to grab.\"",["tractor parking brake","reapply","release the trailer","clutch"],
       variants={
         "manual": "\"Now I will test the tractor parking brake. I will reapply the tractor brake and "
                   "release the trailer parking brake. In first gear I will let up on the clutch just "
                   "until it starts to grab.\"",
         "automatic": "\"Now I will test the tractor parking brake. I will reapply the tractor brake and "
                      "release the trailer parking brake. In drive I will gently apply throttle and try "
                      "to move forward.\""
       },
       variant_must={
         "manual": ["tractor parking brake","reapply","release the trailer","clutch"],
         "automatic": ["tractor parking brake","reapply","release the trailer","drive","try to move"]
       }),
  step("tractor_result","\"Truck did not move — tractor brakes work.\"",
       ["did not move","tractor brakes work"]),
  step("rebuild","\"Now I will rebuild the air back to full pressure.\"",["rebuild","full pressure"]),
 ]},

{"id":"trolley_service","preconditions":['engine_on', 'both_brakes_released', 'full_air_pressure'],"title":"Trolley Brake & Service Brake","order":9,
 "image":f"{IMG}/02_incab_brake_check/service_brake_pedal.png",
 "steps":[
  step("trolley_declare","\"Now I am going to test the trolley brake. I will release both parking "
       "brakes, pull forward at 5 miles per hour and pull down on the trolley brake.\"",
       ["trolley brake","release both","5 miles per hour"]),
  step("trolley_result","\"Truck stopped — trolley brake works.\"",["truck stopped","trolley brake works"]),
  step("service_declare","\"Now I am going to test the service brake. I will pull forward at 5 miles "
       "per hour and test the service brake.\"",["service brake","5 miles per hour"]),
  step("service_result","\"Truck stopped — service brake works.\"",["truck stopped","service brake works"]),
  step("quality","No unusual feel to the pedal. No delay in stopping. Truck did not pull left or "
       "right. No chatter to the wheel. No unusual sounds or smells.",
       ["no unusual feel","no delay","did not pull","no chatter","no unusual sounds"]),
  step("secure","Take out of gear. Set the brakes.",["out of gear","set the brakes"],kind="do"),
  step("done","\"That completes my air-brake test!\"",["completes my air brake test"]),
 ]},
]

doc = {
  "schema_version": "1.0.0",
  "content_version": "2026.09.08",
  "id": "air_brake_test",
  "title": "Air Brake Test",
  "subtitle": "Ordered, timed, spoken procedure",
  "publisher": "Fenix Truck School",
  "source_documents": ["AIR BRAKES TEST handout"],
  "auto_fail": True,
  "ordered": True,
  "note": "Order is graded. A step performed out of sequence scores zero even if the words are right.",
  "transmissions": ["manual", "automatic"],
  "transmission_note": "Steps carrying `variants` differ by transmission. The student picks their "
                       "test vehicle once; render variants[transmission] and grade against "
                       "variant_must[transmission]. Steps without `variants` are identical for both.",
  "variables": {
    "leak_released": {"class_a_combination": 3, "class_b_straight": 2,
                      "_note": "CONFIRMED 2026-09-08: the Fenix AIR BRAKES TEST handout governs, for both FL and MA."},
    "leak_applied":  {"class_a_combination": 4, "class_b_straight": 3}
  },
  "precondition_vocabulary": {
    "engine_on": "Engine running",
    "engine_off": "Engine shut off",
    "key_on": "Key in the ON position (electric on)",
    "shifter_neutral": "Shifter in neutral",
    "parking_brakes_set": "Parking brakes set (valves out)",
    "valves_in": "Both air valves pushed IN",
    "brakes_released": "Brakes released",
    "brake_pedal_applied_90psi": "90 lbs of pressure held on the brake pedal",
    "wheels_chocked": "Wheels chocked",
    "full_air_pressure": "Air built to full pressure (120-140 psi)",
    "both_brakes_released": "Both parking and trailer brakes released",
    "_note": "The UI gates each phase on these. Getting the truck state wrong is the most common way students fail this test, so it is a mechanic, not a footnote. See BUILD_SPEC.md #7."
  },
  "phases": PHASES,
}

n_steps = sum(len(p["steps"]) for p in PHASES)
json.dump(doc, open(f"{ROOT}/content/airbrakes.en.json","w"), indent=2, ensure_ascii=False)
print(f"wrote content/airbrakes.en.json — {len(PHASES)} phases, {n_steps} graded steps")
