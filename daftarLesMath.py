import sys
import mysql.connector
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QComboBox, QDateEdit, 
                             QGroupBox, QGridLayout, QRadioButton, QTableWidget,
                             QScrollArea, QHeaderView, QCheckBox, QTableWidgetItem,
                             QApplication, QMessageBox, QDialog, QTabWidget)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def connect_db(self):
        """Koneksi ke database MySQL"""
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="daftarlesmath"
        )

    def init_ui(self):
        self.setWindowTitle("Pendaftaran math by Aero Afril")
        self.resize(1200, 800)
        
        # Main layout untuk window utama
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header bar
        header_layout = QHBoxLayout()
        header_label = QLabel("Pendaftaran Les Matematika")
        header_label.setObjectName("headerLabel")
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Tab Widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Tab-tab
        self.tab_widget.addTab(self.tab_pendaftar(), "Pendaftaran Siswa")
        self.tab_widget.addTab(self.tab_pengajar(), "Data Pengajar")
        self.tab_widget.addTab(self.tab_penugasan(), "Data Penugasan")

        # Apply stylesheet
        self.setStyleSheet(self.get_stylesheet())

    def get_stylesheet(self):
        """Return CSS stylesheet"""
        return """
        QWidget {
            background-color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
            font-size: 11pt;
            color: #333333;
        }
        QLabel {
            color: #444444;
            font-weight: 600;
            margin-bottom: 4px;
        }
        QLabel#headerLabel {
            font-size: 20pt;
            font-weight: bold;
            color: #2C7873;
            padding: 8px 0;
        }
        QLineEdit#searchInput {
            background-color: #FFFFFF;
            border: 2px solid #6FB98F;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
        }
        QLineEdit#searchInput:focus {
            border: 2px solid #2C7873;
            background-color: #F0FFF5;
        }
        QPushButton#searchButton {
            background-color: #2C7873;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 10pt;
        }
        QPushButton#searchButton:hover { 
            background-color: #236360; 
        }
        QPushButton#searchButton:pressed { 
            background-color: #1A4D4A; 
        }
        QLineEdit, QComboBox, QDateEdit {
            background-color: #F9F9F9;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 6px 10px;
        }
        QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
            border: 1px solid #6FB98F;
            background-color: #F0FFF5;
        }
        QPushButton {
            background-color: #6FB98F;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #58A67C; }
        QPushButton:pressed { background-color: #3F8C66; }
        QPushButton:disabled { background-color: #E0E0E0; color: #999999; }
        QGroupBox {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 8px;
            margin-top: 12px;
            padding: 12px;
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 6px;
            background-color: #FFFFFF;
            color: #2C7873;
            font-weight: bold;
        }
        QTableWidget {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 8px;
            gridline-color: #EEEEEE;
            selection-background-color: #E6F7F1;
            selection-color: #333333;
            alternate-background-color: #FAFAFA;
            font-size: 10pt;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:hover {
            background-color: #F0FFF5;
        }
        QHeaderView::section {
            background-color: #F5F5F5;
            padding: 10px;
            border: none;
            font-weight: bold;
            color: #2C7873;
            font-size: 11pt;
        }
        QCheckBox { spacing: 6px; color: #333333; }
        QRadioButton { spacing: 6px; color: #333333; }
                           
        QScrollBar:vertical {
            background: #CCCCCC;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #666666;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """
        
    # tab pendaftar

    def tab_pendaftar(self):
        tab = QWidget()
        outer_layout = QVBoxLayout(tab)
    
        # Search box di header TAB
        search_layout = QHBoxLayout()
        search_layout.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari siswa...")
        self.search_input.setMaximumWidth(250)
        self.search_input.setObjectName("searchInput")
        search_layout.addWidget(self.search_input)
        
        self.btn_cari_header = QPushButton("Cari")
        self.btn_cari_header.setMaximumWidth(100)
        self.btn_cari_header.setObjectName("searchButton")
        search_layout.addWidget(self.btn_cari_header)
        
        outer_layout.addLayout(search_layout)

        # Scroll Area utama
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Container widget untuk scroll area
        container = QWidget()
        main_layout = QVBoxLayout(container)
        
        scroll_area.setWidget(container)
        outer_layout.addWidget(scroll_area)

        # Form
        form_group = QGroupBox("Form Pendaftaran: ")
        form_layout = QHBoxLayout()
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(Qt.gray))
        form_group.setGraphicsEffect(shadow)

        # Grid form
        form_grid = QGridLayout()
        self.nama_edit = QLineEdit()
        self.tanggal_edit = QDateEdit()
        self.tanggal_edit.setDisplayFormat("yyyy-MM-dd")
        self.tanggal_edit.setCalendarPopup(True)
        self.tanggal_edit.setDate(QDate.currentDate())
        self.telepon_edit = QLineEdit()
        self.desa_edit = QLineEdit()
        self.kecamatan_edit = QLineEdit()
        self.kabupaten_edit = QLineEdit()
        self.pendidikan_edit = QComboBox()
        self.pendidikan_edit.addItems(["SD/Sederajat", "SMP/Sederajat", "SMA/SMK/Sederajat"])
        self.pendidikan_edit.currentTextChanged.connect(self.update_total)
        self.motivasi_edit = QComboBox()
        self.motivasi_edit.addItems(["Olimpiade", "Knowledge", "Masuk Universitas Ternama", "Lainnya"])
        gender_group = QGroupBox("Gender")
        gender_layout = QHBoxLayout()
        self.radio_laki = QRadioButton("Laki-laki")
        self.radio_perempuan = QRadioButton("Perempuan")
        gender_layout.addWidget(self.radio_laki)
        gender_layout.addWidget(self.radio_perempuan)
        gender_group.setLayout(gender_layout)
        self.langganan_edit = QComboBox()
        self.langganan_edit.addItems(["Harian", "Bulanan", "Tahunan"])
        self.langganan_edit.currentTextChanged.connect(self.update_total)
        self.total_edit = QLineEdit()
        self.total_edit.setReadOnly(True)

        # Buttons
        self.btn_tambah = QPushButton("Tambah")
        self.btn_edit = QPushButton("Edit")
        self.btn_hapus = QPushButton("Hapus")
        self.btn_refresh = QPushButton("Refresh")
        self.btn_Pembayaran = QPushButton("Bayar")
        self.btn_tampilkan = QPushButton("Tampilkan Data")

        crud_layout = QVBoxLayout()
        crud_layout.addWidget(self.btn_tambah)
        crud_layout.addWidget(self.btn_edit)
        crud_layout.addWidget(self.btn_hapus)
        crud_layout.addWidget(self.btn_refresh)
        crud_layout.addWidget(self.btn_Pembayaran)
        crud_layout.addWidget(self.btn_tampilkan)

        crud_box = QWidget()
        crud_box.setLayout(crud_layout)

        # Add to grid
        form_grid.addWidget(QLabel("Nama Lengkap"), 0, 0)
        form_grid.addWidget(self.nama_edit, 0, 1)
        form_grid.addWidget(QLabel("Tanggal Lahir"), 1, 0)
        form_grid.addWidget(self.tanggal_edit, 1, 1)
        form_grid.addWidget(QLabel("Nomor Telepon"), 2, 0)
        form_grid.addWidget(self.telepon_edit, 2, 1)
        form_grid.addWidget(QLabel("Desa/Kelurahan"), 3, 0)
        form_grid.addWidget(self.desa_edit, 3, 1)
        form_grid.addWidget(QLabel("Kecamatan"), 4, 0)
        form_grid.addWidget(self.kecamatan_edit, 4, 1)
        form_grid.addWidget(QLabel("Kabupaten/Kota"), 5, 0)
        form_grid.addWidget(self.kabupaten_edit, 5, 1)
        form_grid.addWidget(QLabel("Pendidikan"), 6, 0)
        form_grid.addWidget(self.pendidikan_edit, 6, 1)
        form_grid.addWidget(gender_group, 7, 0, 1, 2)
        form_grid.addWidget(QLabel("Motivasi"), 8, 0)
        form_grid.addWidget(self.motivasi_edit, 8, 1)
        form_grid.addWidget(QLabel("Langganan"), 9, 0)
        form_grid.addWidget(self.langganan_edit, 9, 1)
        form_grid.addWidget(QLabel("Total"), 10, 0)
        form_grid.addWidget(self.total_edit, 10, 1)
        form_grid.addWidget(crud_box, 0, 2, 10, 1)

        form_layout.addLayout(form_grid)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(14)
        self.table.setHorizontalHeaderLabels([
            "Pilih",
            "Nomor ID", 
            "Nama", 
            "Tanggal Lahir", 
            "Nomor Telepon",
            "Desa/Kelurahan",
            "Kecamatan", 
            "Kabupaten/Kota", 
            "Pendidikan", 
            "Gender",
            "Motivasi", 
            "Langganan",  
            "Total",
            "Pembayaran"
        ])

        # Atur lebar kolom spesifik
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 120)
        self.table.setColumnWidth(7, 130)
        self.table.setColumnWidth(8, 150)
        self.table.setColumnWidth(9, 100)
        self.table.setColumnWidth(10, 180)
        self.table.setColumnWidth(11, 100)
        self.table.setColumnWidth(12, 150)
        self.table.setColumnWidth(13, 120)
        
        # Header bisa di-resize manual
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Interactive)

        # Smooth scrolling
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        
        # Tinggi baris lebih besar
        self.table.verticalHeader().setDefaultSectionSize(50)
        
        # Set minimum height untuk tabel agar lebih besar
        self.table.setMinimumHeight(500)
        
        # Enable alternating row colors
        self.table.setAlternatingRowColors(True)

        self.table.hide()
        main_layout.addWidget(self.table)

        # Status label
        self.label_selected = QLabel("ID terpilih: -")
        main_layout.addWidget(self.label_selected)

        # Event handlers
        self.btn_tambah.clicked.connect(self.save_data)
        self.btn_edit.clicked.connect(self.edit_data)
        self.btn_hapus.clicked.connect(self.delete_data)
        self.btn_cari_header.clicked.connect(self.search_data)
        self.search_input.returnPressed.connect(self.search_data)
        self.btn_refresh.clicked.connect(self.refresh_data)
        self.btn_tampilkan.clicked.connect(self.tampilkan_data)
        self.btn_Pembayaran.clicked.connect(self.proses_pembayaran)
        self.table.cellClicked.connect(self.fill_form)

        self.update_total()
        
        return tab

    def update_total(self):
        """Update total biaya berdasarkan langganan"""
        langganan = self.langganan_edit.currentText()
        pendidikan = self.pendidikan_edit.currentText()

        if pendidikan == "SD/Sederajat":
            harga = 1
        elif pendidikan == "SMP/Sederajat":
            harga = 2
        else:
            harga = 3

        if langganan == "Harian":
            harga1 = 5000
        elif langganan == "Bulanan":
            harga1 = 5000*30
        else:
            harga1 = 5000*364

        total = harga * harga1
        
        self.total_edit.setText(str(int(total)))

    def get_gender(self):
        if self.radio_laki.isChecked():
            return 1
        elif self.radio_perempuan.isChecked():
            return 0
        return None


    def clear_form(self):
        """Membersihkan form input"""
        self.nama_edit.clear()
        self.tanggal_edit.setDate(QDate.currentDate())
        self.telepon_edit.clear()
        self.desa_edit.clear()
        self.kecamatan_edit.clear()
        self.kabupaten_edit.clear()
        self.pendidikan_edit.setCurrentIndex(0)
        self.motivasi_edit.setCurrentIndex(0)
        self.langganan_edit.setCurrentIndex(0)
        self.radio_laki.setAutoExclusive(False)
        self.radio_perempuan.setAutoExclusive(False)
        self.radio_laki.setChecked(False)
        self.radio_perempuan.setChecked(False)
        self.radio_laki.setAutoExclusive(True)
        self.radio_perempuan.setAutoExclusive(True)
        self.label_selected.setText("ID terpilih: -")

    def save_data(self):
        """Menyimpan data baru ke database"""
        nama = self.nama_edit.text().strip()
        tanggal = self.tanggal_edit.date().toString("yyyy-MM-dd")
        telepon = self.telepon_edit.text().strip()
        desa = self.desa_edit.text().strip()
        kecamatan = self.kecamatan_edit.text().strip()
        kabupaten = self.kabupaten_edit.text().strip()
        pendidikan = self.pendidikan_edit.currentText()
        motivasi = self.motivasi_edit.currentText()
        langganan = self.langganan_edit.currentText()
        total = self.total_edit.text()

        gender = self.get_gender()
        if gender is None:
            QMessageBox.warning(self, "Peringatan", "Pilih gender terlebih dahulu!")
            return

        if not nama or not telepon or not desa or not kecamatan or not kabupaten:
            QMessageBox.warning(self, "Peringatan", "Lengkapi semua field!")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = """INSERT INTO users (nama_pendaftar, tanggal_lahir, nomorTelepon, desaKelurahan, kecamatan, 
                    kabupatenKota, pendidikan, gender, motivasi, langganan, total, pembayaran)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            cursor.execute(query, (nama, tanggal, telepon, desa, kecamatan, kabupaten, 
                                pendidikan, gender, motivasi, langganan, total, 0))
            conn.commit()
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")
            self.clear_form()
 
            if self.table.isVisible():
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def load_data(self):
        """Memuat semua data dari database ke tabel"""
        self.table.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id_pendaftar DESC")
            results = cursor.fetchall()

            for row_idx, row_data in enumerate(results):
                self.table.insertRow(row_idx)
                
                # Checkbox di kolom pertama
                checkbox = QCheckBox()
                cell_widget = QWidget()
                layout_cb = QHBoxLayout(cell_widget)
                layout_cb.addWidget(checkbox)
                layout_cb.setAlignment(checkbox, Qt.AlignCenter)
                layout_cb.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row_idx, 0, cell_widget)

                # Data di kolom berikutnya
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)

                    # setting kolom pembayaran
                    if col_idx == 12:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setBackground(QColor(144, 238, 144))
                            item.setText("LUNAS")
                        else:
                            item.setBackground(QColor(255, 182, 193))
                            item.setText("BELUM LUNAS")

                    # setting kolom gender
                    if col_idx == 8:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setText("Laki-laki")
                        else:
                            item.setText("Perempuan")

             
                    self.table.setItem(row_idx, col_idx + 1, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def fill_form(self, row, col):
        """Mengisi form dari baris tabel yang diklik"""
        try:
            id_val = self.table.item(row, 1).text()
            self.label_selected.setText(f"ID terpilih: {id_val}")
            
            self.nama_edit.setText(self.table.item(row, 2).text())
            tanggal_str = self.table.item(row, 3).text()
            self.tanggal_edit.setDate(QDate.fromString(tanggal_str, "yyyy-MM-dd"))
            self.telepon_edit.setText(self.table.item(row, 4).text())
            self.desa_edit.setText(self.table.item(row, 5).text())
            self.kecamatan_edit.setText(self.table.item(row, 6).text())
            self.kabupaten_edit.setText(self.table.item(row, 7).text())
            
            pendidikan = self.table.item(row, 8).text()
            idx = self.pendidikan_edit.findText(pendidikan)
            if idx >= 0:
                self.pendidikan_edit.setCurrentIndex(idx)

            try:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT gender FROM users WHERE id_pendaftar=%s", (id_val,))
                result = cursor.fetchone()
                
                if result:
                    gender_val = result[0]
                    # Reset radio buttons
                    self.radio_laki.setAutoExclusive(False)
                    self.radio_perempuan.setAutoExclusive(False)
                    self.radio_laki.setChecked(False)
                    self.radio_perempuan.setChecked(False)
                    self.radio_laki.setAutoExclusive(True)
                    self.radio_perempuan.setAutoExclusive(True)
                    
                    # gender
                    if int(gender_val) == 1:
                        self.radio_laki.setChecked(True)
                    else:
                        self.radio_perempuan.setChecked(True)
                
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting gender: {e}")
                            
            motivasi = self.table.item(row, 10).text()
            idx = self.motivasi_edit.findText(motivasi)
            if idx >= 0:
                self.motivasi_edit.setCurrentIndex(idx)
            
            langganan = self.table.item(row, 11).text()
            idx = self.langganan_edit.findText(langganan)
            if idx >= 0:
                self.langganan_edit.setCurrentIndex(idx)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengisi form: {str(e)}")

    def edit_data(self):
        """Mengupdate data yang sudah ada"""
        id_text = self.label_selected.text()
        if id_text == "ID terpilih: -":
            QMessageBox.warning(self, "Peringatan", "Pilih data dari tabel terlebih dahulu!")
            return

        id_val = id_text.split(": ")[1]
        
        nama = self.nama_edit.text().strip()
        tanggal = self.tanggal_edit.date().toString("yyyy-MM-dd")
        telepon = self.telepon_edit.text().strip()
        desa = self.desa_edit.text().strip()
        kecamatan = self.kecamatan_edit.text().strip()
        kabupaten = self.kabupaten_edit.text().strip()
        pendidikan = self.pendidikan_edit.currentText()
        motivasi = self.motivasi_edit.currentText()
        langganan = self.langganan_edit.currentText()
        total = self.total_edit.text()

        gender = self.get_gender()
        if gender is None:
            QMessageBox.warning(self, "Peringatan", "Pilih gender terlebih dahulu!")
            return

        if not nama or not telepon or not desa or not kecamatan or not kabupaten:
            QMessageBox.warning(self, "Peringatan", "Lengkapi semua field!")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = """UPDATE users SET nama_pendaftar=%s, tanggal_lahir=%s, nomorTelepon=%s, desaKelurahan=%s,
                    kecamatan=%s, kabupatenKota=%s, pendidikan=%s, gender=%s, motivasi=%s, 
                    langganan=%s, total=%s WHERE id_pendaftar=%s"""
            cursor.execute(query, (nama, tanggal, telepon, desa, kecamatan, kabupaten, 
                                pendidikan, gender, motivasi, langganan, total, id_val))
            conn.commit()
            QMessageBox.information(self, "Sukses", "Data berhasil diupdate!")
            self.clear_form()
            if self.table.isVisible():
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal update data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def delete_data(self):
        """Menghapus data yang dipilih via checkbox"""
        ids_to_delete = []
        
        for row in range(self.table.rowCount()):
            cell_widget = self.table.cellWidget(row, 0)
            if cell_widget:
                checkbox = cell_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    id_val = self.table.item(row, 1).text()
                    ids_to_delete.append(id_val)
        
        if not ids_to_delete:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus!")
            return

        reply = QMessageBox.question(self, "Konfirmasi", 
                                    f"Hapus {len(ids_to_delete)} data?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            for id_val in ids_to_delete:
                cursor.execute("DELETE FROM users WHERE id_pendaftar=%s", (id_val,))
            conn.commit()
            QMessageBox.information(self, "Sukses", f"{len(ids_to_delete)} data berhasil dihapus!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menghapus data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()  
                conn.close()

    def search_data(self):
        """Mencari data di semua kolom dari search input di header"""
        keyword = self.search_input.text().strip()
        
        if not keyword:
            QMessageBox.warning(self, "Peringatan", "Masukkan kata kunci untuk mencari!")
            return

        # Tampilkan tabel jika masih tersembunyi
        if not self.table.isVisible():
            self.table.show()
            self.btn_tampilkan.setText("Sembunyikan Data")

        self.table.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            # PERBAIKAN: Cari juga berdasarkan ID
            query = """SELECT * FROM users WHERE 
                    id_pendaftar LIKE %s OR
                    nama_pendaftar LIKE %s OR 
                    tanggal_lahir LIKE %s OR 
                    nomorTelepon LIKE %s OR
                    desaKelurahan LIKE %s OR 
                    kecamatan LIKE %s OR 
                    kabupatenKota LIKE %s OR 
                    pendidikan LIKE %s OR 
                    motivasi LIKE %s OR 
                    langganan LIKE %s"""
            search_param = f"%{keyword}%"
            cursor.execute(query, (search_param,) * 10)
            results = cursor.fetchall()

            if not results:
                QMessageBox.information(self, "Info", "Data tidak ditemukan!")
                return

            for row_idx, row_data in enumerate(results):
                self.table.insertRow(row_idx)
                checkbox = QCheckBox()
                cell_widget = QWidget()
                layout_cb = QHBoxLayout(cell_widget)
                layout_cb.addWidget(checkbox)
                layout_cb.setAlignment(checkbox, Qt.AlignCenter)
                layout_cb.setContentsMargins(0, 0, 0, 0)
                self.table.setCellWidget(row_idx, 0, cell_widget)

                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # pembayaran
                    if col_idx == 12:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setBackground(QColor(144, 238, 144))
                            item.setText("LUNAS")
                        else:
                            item.setBackground(QColor(255, 182, 193))
                            item.setText("BELUM LUNAS")
                    
                    # gender
                    if col_idx == 8:
                        if str(value) == '1':
                            item.setText("Laki-laki")
                        else:
                            item.setText("Perempuan")
                            
                    self.table.setItem(row_idx, col_idx + 1, item)
            
            QMessageBox.information(self, "Hasil Pencarian", 
                                f"Ditemukan {len(results)} data dengan kata kunci '{keyword}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mencari data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def refresh_data(self):
        """Refresh tabel dan clear form"""
        self.clear_form()
        self.load_data()
        QMessageBox.information(self, "Info", "Data berhasil direfresh!")

    def tampilkan_data(self):
        """Menampilkan/menyembunyikan tabel"""
        if self.table.isVisible():
            self.table.hide()
            self.btn_tampilkan.setText("Tampilkan Data")
        else:
            self.table.show()
            self.load_data()
            self.btn_tampilkan.setText("Sembunyikan Data")

    def proses_pembayaran(self):
        """Proses pembayaran dengan QR Code"""
        id_text = self.label_selected.text()
        if id_text == "ID terpilih: -":
            QMessageBox.warning(self, "Peringatan", "Pilih data dari tabel terlebih dahulu!")
            return
        
        id_val = id_text.split(": ")[1]
        
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id_pendaftar=%s", (id_val,))
            data = cursor.fetchone()
            
            if not data:
                QMessageBox.warning(self, "Peringatan", "Data tidak ditemukan!")
                return
            
            # Index pembayaran
            if str(data[12]) == '1' or str(data[12]).lower() == 'true':
                QMessageBox.information(self, "Info", "Pembayaran sudah lunas!")
                return
            
            # Tampilkan dialog QR Code
            self.show_qr_dialog(data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal proses pembayaran: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def show_qr_dialog(self, data):
        """Menampilkan dialog QR Code untuk pembayaran"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Pembayaran QR Code")
        dialog.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        
        # Info pembayaran
        info_label = QLabel(f"""
        <h3>Informasi Pembayaran</h3>
        <p><b>Nama:</b> {data[1]}</p>
        <p><b>Langganan:</b> {data[10]}</p>
        <p><b>Total:</b> {data[11]}</p>
        """)
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Generate QR Code
        qr_data = f"PAYMENT|ID:{data[0]}|NAME:{data[1]}|AMOUNT:{data[11]}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert PIL Image to QPixmap
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        
        qr_pixmap = QPixmap()
        qr_pixmap.loadFromData(buffer.read())
        
        qr_label = QLabel()
        qr_label.setPixmap(qr_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)
        
        # Tombol konfirmasi pembayaran
        btn_confirm = QPushButton("Konfirmasi Pembayaran")
        btn_confirm.clicked.connect(lambda: self.konfirmasi_pembayaran(data, dialog))
        layout.addWidget(btn_confirm)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def konfirmasi_pembayaran(self, data, dialog):
        """Konfirmasi pembayaran dan generate sertifikat"""
        reply = QMessageBox.question(dialog, "Konfirmasi", 
                                    "Apakah pembayaran sudah di-scan dan selesai?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET pembayaran=1 WHERE id_pendaftar=%s", (data[0],))
                conn.commit()
                cursor.close()
                conn.close()
                
                # Generate sertifikat
                self.generate_certificate(data)
                
                # Tutup dialog dan refresh
                dialog.accept()
                if self.table.isVisible():
                    self.load_data()
                self.clear_form()
                
                QMessageBox.information(self, "Sukses", 
                                    "Pembayaran berhasil! Sertifikat telah di-generate.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Gagal konfirmasi pembayaran: {str(e)}")

    def generate_certificate(self, data):
        """Generate sertifikat pembayaran"""
        # Ukuran sertifikat
        width, height = 800, 600
        
        # Buat gambar dengan background putih
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Warna
        color_header = (44, 120, 115) 
        color_text = (51, 51, 51)  
        color_accent = (111, 185, 143)
        
        # Gambar border
        draw.rectangle([20, 20, width-20, height-20], outline=color_header, width=5)
        draw.rectangle([30, 30, width-30, height-30], outline=color_accent, width=2)
        
        # Load font (gunakan font default jika tidak ada)
        try:
            font_title = ImageFont.truetype("Arial.ttf", 40)
            font_subtitle = ImageFont.truetype("Arial.ttf", 24)
            font_text = ImageFont.truetype("Arial.ttf", 18)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
            font_text = ImageFont.load_default()
        
        # Judul
        title = "SERTIFIKAT PEMBAYARAN"
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) / 2, 80), title, fill=color_header, font=font_title)
        
        # Subtitle
        subtitle = "Les Matematika by Aero Afril"
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        draw.text(((width - subtitle_width) / 2, 140), subtitle, fill=color_accent, font=font_subtitle)
        
        # Garis pembatas
        draw.line([100, 180, width-100, 180], fill=color_accent, width=2)
        
        # Detail pembayaran
        y_pos = 220
        details = [
            f"Nomor ID: {data[0]}",
            f"Nama: {data[1]}",
            f"Tanggal Lahir: {data[2]}",
            f"Alamat: {data[4]}, {data[5]}, {data[6]}",
            f"Pendidikan: {data[7]}",
            f"Langganan: {data[10]}",
            f"Total Pembayaran: {data[11]}",
            f"Status: LUNAS"
        ]
        
        for detail in details:
            draw.text((100, y_pos), detail, fill=color_text, font=font_text)
            y_pos += 35
        
        # Footer
        footer = "Terima kasih atas pembayaran Anda"
        footer_bbox = draw.textbbox((0, 0), footer, font=font_text)
        footer_width = footer_bbox[2] - footer_bbox[0]
        draw.text(((width - footer_width) / 2, height - 80), footer, fill=color_text, font=font_text)
        
        # Simpan sertifikat
        filename = f"sertifikat_{data[0]}_{data[1].replace(' ', '_')}.png"
        img.save(filename)
        
        # Tampilkan sertifikat
        self.show_certificate(filename)

    def show_certificate(self, filename):
        """Menampilkan sertifikat yang sudah di-generate"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Sertifikat Pembayaran")
        dialog.setFixedSize(850, 650)
        
        layout = QVBoxLayout()
        
        # Load dan tampilkan gambar
        pixmap = QPixmap(filename)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Info
        info_label = QLabel(f"Sertifikat berhasil disimpan di: {filename}")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #2C7873; font-weight: bold; padding: 10px;")
        layout.addWidget(info_label)
        
        # Tombol tutup
        btn_close = QPushButton("Tutup")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
        
        dialog.setLayout(layout)
        dialog.exec_()


    # tab pengajar

    def tab_pengajar(self):
        """Membuat tab untuk data pengajar"""
        tab = QWidget()
        outer_layout = QVBoxLayout(tab)

        # Search box pengajar
        search_layout = QHBoxLayout()
        search_layout.addStretch()
        self.search_pengajar_input = QLineEdit()
        self.search_pengajar_input.setPlaceholderText("Cari pengajar...")
        self.search_pengajar_input.setMaximumWidth(250)
        self.search_pengajar_input.setObjectName("searchInput")
        search_layout.addWidget(self.search_pengajar_input)
        
        self.btn_cari_pengajar = QPushButton("Cari")
        self.btn_cari_pengajar.setMaximumWidth(100)
        self.btn_cari_pengajar.setObjectName("searchButton")
        search_layout.addWidget(self.btn_cari_pengajar)
        outer_layout.addLayout(search_layout)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        scroll_area.setWidget(container)
        outer_layout.addWidget(scroll_area)

        # Form Pengajar
        form_group = QGroupBox("Form Data Pengajar")
        form_layout = QHBoxLayout()
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(Qt.gray))
        form_group.setGraphicsEffect(shadow)

        # Grid form pengajar
        form_grid = QGridLayout()
        
        # Input fields untuk pengajar
        self.namaPengajar = QLineEdit()
        self.tanggalLahirPengajar = QDateEdit()
        self.tanggalLahirPengajar.setDisplayFormat("yyyy-MM-dd")
        self.tanggalLahirPengajar.setCalendarPopup(True)
        self.tanggalLahirPengajar.setDate(QDate.currentDate())
        self.pendidikanTerakhir = QComboBox()
        self.pendidikanTerakhir.addItems(["D3", "S1", "S2", "S3"])
        self.prestasiPengajar = QLineEdit()
        self.asalKampusPengajar = QLineEdit()
        self.pendidikanDiPengajar = QComboBox()
        self.pendidikanDiPengajar.addItems(["SD/Sederajat", "SMP/Sederajat", "SMA/SMK/Sederajat"])
        self.nomorPengajar = QLineEdit()
        
        # Gender pengajar
        gender_pengajar_group = QGroupBox("Gender")
        gender_pengajar_layout = QHBoxLayout()
        self.pengajar_radio_laki = QRadioButton("Laki-laki")
        self.pengajar_radio_perempuan = QRadioButton("Perempuan")
        gender_pengajar_layout.addWidget(self.pengajar_radio_laki)
        gender_pengajar_layout.addWidget(self.pengajar_radio_perempuan)
        gender_pengajar_group.setLayout(gender_pengajar_layout)

        # Buttons CRUD pengajar
        self.btn_tambah_pengajar = QPushButton("Tambah")
        self.btn_edit_pengajar = QPushButton("Edit")
        self.btn_hapus_pengajar = QPushButton("Hapus")
        self.btn_refresh_pengajar = QPushButton("Refresh")
        self.btn_tampilkan_pengajar = QPushButton("Tampilkan Data")

        crud_layout_pengajar = QVBoxLayout()
        crud_layout_pengajar.addWidget(self.btn_tambah_pengajar)
        crud_layout_pengajar.addWidget(self.btn_edit_pengajar)
        crud_layout_pengajar.addWidget(self.btn_hapus_pengajar)
        crud_layout_pengajar.addWidget(self.btn_refresh_pengajar)
        crud_layout_pengajar.addWidget(self.btn_tampilkan_pengajar)

        crud_box_pengajar = QWidget()
        crud_box_pengajar.setLayout(crud_layout_pengajar)

        # Add to grid
        form_grid.addWidget(QLabel("Nama Pengajar"), 0, 0)
        form_grid.addWidget(self.namaPengajar, 0, 1)
        form_grid.addWidget(QLabel("Tanggal lahir"), 1, 0)
        form_grid.addWidget(self.tanggalLahirPengajar, 1, 1)
        form_grid.addWidget(QLabel("Pendidikan Terakhir"), 2, 0)
        form_grid.addWidget(self.pendidikanTerakhir, 2, 1)
        form_grid.addWidget(QLabel("Prestasi"), 3, 0)
        form_grid.addWidget(self.prestasiPengajar, 3, 1)
        form_grid.addWidget(QLabel("Asal Universitas"), 4, 0)
        form_grid.addWidget(self.asalKampusPengajar, 4, 1)
        form_grid.addWidget(QLabel("Pendidikan"), 5, 0)
        form_grid.addWidget(self.pendidikanDiPengajar, 5, 1)
        form_grid.addWidget(QLabel("Nomor Telepon"), 6, 0)
        form_grid.addWidget(self.nomorPengajar, 6, 1)
        form_grid.addWidget(gender_pengajar_group, 7, 0, 1, 2)
        form_grid.addWidget(crud_box_pengajar, 0, 2, 8, 1)

        form_layout.addLayout(form_grid)

        # Table pengajar
        self.table_pengajar = QTableWidget()
        self.table_pengajar.setColumnCount(10)
        self.table_pengajar.setHorizontalHeaderLabels([
            "Pilih",
            "ID Pengajar",
            "Nama",
            "Tanggal Lahir",
            "Pendidikan Terakhir",
            "Prestasi",
            "Asal Universitas",
            "Mengajar",
            "Nomor Telepon",
            "Gender"
        ])

        # Atur lebar kolom
        self.table_pengajar.setColumnWidth(0, 60)
        self.table_pengajar.setColumnWidth(1, 100)
        self.table_pengajar.setColumnWidth(2, 200)
        self.table_pengajar.setColumnWidth(3, 150)
        self.table_pengajar.setColumnWidth(4, 150)
        self.table_pengajar.setColumnWidth(5, 200)
        self.table_pengajar.setColumnWidth(6, 200)
        self.table_pengajar.setColumnWidth(7, 150)
        self.table_pengajar.setColumnWidth(8, 250)
        self.table_pengajar.setColumnWidth(9, 150)

        header = self.table_pengajar.horizontalHeader()
        for i in range(self.table_pengajar.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Interactive)

        self.table_pengajar.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_pengajar.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_pengajar.verticalHeader().setDefaultSectionSize(50)
        self.table_pengajar.setMinimumHeight(500)
        self.table_pengajar.setAlternatingRowColors(True)
        self.table_pengajar.hide()
        
        main_layout.addWidget(self.table_pengajar)

        # Status label
        self.label_selected_pengajar = QLabel("ID terpilih: -")
        main_layout.addWidget(self.label_selected_pengajar)

        # Event handlers
        self.btn_tambah_pengajar.clicked.connect(self.save_pengajar)
        self.btn_edit_pengajar.clicked.connect(self.edit_pengajar)
        self.btn_hapus_pengajar.clicked.connect(self.delete_pengajar)
        self.btn_refresh_pengajar.clicked.connect(self.refresh_pengajar)
        self.btn_tampilkan_pengajar.clicked.connect(self.tampilkan_pengajar)
        self.btn_cari_pengajar.clicked.connect(self.search_pengajar)
        self.search_pengajar_input.returnPressed.connect(self.search_pengajar)
        self.table_pengajar.cellClicked.connect(self.fill_form_pengajar)

        return tab


    def get_gender_pengajar(self):
        if self.pengajar_radio_laki.isChecked():
            return 1
        elif self.pengajar_radio_perempuan.isChecked():
            return 0
        return None

    def clear_form_pengajar(self):
        """Membersihkan form pengajar"""
        self.namaPengajar.clear()
        self.tanggalLahirPengajar.setDate(QDate.currentDate())
        self.pendidikanTerakhir.setCurrentIndex(0)
        self.prestasiPengajar.clear()
        self.asalKampusPengajar.clear()
        self.pendidikanDiPengajar.setCurrentIndex(0)
        self.nomorPengajar.clear()
        self.pengajar_radio_laki.setAutoExclusive(False)
        self.pengajar_radio_perempuan.setAutoExclusive(False)
        self.pengajar_radio_laki.setChecked(False)
        self.pengajar_radio_perempuan.setChecked(False)
        self.pengajar_radio_laki.setAutoExclusive(True)
        self.pengajar_radio_perempuan.setAutoExclusive(True)
        self.label_selected_pengajar.setText("ID terpilih: -")

    def generate_id_pengajar(self):
        """Generate ID pengajar otomatis (P1, P2, P3, dst)"""
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_pengajar FROM pengajar ORDER BY id_pengajar DESC LIMIT 1")
            result = cursor.fetchone()
            
            if result:
                last_id = result[0]
                if last_id.startswith('P'):
                    last_num = int(last_id[1:])
                    new_num = last_num + 1
                else:
                    new_num = 1
            else:
                new_num = 1
            
            cursor.close()
            conn.close()
            return f"P{new_num}"
        except Exception as e:
            print(f"Error generating ID: {e}")
            return "P1"

    def save_pengajar(self):
        """Menyimpan data pengajar baru"""
        nama = self.namaPengajar.text().strip()
        tanggal = self.tanggalLahirPengajar.date().toString("yyyy-MM-dd")
        pendidikanPengajar = self.pendidikanTerakhir.currentText()
        prestasi = self.prestasiPengajar.text().strip()
        asalKampus = self.asalKampusPengajar.text().strip()
        pendidikan = self.pendidikanDiPengajar.currentText()
        telepon = self.nomorPengajar.text().strip()

        gender = self.get_gender_pengajar()

        if gender is None:
            QMessageBox.warning(self, "Peringatan", "Pilih gender terlebih dahulu!")
            return

        if not nama or not prestasi or not asalKampus or not telepon:
            QMessageBox.warning(self, "Peringatan", "Lengkapi field yang wajib (Nama, Prestasi, Asal Kampus, Telepon)!")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            
            id_pengajar = self.generate_id_pengajar()
            
            query = """INSERT INTO pengajar (id_pengajar, nama_pengajar, tanggal_lahir_pengajar, tingkatLulusTerakhir, prestasi, asal_kampus, pendidikan, nomor_pengajar, gender)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (id_pengajar, nama, tanggal, pendidikanPengajar, prestasi, asalKampus, pendidikan, telepon, gender))
            conn.commit()
            QMessageBox.information(self, "Sukses", f"Data pengajar berhasil disimpan dengan ID: {id_pengajar}")
            self.clear_form_pengajar()
            if self.table_pengajar.isVisible():
                self.load_pengajar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def load_pengajar(self):
        """Memuat data pengajar dari database"""
        self.table_pengajar.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pengajar ORDER BY id_pengajar DESC")
            results = cursor.fetchall()

            for row_idx, row_data in enumerate(results):
                self.table_pengajar.insertRow(row_idx)
                
                # Checkbox
                checkbox = QCheckBox()
                cell_widget = QWidget()
                layout_cb = QHBoxLayout(cell_widget)
                layout_cb.addWidget(checkbox)
                layout_cb.setAlignment(checkbox, Qt.AlignCenter)
                layout_cb.setContentsMargins(0, 0, 0, 0)
                self.table_pengajar.setCellWidget(row_idx, 0, cell_widget)

                # Data
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)

                    if col_idx == 8:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setText("Laki-laki")
                        else:
                            item.setText("Perempuan")

                    self.table_pengajar.setItem(row_idx, col_idx + 1, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def fill_form_pengajar(self, row, col):
        """Mengisi form dari baris tabel yang diklik"""
        try:
            id_val = self.table_pengajar.item(row, 1).text()
            self.label_selected_pengajar.setText(f"ID terpilih: {id_val}")
            
            self.namaPengajar.setText(self.table_pengajar.item(row, 2).text())
            
            tanggal_str = self.table_pengajar.item(row, 3).text()
            tanggal = QDate.fromString(tanggal_str, "yyyy-MM-dd")
            self.tanggalLahirPengajar.setDate(tanggal)
            
            pendidikan_text = self.table_pengajar.item(row, 4).text()
            index = self.pendidikanTerakhir.findText(pendidikan_text)
            if index >= 0:
                self.pendidikanTerakhir.setCurrentIndex(index)
            
            self.prestasiPengajar.setText(self.table_pengajar.item(row, 5).text())
            self.asalKampusPengajar.setText(self.table_pengajar.item(row, 6).text())

            pendidikan = self.table.item(row, 7).text()
            idx = self.pendidikanDiPengajar.findText(pendidikan)
            if idx >= 0:
                self.pendidikanDiPengajar.setCurrentIndex(idx)

            self.nomorPengajar.setText(self.table_pengajar.item(row, 8).text())
            
            # Get gender from database
            try:
                conn = self.connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT gender FROM pengajar WHERE id_pengajar=%s", (id_val,))
                result = cursor.fetchone()
                
                if result:
                    gender_val = result[0]
                    self.pengajar_radio_laki.setAutoExclusive(False)
                    self.pengajar_radio_perempuan.setAutoExclusive(False)
                    self.pengajar_radio_laki.setChecked(False)
                    self.pengajar_radio_perempuan.setChecked(False)
                    self.pengajar_radio_laki.setAutoExclusive(True)
                    self.pengajar_radio_perempuan.setAutoExclusive(True)
                    
                    if int(gender_val) == 1:
                        self.pengajar_radio_laki.setChecked(True)
                    else:
                        self.pengajar_radio_perempuan.setChecked(True)
                
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error getting gender: {e}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mengisi form: {str(e)}")

    def edit_pengajar(self):
        """Mengupdate data pengajar"""
        id_text = self.label_selected_pengajar.text()
        if id_text == "ID terpilih: -":
            QMessageBox.warning(self, "Peringatan", "Pilih data dari tabel terlebih dahulu!")
            return

        id_val = id_text.split(": ")[1]
        
        nama = self.namaPengajar.text().strip()
        tanggal = self.tanggalLahirPengajar.date().toString("yyyy-MM-dd")
        pendidikanTerakhir = self.pendidikanTerakhir.currentText()
        prestasi = self.prestasiPengajar.text().strip()
        asalKampus = self.asalKampusPengajar.text().strip()
        pendidikan = self.pendidikanDiPengajar.currentText()
        telepon = self.nomorPengajar.text().strip()

        gender = self.get_gender_pengajar()

        if gender is None:
            QMessageBox.warning(self, "Peringatan", "Pilih gender terlebih dahulu!")
            return

        if not nama or not prestasi or not asalKampus or not telepon:
            QMessageBox.warning(self, "Peringatan", "Lengkapi field yang wajib!")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = """UPDATE pengajar SET nama_pengajar=%s, tanggal_lahir_pengajar=%s, tingkatLulusTerakhir=%s, prestasi=%s, asal_kampus=%s, pendidikan=%s, nomor_pengajar=%s, gender=%s 
                    WHERE id_pengajar=%s"""
            cursor.execute(query, (nama, tanggal, pendidikanTerakhir, prestasi, asalKampus, pendidikan, telepon, gender, id_val))
            conn.commit()
            QMessageBox.information(self, "Sukses", "Data berhasil diupdate!")
            self.clear_form_pengajar()
            if self.table_pengajar.isVisible():
                self.load_pengajar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal update data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def delete_pengajar(self):
        """Menghapus data pengajar yang dipilih"""
        ids_to_delete = []
        
        for row in range(self.table_pengajar.rowCount()):
            cell_widget = self.table_pengajar.cellWidget(row, 0)
            if cell_widget:
                checkbox = cell_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    id_val = self.table_pengajar.item(row, 1).text()
                    ids_to_delete.append(id_val)
        
        if not ids_to_delete:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus!")
            return

        reply = QMessageBox.question(self, "Konfirmasi", 
                                    f"Hapus {len(ids_to_delete)} data?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            for id_val in ids_to_delete:
                cursor.execute("DELETE FROM pengajar WHERE id_pengajar=%s", (id_val,))
            conn.commit()
            QMessageBox.information(self, "Sukses", f"{len(ids_to_delete)} data berhasil dihapus!")
            self.clear_form_pengajar()
            self.load_pengajar()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menghapus data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def search_pengajar(self):
        """Mencari data pengajar"""
        keyword = self.search_pengajar_input.text().strip()
        
        if not keyword:
            QMessageBox.warning(self, "Peringatan", "Masukkan kata kunci untuk mencari!")
            return

        if not self.table_pengajar.isVisible():
            self.table_pengajar.show()
            self.btn_tampilkan_pengajar.setText("Sembunyikan Data")

        self.table_pengajar.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            query = """SELECT * FROM pengajar WHERE 
                    id_pengajar LIKE %s OR 
                    nama_pengajar LIKE %s OR 
                    tanggal_lahir_pengajar LIKE %s OR 
                    tingkatLulusTerakhir LIKE %s OR 
                    prestasi LIKE %s OR 
                    asal_kampus LIKE %s OR 
                    pendidikan LIKE %s OR
                    nomor_pengajar LIKE %s"""
            search_param = f"%{keyword}%"
            cursor.execute(query, (search_param,) * 8)
            results = cursor.fetchall()

            if not results:
                QMessageBox.information(self, "Info", "Data tidak ditemukan!")
                return

            for row_idx, row_data in enumerate(results):
                self.table_pengajar.insertRow(row_idx)
                checkbox = QCheckBox()
                cell_widget = QWidget()
                layout_cb = QHBoxLayout(cell_widget)
                layout_cb.addWidget(checkbox)
                layout_cb.setAlignment(checkbox, Qt.AlignCenter)
                layout_cb.setContentsMargins(0, 0, 0, 0)
                self.table_pengajar.setCellWidget(row_idx, 0, cell_widget)

                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    if col_idx == 8:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setText("Laki-laki")
                        else:
                            item.setText("Perempuan")
                    
                    self.table_pengajar.setItem(row_idx, col_idx + 1, item)
            
            QMessageBox.information(self, "Hasil Pencarian", 
                                f"Ditemukan {len(results)} data dengan kata kunci '{keyword}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mencari data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def refresh_pengajar(self):
        """Refresh data pengajar"""
        self.clear_form_pengajar()
        self.load_pengajar()
        QMessageBox.information(self, "Info", "Data berhasil direfresh!")

    def tampilkan_pengajar(self):
        """Menampilkan/menyembunyikan tabel pengajar"""
        if self.table_pengajar.isVisible():
            self.table_pengajar.hide()
            self.btn_tampilkan_pengajar.setText("Tampilkan Data")
        else:
            self.table_pengajar.show()
            self.load_pengajar()
            self.btn_tampilkan_pengajar.setText("Sembunyikan Data")

    # tab penugasan
    def tab_penugasan(self):
        tab = QWidget()
        outer_layout = QVBoxLayout(tab)

        search_layout = QHBoxLayout()
        search_layout.addStretch()
        
        self.btn_refresh_penugasan = QPushButton("Refresh")
        self.btn_refresh_penugasan.setMaximumWidth(100)
        self.btn_refresh_penugasan.setObjectName("refreshButton")
        self.btn_refresh_penugasan.clicked.connect(self.refresh_penugasan)
        search_layout.addWidget(self.btn_refresh_penugasan)

        # Input pencarian
        self.search_penugasan_input = QLineEdit()
        self.search_penugasan_input.setPlaceholderText("Cari penugasan...")
        self.search_penugasan_input.setMaximumWidth(250)
        self.search_penugasan_input.setObjectName("searchInput")
        search_layout.addWidget(self.search_penugasan_input)
        
        # Tombol Cari
        self.btn_cari_penugasan = QPushButton("Cari")
        self.btn_cari_penugasan.setMaximumWidth(100)
        self.btn_cari_penugasan.setObjectName("searchButton")
        search_layout.addWidget(self.btn_cari_penugasan)
        
        outer_layout.addLayout(search_layout)

        # Event handlers untuk penugasan
        self.btn_cari_penugasan.clicked.connect(self.search_penugasan)
        self.search_penugasan_input.returnPressed.connect(self.search_penugasan)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        scroll_area.setWidget(container)
        outer_layout.addWidget(scroll_area)

        # Form Penugasan
        form_group = QGroupBox("Form Data Penugasan")
        form_layout = QHBoxLayout()
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor(Qt.gray))
        form_group.setGraphicsEffect(shadow)

        # Table penugasan
        self.table_Penugasan = QTableWidget()
        self.table_Penugasan.setColumnCount(4)
        self.table_Penugasan.setHorizontalHeaderLabels([
            "Nama Siswa",
            "Pendidikan",
            "Nama Pengajar",
            "Status Pembayaran"
        ])

        # Set column widths
        self.table_Penugasan.setColumnWidth(0, 250)
        self.table_Penugasan.setColumnWidth(1, 200)
        self.table_Penugasan.setColumnWidth(2, 250)
        self.table_Penugasan.setColumnWidth(3, 180)

        # Header configuration
        header = self.table_Penugasan.horizontalHeader()
        for i in range(self.table_Penugasan.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Table properties
        self.table_Penugasan.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_Penugasan.setVerticalScrollMode(QTableWidget.ScrollPerPixel)
        self.table_Penugasan.verticalHeader().setDefaultSectionSize(50)
        self.table_Penugasan.setMinimumHeight(500)
        self.table_Penugasan.setAlternatingRowColors(True)
        self.table_Penugasan.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_Penugasan.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_Penugasan.setSelectionMode(QTableWidget.SingleSelection)
        
        main_layout.addWidget(self.table_Penugasan)
        
        # Load data
        self.load_penugasan()
        
        return tab

    def load_penugasan(self):
        """Memuat data penugasan dari database"""
        self.table_Penugasan.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.nama_pendaftar, u.pendidikan, p.nama_pengajar, u.pembayaran 
                FROM users u
                JOIN pengajar p 
                ON u.pendidikan = p.pendidikan 
                WHERE u.pembayaran = 1
            """)
            results = cursor.fetchall()

            for row_idx, row_data in enumerate(results):
                self.table_Penugasan.insertRow(row_idx)
                
                # Data columns
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)

                    # Format status pembayaran
                    if col_idx == 3:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setBackground(QColor(144, 238, 144))
                            item.setForeground(QColor(0, 100, 0))
                            item.setText("LUNAS")
                        else:
                            item.setBackground(QColor(255, 182, 193))
                            item.setForeground(QColor(139, 0, 0))
                            item.setText("BELUM LUNAS")

                    self.table_Penugasan.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def clear_form_penugasan(self):
        """Membersihkan form penugasan"""
        # Clear search input
        self.search_penugasan_input.clear()
        
        # Clear table selection
        self.table_Penugasan.clearSelection()

    def search_penugasan(self):
        """Mencari data penugasan"""
        keyword = self.search_penugasan_input.text().strip()
        
        if not keyword:
            QMessageBox.warning(self, "Peringatan", "Masukkan kata kunci untuk mencari!")
            return

        self.table_Penugasan.setRowCount(0)
        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            # Query pencarian untuk tabel penugasan
            query = """
                SELECT u.nama_pendaftar, u.pendidikan, p.nama_pengajar, u.pembayaran 
                FROM users u
                JOIN pengajar p 
                ON u.pendidikan = p.pendidikan 
                WHERE u.pembayaran = 1
                AND (u.nama_pendaftar LIKE %s 
                    OR u.pendidikan LIKE %s 
                    OR p.nama_pengajar LIKE %s)
            """
            search_param = f"%{keyword}%"
            cursor.execute(query, (search_param, search_param, search_param))
            results = cursor.fetchall()

            if not results:
                QMessageBox.information(self, "Info", "Data tidak ditemukan!")
                return

            for row_idx, row_data in enumerate(results):
                self.table_Penugasan.insertRow(row_idx)
                
                # Data columns
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)

                    # Format status pembayaran
                    if col_idx == 3:
                        if str(value) == '1' or str(value).lower() == 'true':
                            item.setBackground(QColor(144, 238, 144))
                            item.setForeground(QColor(0, 100, 0))
                            item.setText("LUNAS")
                        else:
                            item.setBackground(QColor(255, 182, 193))
                            item.setForeground(QColor(139, 0, 0))
                            item.setText("BELUM LUNAS")

                    self.table_Penugasan.setItem(row_idx, col_idx, item)
            
            QMessageBox.information(self, "Hasil Pencarian", 
                                f"Ditemukan {len(results)} data dengan kata kunci '{keyword}'")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal mencari data: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
                
    def refresh_penugasan(self):
        """Refresh data penugasan"""
        self.clear_form_penugasan()
        self.load_penugasan()
        QMessageBox.information(self, "Info", "Data penugasan berhasil direfresh!")

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())