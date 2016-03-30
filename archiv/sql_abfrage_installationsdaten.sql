SELECT 
  mst.name,
  mst.id, 
  sts.id,
  mst.komplex_id, 
  k.kundennummer
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
  mst.strom_gewandelt, 
 
  
  
  
   

FROM 
  dbfrontend_messstelle as mst, 
  dbfrontend_kunde as k, 
  dbfrontend_messstelle2kunde as m2k,
  dbfrontend_steuerstelle as sts
  dbfrontend_eva as eva
  dbfrontend_person as p
  dbfrontend_vnb as vnb
  dbfrontend_extrazpn as zp

WHERE
  