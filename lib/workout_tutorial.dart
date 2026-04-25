import 'package:flutter/material.dart';

/// Tutorial interattivo: mostra una schermata introduttiva,
/// poi lancia il vero WorkoutEngine in modalità demo (nessun dato salvato).
class WorkoutTutorial extends StatefulWidget {
  final Color accentColor;
  /// Chiamato quando il tutorial è completato (avvia il vero allenamento).
  final VoidCallback onComplete;
  /// Callback che lancia il WorkoutEngine in demoMode e restituisce un Future
  /// che si completa quando l'utente finisce o esce dalla demo.
  /// Se null, il tutorial passa direttamente a onComplete (es. web).
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
      body: Center(
        child: CircularProgressIndicator(color: widget.accentColor),
      ),
    );
  }

  Widget _buildIntroScreen() {
    final accent = widget.accentColor;
    return Scaffold(
      backgroundColor: const Color(0xFF0E0E10),
      body: SafeArea(
        child: Column(
          children: [
            // Top bar con Salta
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Tutorial',
                    style: TextStyle(
                      color: accent,
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  TextButton(
                    onPressed: widget.onComplete,
                    child: Text(
                      'Salta',
                      style: TextStyle(color: Colors.white54, fontSize: 14),
                    ),
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
                    // Icona animata
                    ScaleTransition(
                      scale: _pulseAnim,
                      child: Container(
                        width: 100,
                        height: 100,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: accent.withAlpha(30),
                          border: Border.all(color: accent.withAlpha(120), width: 2),
                        ),
                        child: Center(
                          child: Text(
                            '🏋️',
                            style: TextStyle(fontSize: 52),
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    Text(
                      'Benvenuto in GymApp!',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 26,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Il tuo diario di allenamento intelligente',
                      style: TextStyle(color: Colors.white54, fontSize: 14),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 28),
                    _buildFeatureCard(
                      accent,
                      icon: '⚡',
                      title: 'Timer automatico',
                      body: 'Il recupero parte da solo a fine serie — tu ti concentri solo sul ferro.',
                    ),
                    const SizedBox(height: 12),
                    _buildFeatureCard(
                      accent,
                      icon: '🧠',
                      title: 'L\'app ricorda i tuoi pesi',
                      body: 'GymApp suggerisce automaticamente il peso usato l\'ultima volta.',
                    ),
                    const SizedBox(height: 12),
                    _buildFeatureCard(
                      accent,
                      icon: '📊',
                      title: 'Grafici e progressi',
                      body: 'Tieni traccia dei tuoi progressi sessione dopo sessione.',
                    ),
                    const SizedBox(height: 12),
                    _buildFeatureCard(
                      accent,
                      icon: '🎯',
                      title: 'Streak e badge',
                      body: 'Mantieni la continuità e sblocca badge per ogni allenamento completato.',
                    ),
                    const SizedBox(height: 32),
                    // Info prova
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
                          const Text('💡', style: TextStyle(fontSize: 22)),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Prova con un allenamento reale',
                                  style: TextStyle(
                                    color: accent,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 14,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                const Text(
                                  'Fai una prova completa con Panca Piana e Trazioni (2 serie ciascuno). Puoi inserire il peso con i tasti veloci o dalla tastiera.\nNessun dato verrà salvato.',
                                  style: TextStyle(
                                    color: Colors.white70,
                                    fontSize: 13,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 32),
                    // Bottone principale
                    SizedBox(
                      width: double.infinity,
                      height: 56,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: accent,
                          foregroundColor: Colors.black,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        onPressed: _startDemo,
                        child: const Text(
                          'Inizia la prova 💪',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 17,
                          ),
                        ),
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

  Widget _buildFeatureCard(
    Color accent, {
    required String icon,
    required String title,
    required String body,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(8),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(icon, style: const TextStyle(fontSize: 26)),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  body,
                  style: const TextStyle(color: Colors.white60, fontSize: 13),
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
      backgroundColor: const Color(0xFF0E0E10),
      body: SafeArea(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.greenAccent.withAlpha(30),
                    border: Border.all(
                      color: Colors.greenAccent.withAlpha(120),
                      width: 2,
                    ),
                  ),
                  child: const Center(
                    child: Text('🎉', style: TextStyle(fontSize: 52)),
                  ),
                ),
                const SizedBox(height: 28),
                const Text(
                  'Sei pronto!',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                const Text(
                  'Hai completato la prova e conosci già tutte le funzioni essenziali di GymApp. Adesso inizia il tuo vero allenamento!',
                  style: TextStyle(color: Colors.white70, fontSize: 15),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 40),
                SizedBox(
                  width: double.infinity,
                  height: 56,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: accent,
                      foregroundColor: Colors.black,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    onPressed: widget.onComplete,
                    child: const Text(
                      'Inizia il vero allenamento! 🚀',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
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
