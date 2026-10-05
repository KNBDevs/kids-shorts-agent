import hashlib
ACC = "con acento castellano de España (nada latinoamericano), dicción clara y natural, para un dibujo animado infantil"
VOICES = {
    "pimo": ("Puck", "Voz de niño pequeño, curioso y alegre, " + ACC),
    "ruki": ("Umbriel", "Voz de niño tranquilo y sereno, habla pausado y amable, " + ACC),
    "luma": ("Leda", "Voz de niña pequeña muy alegre y risueña, cálida y expresiva, " + ACC),
    "tuki": ("Fenrir", "Voz de niño travieso y lleno de energía, rápido y juguetón, " + ACC),
    "moki": ("Enceladus", "Voz de niño soñador, suave, dulce y algo soñolienta, " + ACC),
    "bopi": ("Iapetus", "Voz de robot pequeño y simpático, precisa, ordenada y algo entrecortada, " + ACC),
    "bolita": ("Zephyr", "Voz de niña valiente, impulsiva y entusiasta, muy enérgica, " + ACC),
    "gruno": ("Algenib", "Voz de villano cómico de dibujos animados, presumido, teatral y pícaro, nunca aterrador, " + ACC),
    "narrador": ("Sulafat", "Voz de narradora adulta, cálida, serena y cercana, ritmo pausado y claro para niños pequeños, " + ACC),
    "nubi": ("Achernar", "Voz de fantasmita de cuento, suave, dulce y alegre, nada tenebrosa, " + ACC),
}
VERSION = "g1"


def digest(cid, text):
    return hashlib.sha1((VERSION + cid + VOICES[cid][0] + VOICES[cid][1] + text).encode()).hexdigest()[:12]


