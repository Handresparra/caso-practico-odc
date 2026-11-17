"""Genera los datos sintéticos del caso práctico del ODC
«Del dato a la toma de decisiones». Semilla fija: los resultados son reproducibles.
Uso: python scripts/generar_datos.py   (escribe los CSV en la carpeta data/)"""
import numpy as np, pandas as pd
from pathlib import Path
rng = np.random.default_rng(2026)
OUT = Path(__file__).resolve().parents[1] / "data"; OUT.mkdir(exist_ok=True)

# ---------- 1. Catálogo de repuestos (kardex) ----------
cat = []
def add(ref, tipo, marca, stock, costo, desc):
    cat.append(dict(repuesto_ref=ref, tipo_repuesto=tipo, marca_compatible=marca,
                    descripcion=desc, stock_promedio=stock, costo_unitario=costo))
pant = [("PAN-01","Samsung",1,"Pantalla AMOLED Galaxy A54"),("PAN-02","Samsung",2,"Pantalla AMOLED Galaxy A34"),
        ("PAN-03","Xiaomi",0,"Pantalla LCD Redmi Note 12"),("PAN-04","Xiaomi",3,"Pantalla LCD Redmi 12C"),
        ("PAN-05","Otras marcas",1,"Pantalla LCD Motorola G54"),("PAN-06","Samsung",11,"Pantalla LCD Galaxy A14"),
        ("PAN-07","Samsung",14,"Pantalla LCD Galaxy A04"),("PAN-08","Xiaomi",12,"Pantalla LCD Redmi A2"),
        ("PAN-09","Otras marcas",9,"Pantalla LCD Motorola E13"),("PAN-10","Otras marcas",16,"Pantalla LCD Tecno Spark 10")]
for ref,m,s,d in pant: add(ref,"Pantalla",m,s,int(rng.integers(120,320))*1000,d)
for i,(m,s) in enumerate([("Samsung",15),("Samsung",8),("Xiaomi",18),("Xiaomi",10),("Xiaomi",12),("Otras marcas",10),("Otras marcas",4)],1):
    add(f"BAT-0{i}","Batería",m,s,int(rng.integers(45,110))*1000,f"Batería {m} tipo {i}")
for i,(m,s) in enumerate([("Samsung",17),("Xiaomi",13),("Xiaomi",5),("Otras marcas",19),("Otras marcas",7)],1):
    add(f"PUE-0{i}","Puerto de carga",m,s,int(rng.integers(25,60))*1000,f"Puerto de carga USB-C {m} tipo {i}")
for i,(m,s) in enumerate([("Samsung",6),("Xiaomi",9),("Otras marcas",3)],1):
    add(f"CAM-0{i}","Cámara",m,s,int(rng.integers(60,150))*1000,f"Módulo de cámara {m} tipo {i}")
for i,(m,s) in enumerate([("Samsung",13),("Xiaomi",8),("Otras marcas",20)],1):
    add(f"ALT-0{i}","Altavoz",m,s,int(rng.integers(20,45))*1000,f"Altavoz {m} tipo {i}")
for i,(m,s) in enumerate([("Samsung",18),("Xiaomi",14),("Otras marcas",15)],1):
    add(f"OTR-0{i}","Otros",m,s,int(rng.integers(15,40))*1000,f"Botón o flex {m} tipo {i}")
inv = pd.DataFrame(cat)
efecto_ref = dict(zip(inv.repuesto_ref, rng.normal(0, 1.1, len(inv))))   # variación propia de cada repuesto

# ---------- 2. Órdenes de servicio ----------
N = 1200
marcas = rng.permutation(np.array(["Samsung"]*504+["Xiaomi"]*372+["Otras marcas"]*324))
mix = {"Samsung":[.45,.20,.15,.10,.05,.05],"Xiaomi":[.25,.40,.17,.08,.05,.05],"Otras marcas":[.34,.24,.16,.09,.09,.08]}
tipos = ["Pantalla","Batería","Puerto de carga","Cámara","Altavoz","Otros"]
modelos = {"Samsung":["Galaxy A54","Galaxy A34","Galaxy A14","Galaxy A04","Galaxy S21"],
           "Xiaomi":["Redmi Note 12","Redmi 12C","Redmi A2","Poco X5"],
           "Otras marcas":["Motorola G54","Motorola E13","Tecno Spark 10","Huawei Y9"]}
