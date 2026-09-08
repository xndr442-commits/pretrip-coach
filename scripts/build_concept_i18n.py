#!/usr/bin/env python3
"""Author ES/PT accept-lists for every item-specific concept.

The shared defect vocabulary (secure, no_cracks, ...) covers 48% of concept slots
and lives in build_i18n.py. This file covers the other 136 — the item-specific ones
— so the OFFLINE keyword grader works in all three languages, not just English.

Keys are "<item_id>.<concept_id>" because concept ids are only unique within an
item ("both" means both valves, both horns, or both beams depending where you are).

Output: content/i18n/concepts.es.json and concepts.pt.json
"""
import json, os

ROOT = os.path.expanduser("~/Projects/PreTripCoach")

# "item.concept": (spanish phrases, portuguese phrases)
C = {
# ── in-cab / engine start ───────────────────────────────────────────────────
"seat_belt.no_cuts": (["sin cortes","sin deshilachado","no está roto","sin rasgaduras"],
                      ["sem cortes","sem desfiar","não está rasgado","sem rasgos"]),
"seat_belt.latches": (["abrocha","cierra","engancha","suelta correctamente","abre y cierra"],
                      ["trava","fecha","engata","solta corretamente","abre e fecha"]),
"valves_up.both_valves": (["amarilla","freno de estacionamiento","roja","suministro de aire del remolque"],
                          ["amarela","freio de estacionamento","vermelha","suprimento de ar do reboque"]),
"valves_up.up_position": (["posición hacia arriba","afuera","activadas","puestas","hacia arriba"],
                          ["posição para cima","puxadas","acionadas","para fora"]),
"gearshift_neutral.neutral": (["neutral","en neutral","punto muerto"],
                              ["ponto morto","em ponto morto","neutro"]),
"safe_start.brakes_set": (["frenos puestos","freno de estacionamiento","válvulas arriba","frenos aplicados"],
                          ["freios acionados","freio de estacionamento","válvulas para cima","freios aplicados"]),
"safe_start.neutral": (["neutral","en neutral","punto muerto"], ["ponto morto","em ponto morto","neutro"]),
"safe_start.abs_def": (["abs","def","las luces se encienden","se apagan","luces de advertencia"],
                       ["abs","def","as luzes acendem","apagam","luzes de advertência"]),
"safe_start.start": (["arranco el motor","enciendo el motor","prendo el motor"],
                     ["dou partida","ligo o motor","arranco o motor"]),

# ── air brake check ─────────────────────────────────────────────────────────
"air_compressor_governor.range": (["120","140","ciento veinte","ciento cuarenta","presión completa"],
                                  ["120","140","cento e vinte","cento e quarenta","pressão total"]),
"air_compressor_governor.governor": (["gobernador","corte","corta"], ["governador","corte","corta"]),
"air_compressor_governor.reading": (["psi","libras","la presión es"], ["psi","libras","a pressão é"]),
"air_compressor_governor.air_release": (["liberación de aire","escucho el aire","escape de aire","suelta el aire"],
                                        ["liberação de ar","escuto o ar","escape de ar","solta o ar"]),
"air_leak_test.engine_off": (["motor apagado","llave encendida","apago el motor"],
                             ["motor desligado","chave ligada","desligo o motor"]),
"air_leak_test.valves_in": (["válvulas adentro","empujo las válvulas","hacia adentro"],
                            ["válvulas para dentro","empurro as válvulas","para dentro"]),
"air_leak_test.hold_pedal": (["piso el freno","mantengo el pedal","sostengo el freno","90 libras"],
                             ["piso o freio","seguro o pedal","mantenho o freio","90 libras"]),
"air_leak_test.one_minute": (["un minuto","60 segundos","sesenta segundos","cronómetro"],
                             ["um minuto","60 segundos","sessenta segundos","cronômetro"]),
"air_leak_test.limit": (["no puedo perder más de","psi en un minuto","máximo"],
                        ["não posso perder mais de","psi em um minuto","máximo"]),
"air_leak_test.result": (["no perdí","sin fugas","todavía","solo perdí"],
                         ["não perdi","sem vazamentos","ainda","perdi apenas"]),
"low_air_warning.fan": (["bombeo","bombear","abanico","pisar y soltar"],
                        ["bombeio","bombear","abano","pisar e soltar"]),
"low_air_warning.threshold": (["55","cincuenta y cinco","a 55 o más"], ["55","cinquenta e cinco","a 55 ou mais"]),
"low_air_warning.both": (["luz","zumbador","alarma","sonido"], ["luz","campainha","alarme","som"]),
"low_air_warning.reading": (["se encendió en","psi"], ["acendeu em","psi"]),
"spring_brakes_popout.range": (["45","20","cuarenta y cinco","veinte"], ["45","20","quarenta e cinco","vinte"]),
"spring_brakes_popout.both_pop": (["las dos","ambas","saltan","saltaron","botones"],
                                  ["as duas","ambas","saltam","saltaram","botões"]),
"spring_brakes_popout.no_pull": (["no jalo","no tiro","solas","por sí solas","no las jalo"],
                                 ["não puxo","sozinhas","por si só","não puxei"]),
"spring_brakes_popout.reading": (["saltaron en","psi"], ["saltaram em","psi"]),
"rate_of_buildup.rpm": (["1500","mil quinientas","rpm","revoluciones"], ["1500","mil e quinhentas","rpm","rotações"]),
"rate_of_buildup.alarm_off": (["se apaga","apagó","55","cincuenta y cinco"], ["desliga","desligou","55","cinquenta e cinco"]),
"rate_of_buildup.window": (["85","100","ochenta y cinco","cien"], ["85","100","oitenta e cinco","cem"]),
"rate_of_buildup.limit": (["45 segundos","cuarenta y cinco segundos","o menos"],
                          ["45 segundos","quarenta e cinco segundos","ou menos"]),
"rate_of_buildup.reading": (["tomó","segundos"], ["levou","segundos"]),
"parking_brake_check.red_in": (["válvula roja","empujo la roja","freno del remolque"],
                               ["válvula vermelha","empurro a vermelha","freio do reboque"]),
"parking_brake_check.in_gear": (["en marcha","primera","trato de mover","suelto el clutch","en drive"],
                                ["engatado","primeira","tento mover","solto a embreagem","em drive"]),
"parking_brake_check.result": (["no se mueve","no se movió","sostiene","aguanta"],
                               ["não se move","não se moveu","segura","aguenta"]),
"trailer_brake_check.yellow_in": (["válvula amarilla","empujo la amarilla","freno de estacionamiento"],
                                  ["válvula amarela","empurro a amarela","freio de estacionamento"]),
"trailer_brake_check.red_out": (["roja afuera","dejo la roja","suministro de aire afuera"],
                                ["vermelha puxada","deixo a vermelha","suprimento de ar para fora"]),
"trailer_brake_check.in_gear": (["en marcha","primera","trato de mover","suelto el clutch","en drive"],
                                ["engatado","primeira","tento mover","solto a embreagem","em drive"]),
"trailer_brake_check.result": (["no se mueve","no se movió","frenos del remolque funcionan","quinta rueda segura"],
                               ["não se move","não se moveu","freios do reboque funcionam","quinta roda segura"]),
"service_brake_check.both_in": (["ambas válvulas adentro","las dos adentro","suelto los dos frenos"],
                                ["ambas as válvulas para dentro","as duas para dentro","solto os dois freios"]),
"service_brake_check.speed": (["5","10","cinco","diez","millas por hora"],
                              ["5","10","cinco","dez","milhas por hora"]),
"service_brake_check.apply": (["aplico el freno de servicio","piso el freno","freno de servicio"],
                              ["aplico o freio de serviço","piso o freio","freio de serviço"]),
"service_brake_check.no_pull": (["no jala","no me jala","frena derecho","izquierda ni derecha"],
                                ["não puxa","para reto","esquerda nem direita"]),
"service_brake_check.feel": (["sin demora","sin vibración","sin ruidos","normal"],
                             ["sem demora","sem trepidação","sem ruídos","normal"]),

# ── indicators & emergency equipment ────────────────────────────────────────
"light_indicators.high_beam": (["azul","luz alta","altas"], ["azul","farol alto","alto"]),
"light_indicators.turn": (["flecha verde","direccional","izquierda","derecha","intermitente"],
                          ["seta verde","seta","esquerda","direita","pisca"]),
"light_indicators.four_way": (["cuatro vías","intermitentes","emergencia","las dos flechas"],
                              ["quatro vias","pisca-alerta","emergência","as duas setas"]),
"fire_extinguisher.charged": (["cargado","lleno","en el verde","el manómetro"],
                              ["carregado","cheio","no verde","o manômetro"]),
"fire_extinguisher.current": (["vigente","no vencido","al día","fecha"], ["dentro da validade","não vencido","em dia","data"]),
"fire_extinguisher.pin": (["pin","seguro","precinto"], ["pino","lacre","trava"]),
"triangles.three": (["tres","3","tres piezas"], ["três","3","três peças"]),
"triangles.no_damage": (["sin daños","no dañados","no rotos"], ["sem danos","não danificados","não quebrados"]),
"spare_fuses.present": (["fusibles de repuesto","fusibles extra","caja de fusibles","relés"],
                        ["fusíveis reserva","fusíveis extra","caixa de fusíveis","relés"]),
"spare_fuses.count": (["seis","6","al menos seis"], ["seis","6","pelo menos seis"]),

# ── visibility & controls ───────────────────────────────────────────────────
"windshield.no_stickers": (["sin calcomanías","sin calcomanías ilegales","sin pegatinas"],
                           ["sem adesivos","sem adesivos ilegais","sem etiquetas"]),
"windshield.view": (["nada bloquea","visión clara","nada obstruye"], ["nada bloqueia","visão limpa","nada obstrui"]),
"mirrors.adjusted": (["ajustados a mí","ajustados","acomodados"], ["ajustados para mim","ajustados","regulados"]),
"mirrors.view": (["nada bloquea","visión clara"], ["nada bloqueia","visão limpa"]),
"wipers.blades": (["plumillas","sin cortes","sin grietas","hules"], ["palhetas","sem cortes","sem rachaduras","borrachas"]),
"wipers.contact": (["parejo","hacen contacto","pegados al parabrisas","al ras"],
                   ["uniforme","fazem contato","encostados no para-brisa","rente"]),
"washer_fluid.present": (["hay líquido","tiene líquido","lleno","presente"],
                         ["tem fluido","tem líquido","cheio","presente"]),
"heater_defroster.both": (["calefacción","desempañador","los dos"], ["aquecedor","desembaçador","os dois"]),
"horns.both": (["bocina de ciudad","bocina de aire","las dos bocinas","claxon"],
               ["buzina de cidade","buzina de ar","as duas buzinas"]),

# ── front / engine area ─────────────────────────────────────────────────────
"truck_leveled.level": (["nivelado","parejo","derecho"], ["nivelado","reto","alinhado"]),
"truck_leveled.no_puddles": (["sin fugas","sin aceite","sin grasa","sin refrigerante","nada en el piso"],
                             ["sem vazamentos","sem óleo","sem graxa","sem arrefecimento","nada no chão"]),
"headlights.both_beams": (["luz alta","luz baja","las dos luces"], ["farol alto","farol baixo","os dois faróis"]),
"coolant.level": (["nivel correcto","nivel adecuado","lleno","en la marca"],
                  ["nível correto","nível adequado","cheio","na marca"]),
"coolant.how": (["visor","varilla","depósito","mirilla"], ["visor","vareta","reservatório"]),
"coolant.hoses": (["mangueras","sin cortes","sin rajaduras","ambos extremos"],
                  ["mangueiras","sem cortes","sem rasgos","as duas pontas"]),
"oil.dipstick": (["varilla","bayoneta"], ["vareta"]),
"oil.level": (["nivel correcto","lleno","entre las marcas"], ["nível correto","cheio","entre as marcas"]),
"power_steering.level": (["nivel correcto","nivel adecuado","lleno"], ["nível correto","nível adequado","cheio"]),
"power_steering.how": (["visor","varilla","depósito","mirilla"], ["visor","vareta","reservatório"]),
"power_steering.hoses": (["mangueras","sin cortes","sin rajaduras","ambos extremos"],
                         ["mangueiras","sem cortes","sem rasgos","as duas pontas"]),
"fluid_air_leaks.under": (["debajo","por abajo","abajo del motor"], ["embaixo","por baixo","embaixo do motor"]),
"fluid_air_leaks.hoses": (["mangueras","sin cortes","sin burbujas","sin fugas"],
                          ["mangueiras","sem cortes","sem bolhas","sem vazamentos"]),
"pitman_arm.cotter": (["tuerca de castillo","chaveta","chavetas","pasador"],
                      ["porca castelo","cupilha","cupilhas","contrapino"]),
"drag_link.bushings": (["bujes","hules","goma","sin cortes"], ["buchas","borracha","sem cortes"]),
"tie_rod.cotter": (["tuerca de castillo","chaveta","chavetas","pasador"],
                   ["porca castelo","cupilha","cupilhas","contrapino"]),

# ── steering axle ───────────────────────────────────────────────────────────
"front_tire.even_wear": (["desgaste parejo","desgaste uniforme","gastada pareja"],
                         ["desgaste uniforme","desgaste parelho","gasto uniforme"]),
"front_tire.tread": (["cuatro treintaidosavos","4/32","dibujo","profundidad"],
                     ["quatro trinta e dois avos","4/32","sulco","profundidade"]),
"front_tire.no_damage": (["sin cortes","sin abultamientos","sin burbujas","sin daños"],
                         ["sem cortes","sem bolhas","sem estufamentos","sem danos"]),
"front_tire.no_leak": (["sin fugas de aire","no pierde aire"], ["sem vazamento de ar","não perde ar"]),
"front_tire.no_recap": (["sin recauchutado","sin recapado","no recauchutada"],
                        ["sem recapagem","sem recauchutagem","não recapado"]),
"front_tire.pressure": (["100 psi","bien inflada","presión correcta","cien libras"],
                        ["100 psi","bem calibrado","pressão correta","cem libras"]),
"rims.no_holes": (["sin agujeros ilegales","sin perforaciones","sin huecos"],
                  ["sem furos ilegais","sem perfurações","sem buracos"]),
"lug_nuts.all_present": (["todas presentes","no falta ninguna","completas"],
                         ["todas presentes","não falta nenhuma","completas"]),
"lug_nuts.rust": (["sin óxido","óxido","herrumbre","marcas de óxido","sin corrosión"],
                  ["sem ferrugem","ferrugem","marcas de ferrugem","sem corrosão"]),
"leaf_springs.not_shifted": (["no desplazadas","sin cruzarse","alineadas","no corridas"],
                             ["não deslocadas","sem cruzar","alinhadas","no lugar"]),
"shock_absorber.bushings": (["bujes","hules","goma","no desgastados"], ["buchas","borracha","não gastas"]),
"brake_hose.fittings": (["conexiones","ambos extremos","acoples"], ["conexões","as duas pontas","engates"]),
"brake_hose.no_rot": (["sin resequedad","no reseca","sin desgaste","no cuarteada"],
                      ["sem ressecamento","não ressecada","sem desgaste","não rachada"]),
"air_chamber.clamps": (["abrazaderas","no faltan","apretadas"], ["abraçadeiras","não faltam","apertadas"]),
"brake_contaminants.drum": (["tambor","sin grietas","no agrietado"], ["tambor","sem rachaduras","não rachado"]),
"brake_contaminants.lining": (["un cuarto de pulgada","1/4","balata","grosor"],
                              ["um quarto de polegada","1/4","lona","espessura"]),
"brake_contaminants.contaminants": (["sin aceite","sin grasa","sin residuos","sin contaminantes"],
                                    ["sem óleo","sem graxa","sem detritos","sem contaminantes"]),

# ── side of vehicle ─────────────────────────────────────────────────────────
"turn_signal_side.reflectors": (["ámbar","rojo","adelante","atrás","reflectores"],
                                ["âmbar","vermelho","na frente","atrás","refletores"]),
"mirrors_side.view": (["nada bloquea","visión clara","sin calcomanías"],
                      ["nada bloqueia","visão limpa","sem adesivos"]),
"fuel_tank.cap": (["la tapa","tapa presente","tapa apretada"], ["a tampa","tampa presente","tampa apertada"]),
"fuel_tank.straps": (["correas","abrazaderas","cinchos"], ["cintas","abraçadeiras","tiras"]),
"def_tank.cap": (["la tapa","tapa presente","tapa apretada"], ["a tampa","tampa presente","tampa apertada"]),
"battery.welds": (["soldaduras rotas","sin soldaduras rotas"], ["soldas quebradas","sem soldas quebradas"]),
"battery.connectors": (["conectores","terminales","bornes","asegurados"],
                       ["conectores","terminais","bornes","presos"]),
"battery.cables": (["cables","no expuestos","sin corrosión","no corroídos","no rotos"],
                   ["cabos","não expostos","sem corrosão","não corroídos","não rompidos"]),
"frame.rust": (["sin óxido","no oxidado","sin corrosión"], ["sem ferrugem","não enferrujado","sem corrosão"]),

# ── combination ─────────────────────────────────────────────────────────────
"electrical_line.flexible": (["flexible","no roza","no toca","no talla"],
                             ["flexível","não roça","não toca","não atrita"]),
"electrical_line.no_exposed": (["sin cables expuestos","sin cinta ilegal","no pelado"],
                               ["sem fios expostos","sem fita ilegal","não descascado"]),
"electrical_line.pins": (["siete pines","7 pines","los siete","no doblados"],
                         ["sete pinos","7 pinos","os sete","não tortos"]),
"air_lines.colors": (["azul","roja","línea de servicio","línea de emergencia"],
                     ["azul","vermelha","linha de serviço","linha de emergência"]),
"air_lines.flexible": (["flexible","no roza","no toca"], ["flexível","não roça","não toca"]),
"air_lines.no_damage": (["sin cortes","sin burbujas","sin fugas"], ["sem cortes","sem bolhas","sem vazamentos"]),
"air_lines.gladhands": (["glad hands","sellos","hules","no desgastados","acoples"],
                        ["glad hands","vedações","borrachas","não gastas","engates"]),
"fifth_wheel_skid.no_gap": (["sin espacio","sin separación","no hay luz","pegados"],
                            ["sem espaço","sem folga","não há vão","encostados"]),
"king_pin.apron": (["delantal","bien montado al remolque","apron"],
                   ["avental","bem montado ao reboque","apron"]),
"locking_jaws.locked": (["cerrada","posición cerrada","todo alrededor","engranada","trabada"],
                        ["travada","posição travada","toda a volta","engatada"]),
"locking_pins.pins": (["pines presentes","engranados","posición cerrada"],
                      ["pinos presentes","engatados","posição travada"]),
"locking_pins.handle": (["manija","palanca","no rota","hasta el fondo","cerrada"],
                        ["alavanca","manete","não quebrada","até o fim","travada"]),
"locking_pins.pivot": (["pernos pivote","pivotes","sin grietas","no rotos"],
                       ["pinos pivô","pivôs","sem rachaduras","não quebrados"]),

# ── trailer ─────────────────────────────────────────────────────────────────
"landing_gear.raised": (["levantadas","arriba","recogidas","subidas"],
                        ["levantados","para cima","recolhidos","subidos"]),
"landing_gear.handle": (["manivela","manija","presente","guardada"],
                        ["manivela","presente","guardada"]),
"dot_tape.present": (["presente","bien pegada","adherida"], ["presente","bem colada","aderida"]),
"dot_tape.coverage": (["cincuenta por ciento","50","la mitad"], ["cinquenta por cento","50","a metade"]),
"dot_tape.color": (["roja","blanca","clara"], ["vermelha","branca","clara"]),
"rear_lenses.functions": (["direccional","freno","emergencia","marcador","reflector"],
                          ["seta","freio","emergência","marcador","refletor"]),

# ── procedures ──────────────────────────────────────────────────────────────
"rr_procedure.flashers_on": (["200 pies","doscientos pies","intermitentes"],
                             ["200 pés","duzentos pés","pisca-alerta"]),
"rr_procedure.stop_distance": (["15","50","quince","cincuenta","pies"],
                               ["15","50","quinze","cinquenta","pés"]),
"rr_procedure.window": (["ventana","bajo la ventana","escucho","miro"],
                        ["janela","abaixo a janela","escuto","olho"]),
"rr_procedure.clear": (["espacio","lugar","librar las vías","del otro lado"],
                       ["espaço","lugar","liberar os trilhos","do outro lado"]),
"rr_procedure.no_shift": (["sin cambiar de marcha","no hago cambios","sin cambiar velocidad"],
                          ["sem trocar de marcha","não troco marcha","sem mudar a marcha"]),
"rr_procedure.flashers_off": (["apago los intermitentes","intermitentes apagados"],
                              ["desligo o pisca-alerta","pisca-alerta desligado"]),
"emergency_procedure.pull_over": (["me orillo","a la orilla","fuera del camino","acotamiento"],
                                  ["encosto","no acostamento","fora da pista"]),
"emergency_procedure.valves_up": (["válvulas arriba","pongo los frenos","freno de estacionamiento"],
                                  ["válvulas para cima","aciono os freios","freio de estacionamento"]),
"emergency_procedure.neutral": (["neutral","punto muerto"], ["ponto morto","neutro"]),
"emergency_procedure.flashers": (["cuatro vías","intermitentes","emergencia"],
                                 ["quatro vias","pisca-alerta","emergência"]),
"emergency_procedure.triangles": (["tres triángulos","triángulos reflectantes","dispositivos de advertencia"],
                                  ["três triângulos","triângulos refletores","dispositivos de advertência"]),
"emergency_procedure.traffic": (["reviso el tráfico","checo el tráfico","miro el tráfico"],
                                ["verifico o tráfego","olho o tráfego","checo o tráfego"]),
}

