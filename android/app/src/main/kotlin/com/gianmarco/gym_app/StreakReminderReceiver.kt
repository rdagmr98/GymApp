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
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val isSamsung = Build.MANUFACTURER.lowercase() == "samsung"
        // Samsung: IMPORTANCE_HIGH (heads-up, suona) — altri dispositivi: IMPORTANCE_DEFAULT (silenzioso, no sveglia)
        val channelId = if (isSamsung) "streak_reminder" else "streak_reminder_default"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val importance = if (isSamsung) NotificationManager.IMPORTANCE_HIGH else NotificationManager.IMPORTANCE_DEFAULT
            nm.createNotificationChannel(NotificationChannel(channelId, "Streak Reminder", importance))
        }

        val title = intent.getStringExtra("title") ?: "🔥 Non perdere i tuoi progressi!"
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
            .setPriority(if (isSamsung) NotificationCompat.PRIORITY_HIGH else NotificationCompat.PRIORITY_DEFAULT)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setAutoCancel(true)
            .setContentIntent(launchPendingIntent)
        if (isSamsung) builder.setDefaults(NotificationCompat.DEFAULT_ALL)

        nm.notify(9901, builder.build())

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
        val nextTriggerAt = System.currentTimeMillis() + AlarmManager.INTERVAL_DAY
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (isSamsung) {
                alarmManager.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, nextTriggerAt, pendingIntent)
            } else {
                // RTC (non wakeup) + inexact: non appare come sveglia nel Clock su Pixel/stock Android
                alarmManager.setAndAllowWhileIdle(AlarmManager.RTC, nextTriggerAt, pendingIntent)
            }
        } else {
            if (isSamsung) {
                alarmManager.setExact(AlarmManager.RTC_WAKEUP, nextTriggerAt, pendingIntent)
            } else {
                alarmManager.set(AlarmManager.RTC, nextTriggerAt, pendingIntent)
            }
        }
        context.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
            .edit()
            .putString("flutter.streak_reminder_next_fire", nextTriggerAt.toString())
            .apply()
    }
}
