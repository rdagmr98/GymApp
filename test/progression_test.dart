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
  test('peso alzato sulla serie prima -> stesso aumento, reps al target', () {
    final p = progressionPlan(target: 10, lastKg: 60, lastReps: 12, todayPrevKg: 62.5, lastPrevKg: 60);
    expect((p.kg, p.reps, p.aumento), (62.5, 10, false));
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
}