def main():
    master = json.load(open(f"{ROOT}/content/pretrip.en.json"))
    shared = {"secure","no_cracks","not_broken","no_leaks","no_illegal_welds",
              "clean","proper_color","hardware","greased","operational"}

    needed = []
    for s in master["sections"]:
        for it in s.get("items", []):
            for c in it["concepts"]:
                if c["id"] not in shared:
                    needed.append(f"{it['id']}.{c['id']}")

    missing = [k for k in needed if k not in C]
    extra   = [k for k in C if k not in needed]

    for lang, idx in (("es", 0), ("pt", 1)):
        doc = {"language": lang, "schema_version": "1.0.0",
               "for_content_version": master["content_version"],
               "note": "Accept-lists for item-specific concepts, keyed '<item_id>.<concept_id>'. "
                       "Shared defect vocabulary lives in i18n/<lang>.json -> defect_vocabulary. "
                       "Used by the OFFLINE keyword grader; the AI grader works semantically and "
                       "does not need these.",
               "concepts": {k: v[idx] for k, v in C.items() if k in needed}}
        json.dump(doc, open(f"{ROOT}/content/i18n/concepts.{lang}.json", "w"),
                  indent=2, ensure_ascii=False)

    print(f"item-specific concept slots : {len(needed)}")
    print(f"authored in ES and PT       : {len([k for k in needed if k in C])}")
    if missing: print(f"MISSING ({len(missing)}): {missing}")
    if extra:   print(f"unused keys ({len(extra)}): {extra}")
    if not missing: print("coverage: 100%")

if __name__ == "__main__":
    main()
