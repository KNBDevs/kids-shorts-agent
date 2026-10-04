import json, os
FPS = 24
TOTAL = 600
T_HOLA, T_NAME, T_TRAIT, T_ASK, T_BYE = (6, 46, 152, 320, 470)
VOICES = {'pimo': {'pitch': 1.45, 'tempo': 1.12}, 'ruki': {'pitch': 1.15, 'tempo': 1.0}, 'luma': {'pitch': 1.62, 'tempo': 1.15}, 'tuki': {'pitch': 1.5, 'tempo': 1.18}, 'moki': {'pitch': 1.42, 'tempo': 1.0}, 'bopi': {'pitch': 1.3, 'tempo': 1.15, 'robot': True}, 'bolita': {'pitch': 1.58, 'tempo': 1.2}, 'gruno': {'pitch': 0.92, 'tempo': 1.0}}
CHARS = {'pimo': {'name': 'PIMO', 'trait': '¡CURIOSO!', 'gesture': 'wave', 'emote': '?', 'lines': ['¡Holaaa!', '¡Soy Pimo! ¡Encantado!', '¿Sabes qué me encanta? ¡Preguntar! ¿Por qué? ¿Y por qué?', 'Y tú, ¿qué te gustaría descubrir hoy?', '¡Hasta prontito!']}, 'ruki': {'name': 'RUKI', 'trait': '¡TRANQUILO!', 'gesture': 'breathe', 'emote': 'bubble', 'lines': ['Hola, hola...', 'Yo soy Ruki.', 'Cuando me enfado... respiro hondo. Mmm... ¡y ya está!', '¿Lo probamos juntos? Coge aire... y suéltalo.', 'Hasta pronto, amigo.']}, 'luma': {'name': 'LUMA', 'trait': '¡ALEGRE!', 'gesture': 'wave', 'emote': 'spark', 'lines': ['¡Holiii!', '¡Soy Luma, encantada!', 'Cuando sonrío... ¡brillo muchísimo! ¿Lo ves?', '¿Me enseñas tu sonrisa? ¡Oooh, qué bonita!', '¡Chao, chao!']}, 'tuki': {'name': 'TUKI', 'trait': '¡JUGUETÓN!', 'gesture': 'spin', 'emote': '!', 'lines': ['¡Eh, hola!', '¡Soy Tuki!', '¡A mí me encanta saltar, girar y bailar! ¡Yujuuu!', '¿Saltas conmigo? ¡Una, dos y tres!', '¡Hasta luego!']}, 'moki': {'name': 'MOKI', 'trait': '¡SOÑADOR!', 'gesture': 'sway', 'emote': 'Z', 'lines': ['Hola...', 'Soy Moki... una nube.', 'Me encanta flotar... y soñar despierto.', '¿Y tú qué sueñas? Yo... con estrellas.', 'Dulces sueños...']}, 'bopi': {'name': 'BOPI', 'trait': '¡ORDENADO!', 'gesture': 'hops', 'emote': '123', 'lines': ['Hola. ¡Bip, bop!', 'Soy Bopi, el robot.', 'Me gusta tenerlo todo ordenado. ¡Uno, dos y tres!', '¿Me ayudas a contar? Uno, dos, tres... ¡Perfecto!', 'Bopi se despide. ¡Bip!']}, 'bolita': {'name': 'BOLITA', 'trait': '¡VALIENTE!', 'gesture': 'bounce', 'emote': '!', 'lines': ['¡Hola, hola, hola!', '¡Soy Bolita!', '¡Soy muy valiente! ¡Yo primero, yo primero!', 'Bueno... mejor todos juntos. ¿Te vienes?', '¡Hasta la próxima!']}, 'gruno': {'name': 'DOCTOR GRUÑO', 'trait': '¡INVENTOR!', 'gesture': 'bounce', 'emote': 'poof', 'lines': ['Je, je, je...', '¡Soy el Doctor Gruño!', '¡El inventor más genial del mundo mundial!', 'Mirad mi nuevo invento... ¡Ay! ¡Ups!', '¡Ya veréis, Pimoruki! ¡Ya veréis!']}}
ORDER = ['pimo', 'ruki', 'luma', 'tuki', 'moki', 'bopi', 'bolita', 'gruno']

def current():
    cid = os.environ.get('CHAR')
    p = os.environ.get('SPEC_FILE')
    if not cid and p and os.path.exists(p):
        cid = json.load(open(p)).get('char')
    return cid or 'pimo'
