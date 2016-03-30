SELECT 
  mst.name,
  mst.id, 
  mst.komplex_id, 
  p.kundennummer,
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
  dbfrontend_messstelle,
  dbfrontend_person
FULL JOIN dbfrontend_kunde ON dbfrontend_kunde.person_ptr_id = dbfrontend_person.id 
FULL JOIN dbfrontend_messstelle2kunde ON dbfrontend_messstelle2kunde.kunde_id = dbfrontend_kunde.kundennummer
FULL JOIN dbfrontend_messstelle ON dbfrontend_messstelle.id = dbfrontend_messstelle2kunde.messstelle_id 
FULL JOIN dbfrontend_messstelle ON dbfrontend_eva.messstelle_id = mst.id 
FULL JOIN dbfrontend_messstelle2vnb ON dbfrontend_messstelle2vnb.vnb_id = vnb.id 
FULL JOIN dbfrontend_messstelle ON dbfrontend_messstelle.id = dbfrontend_messstelle2vnb.messstelle_id 
FULL JOIN dbfrontend_messstelle ON dbfrontend_messstelle.id = dbfrontend_extrazpn.messstelle_id 
WHERE
  mst.id in (831,836)
  