package com.gianmarco.gym_app

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.RemoteViews

class GymWidgetProvider : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        for (widgetId in appWidgetIds) {
            val options = appWidgetManager.getAppWidgetOptions(widgetId)
            val minWidth = options.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH, 250)
            updateWidget(context, appWidgetManager, widgetId, minWidth)
        }
    }

    override fun onAppWidgetOptionsChanged(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetId: Int,
        newOptions: Bundle
    ) {
        super.onAppWidgetOptionsChanged(context, appWidgetManager, appWidgetId, newOptions)
        val minWidth = newOptions.getInt(AppWidgetManager.OPTION_APPWIDGET_MIN_WIDTH, 250)
        updateWidget(context, appWidgetManager, appWidgetId, minWidth)
    }

    companion object {

        private fun parseJsonArray(json: String): List<String> {
            if (json.length <= 2) return emptyList()
            val inner = json.trim().trimStart('[').trimEnd(']')
            return inner.split(",").map { it.trim().trim('"') }.filter { it.isNotEmpty() }
        }

        private fun muscleDrawable(muscleName: String): Int {
            return when (muscleName) {
                "petto"   -> R.drawable.wm_petto
                "gambe"   -> R.drawable.wm_gambe
                "spalle"  -> R.drawable.wm_spalle
                "braccia" -> R.drawable.wm_braccia
                "dorso"   -> R.drawable.wm_dorso
                "glutei"  -> R.drawable.wm_glutei
                "pull"    -> R.drawable.wm_pull
                "push"    -> R.drawable.wm_push
                else      -> 0
            }
        }

        fun updateWidget(
            context: Context,
            appWidgetManager: AppWidgetManager,
            widgetId: Int,
            widgetWidth: Int = 250
        ) {
            try {
                val prefs = context.getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)

                val streak = try {
                    prefs.getLong("flutter.widget_streak", 0L)
                } catch (e: ClassCastException) {
                    prefs.getInt("flutter.widget_streak", 0).toLong()
                }

                val nextWorkout = prefs.getString("flutter.widget_next_workout", "—") ?: "—"
                val nextMuscle = prefs.getString("flutter.widget_next_muscle", "") ?: ""

                val sessionNamesJson = prefs.getString("flutter.widget_session_names", "[]") ?: "[]"
                val sessionNames = parseJsonArray(sessionNamesJson)

                val doneJson = prefs.getString("flutter.microcycle_done", "[]") ?: "[]"
                val doneSessions = parseJsonArray(doneJson).toSet()

                val views = RemoteViews(context.packageName, R.layout.gym_widget)

                views.setTextViewText(R.id.widget_streak, "\uD83D\uDD25 $streak")
                views.setTextViewText(R.id.widget_workout, nextWorkout)

                // Muscle image: show/hide based on width and available image
                val drawableId = muscleDrawable(nextMuscle)
                if (widgetWidth >= 180 && drawableId != 0) {
                    views.setImageViewResource(R.id.widget_muscle, drawableId)
                    views.setViewVisibility(R.id.widget_muscle_container, View.VISIBLE)
                } else {
                    views.setViewVisibility(R.id.widget_muscle_container, View.GONE)
                }

                // Session dots
                val badgeIds = intArrayOf(
                    R.id.widget_badge_1, R.id.widget_badge_2, R.id.widget_badge_3,
                    R.id.widget_badge_4, R.id.widget_badge_5
                )
                val doneCount = doneSessions.size
                val totalCount = sessionNames.size

                for (i in 0 until 5) {
                    val badgeId = badgeIds[i]
                    if (i < sessionNames.size) {
                        val name = sessionNames[i]
                        when {
                            doneSessions.contains(name) -> {
                                views.setInt(badgeId, "setBackgroundResource", R.drawable.widget_circle_done)
                            }
                            name == nextWorkout -> {
                                views.setInt(badgeId, "setBackgroundResource", R.drawable.widget_circle_active)
                            }
                            else -> {
                                views.setInt(badgeId, "setBackgroundResource", R.drawable.widget_circle_pending)
                            }
                        }
                        views.setTextViewText(badgeId, "")
                        views.setViewVisibility(badgeId, View.VISIBLE)
                    } else {
                        views.setViewVisibility(badgeId, View.INVISIBLE)
                    }
                }

                views.setTextViewText(R.id.widget_progress_label, "$doneCount/$totalCount")

                val launchIntent = Intent(context, MainActivity::class.java).apply {
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
                }
                val pi = PendingIntent.getActivity(
                    context, 0, launchIntent,
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
                )
                views.setOnClickPendingIntent(R.id.widget_root, pi)
                views.setOnClickPendingIntent(R.id.widget_start_btn, pi)

                appWidgetManager.updateAppWidget(widgetId, views)
            } catch (e: Exception) {
                try {
                    val views = RemoteViews(context.packageName, R.layout.gym_widget)
                    views.setTextViewText(R.id.widget_streak, "\uD83D\uDD25 0")
                    views.setTextViewText(R.id.widget_workout, "Apri app")
                    appWidgetManager.updateAppWidget(widgetId, views)
                } catch (_: Exception) {}
            }
        }
    }
}