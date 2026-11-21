import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:gym_app/main.dart';

void main() {
  test('parseProgressiGym accetta Map con logs e List', () {
    const mapText = '\uFEFF  TIPO:PROGRESSI_GYM\n'
        '{"clientName":"Mario","logs":['
        '{"exercise":"Panca Piana","series":[{"s":1,"w":60.0,"r":10}],"date":"2026-09-05T20:00:00","dayName":"Push","session_id":"1"},'
        '{"exercise":"","series":[]}'
        ']}';
    final fromMap = parseProgressiGym(mapText);
    expect(fromMap.length, 1);
    expect(fromMap.first['session_id'], '1');

    const listText = 'TIPO:PROGRESSI_GYM\n'
        '[{"exercise":"Cable Curl","series":[{"s":1,"w":20.0,"r":15}],"date":"2026-09-06T19:00:00","dayName":"Pull","session_id":"2"}]';
    final fromList = parseProgressiGym(listText);
    expect(fromList.length, 1);
    expect(fromList.first['exercise'], 'Cable Curl');
  });

  test('parseProgressiGym lancia FormatException su scheda o JSON rotto', () {
    expect(
      () => parseProgressiGym('TIPO:SCHEDA_GYM\n[{"dayName":"Push","exercises":[]}]'),
      throwsFormatException,
    );
    expect(
      () => parseProgressiGym('TIPO:PROGRESSI_GYM\n{rotto'),
      throwsFormatException,
    );
    expect(
      () => parseProgressiGym('TIPO:PROGRESSI_GYM\n{"logs":[]}'),
      throwsFormatException,
    );
  });

  test('mergeProgressi non duplica, aggiunge nuove e ordina per date stabile', () {
    final history = <dynamic>[
      {
        'exercise': 'Cable Curl',
        'series': [{'s': 1, 'w': 20.0, 'r': 12}],
        'date': '2026-09-10T10:00:00',
        'dayName': 'Pull',
        'session_id': 's2',
        'tag': 'orig_first',
      },
      {
        'exercise': 'Lat Pulldown',
        'series': [{'s': 1, 'w': 50.0, 'r': 10}],
        'date': '2026-09-10T10:00:00',
        'dayName': 'Pull',
        'session_id': 's2',
        'tag': 'orig_second',
      },
    ];
    final incoming = <Map<String, dynamic>>[
      // duplicato già presente in history
      {
        'exercise': 'Cable Curl',
        'series': [{'s': 1, 'w': 99.0, 'r': 99}],
        'date': '2026-09-10T10:00:00',
        'dayName': 'Pull',
        'session_id': 's2',
      },
      // voce con data antecedente
      {
        'exercise': 'Pec Deck Fly',
        'series': [{'s': 1, 'w': 20.0, 'r': 10}],
        'date': '2026-09-05T20:00:00',
        'dayName': 'Push',
        'session_id': 's1',
      },
      // duplicato dentro incoming stesso
      {
        'exercise': 'Pec Deck Fly',
        'series': [{'s': 1, 'w': 20.0, 'r': 10}],
        'date': '2026-09-05T20:00:00',
        'dayName': 'Push',
        'session_id': 's1',
      },
    ];

    final added = mergeProgressi(history, incoming);
    expect(added, 1);
    expect(history.length, 3);
    expect(history[0]['session_id'], 's1');
    expect(history[1]['tag'], 'orig_first');
    expect(history[2]['tag'], 'orig_second');
    expect(mergeProgressi(history, incoming), 0);
  });

  test('parse file reale miei_progressi.gymlog', () {
    final f = File(r'C:\Users\Gianmarco\Downloads\miei_progressi.gymlog');
    if (!f.existsSync()) {
      markTestSkipped('File reale miei_progressi.gymlog non presente');
      return;
    }
    final logs = parseProgressiGym(f.readAsStringSync());
    expect(logs.length, greaterThan(100));
  });
}