tipos_asig = {}
for mm,nn in [("Samsung",504),("Xiaomi",372),("Otras marcas",324)]:
    cnt = np.round(np.array(mix[mm])*nn).astype(int); cnt[0] += nn-cnt.sum()
    tipos_asig[mm] = list(rng.permutation(np.repeat(tipos, cnt)))
rows=[]
for i,m in enumerate(marcas):
    t = tipos_asig[m].pop()
    cand = inv[(inv.tipo_repuesto==t)&(inv.marca_compatible==m)]
    if t=="Pantalla":   # las pantallas de poco stock son las más pedidas
        w = np.where(cand.stock_promedio<=3, 3.2, 1.0); w=w/w.sum()
    else: w = np.ones(len(cand))/len(cand)
    r = cand.sample(1, weights=w, random_state=int(rng.integers(1e9))).iloc[0]
    sede = rng.choice(["Norte","Centro","Sur"], p=[.35,.35,.30])
    dias = 7.2 - 0.33*r.stock_promedio + efecto_ref[r.repuesto_ref] + (1.6 if sede=="Norte" else 0) + rng.normal(0,1.6)
    dias = int(max(1, round(dias)))
    ingreso = pd.Timestamp("2026-01-02") + pd.Timedelta(days=int(rng.integers(0,180)))
    estimado = max(1, int(round(4 + 0.1*rng.normal(0,3))))
    mano = int(rng.integers(40,81))*1000
    calif = int(np.clip(round(5.3 - 0.33*dias + rng.normal(0,0.7)),1,5))
    rows.append(dict(orden_id=1001+i, fecha_ingreso=ingreso.date(), fecha_entrega_estimada=(ingreso+pd.Timedelta(days=estimado)).date(),
        fecha_entrega=(ingreso+pd.Timedelta(days=dias)).date(), sede=sede, marca=m, modelo=rng.choice(modelos[m]),
        tipo_falla=t, repuesto_ref=r.repuesto_ref, costo_total=int(r.costo_unitario+mano), dias_reparacion=dias,
        calificacion=calif, cliente_id=f"C{int(rng.integers(1,951)):04d}"))
ord_ = pd.DataFrame(rows).sort_values("fecha_ingreso").reset_index(drop=True)
limpio = ord_.copy()   # versión sin errores, solo para generar reseñas y notas

# ---------- 3. Reseñas de clientes (350) ----------
TEMAS = {
 "tiempo":   {"pos": ["me entregaron el celular en {d} días, muy rápido", "cumplieron el plazo de entrega a tiempo"],
              "neg": ["tardaron {d} días en entregarme el celular", "mucha demora con el repuesto, {d} días de espera",
                      "esperé {d} días y nadie me daba razón", "se demoraron más de lo prometido en la entrega",
                      "la entrega se retrasó {d} días"]},
 "precio":   {"pos": ["buen precio por el arreglo", "el costo fue justo para el trabajo"],
              "neg": ["me cobraron más de lo que me cotizaron", "el precio del arreglo fue muy alto"]},
 "atencion": {"pos": ["muy amables en la atención", "el técnico me explicó todo el arreglo con paciencia"],
              "neg": ["la atención fue pésima", "nadie contestaba el teléfono del local"]},
 "calidad":  {"pos": ["la pantalla quedó perfecta", "ahora la batería dura todo el día", "el celular quedó como nuevo"],
              "neg": ["el celular volvió con la cámara rayada", "el equipo volvió a fallar a la semana"]}}
NEU = ["Dejé el celular el lunes y lo recogí el miércoles.", "Cambio de {t} en {m}.", "¿Hasta qué hora atienden los sábados?",
       "Recibí el equipo con la factura.", "Fue un cambio de {t}."]
