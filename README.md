# Ergohaven firmware

Firmware is now available in the Ergohaven documentation:

- [Русская версия](https://docs.eh.works/firmware/)
- [English version](https://docs.eh.industries/firmware/)

<details>
<summary>Firmware archive</summary>

<!-- Release URLs are managed by scripts/update-firmware-archive.py. Edit firmware-archive.json to change the asset set. -->

## QMK (wired)
| Previous devices                                    | Current devices                   |
| --------------------------------------------------- | --------------------------------- |
| [K:03 v1/v2][q05]                                   |                                   |
| [Imperial44 v1/v2][q06]                             |                                   |
| [Planeta v1][q08]                                   | [Planeta v2][q09]                 |
| [M4CR0Pad v1][q10]</br>[M4CR0Pad v2][q11]           |                                   |
| [Velvet v1][q13]</br>[Velvet v2][q14]               |                                   |
| [Trackball v1][q15]                                 | [Trackball v2][q20]               |
| [K:03 PRO v1 43mm][q16]</br>[K:03 PRO v1 65mm][q18] |                                   |
| [HPD v1][q04]                                       |                                   |
| [K:02][q07]                                         |                                   |
| [Remnant][q12]                                      |                                   |

[q04]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_hpd_v1.uf2
[q05]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_k03_v1_v2.uf2
[q06]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_imperial44_v1_v2.uf2
[q07]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_k02_v1.uf2
[q08]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_planeta_v1.uf2
[q09]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_planeta_v2.uf2
[q10]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_macropad_v1.uf2
[q11]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_macropad_v2.uf2
[q12]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_remnant_v1.uf2
[q13]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_velvet_v1.uf2
[q14]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_velvet_v2.uf2
[q15]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_trackball_v1.uf2
[q16]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_k03pro_43mm_v1.uf2
[q18]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_k03pro_65mm_v1.uf2
[q20]: https://github.com/ergohaven/vial-qmk/releases/download/4.0.6/4.0.6_trackball_v2.uf2

## ZMK (wireless)
| Device              | Standard layout                                | RuEn layout                          |
| ------------------- | ---------------------------------------------- | ------------------------------------ |
| K:03 v4             | [left][z80] [right][z82]                       | [left][z81] [right][z82]             |
| K:03 v4 + Qube      | [left][z83] [right][z82] [qube][z84]           | [left][z83] [right][z82] [qube][z85] |
| Imperial44          | [left][z90] [right][z92]                       | [left][z91] [right][z92]             |
| Imperial44 + Qube   | [left][z93] [right][z92] [qube][z94]           | [left][z93] [right][z92] [qube][z95] |
| OP36                | [left][z50] [right][z52]                       | [left][z51] [right][z52]             |
| OP36 + Qube         | [left][z53] [right][z52] [qube][z54]           | [left][z53] [right][z52] [qube][z55] |
| Velvet v3           | [left][z60] [right][z62]                       | [left][z61] [right][z62]             |
| Velvet v3 + Qube    | [left][z63] [right][z62] [qube][z64]           | [left][z63] [right][z62] [qube][z65] |
| Velvet v3 UI        | [left][z70] [right][z71]                       | [left][z70] [right][z72]             |
| Velvet v3 UI + Qube | [left][z70] [right][z73] [qube][z74]           | [left][z70] [right][z73] [qube][z75] |

[Reset all settings for ZMK device][z00]

[ZMK - Qube migration from RMK][z01]

[z00]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/settings_reset-ergohaven-zmk.uf2
[z01]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/qube_rmk_to_zmk_reset.uf2

[z50]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_left-ergohaven-zmk.uf2
[z51]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_left_ruen-ergohaven-zmk.uf2
[z52]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_right-ergohaven-zmk.uf2
[z53]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_left_qube-ergohaven-zmk.uf2
[z54]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_qube-ergohaven-zmk.uf2
[z55]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/op36_qube_ruen-ergohaven-zmk.uf2

[z60]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_left-ergohaven-zmk.uf2
[z61]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_left_ruen-ergohaven-zmk.uf2
[z62]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_right-ergohaven-zmk.uf2
[z63]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_left_qube-ergohaven-zmk.uf2
[z64]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_qube-ergohaven-zmk.uf2
[z65]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_qube_ruen-ergohaven-zmk.uf2

[z70]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_left-ergohaven-zmk.uf2
[z71]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_right-ergohaven-zmk.uf2
[z72]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_right_ruen-ergohaven-zmk.uf2
[z73]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_right_qube-ergohaven-zmk.uf2
[z74]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_qube-ergohaven-zmk.uf2
[z75]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/velvet_v3_ui_qube_ruen-ergohaven-zmk.uf2

[z80]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_left-ergohaven-zmk.uf2
[z81]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_left_ruen-ergohaven-zmk.uf2
[z82]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_right-ergohaven-zmk.uf2
[z83]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_left_qube-ergohaven-zmk.uf2
[z84]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_qube-ergohaven-zmk.uf2
[z85]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/k03_qube_ruen-ergohaven-zmk.uf2

[z90]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_left-ergohaven-zmk.uf2
[z91]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_left_ruen-ergohaven-zmk.uf2
[z92]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_right-ergohaven-zmk.uf2
[z93]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_left_qube-ergohaven-zmk.uf2
[z94]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_qube-ergohaven-zmk.uf2
[z95]: https://github.com/ergohaven/ergohaven-zmk/releases/download/2026.03.16/imperial44_qube_ruen-ergohaven-zmk.uf2

</details>
