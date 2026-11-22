import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gym_app/main.dart';

const _accent = Color(0xFFFF0000);

/// Simula il padre reale: tiene i flag di passo e (se [propagate]) li
/// ripassa al widget a ogni onWeightModeChanged, come _setExerciseWeightMode.
class _Harness extends StatefulWidget {
  final double initialKg;
  final bool q, e, s, lb, propagate;
  const _Harness({
    super.key,
    required this.initialKg,
    this.q = false,
    this.e = false,
    this.s = false,
    this.lb = false,
    this.propagate = true,
  });
  @override
  State<_Harness> createState() => HarnessState();
}

class HarnessState extends State<_Harness> {
  late bool q = widget.q, e = widget.e, s = widget.s;
  final kgCalls = <double>[];
  final modeCalls = <List<bool>>[];
  void rebuild() => setState(() {});
  @override
  Widget build(BuildContext context) => MaterialApp(
    home: Scaffold(
      body: Center(
        child: SizedBox(
          width: 320,
          height: 220,
          child: testDrumPickers(
            initialKg: widget.initialKg,
            initialReps: 8,
            useQuarterStep: q,
            useEvenStep: e,
            useSingleStep: s,
            displayInPounds: widget.lb,
            accent: _accent,
            onKgChanged: kgCalls.add,
            onRepsChanged: (_) {},
            onWeightModeChanged: (a, b, c) {
              modeCalls.add([a, b, c]);
              if (widget.propagate) {
                setState(() {
                  q = a;
                  e = b;
                  s = c;
                });
              }
            },
          ),
        ),
      ),
    ),
  );
}

Future<void> _settle(WidgetTester t) async {
  // pumpAndSettle non termina: l'animazione della freccia ripete all'infinito.
  for (var i = 0; i < 30; i++) {
    await t.pump(const Duration(milliseconds: 50));
  }
}

// Testi della colonna kg (metà sinistra), ordinati dall'alto in basso.
List<Text> _kgTexts(WidgetTester t) {
  final all = t.widgetList<Text>(find.byType(Text)).where((w) {
    final d = w.data ?? '';
    return RegExp(r'^\d+(\.\d+)?$').hasMatch(d);
  }).toList();
  final kg = all.where((w) {
    final pos = t.getCenter(find.byWidget(w));
    return pos.dx < 400;
  }).toList();
  kg.sort((a, b) => t
      .getCenter(find.byWidget(a))
      .dy
      .compareTo(t.getCenter(find.byWidget(b)).dy));
  return kg;
}

String _selected(WidgetTester t) {
  final sel = _kgTexts(t).where((w) => w.style?.color == _accent).toList();
  expect(sel.length, 1, reason: 'una sola voce kg selezionata');
  return sel.first.data!;
}

List<String> _neighbours(WidgetTester t) =>
    _kgTexts(t).map((w) => w.data!).toList();

Future<void> _type(WidgetTester t, String txt) async {
  final selFinder = find.text(_selected(t)).first;
  await t.tap(selFinder);
  await _settle(t);
  await t.enterText(find.byType(TextField), txt);
  await t.tap(find.text('OK'));
  await _settle(t);
}

Future<void> _drag(WidgetTester t, double dy) async {
  final wheel = find.byType(ListWheelScrollView).first;
  await t.drag(wheel, Offset(0, dy));
  await _settle(t);
}

Future<HarnessState> _pump(WidgetTester t, _Harness h) async {
  await t.binding.setSurfaceSize(const Size(800, 600));
  await t.pumpWidget(h);
  await _settle(t);
  return t.state<HarnessState>(find.byType(_Harness));
}

