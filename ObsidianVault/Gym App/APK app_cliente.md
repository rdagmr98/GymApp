# APK app_cliente
`flutter build apk --split-per-abi --release` (SEMPRE split-per-abi, mai senza — regola CLAUDE.md) → `GymLogbook-arm64-v8a.apk` (154MB) + `GymLogbook-armeabi-v7a.apk` (151MB)
Poi: copia in `Documents\releases\app_cliente\` → `gh release upload v<tag> ... --clobber` su `rdagmr98/rdagmr98.github.io`.
← [[app_cliente]] → [[releases]]
