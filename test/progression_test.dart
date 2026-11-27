import 'package:flutter_test/flutter_test.dart';
import 'package:gym_app/progression.dart';

void main() {
  test('reps oltre il target: una in più', () {
    final p = progressionPlan(target: 10, lastKg: 60, lastReps: 11);
    expect((p.kg, p.reps, p.aumento, p.provaReps), (60.0, 12, false, 12));
  });
  test('target+2 -> peso + salto, reps al target', () {
    final p = progressionPlan(target: 10, lastKg: 70, lastReps: 12, step: 5);
    expect((p.kg, p.reps, p.aumento, p.provaReps), (75.0, 10, true, null));
  });
  test('sotto il target: una rep in più della volta scorsa', () {
    final p = progressionPlan(target: 10, lastKg: 60, lastReps: 8);
    expect((p.kg, p.reps, p.aumento, p.provaReps), (60.0, 9, false, 9));
  });
  test('aumento fatto oggi sulla serie prima non si porta qui (piramide 70/75 non diventa 80)', () {
    final p = progressionPlan(target: 10, lastKg: 75, lastReps: 10, todayPrevKg: 75, step: 5);
    expect((p.kg, p.reps, p.aumento, p.provaReps), (75.0, 11, false, 11));
  });
  test('serie concatenate: la serie prima di oggi contro quella della volta scorsa', () {
    // volta scorsa 80×8 poi 70×10; oggi la prima viene 80×10: si poteva fare 85, la seconda sale a 75×10
    final su = progressionPlan(target: 10, lastKg: 70, lastReps: 10,
        todayPrevKg: 80, todayPrevReps: 10, lastPrevKg: 80, lastPrevReps: 8, step: 5);
    expect((su.kg, su.reps, su.aumento), (75.0, 10, true));
    // prima uguale alla volta scorsa: solo una rep in più
    final pari = progressionPlan(target: 10, lastKg: 70, lastReps: 10,
        todayPrevKg: 80, todayPrevReps: 8, lastPrevKg: 80, lastPrevReps: 8, step: 5);
    expect((pari.kg, pari.reps, pari.aumento), (70.0, 11, false));
    // la volta scorsa aveva già aumentato (70×12 -> 75 oggi sulla prima): la seconda 75×10 non sale
    final gia = progressionPlan(target: 10, lastKg: 75, lastReps: 10,
        todayPrevKg: 75, todayPrevReps: 10, lastPrevKg: 70, lastPrevReps: 12, step: 5);
    expect((gia.kg, gia.reps, gia.aumento), (75.0, 11, false));
  });
  test('lontani dal target: peso più basso per arrivarci', () {
    final p = progressionPlan(target: 10, lastKg: 80, lastReps: 6, step: 2.5);
    expect((p.kg, p.reps, p.aumento), (70.0, 10, false));
  });
  test('serie senza storico: dalla serie prima di oggi con la fatica', () {
    expect(progressionPlan(target: 10, lastKg: 0, lastReps: 0, todayPrevKg: 80, todayPrevReps: 8).kg, 70);
    expect(progressionPlan(target: 10, lastKg: 0, lastReps: 0, todayPrevKg: 80, todayPrevReps: 10).kg, 75);
  });
  test('record personali: solo se batte tutte le sessioni prima', () {
    final h = [
      {'exercise': 'Panca', 'session_id': 'a', 'series': [{'w': 80, 'r': 8}]},
      {'exercise': 'Panca', 'session_id': 'b', 'series': [{'w': 85, 'r': 6}]},
      {'exercise': 'Squat', 'session_id': 'a', 'series': [{'w': 100, 'r': 5}]},
      {'exercise': 'Panca', 'session_id': 'oggi', 'series': [{'w': 85, 'r': 7}]},
    ];
    final done = [
      {'exercise': 'Panca', 'series': [{'w': 85, 'r': 7}]},
      {'exercise': 'Squat', 'series': [{'w': 100, 'r': 5}]},
      {'exercise': 'Nuovo', 'series': [{'w': 10, 'r': 10}]},
    ];
    final rec = sessionRecords(h, done, 'oggi');
    expect(rec.map((e) => (e.exercise, e.w, e.r)), [('Panca', 85.0, 7)]);
  });
  test('senza storico: peso della serie prima, poi 20 kg', () {
    expect(progressionPlan(target: 8, lastKg: 0, lastReps: 0, todayPrevKg: 40).kg, 40);
    expect(progressionPlan(target: 8, lastKg: 0, lastReps: 0).kg, 20);
  });
  test('corpo libero: niente aumento peso, solo reps', () {
    final p = progressionPlan(target: 12, lastKg: 0, lastReps: 15);
    expect((p.kg, p.reps, p.aumento, p.provaReps), (0.0, 16, false, 16));
  });
  test('ultimo allenamento: conta la sessione, non l esercizio in comune', () {
    final h = [
      {'exercise': 'Panca', 'dayName': 'B', 'date': '2026-11-06T10:00:00'},
      {'exercise': 'Panca', 'dayName': 'A', 'date': '2026-11-01T10:00:00'},
      {'exercise': 'Squat', 'date': '2026-10-20T10:00:00'}, // vecchia, senza dayName
    ];
    expect(lastTrainedDate(h, 'A', ['Panca']), DateTime(2026, 11, 1, 10));
    expect(lastTrainedDate(h, 'b', ['Panca']), DateTime(2026, 11, 6, 10));
    expect(lastTrainedDate(h, 'C', ['Squat']), DateTime(2026, 10, 20, 10));
    expect(lastTrainedDate(h, 'D', ['Stacco']), null);
  });
  test('il peso conta più delle reps: 230×8 batte 220×10', () {
    expect(setScore(230, 8) > setScore(220, 10), true);
    expect(setScore(222.5, 8) > setScore(220, 10), true); // salto minimo della doppia progressione
    expect(setScore(220, 10) > setScore(220, 8), true);
    expect(setScore(0, 12) > setScore(0, 10), true);
    final b = bestSet([{'w': 220, 'r': 10}, {'w': 230, 'r': 8}, {'w': 230, 'r': 6}]);
    expect((b!.w, b.r), (230.0, 8));
    expect(bestSet([]), null);
  });
  test('salto di peso dallo storico, 2,5 se non basta', () {
    final h = [
      {'exercise': 'Fly', 'series': [{'w': 70, 'r': 12}, {'w': 75, 'r': 10}]},
      {'exercise': 'Fly', 'series': [{'w': 65, 'r': 12}]},
      {'exercise': 'Panca', 'series': [{'w': 80, 'r': 8}]},
    ];
    expect(weightStep(h, 'Fly'), 5);
    expect(weightStep(h, 'Panca'), 2.5);
    // pochi pesi diversi (70 e 80): non propone +10 kg
    expect(weightStep([{'exercise': 'Leg', 'series': [{'w': 70, 'r': 12}, {'w': 80, 'r': 8}]}], 'Leg'), 5);
  });
  test('andamento: solo esercizi in comune con la sessione prima', () {
    final i = chainIndex([
      {'A': 100, 'B': 100},
      {'A': 110, 'C': 50}, // B sostituito da C: conta solo A, +10%
      {'A': 110, 'C': 55}, // +5/160
    ]);
    expect(i[0], 100);
    expect(i[1], closeTo(110, 1e-9));
    expect(i[2], closeTo(110 * 165 / 160, 1e-9));
  });
  test('andamento per giorno: A e B concatenati a parte', () {
    final i = sessionIndex(
      {'a1': {'X': 100}, 'b1': {'Y': 50}, 'a2': {'X': 120}},
      {'a1': '2026-01-01', 'b1': '2026-01-02', 'a2': '2026-01-03'},
      {'a1': 'A', 'b1': 'B', 'a2': 'A'},
    );
    expect(i['a1'], 100);
    expect(i['b1'], 100);
    expect(i['a2'], closeTo(120, 1e-9));
  });

  test('renamedDays: giorno rinominato con gli stessi esercizi, giorno nuovo diverso no', () {
    final before = {'Push': {'Panca', 'Croci', 'Dip'}, 'Pull': {'Trazioni', 'Rematore'}};
    final after = {
      'Petto e tricipiti': {'Panca', 'Croci', 'French press'},
      'pull': {'Trazioni', 'Rematore'},
      'Gambe': {'Squat', 'Pressa'},
    };
    expect(renamedDays(before, after), {'Push': 'Petto e tricipiti'});
    final hist = [
      {'dayName': 'push', 'exercise': 'Panca'},
      {'dayName': 'Pull', 'exercise': 'Trazioni'},
      {'exercise': 'Squat'},
    ];
    expect(renameDaysInHistory(hist, {'Push': 'Petto e tricipiti'}), 1);
    expect(hist[0]['dayName'], 'Petto e tricipiti');
    expect(hist[1]['dayName'], 'Pull');
  });

  test('prima serie: la seconda della volta scorsa a pari peso con 2 reps in più alza il peso', () {
    final last = [{'w': 80.0, 'r': 10}, {'w': 80.0, 'r': 12}];
    expect(refReps(last, 1, 80, 10), 12);
    final p = progressionPlan(target: 10, lastKg: 80, lastReps: refReps(last, 1, 80, 10));
    expect((p.kg, p.aumento), (82.5, true));
  });
  test('refReps: piramide e serie prima non contano', () {
    final last = [{'w': 70.0, 'r': 12}, {'weight': 80, 'reps': 8}, {'w': 75.0, 'r': 10}];
    expect(refReps(last, 2, 80, 8), 8);
    expect(refReps(last, 3, 75, 10), 10);
  });
}
