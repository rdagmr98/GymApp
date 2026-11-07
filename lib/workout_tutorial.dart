import 'package:flutter/material.dart';
import 'app_l.dart';

/// Tutorial a pagine (scorri o AVANTI), ultima pagina = prova guidata.
class WorkoutTutorial extends StatefulWidget {
  final Color accentColor;
  final VoidCallback onComplete;
  final Future<void> Function()? onStartDemo;

  const WorkoutTutorial({
    super.key,
    required this.accentColor,
    required this.onComplete,
    this.onStartDemo,
  });

  @override
  State<WorkoutTutorial> createState() => _WorkoutTutorialState();
}

class _WorkoutTutorialState extends State<WorkoutTutorial> {
  final PageController _pages = PageController();
  int _page = 0;
  bool _demoCompleted = false;
  bool _loading = false;

  static const _count = 4;

  @override
  void dispose() {
    _pages.dispose();
    super.dispose();
  }

  Future<void> _startDemo() async {
    if (_loading) return;
    if (widget.onStartDemo == null) {
      widget.onComplete();
      return;
    }
    setState(() => _loading = true);
    await widget.onStartDemo!();
    if (mounted) {
      setState(() {
        _loading = false;
        _demoCompleted = true;
      });
    }
  }

  void _go(int p) => _pages.animateToPage(p, duration: const Duration(milliseconds: 320), curve: Curves.easeOutCubic);

  bool get _dark => Theme.of(context).brightness == Brightness.dark;
  Color get _bg => _dark ? const Color(0xFF0E0E10) : const Color(0xFFF2F2F7);
  Color get _fg => _dark ? Colors.white : Colors.black87;
  Color get _muted => _dark ? Colors.white60 : Colors.black54;
  Color get _card => _dark ? const Color(0xFF1C1C1E) : Colors.white;

  @override
  Widget build(BuildContext context) {
    if (_demoCompleted) return _buildCompletionScreen();
    final accent = widget.accentColor;
    final last = _page == _count - 1;
    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(8, 4, 8, 0),
              child: Row(children: [
                AnimatedOpacity(
                  opacity: _page > 0 ? 1 : 0,
                  duration: const Duration(milliseconds: 200),
                  child: IconButton(
                    icon: Icon(Icons.arrow_back_rounded, color: _muted),
                    onPressed: _page > 0 ? () => _go(_page - 1) : null,
                  ),
                ),
                const Spacer(),
                TextButton(
                  onPressed: widget.onComplete,
                  child: Text(AppL.skip, style: TextStyle(color: _muted, fontSize: 14)),
                ),
              ]),
            ),
            Expanded(
              child: PageView(
                controller: _pages,
                onPageChanged: (p) => setState(() => _page = p),
                children: [
                  _hero(accent, Icons.fitness_center_rounded, AppL.welcomeTitle, AppL.tutorialSubtitle),
                  _list(accent, AppL.tutorialHowItWorks, [
                    (Icons.play_arrow_rounded, AppL.tutorialStep1Title, AppL.tutorialStep1Body),
                    (Icons.edit_note_rounded, AppL.tutorialStep2Title, AppL.tutorialStep2Body),
                    (Icons.timer_outlined, AppL.tutorialStep3Title, AppL.tutorialStep3Body),
                    (Icons.skip_next_rounded, AppL.nextSet, AppL.tutorialStep4Body),
                  ], numbered: true),
                  _list(accent, AppL.tutorialFeatures, [
                    (Icons.history_rounded, AppL.tutorialMemoryTitle, AppL.tutorialMemoryBody),
                    (Icons.show_chart_rounded, AppL.tutorialChartsTitle, AppL.tutorialChartsBody),
                    (Icons.local_fire_department_outlined, AppL.tutorialStreakTitle, AppL.tutorialStreakBody),
                  ]),
                  _hero(accent, Icons.sports_esports_outlined, AppL.tutorialDemoTitle, AppL.tutorialDemoBody),
                ],
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                for (int i = 0; i < _count; i++)
                  AnimatedContainer(
                    duration: const Duration(milliseconds: 250),
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    width: i == _page ? 22 : 7,
                    height: 7,
                    decoration: BoxDecoration(
                      color: i == _page ? accent : _muted.withAlpha(60),
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 20, 24, 24),
              child: SizedBox(
                width: double.infinity,
                height: 54,
                child: FilledButton(
                  style: FilledButton.styleFrom(
                    backgroundColor: accent,
                    foregroundColor: Colors.black,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                  onPressed: _loading ? null : (last ? _startDemo : () => _go(_page + 1)),
                  child: _loading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black))
                      : Text(last ? AppL.tutorialStartDemo : AppL.nextBtn,
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _badge(Color accent, IconData icon, double size) => Container(
    width: size,
    height: size,
    decoration: BoxDecoration(shape: BoxShape.circle, color: accent.withAlpha(_dark ? 30 : 40)),
    child: Icon(icon, color: accent, size: size * 0.48),
  );

  Widget _hero(Color accent, IconData icon, String title, String body) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 32),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _badge(accent, icon, 112),
          const SizedBox(height: 32),
          Text(title,
              textAlign: TextAlign.center,
              style: TextStyle(color: _fg, fontSize: 26, fontWeight: FontWeight.w800, height: 1.2)),
          const SizedBox(height: 12),
          Text(body, textAlign: TextAlign.center, style: TextStyle(color: _muted, fontSize: 15, height: 1.4)),
        ],
      ),
    );
  }

  Widget _list(Color accent, String title, List<(IconData, String, String)> items, {bool numbered = false}) {
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(24, 24, 24, 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: TextStyle(color: _fg, fontSize: 24, fontWeight: FontWeight.w800)),
          const SizedBox(height: 20),
          for (int i = 0; i < items.length; i++)
            Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: _card, borderRadius: BorderRadius.circular(16)),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _badge(accent, items[i].$1, 44),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(numbered ? '${i + 1}. ${items[i].$2}' : items[i].$2,
                            style: TextStyle(color: _fg, fontWeight: FontWeight.w700, fontSize: 15)),
                        const SizedBox(height: 4),
                        Text(items[i].$3, style: TextStyle(color: _muted, fontSize: 13, height: 1.35)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildCompletionScreen() {
    final accent = widget.accentColor;
    return Scaffold(
      backgroundColor: _bg,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            children: [
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _badge(accent, Icons.check_rounded, 112),
                    const SizedBox(height: 32),
                    Text(AppL.tutorialCompleteTitle,
                        textAlign: TextAlign.center,
                        style: TextStyle(color: _fg, fontSize: 26, fontWeight: FontWeight.w800)),
                    const SizedBox(height: 12),
                    Text(AppL.tutorialCompleteBody,
                        textAlign: TextAlign.center,
                        style: TextStyle(color: _muted, fontSize: 15, height: 1.4)),
                  ],
                ),
              ),
              SizedBox(
                width: double.infinity,
                height: 54,
                child: FilledButton(
                  style: FilledButton.styleFrom(
                    backgroundColor: accent,
                    foregroundColor: Colors.black,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  ),
                  onPressed: widget.onComplete,
                  child: Text(AppL.startRealWorkout, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