void main() {
  // ---------- KG ----------
  testWidgets('1) passo 2,5 + 21 -> passo 1 con 21 selezionato', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20));
    expect(_selected(t), '20');
    await _type(t, '21');
    expect(_selected(t), '21');
    expect(h.modeCalls.last, [false, false, true]);
    expect(h.kgCalls.last, 21.0);
    // vicini coerenti col passo 1 -> 22 e 20 visibili intorno
    final n = _neighbours(t);
    expect(n, containsAll(['20', '22']));
    // 5) giro a mano di una tacca: onKgChanged col valore giusto
    await _drag(t, -112);
    expect(_selected(t), '22');
    expect(h.kgCalls.last, 22.0);
    await _drag(t, 224);
    expect(_selected(t), '20');
    expect(h.kgCalls.last, 20.0);
    // 6) rebuild identico non azzera il passo
    h.rebuild();
    await _settle(t);
    expect(_selected(t), '20');
    await _drag(t, -112);
    expect(_selected(t), '21');
  });

  testWidgets('2) passo 2,5 + 23,75 -> passo 1,25', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20));
    await _type(t, '23.75');
    expect(_selected(t), '23.75');
    expect(h.modeCalls.last, [true, false, false]);
    expect(h.kgCalls.last, 23.75);
    expect(_neighbours(t), containsAll(['22.5', '25']));
    await _drag(t, -112);
    expect(_selected(t), '25');
    expect(h.kgCalls.last, 25.0);
  });

  testWidgets('2b) 1,25 da 2,5', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20));
    await _type(t, '1,25');
    expect(_selected(t), '1.25');
    expect(h.modeCalls.last, [true, false, false]);
    await _drag(t, -112);
    expect(_selected(t), '2.5');
  });

  testWidgets('2c) 22,75 (non multiplo di 1,25): cosa succede', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20));
    await _type(t, '22,75');
    // ignore: avoid_print
    print('22,75 -> sel=${_selected(t)} mode=${h.modeCalls.last} '
        'vicini=${_neighbours(t)}');
    expect(_selected(t), '22.75');
  });

  testWidgets('3) passo 2 + 22,5 -> passo 2,5', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 22, e: true));
    expect(_selected(t), '22');
    await _type(t, '22,5');
    expect(_selected(t), '22.5');
    expect(h.modeCalls.last, [false, false, false]);
    expect(_neighbours(t), containsAll(['20', '25']));
    await _drag(t, -112);
    expect(_selected(t), '25');
    expect(h.kgCalls.last, 25.0);
  });

  testWidgets('4) passo 1 + 22,5 -> passo 2,5', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 22, s: true));
    expect(_selected(t), '22');
    await _type(t, '22.5');
    expect(_selected(t), '22.5');
    expect(h.modeCalls.last, [false, false, false]);
    expect(_neighbours(t), containsAll(['20', '25']));
  });

  testWidgets('4b) passo 1,25 + 21 -> passo 1 (flag padre ancora true)',
      (t) async {
    final h = await _pump(t, const _Harness(initialKg: 21.25, q: true));
    await _type(t, '21');
    expect(_selected(t), '21');
    expect(h.modeCalls.last, [false, false, true]);
    await _drag(t, -112);
    expect(_selected(t), '22');
  });

  testWidgets(
    '4c) come 4b ma il padre NON ripassa i flag (es. dialog modifica)',
    (t) async {
      final h = await _pump(
        t,
        const _Harness(initialKg: 21.25, q: true, propagate: false),
      );
      await _type(t, '21');
      expect(_selected(t), '21');
      expect(h.modeCalls.last, [false, false, true]);
      await _drag(t, -112);
      expect(_selected(t), '22');
      expect(h.kgCalls.last, 22.0);
    },
  );

  testWidgets('6b) padre senza propagazione + rebuild: passo resta', (t) async {
    final h = await _pump(
      t,
      const _Harness(initialKg: 20, propagate: false),
    );
    await _type(t, '21');
    h.rebuild();
    await _settle(t);
    expect(_selected(t), '21');
    await _drag(t, -112);
    expect(_selected(t), '22');
  });

  testWidgets('7) sopra 100 kg: 102,5 e 107 e 107,5', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 100));
    await _type(t, '102.5');
    expect(_selected(t), '102.5');
    expect(h.modeCalls.last, [true, false, false]);
    expect(h.kgCalls.last, 102.5);
    await _drag(t, -112);
    expect(_selected(t), '105');
    expect(h.kgCalls.last, 105.0);

    await _type(t, '107');
    expect(_selected(t), '107');
    expect(h.modeCalls.last, [false, false, true]);
    expect(h.kgCalls.last, 107.0);
    expect(_neighbours(t), containsAll(['106', '108']));
    await _drag(t, -112);
    expect(_selected(t), '108');
    expect(h.kgCalls.last, 108.0);

    await _type(t, '107.5');
    expect(_selected(t), '107.5');
    expect(h.modeCalls.last, [true, false, false]);
    await _drag(t, -112);
    expect(_selected(t), '110');

    // ritorno al passo standard sopra 100: 110 con base (5)
    await _type(t, '110');
    expect(_selected(t), '110');
    expect(h.modeCalls.last, [false, false, false]);
    await _drag(t, -112);
    expect(_selected(t), '115');
  });

  // ---------- LIBBRE ----------
  testWidgets('L1) lb: passo 5 + 21 lb -> passo 1', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20 / 2.2046226218, lb: true));
    expect(_selected(t), '20');
    await _type(t, '21');
    expect(_selected(t), '21');
    expect(h.modeCalls.last, [false, false, true]);
    expect((h.kgCalls.last * 2.2046226218 - 21).abs() < 0.01, true);
    await _drag(t, -112);
    expect(_selected(t), '22');
    expect((h.kgCalls.last * 2.2046226218 - 22).abs() < 0.01, true);
    h.rebuild();
    await _settle(t);
    expect(_selected(t), '22');
  });

  testWidgets('L2) lb: passo 5 + 22,5 lb -> passo 2,5', (t) async {
    final h = await _pump(t, const _Harness(initialKg: 20 / 2.2046226218, lb: true));
    await _type(t, '22.5');
    expect(_selected(t), '22.5');
    expect(h.modeCalls.last, [true, false, false]);
    await _drag(t, -112);
    expect(_selected(t), '25');
  });

  testWidgets('L3) lb: passo 1 + 25 lb -> passo 5', (t) async {
    final h = await _pump(
      t,
      const _Harness(initialKg: 21 / 2.2046226218, lb: true, s: true),
    );
    expect(_selected(t), '21');
    await _type(t, '25');
    expect(_selected(t), '25');
    expect(h.modeCalls.last, [false, false, false]);
    await _drag(t, -112);
    expect(_selected(t), '30');
  });

  testWidgets('L4) lb: oltre 300 lb, 305 lb', (t) async {
    final h = await _pump(
      t,
      const _Harness(initialKg: 300 / 2.2046226218, lb: true),
    );
    await _type(t, '305');
    // ignore: avoid_print
    print('305lb -> sel=${_selected(t)} mode=${h.modeCalls.last} '
        'vicini=${_neighbours(t)}');
    expect(_selected(t), '305');
  });
}