cap = lambda x: x[0].upper() + x[1:]
idx = rng.choice(len(limpio), 350, replace=False)
res=[]
for k,j in enumerate(sorted(idx)):
    o = limpio.iloc[j]; d=o.dias_reparacion; largo = d>=7
    p = [.15,.42,.35,.08] if largo else [.53,.21,.14,.12]   # positiva, negativa, mixta, neutra
    pol = rng.choice(["Positiva","Negativa","Mixta","Neutra"], p=p)
    otros = ["precio","atencion","calidad"]
    tema_neg = "tiempo" if (largo and rng.random()<(.97 if o.tipo_falla=="Pantalla" else .4)) else rng.choice(otros)
    tema_pos = rng.choice([t for t in TEMAS if t!=tema_neg and (t!="tiempo" or not largo)])
    if not largo and pol=="Positiva" and rng.random()<.25: tema_pos="tiempo"
    neg = rng.choice(TEMAS[tema_neg]["neg"]).format(d=d); pos = rng.choice(TEMAS[tema_pos]["pos"]).format(d=d)
    if pol=="Positiva": txt = cap(pos)+"."
    elif pol=="Negativa": txt = cap(neg)+"."
    elif pol=="Mixta": txt = cap(pos)+(", pero " if rng.random()<.7 else ", aunque ")+neg+"."
    else: txt = rng.choice(NEU).format(t=o.tipo_falla.lower(), m=o.marca)
    res.append(dict(resena_id=f"R{k+1:03d}", orden_id=o.orden_id, fecha_resena=(pd.Timestamp(o.fecha_entrega)+pd.Timedelta(days=int(rng.integers(0,4)))).date(),
                    texto=txt, calificacion=o.calificacion if rng.random()<.9 else None, polaridad_etiquetada=pol if k<120 else None))
resenas = pd.DataFrame(res)
# Una persona etiquetó 120 reseñas; como en la vida real, en algunos casos dudosos su criterio difiere
vecina = {"Mixta":"Negativa","Negativa":"Mixta","Positiva":"Neutra","Neutra":"Positiva"}
cambia = rng.choice(120, 9, replace=False)
resenas.loc[cambia,"polaridad_etiquetada"] = resenas.loc[cambia,"polaridad_etiquetada"].map(vecina)

# ---------- 4. Notas de los técnicos ----------
notas=[]
for _,o in limpio.iterrows():
    st = inv.set_index("repuesto_ref").stock_promedio[o.repuesto_ref]
    base = f"Diagnóstico: falla de {o.tipo_falla.lower()}. Se usa repuesto {o.repuesto_ref}."
    if st<=3 and rng.random()<.8: base += " Sin stock en bodega, se pide al proveedor."
    elif rng.random()<.15: base += " Cliente pide revisión adicional."
    notas.append(dict(orden_id=o.orden_id, nota_tecnico=base))
notas = pd.DataFrame(notas)

# ---------- 5. Problemas de calidad intencionales (para el paso 3) ----------
sucio = ord_.copy()
m = rng.random(N)<.05; sucio.loc[m,"marca"] = sucio.loc[m,"marca"].map(lambda x: rng.choice([x.upper(), x.lower()]))
sucio.loc[rng.random(N)<.18,"modelo"] = np.nan
sucio.loc[rng.random(N)<.03,"fecha_entrega"] = np.nan
e = rng.random(N)<.01; sucio.loc[e,"costo_total"] = sucio.loc[e,"costo_total"]*10
sucio = pd.concat([sucio, sucio.sample(12, random_state=1)]).sort_values("fecha_ingreso").reset_index(drop=True)

sucio.to_csv(OUT/"ordenes.csv", index=False)
inv.to_csv(OUT/"inventario.csv", index=False)
resenas.to_csv(OUT/"resenas.csv", index=False)
notas.to_csv(OUT/"notas_tecnicos.csv", index=False)
print("órdenes:",len(sucio),"· reseñas:",len(resenas),"· repuestos:",len(inv),"· notas:",len(notas))
