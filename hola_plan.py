import json, os
FPS = 24
TOTAL = 600
T_HOLA, T_NAME, T_TRAIT, T_ASK, T_BYE = (6, 46, 152, 320, 470)
VOICES = {'pimo': {'pitch': 1.45, 'tempo': 1.12}, 'ruki': {'pitch': 1.15, 'tempo': 1.0}, 'luma': {'pitch': 1.62, 'tempo': 1.15}, 'tuki': {'pitch': 1.5, 'tempo': 1.18}, 'moki': {'pitch': 1.42, 'tempo': 1.0}, 'bopi': {'pitch': 1.3, 'tempo': 1.15, 'robot': True}, 'bolita': {'pitch': 1.58, 'tempo': 1.2}, 'gruno': {'pitch': 0.92, 'tempo': 1.0}}
CHARS = {'pimo': {'name': 'PIMO', 'trait': '¡CURIOSO!', 'gesture': 'wave', 'emote': '?', 'lines': ['¡Hola!', '¡Soy Pimo!', '¡Me encanta preguntar! ¿Por qué? ¿Y por qué?', '¿Y tú? ¿Qué quieres saber hoy?', '¡Hasta pronto!']}, 'ruki': {'name': 'RUKI', 'trait': '¡TRANQUILO!', 'gesture': 'breathe', 'emote': 'bubble', 'lines': ['Hola.', 'Soy Ruki.', 'Cuando me enfado, respiro hondo... ¡así!', '¿Respiras conmigo? Uno... y dos...', '¡Hasta pronto!']}, 'luma': {'name': 'LUMA', 'trait': '¡ALEGRE!', 'gesture': 'wave', 'emote': 'spark', 'lines': ['¡Hola, hola!', '¡Soy Luma!', '¡Cuando sonrío, brillo un montón!', '¿Me enseñas tu sonrisa?', '¡Hasta pronto!']}, 'tuki': {'name': 'TUKI', 'trait': '¡JUGUETÓN!', 'gesture': 'spin', 'emote': '!', 'lines': ['¡Hola!', '¡Soy Tuki!', '¡Me encanta saltar, girar y bailar!', '¿Saltas conmigo? ¡Uno, dos, tres!', '¡Hasta pronto!']}, 'moki': {'name': 'MOKI', 'trait': '¡SOÑADOR!', 'gesture': 'sway', 'emote': 'Z', 'lines': ['Hola...', 'Soy Moki.', 'Soy una nube, y me encanta soñar.', '¿Tú qué sueñas? Yo... ¡con nubes!', '¡Hasta pronto!']}, 'bopi': {'name': 'BOPI', 'trait': '¡ORDENADO!', 'gesture': 'hops', 'emote': '123', 'lines': ['Hola. Bip, bop.', 'Soy Bopi.', 'Me gusta ordenar: uno, dos, tres.', '¿Me ayudas a contar? ¡Uno, dos, tres!', '¡Hasta pronto!']}, 'bolita': {'name': 'BOLITA', 'trait': '¡VALIENTE!', 'gesture': 'bounce', 'emote': '!', 'lines': ['¡Hola!', '¡Soy Bolita!', '¡Soy muy valiente! ¡Yo primero!', 'Pero... ¡mejor juntos! ¿Vienes?', '¡Hasta pronto!']}, 'gruno': {'name': 'DOCTOR GRUÑO', 'trait': '¡INVENTOR!', 'gesture': 'bounce', 'emote': 'poof', 'lines': ['¡Je, je!', '¡Soy el Doctor Gruño!', '¡El inventor más genial del mundo!', 'Mirad mi invento... ¡Ups!', '¡Ya veréis, Pimoruki!']}}
ORDER = ['pimo', 'ruki', 'luma', 'tuki', 'moki', 'bopi', 'bolita', 'gruno']

def current():
    cid = os.environ.get('CHAR')
    p = os.environ.get('SPEC_FILE')
    if not cid and p and os.path.exists(p):
        cid = json.load(open(p)).get('char')
    return cid or 'pimo'
