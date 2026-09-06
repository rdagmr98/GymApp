// Schede settimanali predefinite (2–5 giorni, livelli + booty).
// Importato da main.dart.

Map<String, dynamic> _ex(
  String name,
  String gif,
  int sets,
  List<int> reps, {
  int rest = 90,
  int pause = 120,
  String note = '',
}) =>
    {
      'name': name,
      'targetSets': sets,
      'repsList': reps,
      'recoveryTime': rest,
      'interExercisePause': pause,
      'notePT': note,
      'noteCliente': '',
      'supersetGroup': 0,
      'gifFilename': gif,
    };

Map<String, dynamic> _day(
  String dayName,
  List<String> bodyParts,
  String? muscleImage,
  List<Map<String, dynamic>> exercises,
) =>
    {
      'dayName': dayName,
      'bodyParts': bodyParts,
      if (muscleImage != null) 'muscleImage': muscleImage,
      'exercises': exercises,
    };

Map<String, dynamic> _tpl(
  String name,
  String desc,
  String icon,
  List<Map<String, dynamic>> days,
) =>
    {
      'name': name,
      'desc': desc,
      'icon': icon,
      'days': days,
    };

final List<Map<String, dynamic>> kWorkoutTemplates = [
  // —— Principiante ——
  _tpl('Principiante 2gg', '2 giorni · full body A/B', '🌱', [
    _day('Full Body A', ['petto', 'dorso', 'gambe'], null, [
      _ex('Leg Press', 'leg-press', 3, [12, 12, 10], rest: 120),
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [12, 10, 10]),
      _ex('Leg Curl', 'leg-curl', 2, [12, 12], rest: 60),
      _ex('Plank', 'plank', 3, [30, 30, 30], rest: 45),
    ]),
    _day('Full Body B', ['gambe', 'petto', 'dorso'], null, [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 3, [12, 12, 10], rest: 120),
      _ex('Peck Deck', 'pec-deck-fly', 3, [12, 12, 10]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 12], rest: 60),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [12, 12, 10]),
      _ex('Crunch', 'crunch', 3, [15, 15, 15], rest: 45),
    ]),
  ]),
  _tpl('Principiante 3gg', '3 giorni · full body ruotato', '🌱', [
    _day('Full Body A', ['petto', 'gambe', 'dorso'], null, [
      _ex('Leg Press', 'leg-press', 3, [12, 12, 10], rest: 120),
      _ex('Panca Piana', 'bench-press', 3, [10, 10, 8]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 2, [12, 12]),
      _ex('Plank', 'plank', 3, [30, 30, 30], rest: 45),
    ]),
    _day('Full Body B', ['dorso', 'gambe', 'braccia'], null, [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 3, [12, 10, 10], rest: 120),
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Curl Martello', 'hammer-curl', 2, [12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 2, [12, 10], rest: 60),
      _ex('Crunch', 'crunch', 3, [15, 15, 12], rest: 45),
    ]),
    _day('Full Body C', ['gambe', 'spalle', 'glutei'], 'gambe.png', [
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [10, 10, 8], rest: 120),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [12, 12, 10]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [10, 10, 8]),
      _ex('Affondi', 'bodyweight-lunge', 2, [10, 10]),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
      _ex('Leg Raise', 'hanging-leg-raises', 2, [10, 10], rest: 45),
    ]),
  ]),
  _tpl('Principiante 4gg', '4 giorni · upper / lower', '🌱', [
    _day('Upper A', ['petto', 'dorso', 'spalle'], 'push.png', [
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [10, 10, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 2, [12, 12], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 2, [12, 10], rest: 60),
    ]),
    _day('Lower A', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Leg Press', 'leg-press', 3, [12, 12, 10], rest: 120),
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [10, 10, 8], rest: 120),
      _ex('Leg Extension', 'leg-extension', 2, [12, 12], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 2, [12, 12], rest: 60),
      _ex('Calf Raise', 'calf-raise', 3, [15, 15, 12], rest: 45),
    ]),
    _day('Upper B', ['petto', 'dorso', 'braccia'], 'pull.png', [
      _ex('Peck Deck', 'pec-deck-fly', 3, [12, 12, 10]),
      _ex('Seated Row Machine', 'seated-row-machine', 3, [12, 10, 10]),
      _ex('Distensioni con Manubri', 'alternate-dumbbell-bench-press', 3, [10, 10, 8]),
      _ex('Curl Martello', 'hammer-curl', 2, [12, 10], rest: 60),
      _ex('Push Down', 'push-down', 2, [12, 10], rest: 60),
      _ex('Face Pull', 'face-pull', 2, [15, 12], rest: 60),
    ]),
    _day('Lower B', ['gambe', 'glutei'], 'glutei.png', [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 3, [12, 10, 10], rest: 120),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [12, 12, 10]),
      _ex('Affondi', 'bodyweight-lunge', 2, [10, 10]),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 2, [15, 12], rest: 60),
      _ex('Calf Raise', 'calf-raise', 3, [15, 12, 12], rest: 45),
    ]),
  ]),
  _tpl('Principiante 5gg', '5 giorni · full body + focus', '🌱', [
    _day('Full Body', ['petto', 'dorso', 'gambe'], null, [
      _ex('Leg Press', 'leg-press', 3, [12, 10, 10], rest: 120),
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 2, [10, 10]),
      _ex('Plank', 'plank', 3, [30, 30, 30], rest: 45),
    ]),
    _day('Upper Push', ['petto', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 3, [10, 10, 8]),
      _ex('Peck Deck', 'pec-deck-fly', 2, [12, 12]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 2, [12, 10], rest: 60),
    ]),
    _day('Lower', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 3, [12, 10, 10], rest: 120),
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [10, 10, 8]),
      _ex('Leg Extension', 'leg-extension', 2, [12, 12], rest: 60),
      _ex('Leg Curl', 'leg-curl', 2, [12, 12], rest: 60),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 2, [12, 10]),
    ]),
    _day('Upper Pull', ['dorso', 'braccia'], 'pull.png', [
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Curl Martello', 'hammer-curl', 2, [12, 10], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Glutei + Core', ['glutei', 'core'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [12, 12, 10]),
      _ex('Glute Kickback', 'glute-kickback-machine', 3, [12, 12, 12], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 2, [15, 15], rest: 60),
      _ex('Crunch', 'crunch', 3, [15, 15, 12], rest: 45),
      _ex('Plank', 'plank', 3, [30, 30, 30], rest: 45),
    ]),
  ]),

  // —— Intermedio ——
  _tpl('Intermedio 2gg', '2 giorni · upper / lower volume', '⚡', [
    _day('Upper', ['petto', 'dorso', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 4, [10, 8, 8, 6], rest: 120),
      _ex('Lat Machine', 'lat-pulldown', 4, [10, 8, 8, 8]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [8, 8, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [10, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Curl con Bilanciere', 'barbell-curl', 3, [10, 8, 8], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 3, [12, 10, 8], rest: 60),
    ]),
    _day('Lower', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 4, [8, 8, 6, 6], rest: 150),
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [8, 8, 8, 6], rest: 120),
      _ex('Leg Press', 'leg-press', 3, [12, 10, 10]),
      _ex('Leg Curl', 'seated-leg-curl', 3, [10, 10, 8]),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [10, 10, 8]),
      _ex('Calf Raise', 'calf-raise', 4, [15, 12, 12, 12], rest: 45),
    ]),
  ]),
  _tpl('Intermedio 3gg PPL', '3 giorni · pull / push / legs', '⚡', [
    _day('Pull', ['dorso', 'braccia'], 'pull.png', [
      _ex('Lat Machine', 'lat-pulldown', 4, [10, 8, 8, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 4, [10, 8, 8, 8]),
      _ex('Dumbbell Row', 'dumbbell-row', 3, [10, 8, 8]),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
      _ex('Curl con Bilanciere', 'barbell-curl', 3, [10, 8, 8], rest: 60),
      _ex('Curl Martello', 'hammer-curl', 2, [12, 10], rest: 60),
    ]),
    _day('Push', ['petto', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 4, [8, 8, 6, 6], rest: 120),
      _ex('Panca Inclinata', 'incline-barbell-bench-press', 3, [10, 8, 8]),
      _ex('Peck Deck', 'pec-deck-fly', 3, [12, 10, 10], rest: 60),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [8, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 3, [12, 10, 8], rest: 60),
    ]),
    _day('Legs', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 4, [8, 8, 6, 6], rest: 150),
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [8, 8, 8], rest: 120),
      _ex('Leg Press', 'leg-press', 3, [12, 10, 10]),
      _ex('Leg Extension', 'leg-extension', 3, [12, 10, 10], rest: 60),
      _ex('Leg Curl', 'leg-curl', 3, [10, 10, 8], rest: 60),
      _ex('Calf Raise', 'calf-raise', 4, [15, 12, 12, 12], rest: 45),
    ]),
  ]),
  _tpl('Intermedio 4gg', '4 giorni · upper / lower x2', '⚡', [
    _day('Upper A', ['petto', 'dorso', 'spalle'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 4, [8, 8, 6, 6], rest: 120),
      _ex('Lat Machine', 'lat-pulldown', 4, [10, 8, 8, 8]),
      _ex('Arnold Press', 'arnold-press', 3, [10, 8, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [10, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 3, [12, 10, 8], rest: 60),
    ]),
    _day('Lower A', ['gambe'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 4, [8, 8, 6, 6], rest: 150),
      _ex('Leg Press', 'leg-press', 3, [12, 10, 8]),
      _ex('Leg Extension', 'leg-extension', 3, [12, 10, 10], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 3, [10, 10, 8]),
      _ex('Calf Raise', 'calf-raise', 4, [15, 12, 12, 12], rest: 45),
    ]),
    _day('Upper B', ['petto', 'dorso', 'braccia'], 'pull.png', [
      _ex('Distensioni con Manubri', 'alternate-dumbbell-bench-press', 4, [10, 8, 8, 8]),
      _ex('T Bar Row', 't-bar-row', 4, [8, 8, 8, 6]),
      _ex('High Cable Crossover', 'high-cable-crossover', 3, [12, 10, 10], rest: 60),
      _ex('Curl con Bilanciere', 'barbell-curl', 3, [10, 8, 8], rest: 60),
      _ex('French Press', 'seated-ez-bar-overhead-triceps-extension', 3, [10, 8, 8], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Lower B', ['gambe', 'glutei'], 'glutei.png', [
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [8, 8, 8, 6], rest: 120),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [10, 8, 8, 8]),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [8, 8, 8]),
      _ex('Leg Curl', 'leg-curl', 3, [10, 10, 8], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 3, [15, 12, 12], rest: 60),
    ]),
  ]),
  _tpl('Intermedio 5gg', '5 giorni · PPL + upper/lower', '⚡', [
    _day('Push', ['petto', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 4, [8, 8, 6, 6], rest: 120),
      _ex('Incline Dumbbell Press', 'incline-dumbbell-press', 3, [10, 8, 8]),
      _ex('Lento Avanti', 'barbell-shoulder-press', 3, [8, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 3, [12, 10, 8], rest: 60),
    ]),
    _day('Pull', ['dorso', 'braccia'], 'pull.png', [
      _ex('Lat Machine', 'lat-pulldown', 4, [10, 8, 8, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 4, [10, 8, 8, 8]),
      _ex('Dumbbell Row', 'dumbbell-row', 3, [10, 8, 8]),
      _ex('Curl Martello', 'hammer-curl', 3, [10, 8, 8], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Legs', ['gambe'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 4, [8, 8, 6, 6], rest: 150),
      _ex('Leg Press', 'leg-press', 3, [12, 10, 10]),
      _ex('Leg Extension', 'leg-extension', 3, [12, 10, 10], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 3, [10, 10, 8]),
      _ex('Calf Raise', 'calf-raise', 4, [15, 12, 12, 12], rest: 45),
    ]),
    _day('Upper', ['petto', 'dorso', 'spalle'], 'spalle.png', [
      _ex('Distensioni con Manubri', 'alternate-dumbbell-bench-press', 3, [10, 8, 8]),
      _ex('Seated Row Machine', 'seated-row-machine', 3, [10, 8, 8]),
      _ex('Arnold Press', 'arnold-press', 3, [10, 8, 8]),
      _ex('Peck Deck', 'pec-deck-fly', 2, [12, 12], rest: 60),
      _ex('Curl con Bilanciere', 'barbell-curl', 2, [10, 8], rest: 60),
    ]),
    _day('Lower Posterior', ['gambe', 'glutei'], 'glutei.png', [
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [8, 8, 8, 6], rest: 120),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [10, 8, 8, 8]),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [8, 8, 8]),
      _ex('Leg Curl', 'leg-curl', 3, [10, 10, 8], rest: 60),
      _ex('Hyperextension', 'hyperextension', 3, [12, 12, 10], rest: 60),
    ]),
  ]),

  // —— Avanzato ——
  _tpl('Avanzato 2gg', '2 giorni · force upper/lower', '🔥', [
    _day('Upper Strength', ['petto', 'dorso', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 5, [5, 5, 5, 5, 5], rest: 180),
      _ex('Rematore Bilanciere', 'barbell-bent-over-row', 4, [6, 6, 6, 6], rest: 150),
      _ex('Lento Avanti', 'barbell-shoulder-press', 4, [6, 6, 6, 6], rest: 120),
      _ex('Lat Machine', 'lat-pulldown', 3, [8, 8, 8]),
      _ex('Dip', 'triceps-dips', 3, [8, 8, 6], rest: 90),
      _ex('Curl con Bilanciere', 'barbell-curl', 3, [8, 8, 6], rest: 60),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 4, [12, 10, 10, 10], rest: 60),
    ]),
    _day('Lower Strength', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 5, [5, 5, 5, 5, 5], rest: 180),
      _ex('Stacco Rumeno', 'romanian-deadlift', 4, [6, 6, 6, 6], rest: 150),
      _ex('Leg Press', 'leg-press', 4, [10, 8, 8, 8], rest: 120),
      _ex('Bodyweight Walking Lunge', 'bodyweight-walking-lunge', 3, [8, 8, 8]),
      _ex('Leg Curl', 'leg-curl', 3, [10, 8, 8]),
      _ex('Calf Raise', 'calf-raise', 4, [12, 12, 10, 10], rest: 60),
    ]),
  ]),
  _tpl('Avanzato 3gg PPL', '3 giorni · PPL alta intensita', '🔥', [
    _day('Pull', ['dorso', 'braccia'], 'pull.png', [
      _ex('Deadlift', 'deadlift', 4, [5, 5, 3, 3], rest: 180),
      _ex('Lat Machine', 'lat-pulldown', 4, [8, 8, 6, 6]),
      _ex('Pulley Basso', 'seated-cable-row', 4, [8, 8, 8, 6]),
      _ex('Dumbbell Row', 'dumbbell-row', 3, [8, 8, 8]),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
      _ex('Curl con Bilanciere', 'barbell-curl', 4, [8, 8, 6, 6], rest: 60),
      _ex('Curl Martello', 'hammer-curl', 3, [10, 8, 8], rest: 60),
    ]),
    _day('Push', ['petto', 'spalle', 'braccia'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 5, [5, 5, 5, 3, 3], rest: 180),
      _ex('Panca Inclinata', 'incline-barbell-bench-press', 4, [8, 8, 6, 6], rest: 120),
      _ex('High Cable Crossover', 'high-cable-crossover', 3, [12, 10, 10], rest: 60),
      _ex('Lento Avanti', 'barbell-shoulder-press', 4, [6, 6, 6, 6], rest: 120),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 4, [12, 10, 10, 10], rest: 60),
      _ex('Alzate Posteriori', 'bent-over-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 4, [12, 10, 8, 8], rest: 60),
    ]),
    _day('Legs', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 5, [5, 5, 5, 3, 3], rest: 180),
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [6, 6, 6, 6], rest: 150),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [8, 8, 8], rest: 90),
      _ex('Leg Extension', 'leg-extension', 3, [12, 10, 10], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 4, [10, 8, 8, 8], rest: 60),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 3, [8, 8, 8]),
      _ex('Calf Raise', 'calf-raise', 5, [12, 12, 10, 10, 10], rest: 45),
    ]),
  ]),
  _tpl('Avanzato 4gg', '4 giorni · upper/lower intensita', '🔥', [
    _day('Upper Power', ['petto', 'dorso', 'spalle'], 'push.png', [
      _ex('Panca Piana', 'bench-press', 5, [5, 5, 5, 3, 3], rest: 180),
      _ex('Rematore Bilanciere', 'barbell-bent-over-row', 4, [6, 6, 6, 6], rest: 150),
      _ex('Lento Avanti', 'barbell-shoulder-press', 4, [6, 6, 6, 6], rest: 120),
      _ex('Lat Machine', 'lat-pulldown', 3, [8, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 4, [12, 10, 10, 10], rest: 60),
      _ex('French Press', 'seated-ez-bar-overhead-triceps-extension', 3, [8, 8, 8], rest: 60),
    ]),
    _day('Lower Power', ['gambe'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 5, [5, 5, 5, 3, 3], rest: 180),
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [6, 6, 6, 6], rest: 150),
      _ex('Leg Press', 'leg-press', 4, [10, 8, 8, 8], rest: 120),
      _ex('Leg Curl', 'leg-curl', 3, [10, 8, 8]),
      _ex('Calf Raise', 'calf-raise', 4, [12, 12, 10, 10], rest: 45),
    ]),
    _day('Upper Hypertrophy', ['petto', 'dorso', 'braccia'], 'pull.png', [
      _ex('Distensioni con Manubri', 'alternate-dumbbell-bench-press', 4, [10, 8, 8, 8]),
      _ex('Pulley Basso', 'seated-cable-row', 4, [10, 8, 8, 8]),
      _ex('Peck Deck', 'pec-deck-fly', 3, [12, 12, 10], rest: 60),
      _ex('Cable Straight Arm Pulldown', 'cable-straight-arm-pulldown', 3, [12, 10, 10], rest: 60),
      _ex('Curl Martello', 'hammer-curl', 3, [10, 8, 8], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 3, [12, 10, 8], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Lower Hypertrophy', ['gambe', 'glutei'], 'glutei.png', [
      _ex('Hack Squats Machine', 'hack-squats-machine', 4, [10, 8, 8, 8], rest: 120),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [10, 8, 8, 8]),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [8, 8, 8]),
      _ex('Leg Extension', 'leg-extension', 3, [12, 12, 10], rest: 60),
      _ex('Seated Leg Curl', 'seated-leg-curl', 3, [10, 10, 8], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 3, [15, 12, 12], rest: 60),
    ]),
  ]),
  _tpl('Avanzato 5gg', '5 giorni · split classico', '🔥', [
    _day('Petto', ['petto'], 'petto.png', [
      _ex('Panca Piana', 'bench-press', 5, [6, 6, 5, 5, 5], rest: 150),
      _ex('Panca Inclinata', 'incline-barbell-bench-press', 4, [8, 8, 6, 6], rest: 120),
      _ex('Distensioni con Manubri', 'alternate-dumbbell-bench-press', 3, [10, 8, 8]),
      _ex('High Cable Crossover', 'high-cable-crossover', 3, [12, 10, 10], rest: 60),
      _ex('Peck Deck', 'pec-deck-fly', 3, [12, 12, 10], rest: 60),
    ]),
    _day('Dorso', ['dorso'], 'dorso.png', [
      _ex('Deadlift', 'deadlift', 4, [5, 5, 3, 3], rest: 180),
      _ex('Lat Machine', 'lat-pulldown', 4, [8, 8, 6, 6]),
      _ex('Pulley Basso', 'seated-cable-row', 4, [8, 8, 8, 6]),
      _ex('Dumbbell Row', 'dumbbell-row', 3, [8, 8, 8]),
      _ex('Cable Straight Arm Pulldown', 'cable-straight-arm-pulldown', 3, [12, 10, 10], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Gambe', ['gambe'], 'gambe.png', [
      _ex('Squat con Bilanciere', 'squat', 5, [5, 5, 5, 3, 3], rest: 180),
      _ex('Leg Press', 'leg-press', 4, [10, 8, 8, 8], rest: 120),
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [8, 8, 6], rest: 120),
      _ex('Leg Extension', 'leg-extension', 3, [12, 10, 10], rest: 60),
      _ex('Leg Curl', 'seated-leg-curl', 3, [10, 10, 8], rest: 60),
      _ex('Calf Raise', 'calf-raise', 5, [12, 12, 10, 10, 10], rest: 45),
    ]),
    _day('Spalle', ['spalle'], 'spalle.png', [
      _ex('Lento Avanti', 'barbell-shoulder-press', 4, [6, 6, 6, 6], rest: 120),
      _ex('Arnold Press', 'arnold-press', 3, [8, 8, 8]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 5, [12, 10, 10, 10, 10], rest: 60),
      _ex('Alzate Frontali', 'dumbbell-front-raise', 3, [12, 10, 10], rest: 60),
      _ex('Alzate Posteriori', 'bent-over-lateral-raise', 4, [12, 12, 10, 10], rest: 60),
      _ex('Face Pull', 'face-pull', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Braccia', ['braccia'], 'braccia.png', [
      _ex('Curl con Bilanciere', 'barbell-curl', 4, [8, 8, 6, 6], rest: 60),
      _ex('Curl Martello', 'hammer-curl', 3, [10, 8, 8], rest: 60),
      _ex('Curl al Cavo Basso', 'cable-curl', 3, [12, 10, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 4, [12, 10, 8, 8], rest: 60),
      _ex('French Press', 'seated-ez-bar-overhead-triceps-extension', 3, [10, 8, 8], rest: 60),
      _ex('Dip', 'triceps-dips', 3, [10, 8, 8], rest: 60),
    ]),
  ]),

  // —— Booty / lower focus (donne) ——
  _tpl('Booty 2gg', '2 giorni · lower focus donna', '💃', [
    _day('Glutei A', ['glutei', 'gambe'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [12, 10, 10, 8], rest: 90),
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 3, [12, 10, 10], rest: 90),
      _ex('Romanian Deadlift', 'romanian-deadlift', 3, [10, 10, 8], rest: 90),
      _ex('Glute Kickback', 'glute-kickback-machine', 3, [15, 12, 12], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 3, [15, 15, 12], rest: 60),
      _ex('Calf Raise', 'calf-raise', 3, [15, 15, 12], rest: 45),
    ]),
    _day('Glutei B + Upper', ['glutei', 'petto', 'dorso'], 'glutei.png', [
      _ex('Sumo Deadlift', 'sumo-deadlift', 3, [10, 8, 8], rest: 120),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [10, 10, 8]),
      _ex('Donkey Kicks', 'donkey-kicks', 3, [15, 15, 12], rest: 45),
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Plank', 'plank', 3, [30, 30, 30], rest: 45),
    ]),
  ]),
  _tpl('Booty 3gg', '3 giorni · glutei / hamstring / upper light', '💃', [
    _day('Glute Focus', ['glutei'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [12, 10, 10, 8], rest: 90),
      _ex('Sumo Deadlift', 'sumo-deadlift', 3, [8, 8, 8], rest: 120),
      _ex('Glute Kickback', 'glute-kickback-machine', 4, [15, 12, 12, 12], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 3, [15, 15, 12], rest: 60),
      _ex('Donkey Kicks', 'donkey-kicks', 3, [15, 15, 15], rest: 45),
    ]),
    _day('Quad + Ham', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 4, [12, 10, 10, 8], rest: 90),
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [10, 8, 8, 8], rest: 90),
      _ex('Leg Press', 'leg-press', 3, [12, 12, 10]),
      _ex('Leg Curl', 'seated-leg-curl', 3, [12, 10, 10], rest: 60),
      _ex('Affondi', 'bodyweight-lunge', 3, [10, 10, 10]),
      _ex('Calf Raise', 'calf-raise', 3, [15, 15, 12], rest: 45),
    ]),
    _day('Upper Light + Core', ['petto', 'dorso', 'core'], 'push.png', [
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Seated Row Machine', 'seated-row-machine', 3, [12, 10, 10]),
      _ex('Crunch', 'crunch', 3, [15, 15, 12], rest: 45),
      _ex('Plank', 'plank', 3, [40, 40, 30], rest: 45),
    ]),
  ]),
  _tpl('Booty 4gg', '4 giorni · lower / upper / glute specialty', '💃', [
    _day('Lower A Quads', ['gambe', 'glutei'], 'gambe.png', [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 4, [12, 10, 8, 8], rest: 90),
      _ex('Leg Press', 'leg-press', 4, [12, 10, 10, 8]),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [10, 10, 8]),
      _ex('Leg Extension', 'leg-extension', 3, [15, 12, 12], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 3, [15, 15, 12], rest: 60),
    ]),
    _day('Upper', ['petto', 'dorso', 'spalle'], 'push.png', [
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Rope Pushdown', 'rope-pushdown', 2, [12, 10], rest: 60),
    ]),
    _day('Lower B Posterior', ['glutei', 'gambe'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 5, [12, 10, 10, 8, 8], rest: 90),
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [10, 8, 8, 8], rest: 90),
      _ex('Sumo Deadlift', 'sumo-deadlift', 3, [8, 8, 8], rest: 120),
      _ex('Leg Curl', 'leg-curl', 3, [12, 10, 10], rest: 60),
      _ex('Glute Kickback', 'glute-kickback-machine', 3, [15, 12, 12], rest: 60),
    ]),
    _day('Glute Pump', ['glutei'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [15, 12, 12, 10], rest: 60),
      _ex('Donkey Kicks', 'donkey-kicks', 4, [15, 15, 15, 15], rest: 45),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 4, [20, 15, 15, 15], rest: 45),
      _ex('Glute Kickback', 'glute-kickback-machine', 3, [15, 15, 12], rest: 45),
      _ex('Affondi', 'bodyweight-lunge', 3, [12, 12, 10], rest: 60),
      _ex('Plank', 'plank', 3, [40, 40, 30], rest: 45),
    ]),
  ]),
  _tpl('Booty 5gg', '5 giorni · glute specialization', '💃', [
    _day('Glute Strength', ['glutei'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 5, [8, 8, 8, 6, 6], rest: 120),
      _ex('Sumo Deadlift', 'sumo-deadlift', 4, [6, 6, 6, 6], rest: 150),
      _ex('Bulgarian Split Squat', 'barbell-bulgarian-split-squat', 3, [8, 8, 8], rest: 90),
      _ex('Glute Kickback', 'glute-kickback-machine', 3, [12, 12, 10], rest: 60),
    ]),
    _day('Quads', ['gambe'], 'quadricipiti.png', [
      _ex('Goblet Squat', 'kettlebell-goblet-squat', 4, [10, 10, 8, 8], rest: 90),
      _ex('Leg Press', 'leg-press', 4, [12, 10, 10, 8]),
      _ex('Leg Extension', 'leg-extension', 4, [15, 12, 12, 10], rest: 60),
      _ex('Affondi', 'bodyweight-lunge', 3, [10, 10, 10]),
      _ex('Calf Raise', 'calf-raise', 4, [15, 12, 12, 12], rest: 45),
    ]),
    _day('Upper', ['petto', 'dorso', 'spalle'], 'push.png', [
      _ex('Chest Press Macchina', 'chest-press-machine', 3, [12, 10, 10]),
      _ex('Lat Machine', 'lat-pulldown', 3, [12, 10, 10]),
      _ex('Pulley Basso', 'seated-cable-row', 3, [12, 10, 10]),
      _ex('Alzate Laterali', 'dumbbell-lateral-raise', 3, [12, 12, 10], rest: 60),
      _ex('Curl Martello', 'hammer-curl', 2, [12, 10], rest: 60),
    ]),
    _day('Hamstrings + Glute', ['gambe', 'glutei'], 'femorali.png', [
      _ex('Romanian Deadlift', 'romanian-deadlift', 4, [8, 8, 8, 6], rest: 120),
      _ex('Leg Curl', 'seated-leg-curl', 4, [12, 10, 10, 8], rest: 60),
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [12, 10, 10, 8], rest: 90),
      _ex('Hyperextension', 'hyperextension', 3, [12, 12, 10], rest: 60),
      _ex('Donkey Kicks', 'donkey-kicks', 3, [15, 15, 12], rest: 45),
    ]),
    _day('Glute Pump + Core', ['glutei', 'core'], 'glutei.png', [
      _ex('Hip Thrust', 'barbell-hip-thrusts', 4, [15, 12, 12, 12], rest: 60),
      _ex('Hip Abduction Machine', 'hip-abduction-machine', 4, [20, 15, 15, 15], rest: 45),
      _ex('Glute Kickback', 'glute-kickback-machine', 4, [15, 15, 12, 12], rest: 45),
      _ex('Crunch', 'crunch', 3, [15, 15, 15], rest: 45),
      _ex('Russian Twist', 'russian-twist', 3, [20, 20, 16], rest: 45),
      _ex('Plank', 'plank', 3, [45, 40, 40], rest: 45),
    ]),
  ]),
  // —— Scheda personale Gianmarco (import .workout) ——
  _tpl(
    'Scheda Gianmarco',
    '5 giorni · split personale petto / dorso / gambe / spalle / braccia',
    '🏋️',
    [
    _day('Petto', ['petto'], 'petto.png', [
      _ex('Smith Machine Bench Press', 'smith-machine-bench-press', 4, [8, 8, 8, 8], note: 'Utilizzare Multipower'),
      _ex('High Cable Crossover', 'high-cable-crossover', 4, [8, 8, 8, 8]),
      _ex('Distensioni manubri', 'dumbbell-press', 4, [8, 8, 8, 8]),
      _ex('Pectoral machine', 'pec-deck-fly', 4, [8, 8, 8, 8]),
    ]),
    _day('Dorso', ['dorso'], 'dorso.png', [
      _ex('Lat machine convergente', 'lat-pulldown', 4, [8, 8, 8, 8]),
      _ex('Row machine', 'seated-row-machine', 4, [8, 8, 8, 8]),
      _ex('Pulley', 'seated-cable-row', 4, [8, 8, 8, 8]),
      _ex('Cable Straight Arm Pulldown', 'cable-straight-arm-pulldown', 4, [10, 10, 10, 10]),
    ]),
    _day('Gambe', ['gambe'], 'gambe.png', [
      _ex('Belt squat', 'belt-squat', 8, [8, 8, 8, 8, 8, 8, 8, 8]),
      _ex('Leg extension', 'leg-extension', 3, [15, 12, 10]),
      _ex('Leg Curl Seduto', 'seated-leg-curl', 4, [8, 8, 8, 8]),
      _ex('Leg Curl', 'leg-curl', 4, [8, 8, 8, 8]),
    ]),
    _day('Spalle', ['spalle'], 'spalle.png', [
      _ex('Shoulder Press Macchina', 'lever-shoulder-press', 4, [8, 8, 8, 8]),
      _ex('Alzate frontali', 'dumbbell-front-raise', 3, [10, 10, 10], rest: 60),
      _ex('Lateral Raise Machine', 'lateral-raise-machine', 8, [12, 10, 12, 10, 12, 10, 12, 10], rest: 60),
      _ex('Alzate laterali', 'dumbbell-lateral-raise', 4, [10, 8, 12, 10], rest: 60),
      _ex('Alzate Posteriori', 'bent-over-lateral-raise', 4, [12, 10, 10, 8], rest: 60),
    ]),
    _day('Braccia', ['braccia'], 'braccia.png', [
      _ex('Biceps machine', 'lever-preacher-curl', 5, [8, 8, 8, 8, 8], rest: 60),
      _ex('Curl cavi dal basso', 'cable-two-arm-curl-on-incline-bench', 5, [8, 8, 8, 8, 8], rest: 60),
      _ex('Curl hammer', 'cable-rope-hammer-curl', 5, [8, 8, 8, 8, 8], rest: 60),
      _ex('Push down cavo', 'one-arm-reverse-push-down', 5, [8, 8, 8, 8, 8], rest: 60),
      _ex('Push down corda', 'rope-pushdown', 5, [8, 8, 8, 8, 8], rest: 60),
      _ex('Spaccacranio', 'seated-one-arm-dumbbell-triceps-extension', 5, [8, 8, 8, 8, 8], rest: 60),
    ]),
  ]),
];

const List<Map<String, dynamic>> kCuratedWorkoutTemplates = [];

List<Map<String, dynamic>> get kAllWorkoutTemplates => [
      ...kWorkoutTemplates,
      ...kCuratedWorkoutTemplates,
    ];
