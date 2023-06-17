""" GUI class"""
from typing import Protocol
import tkinter as tk
import ttkbootstrap as ttk

from robomouse.utilities import MouseState, SettingsElement, Movement, Color, SettingsStrings

# window params
WINDOW_MAIN_SIZE = "445x120"
WINDOW_MAIN_TITLE = "Move it !"

WINDOW_SETTINGS_SIZE = "280x200"
WINDOW_SETTINGS_TITLE = "Settings"


class Presenter(Protocol):
    """Protocol implementation for Presenter"""
    def handle_get_saved_settings(self):
        ...

    def handle_save_settings_data(self, settings_obj: SettingsElement):
        ...

    def handle_exit_button(self):
        ...

    def transfer_mouse_state(self, mouse_active: MouseState):
        ...


class Gui(ttk.Window):
    """Class implements the main window """

    def __init__(self, style_name):
        """Create entire GUI frame """
        super().__init__(themename=style_name)
        self.title(WINDOW_MAIN_TITLE)
        self.geometry(WINDOW_MAIN_SIZE)
        self.resizable(False, False)

        self._mouse_state = MouseState.ACTIVE
        self.data_to_be_sent = None
        self.settings_win = None
        self._loaded_settings = None
        self.presenter = None
        self.lbl_status = None

    def create_gui(self, presenter):
        """ Create main window gui """
        self.presenter = presenter
        self._loaded_settings, use_custom  = self.presenter.handle_get_saved_settings()
        #TODO
        print(f'GUI > loaded settings \n{self._loaded_settings}')

        frm_main = ttk.Frame()

        frm_btn_toggle = ttk.Frame(master=frm_main)
        btn_toggle = ttk.Button(master=frm_btn_toggle, text="Toggle me !!!",
                                command=self._toggle_state,
                                bootstyle="dark")
        btn_toggle.pack(expand=True, fill="both", padx=5, pady=5)
        frm_btn_toggle.pack(expand=True, fill="both")

        frm_status = ttk.Frame(master=frm_main)
        tk.Label(master=frm_status, text="Status:", anchor="e").pack(side="left",
                                                                          expand=True,
                                                                          fill="both",
                                                                          anchor="e",
                                                                          pady=5, padx=5)
        self.lbl_status = tk.Label(master=frm_status,
                            font=(None, 18, "bold"),
                            text=self._mouse_state.name.title())
        self.lbl_status.configure(width="8")
        self.lbl_status.pack(side="left",
                        expand=True,
                        fill="both",
                        anchor="center",
                        pady=5, padx=5)
        lbl_executions = ttk.Label(master=frm_status, text="0")
        lbl_executions.configure(width="8")
        lbl_executions.pack(side="left",
                            expand=True,
                            fill="both",
                            anchor="w")
        frm_status.pack(expand=True, fill="both")

        frm_navigation = ttk.Frame(master=frm_main)
        frm_btn_settings = ttk.Frame(master=frm_navigation)
        btn_settings = ttk.Button(master=frm_btn_settings,
                                    text="Settings",
                                    width=10,
                                    command=self._show_settings,
                                    bootstyle="secondary")
        btn_settings.pack(side="left",
                        pady=5,
                        padx=5,
                        anchor="w")
        frm_btn_exit = ttk.Frame(master=frm_navigation)
        self.btn_exit = ttk.Button(master=frm_btn_exit,
                            text="Exit",
                            width=10,
                            command=presenter.handle_exit_button,
                            bootstyle="secondary")
        self.btn_exit.pack(side="right",
                    pady=5,
                    padx=5,
                    anchor="e")
        frm_btn_settings.pack(side="left", expand=True, fill="both")
        frm_btn_exit.pack(side="left", expand=True, fill="both")
        frm_navigation.pack(expand=True, fill="both")

        frm_main.pack(expand=True, fill="both")
        self.update_status()
        if not use_custom:
            ttk.dialogs.dialogs.Messagebox.show_warning(
                message="Error loading saved configuration!\n\tDefault values will be used.",
                title="Configuration loading ...",
                alert =True
            )

    def update_status(self):
        """Update the status label text and color """
        if self._mouse_state == MouseState.INACTIVE:
            use_color = self._loaded_settings.color_disable.value
        else:
            use_color = self._loaded_settings.color_enable.value
        self.lbl_status.config(text=self._mouse_state.name.title())
        self.lbl_status.config(bg=use_color)

    def _toggle_state(self):
        """Toggle internal mouse_state and call update status """
        if self._mouse_state == MouseState.INACTIVE:
            self._mouse_state = MouseState.ACTIVE
        elif self._mouse_state == MouseState.ACTIVE:
            self._mouse_state = MouseState.INACTIVE

        self.update_status()

        # trigger presenter to copy mouse_state data
        self.presenter.transfer_mouse_state(self._mouse_state)

    @property
    def mouse_state(self):
        """Protected var getter """
        return self._mouse_state

    def set_executions_text(self, extra_val):
        """Set the number of executions in a label"""
        self.lbl_executions.config(text=str(extra_val))

    def _show_settings(self):
        """Creates a setting window """
        self.settings_win = SettingsWinManager.get_settings_window(self._loaded_settings,
                                                                   self.presenter)

    def update_settings(self, settings_obj):
        """Updates the settings used for main window """
        self._loaded_settings = settings_obj
        self.update_status()
        print(self._loaded_settings)


