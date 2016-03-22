SELECT 
  mst.name as name,
  mst.id as messstelle, 
  sts.id as steuerstelle,
  mst.komplex_id as komplex, 
  k.kundennummer as kunde,
  mst.anschrift_plz as mst_plz, 
  mst.anschrift_stadt as mst_stadt, 
  mst.anschrift_strasse as mst_strasse, 
  mst.anschrift_hausnummer as mst_hausnummer, 
  eva.technologie as anlagentyp,
  p.anrede as k_anrede,
  p.nachname as k_nachname,
  p.vorname as k_vorname,
  vnb.name as verteilnetzbetreiber,
  m2k.zpn_kunde as zählpunkt_kunde,
  m2vnb.zpn_wim as zählpunkt_wim,
  mst.hinweise_zugang, 
  mst.zaehler_vorher, 
  mst.msb_vorher, 
  mst.wandler_faktor, 
  mst.spannung_ungewandelt, 
  mst.spannung_gewandelt, 
  mst.strom_ungewandelt,
  mst.strom_gewandelt
FROM 
  dbfrontend_messstelle as mst
LEFT JOIN dbfrontend_steuerstelle as sts ON mst.komplex_id = sts.komplex_id
LEFT JOIN dbfrontend_messstelle2kunde as m2k ON mst.id = m2k.messstelle_id 
LEFT JOIN dbfrontend_kunde as k ON m2k.kunde_id = k.kundennummer
LEFT JOIN dbfrontend_person as p ON k.person_ptr_id = p.id 
LEFT JOIN dbfrontend_eva as eva ON mst.id = eva.messstelle_id 
LEFT JOIN dbfrontend_messstelle2vnb m2vnb ON mst.id = m2vnb.messstelle_id
LEFT JOIN dbfrontend_vnb as vnb ON m2vnb.vnb_id = vnb.id
WHERE
  mst.id in (89, 836)
GROUP BY
  mst.id,
  sts.id,
  k.kundennummer,
  eva.technologie,
  p.anrede,
  p.nachname,
  p.vorname,
  vnb.name,
  m2k.zpn_kunde,
  m2vnb.zpn_wim
ORDER BY
  mst.id,
  sts.id
 
  