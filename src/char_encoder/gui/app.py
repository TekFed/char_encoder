"""Tkinter GUI for the Character Encoder."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from ..core.converter import analyze_text


class EncoderApp(tk.Tk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Character Encoder")
        self.geometry("1000x720")
        self.minsize(820, 560)
        self._build_ui()
        self._convert()  # pre-populate with sample

    # ------------------------------------------------------------------ UI --
    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)
        self._build_input(root)
        self._build_results(root)

    def _build_input(self, parent: ttk.Frame) -> None:
        frame = ttk.LabelFrame(parent, text="Input", padding=10)
        frame.pack(fill="x", pady=(0, 10))

        self.input_text = tk.Text(frame, height=3, wrap="word", font=("Consolas", 12))
        self.input_text.pack(fill="x")
        self.input_text.insert("1.0", "Hello, 你好 🌍")
        self.input_text.bind("<Control-Return>", lambda _e: self._convert())

        bar = ttk.Frame(frame)
        bar.pack(fill="x", pady=(8, 0))

        ttk.Button(bar, text="Convert (Ctrl+Enter)", command=self._convert).pack(side="left")
        ttk.Button(bar, text="Clear", command=self._clear).pack(side="left", padx=6)
        ttk.Button(bar, text="Copy Bytes", command=self._copy_bytes).pack(side="left")

        self.status = ttk.Label(bar, text="", foreground="#666")
        self.status.pack(side="right")

    def _build_results(self, parent: ttk.Frame) -> None:
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True)

        char_tab = ttk.Frame(nb, padding=6)
        nb.add(char_tab, text="Per Character")
        self._build_char_table(char_tab)

        enc_tab = ttk.Frame(nb, padding=6)
        nb.add(enc_tab, text="Encoded Bytes")
        self._build_encoding_view(enc_tab)

    def _build_char_table(self, parent: ttk.Frame) -> None:
        cols = ("char", "cp_hex", "dec", "cp_bin", "ascii", "name")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings")

        spec = {
            "char":   ("Char",            70),
            "cp_hex": ("Code Point",     110),
            "dec":    ("Decimal",        100),
            "cp_bin": ("Code Point Binary", 240),
            "ascii":  ("ASCII (dec)",    100),
            "name":   ("Unicode Name",   320),
        }
        for key, (label, width) in spec.items():
            self.tree.heading(key, text=label)
            self.tree.column(key, width=width, anchor="w")

        scroll = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def _build_encoding_view(self, parent: ttk.Frame) -> None:
        self.enc_text = tk.Text(parent, wrap="none", font=("Consolas", 10))
        sy = ttk.Scrollbar(parent, orient="vertical", command=self.enc_text.yview)
        sx = ttk.Scrollbar(parent, orient="horizontal", command=self.enc_text.xview)
        self.enc_text.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)

        self.enc_text.grid(row=0, column=0, sticky="nsew")
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

    # ------------------------------------------------------------- Actions --
    def _convert(self) -> None:
        text = self.input_text.get("1.0", "end-1c")
        if not text:
            self.status.configure(text="Nothing to convert.")
            return

        chars, encodings = analyze_text(text)

        self.tree.delete(*self.tree.get_children())
        for ci in chars:
            self.tree.insert("", "end", values=(
                self._display_char(ci.char),
                ci.codepoint_hex,
                ci.codepoint,
                ci.codepoint_binary,
                ci.ascii_decimal,
                ci.name,
            ))

        self.enc_text.delete("1.0", "end")
        for res in encodings:
            self.enc_text.insert("end", f"── {res.encoding.upper()} ──\n")
            if res.ok:
                self.enc_text.insert("end",
                    f"  {res.size} byte(s)\n"
                    f"  hex:    {res.hex}\n"
                    f"  binary: {res.binary}\n\n")
            else:
                self.enc_text.insert("end", f"  ⚠  {res.error}\n\n")

        self.status.configure(
            text=f"{len(chars)} char(s) • {len(text.encode('utf-8'))} UTF-8 byte(s)"
        )

    def _clear(self) -> None:
        self.input_text.delete("1.0", "end")
        self.tree.delete(*self.tree.get_children())
        self.enc_text.delete("1.0", "end")
        self.status.configure(text="")

    def _copy_bytes(self) -> None:
        payload = self.enc_text.get("1.0", "end-1c")
        if not payload:
            return
        self.clipboard_clear()
        self.clipboard_append(payload)
        self.status.configure(text="Copied to clipboard.")

    # ------------------------------------------------------------- Helpers --
    @staticmethod
    def _display_char(ch: str) -> str:
        return {" ": "␠", "\t": "⇥", "\n": "⏎", "\r": "␍"}.get(ch, ch)


def main() -> None:
    EncoderApp().mainloop()


if __name__ == "__main__":
    main()