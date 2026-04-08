"""
cajero_gui.py — BANCO TECMILENIO  |  ATM v3.0
Interfaz rediseñada con estética de cajero automático profesional moderno.
Lógica de negocio sin cambios; solo mejoras visuales y de estructura.
"""

import tkinter as tk
from tkinter import font as tkfont
import datetime

# ── Datos globales ─────────────────────────────────────────────────────────
users = []

# ══════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES — ATM Moderno (azul marino + teal + dorado)
# ══════════════════════════════════════════════════════════════════════════
ATM_BG          = "#0F1923"   # Cuerpo del cajero (azul marino muy oscuro)
ATM_BEZEL       = "#0B1220"   # Bisel interior

SCR_BG          = "#060E1A"   # Fondo de la pantalla LCD
SCR_HEADER_BG   = "#0A1628"   # Barra superior de la pantalla
SCR_BORDER      = "#1E3A5F"   # Marco exterior de la pantalla
SCR_INNER       = "#0A1628"   # Fondo de los campos de entrada

TXT_WHITE       = "#074719"   # Texto principal
TXT_SECONDARY   = "#7B8FAB"   # Texto secundario (gris azulado)
TXT_TEAL        = "#00C9A7"   # Acento primario de marca (teal)
TXT_GOLD        = "#FFD166"   # Importe / saldo (dorado)
TXT_WARN        = "#F4A261"   # Advertencia (naranja)
TXT_ERR         = "#E63946"   # Error (rojo)
TXT_SUCCESS     = "#2DC653"   # Éxito (verde)

BTN_BG          = "#152032"   # Fondo botón normal
BTN_HOV         = "#1F3352"   # Hover botón normal
BTN_BORDER      = "#2A4A72"   # Borde botón normal
BTN_ACCENT      = "#007F6E"   # Fondo botón acento (confirmar)
BTN_ACCENT_HOV  = "#00A38E"   # Hover botón acento
BTN_DANGER      = "#6B1A20"   # Fondo botón peligro (cancelar)
BTN_DANGER_HOV  = "#8F2530"   # Hover botón peligro

DIVIDER         = "#1E3A5F"   # Línea separadora
GLOW            = "#00C9A7"   # Borde iluminado al enfocar un campo


# ══════════════════════════════════════════════════════════════════════════
# MODELO DE DATOS — sin cambios respecto a la versión anterior
# ══════════════════════════════════════════════════════════════════════════
class Usuario:
    """Representa una cuenta bancaria con saldo e historial."""

    def __init__(self, nombre: str, NIP: str):
        self.nombre    = nombre
        self.NIP       = NIP
        self.saldo     = 0.0
        self.historial = []

    def agregarSaldo(self, monto: float):
        self.saldo += monto
        self.historial.append(("DEP", monto, self.saldo))

    def retirarSaldo(self, monto: float) -> bool:
        if monto > self.saldo:
            return False
        self.saldo -= monto
        self.historial.append(("RET", monto, self.saldo))
        return True

    def ingresar(self, nombre: str, nip: str) -> bool:
        return nombre == self.nombre and nip == self.NIP


# ══════════════════════════════════════════════════════════════════════════
# COMPONENTE: BOTÓN ESTILIZADO CON HOVER
# ══════════════════════════════════════════════════════════════════════════
class ATMButton(tk.Frame):
    """
    Botón con borde de 1 px y efecto hover de color.
    Estilos disponibles: 'normal' | 'accent' | 'danger' | 'numpad'
    """

    _PALETTE = {
        "normal": (BTN_BG,    BTN_HOV,        BTN_BORDER,  TXT_WHITE),
        "accent": (BTN_ACCENT, BTN_ACCENT_HOV, BTN_ACCENT,  TXT_WHITE),
        "danger": (BTN_DANGER, BTN_DANGER_HOV, BTN_DANGER,  TXT_WHITE),
    }

    def __init__(self, parent, text: str, command,
                 style: str = "normal", **kwargs):
        bg_n, bg_h, border, fg = self._PALETTE[style]
        self._bg_normal = bg_n
        self._bg_hover  = bg_h

        super().__init__(parent, bg=border, padx=1, pady=1, **kwargs)

        self.btn = tk.Button(
            self,
            text=text, command=command,
            bg=bg_n, fg=fg,
            activebackground=bg_h, activeforeground=TXT_WHITE,
            relief="flat", bd=0, cursor="hand2",
        )
        self.btn.pack(fill="both", expand=True)
        self.btn.bind("<Enter>", lambda _: self.btn.config(bg=self._bg_hover))
        self.btn.bind("<Leave>", lambda _: self.btn.config(bg=self._bg_normal))

    def config_font(self, font):
        self.btn.config(font=font)


