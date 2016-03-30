SELECT 
  mst.name,
  mst.id, 
  mst.komplex_id, 
  k.kundennummer,
  mst.anschrift_plz, 
  mst.anschrift_stadt, 
  mst.anschrift_strasse, 
  mst.anschrift_hausnummer, 
  eva.technologie,
  p.anrede,
  p.nachname,
  p.vorname,
  vnb.name,
  zp.zpn,
  mst.hinweise_zugang, 
  mst.zaehler_vorher, 
  mst.msb_vorher, 
  mst.wandler_faktor, 
  mst.spannung_ungewandelt, 
  mst.spannung_gewandelt, 
  mst.strom_ungewandelt,
  mst.strom_gewandelt
FROM 
  dbfrontend_messstelle as mst, 
  dbfrontend_kunde as k, 
  dbfrontend_steuerstelle as sts,
  dbfrontend_eva as eva,
  dbfrontend_person as p,
  dbfrontend_vnb as vnb,
  dbfrontend_extrazpn as zp,
  dbfrontend_messstelle2kunde as m2k,
  dbfrontend_messstelle2vnb as m2vnb
JOIN k   ON k.person_ptr_id = p.id
JOIN m2k ON m2k.kunde_id = k.kundennummer
JOIN mst ON mst.id = m2k.messstelle_id
JOIN mst ON eva.messstelle_id = mst.id
JOIN m2vnb ON m2vnb.vnb_id = vnb.id
JOIN mst ON mst.id = m2vnb.messstelle_id
JOIN mst ON mst.id = zp.messstelle_id
WHERE
  mst.id in (831,836)
  