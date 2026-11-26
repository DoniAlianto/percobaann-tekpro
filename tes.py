from datetime import date
import streamlit as st

# ==================================
# 1. KONFIGURASI HALAMAN & GAYA UI
# ==================================
st.set_page_config(
    page_title="Jadwal Tugas",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .stApp {
            background: #f8fafc;
        }
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1140px;
        }

        /* Hero Commercial Style */
        .hero {
            background: linear-gradient(125deg, #090d16 0%, #111c33 52%, #0c4a6e 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 22px;
            padding: 32px 34px;
            color: #ffffff;
            box-shadow: 0 20px 45px -15px rgba(15, 23, 42, 0.35);
            margin-bottom: 20px;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(56, 189, 248, 0.14);
            border: 1px solid rgba(125, 211, 252, 0.3);
            color: #bae6fd;
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .hero h1 {
            margin: 0 0 8px 0;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            color: #ffffff;
        }
        .hero p {
            margin: 0;
            color: #cbd5e1;
            font-size: 1rem;
            max-width: 680px;
            line-height: 1.6;
        }

        /* KPI Metric Cards */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
            margin-bottom: 22px;
        }
        .kpi-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
        }
        .kpi-label {
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #64748b;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 1.85rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }
        .kpi-sub {
            font-size: 0.8rem;
            color: #64748b;
            margin-top: 6px;
        }

        /* Section Card */
        .section-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.03);
            margin-bottom: 18px;
        }

        /* Task Card */
        .task-item {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #0284c7;
            border-radius: 16px;
            padding: 18px 20px;
            margin-top: 12px;
            margin-bottom: 8px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .task-item:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }
        .task-item.tinggi { border-left-color: #e11d48; }
        .task-item.sedang { border-left-color: #d97706; }
        .task-item.rendah { border-left-color: #2563eb; }
        .task-item.selesai {
            background: #f8fafc;
            opacity: 0.76;
        }
        .task-title {
            font-size: 1.12rem;
            font-weight: 700;
            color: #0f172a;
            margin: 8px 0 5px 0;
        }
        .task-desc {
            color: #475569;
            font-size: 0.92rem;
            line-height: 1.55;
            margin-bottom: 10px;
        }
        .task-footer {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            font-size: 0.84rem;
            color: #334155;
            font-weight: 500;
        }

        /* Pills & Badges */
        .tag {
            display: inline-block;
            padding: 4px 11px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
            margin-right: 6px;
        }
        .tag-matkul { background: #e0f2fe; color: #0369a1; }
        .tag-tinggi { background: #ffe4e6; color: #be123c; }
        .tag-sedang { background: #fef3c7; color: #b45309; }
        .tag-rendah { background: #dbeafe; color: #1d4ed8; }
        .tag-selesai { background: #dcfce7; color: #15803d; }
        .tag-proses { background: #fef9c3; color: #a16207; }
        .tag-belum { background: #f1f5f9; color: #334155; }

        /* Primary Button Polish */
        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7, #2563eb);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            padding: 0.5rem 1.1rem;
        }

        @media (max-width: 820px) {
            .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .hero { padding: 24px 20px; }
            .hero h1 { font-size: 1.65rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================
# 2. DATA DI MEMORI SESI
# ==================================
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "nama": "Laporan Praktikum Metode Seismik",
            "matkul": "Metode Seismik",
            "deskripsi": "Picking gelombang P dan S serta interpretasi penampang waktu.",
            "deadline": date(2026, 12, 2),
            "prioritas": "Tinggi",
            "status": "Sedang Dikerjakan",
        },
        {
            "nama": "Latihan Soal Analisis Data",
            "matkul": "Fisika Matematika 2",
            "deskripsi": "Kerjakan latihan soal bagian 1–5 sebelum pertemuan berikutnya.",
            "deadline": date(2026, 12, 5),
            "prioritas": "Sedang",
            "status": "Belum Dikerjakan",
        },
    ]

tasks = st.session_state.tasks


def status_deadline(dl: date, status: str) -> str:
    if status == "Selesai":
        return "✅ Selesai"
    selisih = (dl - date.today()).days
    if selisih < 0:
        return f"🚨 Terlewat {abs(selisih)} hari"
    if selisih == 0:
        return "⚠️ Deadline hari ini"
    if selisih <= 3:
        return f"⏳ Tinggal {selisih} hari"
    return f"📅 {selisih} hari lagi"


# ==================================
# 3. HERO & NAVIGASI ATAS
# ==================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✦ Workspace Akademik Modern</div>
        <h1>Jadwal Tugas</h1>
        <p>Atur jadwal pengerjaan tugas kuliah, pantau tenggat waktu, dan jaga progres belajar tetap terarah dalam satu tampilan ringkas.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_dash, tab_tambah, tab_daftar = st.tabs(
    ["📊 Ringkasan Jadwal", "➕ Tambah Tugas", "📋 Semua Jadwal Tugas"]
)

# ==================================
# 4. TAB RINGKASAN JADWAL
# ==================================
with tab_dash:
    total = len(tasks)
    selesai = sum(1 for t in tasks if t["status"] == "Selesai")
    proses = sum(1 for t in tasks if t["status"] == "Sedang Dikerjakan")
    belum = sum(1 for t in tasks if t["status"] == "Belum Dikerjakan")

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Tugas</div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-sub">Seluruh jadwal terdaftar</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Belum Dikerjakan</div>
                <div class="kpi-value">{belum}</div>
                <div class="kpi-sub">Menunggu antrean kerja</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Sedang Dikerjakan</div>
                <div class="kpi-value">{proses}</div>
                <div class="kpi-sub">Dalam tahap pengerjaan</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Selesai</div>
                <div class="kpi-value">{selesai}</div>
                <div class="kpi-sub">Tugas tuntas dikumpulkan</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Progres Penyelesaian")
    if total > 0:
        rasio = selesai / total
        st.progress(rasio, text=f"{rasio * 100:.0f}% selesai ({selesai} dari {total} tugas)")
    else:
        st.info("Belum ada tugas terjadwal. Buka tab **Tambah Tugas** untuk membuat jadwal baru.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Tenggat Terdekat")
    aktif = sorted(
        [t for t in tasks if t["status"] != "Selesai"],
        key=lambda x: x["deadline"],
    )
    if aktif:
        for t in aktif[:5]:
            st.markdown(
                f"- **{t['nama']}** (`{t['matkul']}`) — "
                f"**{t['deadline'].strftime('%d %b %Y')}** • *{status_deadline(t['deadline'], t['status'])}*"
            )
    else:
        st.success("Semua jadwal tugas aktif sudah selesai.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================
# 5. TAB TAMBAH TUGAS
# ==================================
with tab_tambah:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Buat Jadwal Tugas Baru")

    with st.form("form_jadwal_tugas", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nama = col1.text_input("Nama Tugas *", placeholder="Contoh: Laporan Praktikum Geolistrik")
        matkul = col2.text_input("Mata Kuliah *", placeholder="Contoh: Metode Geolistrik")

        deskripsi = st.text_area(
            "Deskripsi & Catatan",
            placeholder="Tambahkan poin pengerjaan, format file, atau catatan penting...",
        )

        col3, col4, col5 = st.columns(3)
        deadline = col3.date_input("Deadline *", value=date.today())
        prioritas = col4.selectbox("Prioritas", ["Tinggi", "Sedang", "Rendah"], index=1)
        status = col5.selectbox(
            "Status Awal",
            ["Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"],
        )

        simpan = st.form_submit_button("Simpan ke Jadwal Tugas", type="primary")
        if simpan:
            if nama.strip() and matkul.strip():
                tasks.append(
                    {
                        "nama": nama.strip(),
                        "matkul": matkul.strip(),
                        "deskripsi": deskripsi.strip(),
                        "deadline": deadline,
                        "prioritas": prioritas,
                        "status": status,
                    }
                )
                st.success("Tugas berhasil ditambahkan ke Jadwal Tugas!")
                st.rerun()
            else:
                st.error("Nama tugas dan mata kuliah wajib diisi.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==================================
# 6. TAB SEMUA JADWAL TUGAS
# ==================================
with tab_daftar:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### Filter & Pencarian Jadwal")

    if not tasks:
        st.info("Belum ada tugas tersimpan.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        f1, f2, f3 = st.columns([2, 1, 1])
        cari = f1.text_input("Cari tugas atau mata kuliah", placeholder="Ketik kata kunci...").strip().lower()
        filter_status = f2.selectbox(
            "Status",
            ["Semua", "Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"],
        )
        filter_prio = f3.selectbox("Prioritas", ["Semua", "Tinggi", "Sedang", "Rendah"])
        st.markdown("</div>", unsafe_allow_html=True)

        ditampilkan = []
        for idx, t in enumerate(tasks):
            if filter_status != "Semua" and t["status"] != filter_status:
                continue
            if filter_prio != "Semua" and t["prioritas"] != filter_prio:
                continue
            if cari and cari not in f"{t['nama']} {t['matkul']} {t['deskripsi']}".lower():
                continue
            ditampilkan.append((idx, t))

        ditampilkan.sort(key=lambda pair: (pair[1]["status"] == "Selesai", pair[1]["deadline"]))

        if not ditampilkan:
            st.warning("Tidak ada jadwal tugas yang cocok dengan filter.")
        else:
            for idx, t in ditampilkan:
                prio_low = t["prioritas"].lower()
                is_done = t["status"] == "Selesai"

                if is_done:
                    status_tag = '<span class="tag tag-selesai">Selesai</span>'
                elif t["status"] == "Sedang Dikerjakan":
                    status_tag = '<span class="tag tag-proses">Sedang Dikerjakan</span>'
                else:
                    status_tag = '<span class="tag tag-belum">Belum Dikerjakan</span>'

                st.markdown(
                    f"""
                    <div class="task-item {prio_low} {'selesai' if is_done else ''}">
                        <div>
                            <span class="tag tag-matkul">{t['matkul']}</span>
                            <span class="tag tag-{prio_low}">Prioritas {t['prioritas']}</span>
                            {status_tag}
                        </div>
                        <div class="task-title">{t['nama']}</div>
                        <div class="task-desc">{t['deskripsi'] or '<em>Tidak ada deskripsi tambahan.</em>'}</div>
                        <div class="task-footer">
                            <span>🗓️ Deadline: <strong>{t['deadline'].strftime('%d %B %Y')}</strong></span>
                            <span>•</span>
                            <span>{status_deadline(t['deadline'], t['status'])}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c_sel, c_upd, c_del = st.columns([3, 1, 1])
                opsi = ["Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"]
                status_baru = c_sel.selectbox(
                    "Status",
                    opsi,
                    index=opsi.index(t["status"]),
                    key=f"status_{idx}",
                    label_visibility="collapsed",
                )
                if c_upd.button("Update", key=f"upd_{idx}", use_container_width=True):
                    tasks[idx]["status"] = status_baru
                    st.rerun()

                if c_del.button("Hapus", key=f"del_{idx}", use_container_width=True):
                    tasks.pop(idx)
                    st.rerun()