package com.gianmarco.gym_app

import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat

class StreakReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        // L'allarme è schedulato in anticipo e può sopravvivere a un allenamento nel frattempo
        // (cancel mancato per engine non attivo, Doze, race al risveglio): verifica qui, alla
        // sorgente unica della notifica, se l'utente si è davvero allenato da meno di 2 giorni.
        val prefs = context.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
        val lastWorkoutStr = prefs.getString("flutter.last_workout_date", null)
        if (lastWorkoutStr != null) {
            val lastWorkoutMillis = try {
                java.time.Instant.parse(lastWorkoutStr).toEpochMilli()
            } catch (e: Exception) {
                null
            }
            if (lastWorkoutMillis != null &&
                System.currentTimeMillis() - lastWorkoutMillis < 2 * AlarmManager.INTERVAL_DAY) {
                rescheduleAt(context, lastWorkoutMillis + 2 * AlarmManager.INTERVAL_DAY, null, null)
                return
            }
        }

        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "streak_reminder"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(NotificationChannel(channelId, "Streak Reminder", NotificationManager.IMPORTANCE_HIGH))
        }

        val title = intent.getStringExtra("title") ?: "Non perdere i tuoi progressi!"
        val body = intent.getStringExtra("body")
            ?: "Non ti alleni da 2 giorni. Allenati oggi per non perdere i tuoi progressi!"

        val launchIntent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
        }
        val launchPendingIntent = PendingIntent.getActivity(
            context, 101, launchIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(title)
            .setContentText(body)
            .setStyle(NotificationCompat.BigTextStyle().bigText(body))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setAutoCancel(true)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setContentIntent(launchPendingIntent)

        nm.notify(9901, builder.build())

        rescheduleAt(context, System.currentTimeMillis() + AlarmManager.INTERVAL_DAY, title, body)
    }

    private fun rescheduleAt(context: Context, triggerAt: Long, title: String?, body: String?) {
        val nextIntent = Intent(context, StreakReminderReceiver::class.java).apply {
            putExtra("title", title)
            putExtra("body", body)
        }
        val pendingIntent = PendingIntent.getBroadcast(
            context,
            1991,
            nextIntent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            alarmManager.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, triggerAt, pendingIntent)
        } else {
            alarmManager.set(AlarmManager.RTC_WAKEUP, triggerAt, pendingIntent)
        }
        context.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
            .edit()
            .putString("flutter.streak_reminder_next_fire", triggerAt.toString())
            .apply()
    }
}
