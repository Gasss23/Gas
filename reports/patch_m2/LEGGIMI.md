# Copie di sicurezza del lavoro locale di M2 (notte 9/11)
- `r8_sicurezza_fetta1.patch`: SOLO la parte di `modules/voice/server.py` della fetta di sicurezza R8 (commit locale 7e7f14b di M2, base 0d34fe6 = head della #356). I test (`tests/test_unit_voice_server.py`, classe TestR8Limiti e test_r8_*) e `reports/proposta_voce_sicura.md` NON sono qui: li ha M2 in locale; se il suo container si ricicla vanno riscritti.
- Uso: copia di emergenza, non da applicare senza revisore. Si toglie appena M2 pubblica la PR.