class GuiSettings(ttk.Toplevel):
    """Settings window class"""
    def __init__(self, settings, presenter):
        super().__init__()
        self._loaded_settings = settings
        self._active_settings = None
        self.title(WINDOW_SETTINGS_TITLE)
        self.geometry(WINDOW_SETTINGS_SIZE)
        self.resizable(False, False)
        self.presenter = presenter

        self._create_gui_settings()

    def _create_gui_settings(self):
        """Create gui elements """
        frm_settings = ttk.Frame(master=self)
        frm_timing = ttk.Frame(master=frm_settings)
        frm_movement = ttk.Frame(master=frm_settings)
        frm_color_enable = ttk.Frame(master=frm_settings)
        frm_color_disable = ttk.Frame(master=frm_settings)
        frm_navigation = ttk.Frame(master=frm_settings)
        frm_btn_save = ttk.Frame(master=frm_navigation)
        frm_btn_close = ttk.Frame(master=frm_navigation)

        # timing
        tk.Label(master=frm_timing, text=str(SettingsStrings.TIMING) + " [min] ").pack(side="left",
                                                                                        expand=True,
                                                                                        fill="both",
                                                                                        anchor="e")
        self.loop_value = tk.IntVar(master=frm_settings,
                                    value=self._loaded_settings.timing_minutes)
        ttk.Label(master=frm_timing, textvariable=self.loop_value).pack(side="left",
                                                                        padx=10,
                                                                        anchor="e")
        self.scale_timming = ttk.Scale(master=frm_timing,
                                        value=self.loop_value.get(),
                                        from_=1, to=9,
                                        command=self._round_scale_value,
                                        bootstyle="info")
        self.scale_timming.pack(side="left", expand=True, fill="both", pady=5, anchor="w")
        frm_timing.pack(expand=True, fill="both")

        # move type
        tk.Label(master=frm_movement, text=str(SettingsStrings.MOVEMENT)).pack(side="left",
                                                                            expand=True,
                                                                            fill="both",
                                                                            anchor="e")
        self.movement_value = tk.IntVar(master=frm_settings,
                                        value=self._loaded_settings.movement_type.value)
        rbtn_opt1 = ttk.Radiobutton(master=frm_movement,
                                    text=" ".join(Movement.MOVE_AND_CLICK.name.split("_")).capitalize(),
                                    variable=self.movement_value,
                                    value=Movement.MOVE_AND_CLICK.value,
                                    bootstyle="info")
        rbtn_opt1.pack(side="left", expand=True, fill="both", anchor="w")

        rbtn_opt2 = ttk.Radiobutton(master=frm_movement,
                                    text=" ".join(Movement.JITTER.name.split("_")).capitalize(),
                                    variable=self.movement_value,
                                    value=Movement.JITTER.value,
                                    bootstyle="info")
        rbtn_opt2.pack(side="left", expand=True, fill="both", anchor="e")
        frm_movement.pack(expand=True, fill="both")

        # colors
        tk.Label(master=frm_color_enable, text=str(SettingsStrings.COLOR_ENABLE)).pack(side="left",
                                                                                        expand=True,
                                                                                        padx=2, pady=2,
                                                                                        fill="both",
                                                                                        anchor="e")
        self.color_enable = tk.StringVar(master=frm_settings,
                                         value=self._loaded_settings.color_enable.value)
        cbox_enable_color = ttk.Combobox(master=frm_color_enable, state="readonly",
                                              textvariable=self.color_enable,
                                              values=[e.value for e in Color])
        cbox_enable_color.pack(side="left", expand=True, padx=2, pady=2, fill="x", anchor="w")
        frm_color_enable.pack(expand=True, fill="both")

        tk.Label(master=frm_color_disable,
                 text=str(SettingsStrings.COLOR_DISABLE)).pack(side="left",
                                                                    expand=True,
                                                                    padx=2, pady=2,
                                                                    fill="both",
                                                                    anchor="e")
        self.color_disable = tk.StringVar(master=frm_settings,
                                          value=self._loaded_settings.color_disable.value)
        cbox_disable_color = ttk.Combobox(master=frm_color_disable, state="readonly",
                                               textvariable=self.color_disable,
                                               values=[e.value for e in Color])
        cbox_disable_color.pack(side="left", expand=True, padx=2, pady=2, fill="x", anchor="w")
        frm_color_disable.pack(expand=True, fill="both")

        self.btn_save = ttk.Button(master=frm_btn_save,
                                  text="Save",
                                  width=10,
                                  command=self.callback_save_settings,
                                  bootstyle="secondary")
        self.btn_save.pack(side="left", anchor="w")
        frm_btn_save.pack(side="left", expand=True, fill="x")

        btn_close_settings = ttk.Button(master=frm_btn_close,
                                            text="Close",
                                            width=10,
                                            command=self._close_settings,
                                            bootstyle="secondary")
        btn_close_settings.pack(side="right", anchor="e")
        frm_btn_close.pack(side="left", expand=True, fill="x")
        frm_navigation.pack(expand=True, fill="x", pady=5, padx=5)
        frm_settings.pack(expand=True, fill="both", padx=15)

    def callback_save_settings(self):
        """Sends the active settings to presenter """
        active_settings = SettingsElement(self.loop_value.get(),
                                                Movement(self.movement_value.get()),
                                                Color(self.color_enable.get()),
                                                Color(self.color_disable.get()))
        self.presenter.handle_save_settings_data(active_settings)

    def _round_scale_value(self, extra=None):
        """Converts Scale float value to int and saves it in IntVar """
        scale_value = round(self.scale_timming.get())
        if scale_value != self.scale_timming.get():
            self.loop_value.set(scale_value)

    def _close_settings(self):
        """Destroy the setting window """
        SettingsWinManager.destroy_settings_window()


class SettingsWinManager:
    """Window manager that returns the existing object """
    _settings_window = None

    @staticmethod
    def get_settings_window(settings, presenter):
        """Returns a settings windows """
        if not SettingsWinManager._settings_window:
            SettingsWinManager._settings_window = GuiSettings(settings, presenter)
        return SettingsWinManager._settings_window

    @staticmethod
    def destroy_settings_window():
        """Destroys the window object """
        if SettingsWinManager._settings_window:
            SettingsWinManager._settings_window.destroy()
        SettingsWinManager._settings_window = None


if __name__ == "__main__":
    pass
