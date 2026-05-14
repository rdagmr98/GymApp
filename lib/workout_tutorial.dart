import 'package:flutter/material.dart';
import 'app_l.dart';

/// Interactive tutorial widget for GymApp.
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

class _WorkoutTutorialState extends State<WorkoutTutorial>
    with SingleTickerProviderStateMixin {
  bool _demoStarted = false;
  bool _demoCompleted = false;
  bool _loading = false;

  late final AnimationController _pulseCtrl;
  late final Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();
    _pulseCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
    _pulseAnim = Tween<double>(begin: 1.0, end: 1.08).animate(
      CurvedAnimation(parent: _pulseCtrl, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _pulseCtrl.dispose();
    super.dispose();
  }

  Future<void> _startDemo() async {
    if (_loading) return;
    if (widget.onStartDemo == null) {
      widget.onComplete();
      return;
    }
    setState(() {
      _demoStarted = true;
      _loading = true;
    });
    await widget.onStartDemo!();
    if (mounted) {
      setState(() {
        _loading = false;
        _demoCompleted = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_demoCompleted) return _buildCompletionScreen();
    if (_demoStarted && _loading) return _buildLoadingScreen();
    return _buildIntroScreen();
  }

  Widget _buildLoadingScreen() {
    return Scaffold(
      backgroundColor: const Color(0xFF0E0E10),
      body: Center(child: CircularProgressIndicator(color: widget.accentColor)),
    );
  }

  Widget _buildIntroScreen() {
    final accent = widget.accentColor;
    return Scaffold(
      backgroundColor: const Color(0xFF0E0E10),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(AppL.tutorialTitle,
                      style: TextStyle(color: accent, fontWeight: FontWeight.bold, fontSize: 16)),
                  TextButton(
                    onPressed: widget.onComplete,
                    child: Text(AppL.skip,
                        style: const TextStyle(color: Colors.white54, fontSize: 14)),
                  ),
                ],
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Column(
                  children: [
                    const SizedBox(height: 8),
                    ScaleTransition(
                      scale: _pulseAnim,
                      child: Container(
                        width: 100, height: 100,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: accent.withAlpha(30),
                          border: Border.all(color: accent.withAlpha(120), width: 2),
                        ),
                        child: const Center(child: Text('🏋️', style: TextStyle(fontSize: 52))),
                      ),
                    ),
                    const SizedBox(height: 24),
                    Text(AppL.welcomeTitle,
                        style: const TextStyle(color: Colors.white, fontSize: 26, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center),
                    const SizedBox(height: 8),
                    Text(AppL.tutorialSubtitle,
                        style: const TextStyle(color: Colors.white54, fontSize: 14),
                        textAlign: TextAlign.center),
                    const SizedBox(height: 28),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.white.withAlpha(8),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: Colors.white.withAlpha(20)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(AppL.tutorialHowItWorks,
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                          const SizedBox(height: 14),
                          _step(accent, '1', '💪', AppL.tutorialStep1Title, AppL.tutorialStep1Body),
                          const SizedBox(height: 10),
                          _step(accent, '2', '📝', AppL.tutorialStep2Title, AppL.tutorialStep2Body),
                          const SizedBox(height: 10),
                          _step(accent, '3', '⏱️', AppL.tutorialStep3Title, AppL.tutorialStep3Body),
                          const SizedBox(height: 10),
                          _step(accent, '4', '🔁', AppL.nextSet, AppL.tutorialStep4Body),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),
                    _featureCard(accent, '🧠', AppL.tutorialMemoryTitle, AppL.tutorialMemoryBody),
                    const SizedBox(height: 12),
                    _featureCard(accent, '📊', AppL.tutorialChartsTitle, AppL.tutorialChartsBody),
                    const SizedBox(height: 12),
                    _featureCard(accent, '🎯', AppL.tutorialStreakTitle, AppL.tutorialStreakBody),
                    const SizedBox(height: 24),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: accent.withAlpha(25),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: accent.withAlpha(80)),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('🎮', style: TextStyle(fontSize: 22)),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(AppL.tutorialDemoTitle,
                                    style: TextStyle(color: accent, fontWeight: FontWeight.bold, fontSize: 14)),
                                const SizedBox(height: 4),
                                Text(AppL.tutorialDemoBody,
                                    style: const TextStyle(color: Colors.white70, fontSize: 13)),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),
                    SizedBox(
                      width: double.infinity, height: 56,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: accent, foregroundColor: Colors.black,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        onPressed: _startDemo,
                        child: Text(AppL.tutorialStartDemo,
                            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 17)),
                      ),
                    ),
                    const SizedBox(height: 32),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _step(Color accent, String num, String icon, String title, String body) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 24, height: 24,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: accent.withAlpha(40),
            border: Border.all(color: accent.withAlpha(120), width: 1),
          ),
          child: Center(
              child: Text(num, style: TextStyle(color: accent, fontSize: 12, fontWeight: FontWeight.bold))),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                Text(icon, style: const TextStyle(fontSize: 16)),
                const SizedBox(width: 6),
                Flexible(child: Text(title,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13))),
              ]),
              const SizedBox(height: 2),
              Text(body, style: const TextStyle(color: Colors.white54, fontSize: 12)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _featureCard(Color accent, String icon, String title, String body) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
          color: Colors.white.withAlpha(8), borderRadius: BorderRadius.circular(14)),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(icon, style: const TextStyle(fontSize: 26)),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                const SizedBox(height: 4),
                Text(body, style: const TextStyle(color: Colors.white60, fontSize: 13)),
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
      backgroundColor: const Color(0xFF0E0E10),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 100, height: 100,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.greenAccent.withAlpha(30),
                    border: Border.all(color: Colors.greenAccent.withAlpha(120), width: 2),
                  ),
                  child: const Center(child: Text('🎉', style: TextStyle(fontSize: 52))),
                ),
                const SizedBox(height: 28),
                Text(AppL.tutorialCompleteTitle,
                    style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                Text(AppL.tutorialCompleteBody,
                    style: const TextStyle(color: Colors.white70, fontSize: 15),
                    textAlign: TextAlign.center),
                const SizedBox(height: 40),
                SizedBox(
                  width: double.infinity, height: 56,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: accent, foregroundColor: Colors.black,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    ),
                    onPressed: widget.onComplete,
                    child: Text(AppL.startRealWorkout,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
