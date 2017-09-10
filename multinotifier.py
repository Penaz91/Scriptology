#!/usr/bin/env python3
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gi
import alsaaudio
from os.path import join as pj
from subprocess import Popen, PIPE
gi.require_version("Notify", "0.7")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf, Notify, GLib
from syslog import syslog
import dbus.service


d = pj("/", "home", "penaz", "Varie", "Progetti",
       "Roba In Python", "multinotifier")


class Notifier(object):
    def __init__(self):
        syslog("Creating icons")
        self.audio_icons = (GdkPixbuf.Pixbuf.new_from_file(
            pj(d, "audio_muted.svg")),
                            GdkPixbuf.Pixbuf.new_from_file(
                                pj(d, "audio_low.svg")),
                            GdkPixbuf.Pixbuf.new_from_file(
                                pj(d, "audio_medium.svg")),
                            GdkPixbuf.Pixbuf.new_from_file(
                                pj(d, "audio_high.svg"))
                            )
        self.batt_icons = (GdkPixbuf.Pixbuf.new_from_file(
            pj(d, "battery_low.svg")),
                           GdkPixbuf.Pixbuf.new_from_file(
                               pj(d, "battery_plugged.svg")),
                           GdkPixbuf.Pixbuf.new_from_file(
                               pj(d, "battery_unplugged.svg"))
                           )
        self.backup_icon = GdkPixbuf.Pixbuf.new_from_file(pj(d, "backup.svg"))
        self.bright_icon = GdkPixbuf.Pixbuf.new_from_file(
                pj(d, "brightness.svg"))
        syslog("Initializing Notifications")
        Notify.init("Notification System")
        self.barnotification = Notify.Notification.new("MultiNotifier")
        self.normalnotification = Notify.Notification.new("MultiNotifier")
        DBusGMainLoop(set_as_default=True)
        self.dbus_session = dbus.SessionBus()
        syslog("Requesting Names")
        self.dbus_session.request_name("com.penaz.AudioChanged")
        self.dbus_session.request_name("com.penaz.StopListening")
        self.dbus_session.request_name("com.penaz.BrightnessChanged")
        self.dbus_session.request_name("com.penaz.LowBattery")
        self.dbus_session.request_name("com.penaz.PowerPlugged")
        self.dbus_session.request_name("com.penaz.PowerUnplugged")
        self.dbus_session.request_name("com.penaz.BackupStart")
        self.dbus_session.request_name("com.penaz.BackupErr")
        self.dbus_session.request_name("com.penaz.SpaceLow")
        self.dbus_session.request_name("com.penaz.BackupEnd")
        syslog("Adding signal receivers")
        self.dbus_session.add_signal_receiver(
                self.backupStart,
                dbus_interface="com.penaz",
                signal_name="BackupStart")
        self.dbus_session.add_signal_receiver(
                self.backupLow,
                dbus_interface="com.penaz",
                signal_name="SpaceLow")
        self.dbus_session.add_signal_receiver(
                self.backupErr, dbus_interface="com.penaz",
                signal_name="BackupErr")
        self.dbus_session.add_signal_receiver(
                self.backupEnd, dbus_interface="com.penaz",
                signal_name="BackupEnd")
        self.dbus_session.add_signal_receiver(
                self.stop, dbus_interface="com.penaz",
                signal_name="StopListening")
        self.dbus_session.add_signal_receiver(
                self.audio_changed, dbus_interface="com.penaz",
                signal_name="AudioChanged")
        self.dbus_session.add_signal_receiver(
                self.brightness_changed, dbus_interface="com.penaz",
                signal_name="BrightnessChanged")
        self.dbus_session.add_signal_receiver(
                self.low_battery, dbus_interface="com.penaz",
                signal_name="LowBattery")
        self.dbus_session.add_signal_receiver(
                self.power_plugged, dbus_interface="com.penaz",
                signal_name="PowerPlugged")
        self.dbus_session.add_signal_receiver(
                self.power_unplugged, dbus_interface="com.penaz",
                signal_name="PowerUnplugged")
        self.loop = GLib.MainLoop()
        syslog("MultiNotification Daemon objects created successfully")
        self.loop.run()

    def stop(self):
        self.loop.quit()
        syslog("MultiNotification Daemon Stopped")

    def audio_changed(self):
        syslog("Received Audio change Signal")
        mix = alsaaudio.Mixer()
        muted = mix.getmute()
        volume = mix.getvolume()
        icon = self.audio_icons[0]
        if muted == [1, 1]:
            self.barnotification.update("MultiNotifier", "")
            self.barnotification.set_image_from_pixbuf(self.audio_icons[0])
            self.barnotification.set_hint_int32("value", 0)
            self.barnotification.show()
        else:
            if volume[0] <= 33:
                icon = self.audio_icons[1]
            elif volume[0] <= 66:
                icon = self.audio_icons[2]
            else:
                icon = self.audio_icons[3]
            self.barnotification.update("MultiNotifier", "")
            self.barnotification.set_image_from_pixbuf(icon)
            self.barnotification.set_hint_int32("value", volume[0])
            self.barnotification.show()

    def brightness_changed(self):
        bright = float(Popen(["xbacklight", "-get"], stdout=PIPE).communicate()[0])
        self.barnotification.update("MultiNotifier", "")
        self.barnotification.set_image_from_pixbuf(self.bright_icon)
        self.barnotification.set_hint_int32("value", bright)
        self.barnotification.show()

    def low_battery(self):
        self.normalnotification.update("MultiNotifier", "Battery Low")
        self.normalnotification.set_image_from_pixbuf(self.batt_icons[0])
        self.normalnotification.show()

    def backup(self, message):
        self.normalnotification.update("MultiNotifier", message)
        self.normalnotification.set_image_from_pixbuf(self.backup_icon)
        self.normalnotification.show()

    def backupStart(self):
        self.backup("Inizio Backup Giornaliero")

    def backupLow(self):
        self.backup("Spazio sulla partizione di Backup inferiore al 10%")

    def backupEnd(self):
        self.backup("Backup terminato")

    def backupErr(self):
        self.backup("Si è verificato un errore durante il backup")

    def power_plugged(self):
        self.normalnotification.update("MultiNotifier", "AC Adapter Plugged")
        self.normalnotification.set_image_from_pixbuf(self.batt_icons[1])
        self.normalnotification.show()

    def power_unplugged(self):
        self.normalnotification.update("MultiNotifier", "AC Adapter Unplugged")
        self.normalnotification.set_image_from_pixbuf(self.batt_icons[2])
        self.normalnotification.show()


if __name__ == "__main__":
    Notifier()