# ══════════════════════════════════════════════════════════════════════════
# APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════
class CajeroApp:
    """Controlador principal del cajero automático."""

    # ── Constructor ───────────────────────────────────────────────────────
    def __init__(self, root: tk.Tk):
        self.root            = root
        self.usuario_actual  = None

        self.root.title("BANCO TECMILENIO — ATM v3.0")
        self.root.resizable(False, False)
        self.root.configure(bg=ATM_BG)
        self.root.geometry("540x720")

        self._init_fonts()
        self._build_layout()
        self.mostrar_bienvenida()

    # ── Tipografía ────────────────────────────────────────────────────────
    def _init_fonts(self):
        F = "SF Pro Display"  # macOS; en otros OS usará Segoe UI / Helvetica
        fallback = ("Helvetica Neue", "Segoe UI", "Arial")

        def mf(size, weight="normal"):
            for family in (F, *fallback):
                try:
                    f = tkfont.Font(family=family, size=size, weight=weight)
                    if f.actual("family") != "":
                        return f
                except Exception:
                    pass
            return tkfont.Font(size=size, weight=weight)

        self.f_title    = mf(15, "bold")
        self.f_subtitle = mf(11)
        self.f_body     = mf(10)
        self.f_small    = mf(9)
        self.f_balance  = mf(24, "bold")
        self.f_btn      = mf(10, "bold")

    # ── Construcción del layout fijo ──────────────────────────────────────
    def _build_layout(self):
        """Arma los contenedores permanentes del cajero."""
        self._build_header()

        # Área central: pantalla LCD
        center = tk.Frame(self.root, bg=ATM_BG)
        center.pack(fill="x", padx=20, pady=6)
        self._build_screen(center)

        # Área inferior: botones de acción
        bottom = tk.Frame(self.root, bg=ATM_BG)
        bottom.pack(fill="both", expand=True, padx=20, pady=(4, 6))

        self.action_frame = tk.Frame(bottom, bg=ATM_BG)
        self.action_frame.pack(fill="both", expand=True)

        self._build_footer()

    def _build_header(self):
        """Encabezado con nombre del banco, reloj y estado de sesión."""
        hdr = tk.Frame(self.root, bg=ATM_BG, pady=10)
        hdr.pack(fill="x", padx=20)

        # Nombre + subtítulo (izquierda)
        left = tk.Frame(hdr, bg=ATM_BG)
        left.pack(side="left")
        tk.Label(left, text="◈  BANCO TECMILENIO",
                 font=self.f_title, fg=TXT_TEAL, bg=ATM_BG).pack(anchor="w")
        tk.Label(left, text="CAJERO AUTOMÁTICO  /  ATM  v3.0",
                 font=self.f_small, fg=TXT_SECONDARY, bg=ATM_BG).pack(anchor="w")

        # Reloj + estado (derecha)
        right = tk.Frame(hdr, bg=ATM_BG)
        right.pack(side="right")
        self.lbl_clock = tk.Label(right, text="",
                                  font=self.f_small, fg=TXT_SECONDARY, bg=ATM_BG)
        self.lbl_clock.pack(anchor="e")
        self.lbl_status = tk.Label(right, text="● LISTO",
                                   font=self.f_small, fg=TXT_SUCCESS, bg=ATM_BG)
        self.lbl_status.pack(anchor="e")

        tk.Frame(self.root, bg=DIVIDER, height=1).pack(fill="x", padx=20)
        self._tick()

    def _build_screen(self, parent):
        """Pantalla LCD con bisel, barra de estado y zona de contenido."""
        # Bisel (borde de 3 px de color SCR_BORDER)
        bezel = tk.Frame(parent, bg=SCR_BORDER, padx=3, pady=3)
        bezel.pack(fill="x")

        # Superficie de la pantalla
        scr = tk.Frame(bezel, bg=SCR_BG)
        scr.pack(fill="both", expand=True)

        # Barra superior de la pantalla
        bar = tk.Frame(scr, bg=SCR_HEADER_BG, pady=7)
        bar.pack(fill="x")
        self.scr_title = tk.Label(bar, text="",
                                  font=self.f_subtitle, fg=TXT_TEAL,
                                  bg=SCR_HEADER_BG)
        self.scr_title.pack(side="left", padx=14)
        self.scr_sub = tk.Label(bar, text="",
                                font=self.f_small, fg=TXT_SECONDARY,
                                bg=SCR_HEADER_BG)
        self.scr_sub.pack(side="right", padx=14)

        tk.Frame(scr, bg=DIVIDER, height=1).pack(fill="x")

        # Zona de contenido dinámico
        self.content = tk.Frame(scr, bg=SCR_BG, padx=22, pady=14)
        self.content.pack(fill="both", expand=True)

    def _build_footer(self):
        """Pie con etiquetas de componentes físicos del cajero."""
        tk.Frame(self.root, bg=DIVIDER, height=1).pack(fill="x", padx=20, pady=(4, 0))
        foot = tk.Frame(self.root, bg=ATM_BEZEL, pady=5)
        foot.pack(fill="x", padx=20)
        for label in ("▣ RANURA DE TARJETA", "⊠ DISPENSADOR", "✉ RECIBO"):
            tk.Label(foot, text=label, font=self.f_small,
                     fg=TXT_SECONDARY, bg=ATM_BEZEL).pack(side="left", padx=12)

    # ── Helpers internos ──────────────────────────────────────────────────

    def _tick(self):
        """Actualiza el reloj cada segundo."""
        self.lbl_clock.config(
            text=datetime.datetime.now().strftime("%d/%m/%Y   %H:%M:%S"))
        self.root.after(1000, self._tick)

    def limpiar(self):
        """Vacía la pantalla y el área de botones de acción."""
        for w in self.content.winfo_children():
            w.destroy()
        for w in self.action_frame.winfo_children():
            w.destroy()
        self.lbl_msg = None

    def _set_header(self, title: str, subtitle: str = ""):
        self.scr_title.config(text=title)
        self.scr_sub.config(text=subtitle)

    def _set_status(self, text: str, color: str):
        self.lbl_status.config(text=text, fg=color)

    # ── Widget builders ───────────────────────────────────────────────────

    def _label(self, text: str, fg=None, font=None, **kw) -> tk.Label:
        lbl = tk.Label(self.content, text=text,
                       font=font or self.f_body,
                       fg=fg or TXT_WHITE, bg=SCR_BG, **kw)
        lbl.pack(fill="x", pady=1)
        return lbl

    def _sep(self):
        tk.Frame(self.content, bg=DIVIDER, height=1).pack(fill="x", pady=8)

    def _spacer(self, h: int = 8):
        tk.Frame(self.content, bg=SCR_BG, height=h).pack()

    def _entry(self, show: str = None) -> tk.Entry:
        """Campo de texto con borde iluminado al hacer foco."""
        border_frame = tk.Frame(self.content, bg=SCR_BORDER, padx=1, pady=1)
        border_frame.pack(fill="x", pady=4)

        e = tk.Entry(border_frame,
                     font=self.f_body,
                     fg=TXT_WHITE, bg=SCR_INNER,
                     insertbackground=TXT_TEAL,
                     relief="flat", bd=0)
        if show:
            e.config(show=show)
        e.pack(fill="x", ipady=8, padx=6)

        # Efecto glow al enfocar
        e.bind("<FocusIn>",  lambda _: border_frame.config(bg=GLOW))
        e.bind("<FocusOut>", lambda _: border_frame.config(bg=SCR_BORDER))
        return e

    def _msg_label(self) -> tk.Label:
        """Crea (y almacena) la etiqueta de mensajes de estado."""
        self.msg_var = tk.StringVar()
        self.lbl_msg = tk.Label(self.content, textvariable=self.msg_var,
                                font=self.f_small, fg=TXT_WARN,
                                bg=SCR_BG, wraplength=360, justify="center")
        self.lbl_msg.pack(pady=4)
        return self.lbl_msg

    def _show_msg(self, text: str, color: str = TXT_WARN):
        """Muestra un mensaje en la etiqueta de estado."""
        if hasattr(self, "msg_var") and self.msg_var is not None:
            self.msg_var.set(text)
        if self.lbl_msg:
            self.lbl_msg.config(fg=color)

    def _action_btn(self, text: str, command, style: str = "normal") -> ATMButton:
        """Agrega un botón al panel de acciones."""
        btn = ATMButton(self.action_frame, text=text,
                        command=command, style=style)
        btn.config_font(self.f_btn)
        btn.pack(fill="x", pady=3, ipady=7)
        return btn

    # ══════════════════════════════════════════════════════════════════════
    # PANTALLAS
    # ══════════════════════════════════════════════════════════════════════

    def mostrar_bienvenida(self):
        """Pantalla de bienvenida y menú principal."""
        self.limpiar()
        self.usuario_actual = None
        self._set_header("BIENVENIDO / WELCOME", "Seleccione una opción")
        self._set_status("● LISTO", TXT_SUCCESS)

        self._spacer(20)
        tk.Label(self.content, text="🏦",
                 font=tkfont.Font(size=40), bg=SCR_BG).pack()
        self._spacer(6)

        self._label("BANCO TECMILENIO",
                    fg=TXT_TEAL, font=self.f_title, justify="center")
        self._label("Introduzca su tarjeta o seleccione una opción",
                    fg=TXT_SECONDARY, font=self.f_small, justify="center")
        self._spacer(18)
        self._sep()
        self._label("Use los botones del lateral para continuar",
                    fg=TXT_SECONDARY, font=self.f_small, justify="center")

        # Botones de acción
        self._action_btn("[ 1 ]  CREAR CUENTA",    self.pantalla_crear_usuario, "accent")
        self._action_btn("[ 2 ]  INICIAR SESIÓN",  self.pantalla_login,         "normal")
        tk.Frame(self.action_frame, bg=ATM_BG, height=10).pack()
        self._action_btn("[ 0 ]  SALIR",           self.root.quit,              "danger")

    def pantalla_crear_usuario(self):
        """Formulario de alta de nueva cuenta."""
        self.limpiar()
        self._set_header("NUEVA CUENTA", "Registro / New Account")
        self._set_status("● REGISTRO", TXT_WARN)

        self._label("Complete los campos para crear su cuenta",
                    fg=TXT_SECONDARY, font=self.f_small)
        self._sep()

        self._label("  NOMBRE DE USUARIO", fg=TXT_SECONDARY, font=self.f_small)
        entry_nombre = self._entry()
        entry_nombre.focus_set()

        self._spacer(4)
        self._label("  NIP  (4 – 6 dígitos)", fg=TXT_SECONDARY, font=self.f_small)
        entry_nip = self._entry(show="●")


        self._msg_label()

        def crear():
            nombre = entry_nombre.get().strip()
            nip    = entry_nip.get().strip()
            if not nombre:
                self._show_msg("⚠  Ingresa un nombre de usuario.", TXT_WARN)
                return
            if not nip or len(nip) < 4:
                self._show_msg("⚠  El NIP debe tener al menos 4 dígitos.", TXT_WARN)
                return
            nuevo = Usuario(nombre, nip)
            users.append(nuevo)
            self.usuario_actual = nuevo
            self._show_msg("✔  Cuenta creada. Redirigiendo…", TXT_SUCCESS)
            self.root.after(800, self.pantalla_menu_usuario)

        self._action_btn("✔  CONFIRMAR",       crear,                  "accent")
        self._action_btn("✖  CANCELAR",        self.mostrar_bienvenida, "danger")

    def pantalla_login(self):
        """Pantalla de autenticación."""
        self.limpiar()
        self._set_header("IDENTIFICACIÓN", "Login / Acceso")
        self._set_status("▶ LEYENDO TARJETA…", TXT_TEAL)

        self._label("Introduzca sus credenciales para continuar",
                    fg=TXT_SECONDARY, font=self.f_small)
        self._sep()

        self._label("  NOMBRE DE USUARIO", fg=TXT_SECONDARY, font=self.f_small)
        entry_nombre = self._entry()
        entry_nombre.focus_set()

        self._spacer(4)
        self._label("  NIP", fg=TXT_SECONDARY, font=self.f_small)
        entry_nip = self._entry(show="●")


        self._msg_label()
        attempt = [0]

        def ingresar():
            nombre = entry_nombre.get().strip()
            nip    = entry_nip.get().strip()
            for user in users:
                if user.ingresar(nombre, nip):
                    self.usuario_actual = user
                    self._set_status("● SESIÓN ACTIVA", TXT_SUCCESS)
                    self._show_msg("✔  Acceso autorizado. Bienvenido.", TXT_SUCCESS)
                    self.root.after(700, self.pantalla_menu_usuario)
                    return
            attempt[0] += 1
            entry_nip.delete(0, tk.END)
            if attempt[0] < 3:
                self._show_msg(
                    f"✖  NIP incorrecto. Intento {attempt[0]} de 3.", TXT_ERR)
            else:
                self._show_msg("✖  Cuenta bloqueada temporalmente.", TXT_ERR)

        self._action_btn("✔  ACEPTAR",         ingresar,               "accent")
        self._action_btn("✖  CANCELAR",        self.mostrar_bienvenida, "danger")

    def pantalla_menu_usuario(self):
        """Panel de operaciones del usuario autenticado."""
        self.limpiar()
        user = self.usuario_actual
        self._set_header(f"BIENVENIDO, {user.nombre.upper()}", "Panel de operaciones")
        self._set_status("● SESIÓN ACTIVA", TXT_SUCCESS)

        # ── Tarjeta de saldo ──────────────────────────────────────────
        card = tk.Frame(self.content, bg=SCR_HEADER_BG, padx=16, pady=12)
        card.pack(fill="x", pady=(0, 8))

        tk.Label(card, text="SALDO DISPONIBLE",
                 font=self.f_small, fg=TXT_SECONDARY,
                 bg=SCR_HEADER_BG, anchor="w").pack(anchor="w")

        self.lbl_saldo = tk.Label(
            card,
            text=f"$  {user.saldo:,.2f}   MXN",
            font=self.f_balance, fg=TXT_GOLD,
            bg=SCR_HEADER_BG, anchor="w",
        )
        self.lbl_saldo.pack(anchor="w")

        # ── Campo de importe ──────────────────────────────────────────
        self._sep()
        self._label("  CANTIDAD A OPERAR  (MXN)", fg=TXT_SECONDARY, font=self.f_small)
        self.entry_cantidad = self._entry()
        self.entry_cantidad.focus_set()

        self._msg_label()

        # ── Botones de operación ──────────────────────────────────────
        self._action_btn("[ 1 ]  DEPOSITAR",    self.depositar,          "accent")
        self._action_btn("[ 2 ]  RETIRAR",      self.retirar,            "normal")
        tk.Frame(self.action_frame, bg=ATM_BG, height=8).pack()
        self._action_btn("[ 0 ]  CERRAR SESIÓN", self.mostrar_bienvenida, "danger")

    # ══════════════════════════════════════════════════════════════════════
    # OPERACIONES (lógica sin cambios)
    # ══════════════════════════════════════════════════════════════════════

    def _obtener_cantidad(self) -> float | None:
        """Valida y devuelve el importe del campo; muestra error si es inválido."""
        try:
            valor = float(self.entry_cantidad.get().replace(",", ""))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            self._show_msg("⚠  Ingresa una cantidad válida.", TXT_WARN)
            return None

    def depositar(self):
        cantidad = self._obtener_cantidad()
        if cantidad is None:
            return
        self.usuario_actual.agregarSaldo(cantidad)
        self.entry_cantidad.delete(0, tk.END)
        self.lbl_saldo.config(text=f"$  {self.usuario_actual.saldo:,.2f}   MXN")
        self._show_msg(f"✔  Depósito exitoso:  + ${cantidad:,.2f}", TXT_SUCCESS)

    def retirar(self):
        cantidad = self._obtener_cantidad()
        if cantidad is None:
            return
        if self.usuario_actual.retirarSaldo(cantidad):
            self.entry_cantidad.delete(0, tk.END)
            self.lbl_saldo.config(text=f"$  {self.usuario_actual.saldo:,.2f}   MXN")
            self._show_msg(f"✔  Retiro exitoso:  − ${cantidad:,.2f}", TXT_SUCCESS)
        else:
            self._show_msg("✖  Saldo insuficiente para esta operación.", TXT_ERR)


# ══════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app  = CajeroApp(root)
    root.mainloop()
