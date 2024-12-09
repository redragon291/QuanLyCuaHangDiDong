import tkinter as tk
from tkinter import Tk, Label, Entry, Button, Listbox, messagebox, END, StringVar, Frame, Toplevel, PhotoImage, Image, simpledialog, Canvas, image_names,ttk
import csv
import os
from datetime import date,datetime
from PIL import Image,ImageTk

def hide_all_frames():
    for widget in GDienChinh.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.place_forget()
def GiaoDien_HD():
    hide_all_frames()
    dataKhachhang = "Datakhachhang.csv"
    columnsKhachHang = ["Mã Khách Hàng", "Tên Khách Hàng", "Địa Chỉ", "Số Điện Thoại"]
    if not os.path.exists(dataKhachhang):
        with open(dataKhachhang, mode='w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(columnsKhachHang)

    dataHoaDon="DataHoaDon.csv"
    columnsHoaDon = ["Mã Hoá Đơn", "Tên Khách Hàng", "Tên Nhân Viên","Tên sản phẩm","Sô lượng mua","Thành tiền","Ngày Mua"]
    if not os.path.exists(dataHoaDon):
        with open(dataHoaDon, mode='w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(columnsHoaDon)
    def LayDataNgay(file_path):
        dates = set()
        try:
            with open(file_path, "r", encoding="utf8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date_str = row.get("Ngày Mua", "")
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        dates.add(date_obj.strftime("%Y-%m-%d"))
                    except ValueError:
                        continue
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại.")
        return sorted(dates)
    def LaySanPham(file):
        sanpham = []
        try:
            with open(file, "r", encoding="utf8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sanpham.append(row["Tên Sản Phẩm"])
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"File {file} không tồn tại.")
        return sanpham
    def TinhThanhTien(TenSp,SoLuong):
        ThanhTien=0
        if TenSp:
            TenSp = TenSp.lower()
        else:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        try:
            SoLuong = int(SoLuong)
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là một số nguyên.")
            return 0
        with open("Datakho.csv",'r',encoding='utf8') as f:
            reader = csv.DictReader(f)
            found = False
            for row in reader:
                if TenSp in row["Tên Sản Phẩm"].lower():
                    try:
                        gia = int(row["Giá"])
                    except ValueError:
                        messagebox.showerror("Lỗi", "Giá sản phẩm không hợp lệ.")
                        return 0
                    ThanhTien=ThanhTien+(gia*SoLuong)
                    found = True
                    break
            if not found:
                ls.insert(END, "Không tìm thấy sản phẩm phù hợp.")
                return 0
        return ThanhTien
    def LuuKhachHang(Ma_Kh,ten_Kh,Dia_chi,Sdt):
        with open(dataKhachhang, mode='a', newline='', encoding='utf-8') as file:
            writer=csv.writer(file)
            writer.writerow([Ma_Kh,ten_Kh, Dia_chi,Sdt])
        messagebox.showinfo("Thông Báo", f"Khách Hàng '{ten_Kh}' đã được thêm.")
    def LuuHoaDon(Ma_Hoa,ten_Kh,tennv,Ten_sp,SL_Mua,TTien,NgayMua):
        with open(dataHoaDon, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([Ma_Hoa, ten_Kh,tennv ,Ten_sp,SL_Mua,TTien,NgayMua])
        messagebox.showinfo("Thông Báo", f"Hoá Đơn '{Ma_Hoa}' đã được thêm.")
    def SinhMaKh():
        existing_ids = set()
        with open(dataKhachhang, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(row["Mã Khách Hàng"])

        new_id = 1
        while True:
            new_id_str = f"KH{new_id:03}"
            if new_id_str not in existing_ids:
                return new_id_str
            new_id += 1
    def SinhMaHD():
        existing_ids = set()
        with open(dataHoaDon, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(row["Mã Hoá Đơn"])

        new_id = 1
        while True:
            new_id_str = f"HD{new_id:03}"
            if new_id_str not in existing_ids:
                return new_id_str
            new_id += 1
    def XuatHoaDon():
        ls.delete(0, END)
        Ma_Hoa = SinhMaHD()
        stringMaHoaDon.set(Ma_Hoa)
        Ma_Kh = SinhMaKh()
        stringMakh.set(Ma_Kh)
        ten_Kh = stringTenkh.get()
        Ten_sp=cbsanpham.get()
        SL_Mua=stringSoLuongMua.get()
        Dia_chi = stringDiaChi.get()
        Sdt = stringSoDienThoai.get()
        NgayMua=date.today()
        tennhanvien=''
        manv=stringMaNhanVien.get()
        rowss = []
        with open("DataNhanVien.csv",'r',encoding="utf8") as f:
            reader = csv.DictReader(f)
            soluongmoi=0
            found = False
            for row in reader:
                if manv.lower() == row["Mã Nhân Viên"].lower():
                    sohientai = int(row["Số Lượng Bán"])
                    soluongmoi = sohientai + int(SL_Mua)
                    row["Số Lượng Bán"] = str(soluongmoi)
                    tennhanvien = row["Tên Nhân Viên"]
                    found = True
                rowss.append(row)
            if not found:
                messagebox.showinfo("Lỗi", "Mã Nhân Viên Không Hợp Lệ!")
                return
        with open("DataNhanVien.csv",'w',encoding='utf8') as f:
            write = csv.DictWriter(f,fieldnames=["Mã Nhân Viên", "Tên Nhân Viên", "Số Điện Thoại", "Địa Chỉ","Chức Vụ","Số Lượng Bán","Lương"])
            write.writeheader()
            write.writerows(rowss)
        datakho = "Datakho.csv"
        rows = []
        sl_mua_int = int(SL_Mua)

        with open(datakho, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Tên Sản Phẩm"] == Ten_sp:
                    so_luong_hien_tai = int(row["Số Lượng"])
                    so_luong_moi = so_luong_hien_tai - sl_mua_int
                    if so_luong_moi < 0:
                        messagebox.showerror("Lỗi", "Số lượng mua vượt quá số lượng có trong kho.")
                        return
                    row["Số Lượng"] = str(so_luong_moi)
                rows.append(row)

        with open(datakho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Mã Sản Phẩm", "Tên Sản Phẩm", "Giá", "Số Lượng"])
            writer.writeheader()
            writer.writerows(rows)
        TTien=TinhThanhTien(Ten_sp,SL_Mua)
        ls.insert(END, "-" * 50)
        ls.insert(END, f"{'HÓA ĐƠN BÁN HÀNG':^50}")
        ls.insert(END, "-" * 50)
        ls.insert(END, f"{'Mã Hóa Đơn:':<20} {Ma_Hoa}")
        ls.insert(END, f"{'Tên Khách Hàng:':<20} {ten_Kh}")
        ls.insert(END, f"{'Mã Khách Hàng:':<20} {Ma_Kh}")
        ls.insert(END, f"{'Địa Chỉ:':<20} {Dia_chi}")
        ls.insert(END, f"{'Số Điện Thoại:':<20} {Sdt}")
        ls.insert(END, "-" * 50)
        ls.insert(END, f"{'Tên Sản Phẩm':<25} {'Số Lượng':<10} {'Thành Tiền'}")
        ls.insert(END, "-" * 50)
        ls.insert(END, f"{Ten_sp:<25} {SL_Mua:<10} {TTien} VND")
        ls.insert(END, "-" * 50)
        ls.insert(END, f"{'Tên Nhân Viên Lập Bán:':<20} {tennhanvien}")
        ls.insert(END, f"{'Ngày Mua:':<20} {NgayMua}")
        ls.insert(END, "-" * 50)
        if not Ma_Kh or not ten_Kh or not Dia_chi or not Sdt:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        LuuKhachHang(Ma_Kh,ten_Kh, Dia_chi, Sdt)
        LuuHoaDon(Ma_Hoa,ten_Kh,tennhanvien ,Ten_sp, SL_Mua, TTien, NgayMua)
    def Xoa():
        index = ls.curselection()
        if not index or index[0] == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa!")
            return
        text = ls.get(index)
        tx = text.split(" - ")
        ma_de_xoa = tx[0]
        ten_de_xoa=tx[1]
        changeKhachHang = []
        with open(dataKhachhang, 'r', encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Mã Khách Hàng"] != ma_de_xoa:
                    changeKhachHang.append(row)
        with open(dataKhachhang, 'w', newline='', encoding="utf8") as f:
            wr = csv.DictWriter(f, fieldnames=columnsKhachHang)
            wr.writeheader()
            wr.writerows(changeKhachHang)
        changeHoaDon=[]
        with open(dataHoaDon, 'r', encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Mã Hoá Đơn"] != ma_de_xoa:
                    changeHoaDon.append(row)
        with open(dataHoaDon, 'w', newline='', encoding="utf8") as f:
            wr = csv.DictWriter(f, fieldnames=columnsHoaDon)
            wr.writeheader()
            wr.writerows(changeHoaDon)
        messagebox.showinfo("Thông Báo", f"Đã xoá.")
    def HienThiKhachHang():
        ls.delete(0, END)
        header = " - ".join(columnsKhachHang)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))
        with open(dataKhachhang, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = f"{row['Mã Khách Hàng']} - {row['Tên Khách Hàng']} - {row['Địa Chỉ']} - {row['Số Điện Thoại']}"
                ls.insert(END, item)
    def HienThiHoaDon():
        ls.delete(0, END)
        header = " - ".join(columnsHoaDon)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))
        with open(dataHoaDon, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = f"{row['Mã Hoá Đơn']} - {row['Tên Khách Hàng']} - {row['Tên sản phẩm']} - {row['Tên Nhân Viên']} - {row['Sô lượng mua']} - {row['Thành tiền']} - {row['Ngày Mua']}"
                ls.insert(END, item)
    def HoiDuLieu():
        HoiDL=tk.Toplevel()
        LuaChon=StringVar()
        LuaChon.set("Chưa Chọn")
        Label(HoiDL,text="Lựa chọn file dữ liệu cần tìm kiếm:",fg='black', justify=tk.CENTER,font=(15)).pack(pady=10)
        frRadiobox=tk.Frame(HoiDL)
        frRadiobox.pack(pady=10)
        raHoaDon=tk.Radiobutton(frRadiobox,text="Hoá Đơn",variable=LuaChon,value="Hoá Đơn")
        raHoaDon.pack(side="left", padx=10)
        raKhachHang = tk.Radiobutton(frRadiobox, text="Khách Hàng", variable=LuaChon, value="Khách Hàng")
        raKhachHang.pack(side="left", padx=10)
        def submit():
            Chon = LuaChon.get()
            if Chon == "Chưa Chọn":
                messagebox.showinfo("Lỗi", "Vui lòng chọn loại dữ liệu!")
            else:
                HoiDL.destroy()
                TimKiem(Chon)
        tk.Button(HoiDL, text="Xác nhận", command=lambda: submit()).pack(pady=10)
        def center_window(root):
            root.update_idletasks()
            width = root.winfo_width()
            height = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (width // 2)
            y = (root.winfo_screenheight() // 2) - (height // 2)
            root.geometry(f'{width}x{height}+{x}+{y}')
        center_window(HoiDL)
        HoiDL.mainloop()
    def TimKiem(Chon):
        ls.delete(0, END)
        if Chon:
            Chon = Chon.lower()
        else:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        tukhoa = simpledialog.askstring("Thông Báo", f"{'Vui lòng nhập mã'} {Chon} {' cần tìm của bạn:'}")
        if tukhoa:
            tukhoa = tukhoa.lower()
        else:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if not tukhoa:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if (Chon =="khách hàng"):
            with open(dataKhachhang, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                found = False
                for row in reader:
                    if tukhoa in row["Mã Khách Hàng"].lower() or tukhoa in row["Tên Khách Hàng"].lower():
                        item = f"{row['Mã Khách Hàng']} - {row['Tên Khách Hàng']} - {row['Địa Chỉ']} - {row['Số Điện Thoại']}"
                        ls.insert(END, item)
                        found = True
                if not found:
                    ls.insert(END, "Không tìm thấy sản phẩm phù hợp.")
        else :
            with open(dataHoaDon, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                found = False
                for row in reader:
                    if tukhoa in row["Mã Hoá Đơn"].lower():
                        item = f"{row['Mã Hoá Đơn']} - {row['Tên Khách Hàng']} - {row['Tên Nhân Viên']} -{row['Tên sản phẩm']} - {row['Sô lượng mua']} - {row['Thành tiền']} - {row['Ngày Mua']}"
                        ls.insert(END, item)
                        found = True
                if not found:
                    ls.insert(END, "Không tìm thấy sản phẩm phù hợp.")
    def SapXep():
        with open(dataKhachhang, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            sx = sorted(reader, key=lambda x: x["Tên Khách Hàng"])
        ls.delete(0, END)
        header = " - ".join(columnsKhachHang)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))

        for row in sx:
            item = f"{row['Mã Khách Hàng']} - {row['Tên Khách Hàng']} - {row['Địa Chỉ']} - {row['Số Điện Thoại']}"
            ls.insert(END, item)

    def hoiNgay():
        HoiNgay = tk.Toplevel()
        HoiNgay.title("Chọn khoảng thời gian")
        dataNgay = LayDataNgay(dataHoaDon)

        tk.Label(HoiNgay, text="Ngày bắt đầu (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        comboStart = ttk.Combobox(HoiNgay, values=dataNgay)
        comboStart.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(HoiNgay, text="Ngày kết thúc (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
        comboEnd = ttk.Combobox(HoiNgay, values=dataNgay)
        comboEnd.grid(row=1, column=1, padx=10, pady=10)

        def submit():
            start_date = comboStart.get()
            end_date = comboEnd.get()
            HoiNgay.destroy()
            Tinh(start_date, end_date)

        tk.Button(HoiNgay, text="Xác nhận", command=submit).grid(row=2, columnspan=2, padx=10, pady=10)

        def center_window(root):
            HoiNgay.update_idletasks()
            width = HoiNgay.winfo_width()
            height = HoiNgay.winfo_height()
            x = (HoiNgay.winfo_screenwidth() // 2) - (width // 2)
            y = (HoiNgay.winfo_screenheight() // 2) - (height // 2)
            HoiNgay.geometry(f'{width}x{height}+{x}+{y}')

        center_window(HoiNgay)
        HoiNgay.mainloop()

    def Tinh(ngay_bat_dau, ngay_ket_thuc):
        ls.delete(0, tk.END)
        if not ngay_bat_dau or not ngay_ket_thuc:
            messagebox.showwarning("Warning", "Bạn phải nhập cả hai ngày!")
            return
        try:
            ngay_bd = datetime.strptime(ngay_bat_dau, "%Y-%m-%d")
            ngay_kt = datetime.strptime(ngay_ket_thuc, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ (nên là YYYY-MM-DD)")
            return
        tong_doanh_thu = 0
        with open(dataHoaDon, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ngay_mua = datetime.strptime(row["Ngày Mua"], "%Y-%m-%d")
                    if ngay_bd <= ngay_mua <= ngay_kt:
                        tong_doanh_thu += int(row["Thành tiền"])
                except ValueError:
                    continue
        ls.insert(tk.END, f"Tổng doanh thu từ {ngay_bat_dau} đến {ngay_ket_thuc}: {tong_doanh_thu}")

    def TinhTongDoanhThu():
        hoiNgay()
    stringMaHoaDon = StringVar()
    stringMakh = StringVar()
    stringTenkh = StringVar()
    stringSoLuongMua= StringVar()
    stringDiaChi = StringVar()
    stringSoDienThoai = StringVar()
    stringMaNhanVien= StringVar()

    heading = tk.Frame(GDienChinh, bg='#e6f0fa', bd=3, relief="ridge")
    heading.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.05)

    KetQua = tk.Frame(GDienChinh, bd=3, relief="ridge")
    KetQua.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.4)

    frInput = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frInput.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.2)

    frButtons = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frButtons.place(relx=0.05, rely=0.9, relwidth=0.9, relheight=0.08)
    lbtt = tk.Label(heading, text="Thông Tin Khách Hàng", fg='black', justify=tk.CENTER,font=(30))
    lbtt.place(relx=0.5,rely=0.5,anchor="center")
    ls=tk.Listbox(KetQua,width=100)
    ls.place(relwidth=1, relheight=1)
    HienThiKhachHang();
    lbTenKH = tk.Label(frInput, text="Tên Khách Hàng: ", fg='black', justify=tk.CENTER)
    lbTenKH.grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringTenkh).grid(row=0, column=1, padx=5, pady=5)

    dataSanPham = "Datakho.csv"
    sanpham = LaySanPham(dataSanPham)
    lbTenSP = tk.Label(frInput, text="Tên Sản Phẩm: ", fg='black', justify=tk.CENTER)
    lbTenSP.grid(row=0, column=2, padx=5, pady=5)
    cbsanpham = ttk.Combobox(frInput, values=sanpham)
    cbsanpham.grid(row=0, column=3, padx=5, pady=5)

    lbSLMua = tk.Label(frInput, text="Số lượng mua: ", fg='black', justify=tk.CENTER)
    lbSLMua.grid(row=1, column=2, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringSoLuongMua).grid(row=1, column=3, padx=5, pady=5)

    lbSodt = tk.Label(frInput, text="Số Điện Thoại: ", fg='black', justify=tk.CENTER)
    lbSodt.grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringSoDienThoai).grid(row=1, column=1, padx=5, pady=5)

    lbDiaChi = tk.Label(frInput, text="Địa chỉ: ", fg='black', justify=tk.CENTER)
    lbDiaChi.grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringDiaChi).grid(row=3, column=1, padx=5, pady=5)

    lbNhanVien = tk.Label(frInput, text="Mã Nhân Viên Lập Hoá Đơn: ", fg='black', justify=tk.CENTER)
    lbNhanVien.grid(row=3, column=2, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringMaNhanVien).grid(row=3, column=3, padx=5, pady=5)

    btnAdd = tk.Button(frButtons, text="Thêm", justify=tk.CENTER, bg='lightblue', command=XuatHoaDon)
    btnAdd.grid(row=0, column=0, padx=5, pady=5)
    btnXoa = tk.Button(frButtons, text="Xoá", justify=tk.CENTER, bg='lightblue', command=Xoa)
    btnXoa.grid(row=0, column=1, padx=5, pady=5)
    btnHienThiKH = tk.Button(frButtons, text="Danh Sách Khách Hàng", justify=tk.CENTER, bg='lightblue',command=HienThiKhachHang)
    btnHienThiKH.grid(row=0, column=2, padx=5, pady=5)
    btnHienThiHD = tk.Button(frButtons, text="Danh Sách Hoá Đơn", justify=tk.CENTER, bg='lightblue',command=HienThiHoaDon)
    btnHienThiHD.grid(row=0, column=3, padx=5, pady=5)
    btnTimKiem = tk.Button(frButtons, text="Tìm kiếm", justify=tk.CENTER, bg='lightblue', command=HoiDuLieu)
    btnTimKiem.grid(row=0, column=4, padx=5, pady=5)
    btnSapXep = tk.Button(frButtons, text="Sắp xếp", justify=tk.CENTER, bg="lightblue", command=SapXep)
    btnSapXep.grid(row=0, column=5, padx=5, pady=5)
    btnTinhDoanhThu = tk.Button(frButtons, text="Tính Doanh Thu", justify=tk.CENTER, bg="lightblue",command=TinhTongDoanhThu)
    btnTinhDoanhThu.grid(row=0, column=6, padx=5, pady=5)
def GiaoDien_Kho():
    hide_all_frames()
    datakho = "Datakho.csv"
    columns = ["Mã Sản Phẩm", "Tên Sản Phẩm", "Giá", "Số Lượng"]

    if not os.path.exists(datakho):
        with open(datakho, mode='w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(columns)
    def SinhMaSP():
        existing_ids = set()
        with open(datakho, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(row["Mã Sản Phẩm"])

        new_id = 1
        while True:
            new_id_str = f"SP{new_id:03}"
            if new_id_str not in existing_ids:
                return new_id_str
            new_id += 1
    def ThemSanPham():
        ls.delete(0, END)
        Ma_sp = SinhMaSP()
        stringMasp.set(Ma_sp)
        ten_sp = stringTensp.get()
        so_luong = stringSoluong.get()
        Gia_ban = stringGiaban.get()

        if not Ma_sp or not ten_sp or not Gia_ban or not so_luong:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            so_luong = int(so_luong)
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là một số nguyên.")
            return

        sanpham_tontai = False
        rows = []

        with open(datakho, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Tên Sản Phẩm"] == ten_sp:
                    row["Số Lượng"] = str(int(row["Số Lượng"]) + so_luong)
                    sanpham_tontai = True
                rows.append(row)

        if not sanpham_tontai:
            rows.append({"Mã Sản Phẩm": Ma_sp, "Tên Sản Phẩm": ten_sp, "Giá": Gia_ban, "Số Lượng": str(so_luong)})

        with open(datakho, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

        messagebox.showinfo("Thông Báo", f"Sản phẩm '{ten_sp}' đã được thêm.")
        HienThi()
    def Xoa():
        index = ls.curselection()
        if not index or index[0] == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa!")
            return
        text = ls.get(index)
        tx = text.split(" - ")
        ma_de_xoa = tx[0]
        change = []
        with open(datakho, 'r', encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Mã Sản Phẩm"] != ma_de_xoa:
                    change.append(row)
        with open(datakho, 'w', newline='', encoding="utf8") as f:
            wr = csv.DictWriter(f, fieldnames=columns)
            wr.writeheader()
            wr.writerows(change)
        HienThi()
        messagebox.showinfo("Thông Báo", f"Sản phẩm có Mã {ma_de_xoa} đã được xoá.")
    def HienThi():
        ls.delete(0, END)
        header = " - ".join(columns)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))
        with open("Datakho.csv", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = f"{row['Mã Sản Phẩm']} - {row['Tên Sản Phẩm']} - {row['Giá']} - {row['Số Lượng']}"
                ls.insert(END, item)
    def TimKiem():
        ls.delete(0, END)
        tukhoa = simpledialog.askstring("Thông Báo", "Vui lòng sản phẩm cần tìm của bạn:")
        if tukhoa:
            tukhoa = tukhoa.lower()
        else:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if not tukhoa:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        with open(datakho, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if tukhoa in row["Mã Sản Phẩm"].lower() or tukhoa in row["Tên Sản Phẩm"].lower():
                    item = f"{row['Mã Sản Phẩm']} - {row['Tên Sản Phẩm']} - {row['Giá']} - {row['Số Lượng']}"
                    ls.insert(END, item)
                    found = True
            if not found:
                ls.insert(END, "Không tìm thấy sản phẩm phù hợp.")
    def SapXep():
        with open(datakho, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            sx = sorted(reader, key=lambda x: x["Mã Sản Phẩm"])
        ls.delete(0, END)
        header = " - ".join(columns)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))

        for row in sx:
            item = f"{row['Mã Sản Phẩm']} - {row['Tên Sản Phẩm']} - {row['Giá']} - {row['Số Lượng']}"
            ls.insert(END, item)
    def SuaSanPham():
        index = ls.curselection()
        if not index or index[0] == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để sửa!")
            return
        text = ls.get(index)
        tx = text.split(" - ")
        ma_sp = tx[0]

        with open(datakho, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            rows = []
            found = False
            for row in reader:
                if row["Mã Sản Phẩm"] == ma_sp:
                    stringMasp.set(row["Mã Sản Phẩm"])
                    stringTensp.set(row["Tên Sản Phẩm"])
                    stringGiaban.set(row["Giá"])
                    stringSoluong.set(row["Số Lượng"])
                    found = True
                rows.append(row)

            if not found:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm để sửa.")
                return

        def LuuSanPham():
            new_ma_sp = stringMasp.get()
            new_ten_sp = stringTensp.get()
            new_gia_ban = stringGiaban.get()
            try:
                new_so_luong = int(stringSoluong.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên.")
                return
            for row in rows:
                if row["Mã Sản Phẩm"] == ma_sp:
                    row["Mã Sản Phẩm"] = new_ma_sp
                    row["Tên Sản Phẩm"] = new_ten_sp
                    row["Giá"] = new_gia_ban
                    row["Số Lượng"] = str(new_so_luong)
            with open(datakho, 'w', newline='', encoding='utf8') as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Thông Báo", f"Sản phẩm '{new_ten_sp}' đã được sửa.")
            HienThi()
            btnLuu.destroy()
        btnLuu = tk.Button(frButtons, text="Lưu", justify=tk.CENTER, bg='lightgreen', command=LuuSanPham)
        btnLuu.grid(row=0, column=6, padx=5, pady=5)

    def HienThiSanPhamBanChay():
        ls.delete(0, END)
        rows = {}

        with open("DataHoaDon.csv", "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tensanpham = row["Tên sản phẩm"]
                soluongban = int(row["Sô lượng mua"])

                if tensanpham in rows:
                    rows[tensanpham] += soluongban
                else:
                    rows[tensanpham] = soluongban

        sapxep = sorted(rows.items(), key=lambda x: x[1], reverse=True)
        top_5 = sapxep[:5]

        ls.insert(END, "5 Sản Phẩm Bán Chạy Nhất:")
        ls.insert(END, "-" * 50)
        for product in top_5:
            ls.insert(END, f"{product[0]} - Số lượng bán: {product[1]}")
        ls.insert(END, "-" * 50)
    stringMasp = StringVar()
    stringTensp = StringVar()
    stringGiaban = StringVar()
    stringSoluong = StringVar()

    heading = tk.Frame(GDienChinh, bg='#e6f0fa', bd=3, relief="ridge")
    heading.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.05)

    KetQua = tk.Frame(GDienChinh, bd=3, relief="ridge")
    KetQua.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.4)

    frInput = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frInput.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.2)

    frButtons = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frButtons.place(relx=0.05, rely=0.9, relwidth=0.9, relheight=0.08)

    lbtt = tk.Label(heading, text="Thông Tin Kho",justify=tk.CENTER,font=("Arial", 18, "bold"), bg='#e6f0fa', fg='#004080')
    lbtt.place(relx=0.5,rely=0.5,anchor="center")
    ls=tk.Listbox(KetQua,width=80)
    ls.place(relwidth=1, relheight=1)
    HienThiSanPhamBanChay()

    lbTenSanpham = tk.Label(frInput, text="Tên sản phẩm: ", fg='black', justify=tk.CENTER)
    lbTenSanpham.grid(row=0,column=0,padx=5,pady=5)
    tk.Entry(frInput, width=30,textvariable=stringTensp).grid(row=0,column=1,padx=5,pady=5)

    lbSoluong = tk.Label(frInput, text="Số lượng: ", fg='black', justify=tk.CENTER)
    lbSoluong.grid(row=1,column=0,padx=5,pady=5)
    tk.Entry(frInput, width=30,textvariable=stringSoluong).grid(row=1,column=1,padx=5,pady=5)

    lbGiaBan = tk.Label(frInput, text="Giá bán: ", fg='black', justify=tk.CENTER)
    lbGiaBan.grid(row=0,column=2,padx=5,pady=5)
    tk.Entry(frInput, width=30,textvariable=stringGiaban).grid(row=0,column=3,padx=5,pady=5)

    btnAdd=tk.Button(frButtons,text="Thêm",justify=tk.CENTER,bg='lightblue',command=ThemSanPham)
    btnAdd.grid(row=0,column=0,padx=5,pady=5)
    btnXoa = tk.Button(frButtons, text="Xoá", justify=tk.CENTER, bg='lightblue', command=Xoa)
    btnXoa.grid(row=0,column=1,padx=5,pady=5)
    btnHienThi = tk.Button(frButtons, text="Hien Thi", justify=tk.CENTER, bg='lightblue', command=HienThi)
    btnHienThi.grid(row=0,column=2,padx=5,pady=5)
    btnTimKiem = tk.Button(frButtons,text="Tìm kiếm",justify=tk.CENTER,bg='lightblue',command=TimKiem)
    btnTimKiem.grid(row=0, column=3, padx=5, pady=5)
    btnSapXep=tk.Button(frButtons,text="Sắp xếp",justify=tk.CENTER,bg="lightblue",command=SapXep)
    btnSapXep.grid(row=0,column=4,padx=5,pady=5)
    btnSua = tk.Button(frButtons, text="Sửa", justify=tk.CENTER, bg='lightblue', command=SuaSanPham)
    btnSua.grid(row=0, column=5, padx=5, pady=5)
def GiaoDien_NhanVien():
    hide_all_frames()
    dataNhanVien = "DataNhanVien.csv"
    columns = ["Mã Nhân Viên", "Tên Nhân Viên", "Số Điện Thoại", "Địa Chỉ","Số Lượng Bán","Lương"]

    if not os.path.exists(dataNhanVien):
        with open(dataNhanVien, mode='w', newline='', encoding='utf-8') as f:
            wr = csv.writer(f)
            wr.writerow(columns)
    LuongCb = 3000000.0

    def TinhLuongNv():
        rows = []
        with open(dataNhanVien, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            fieldnames.append('Lương')
            for row in reader:
                luongnv = 0
                slBan = int(row["Số Lượng Bán"])
                if slBan==0:
                    luongnv=LuongCb
                elif 0< slBan < 5:
                    luongnv = (LuongCb * 1) + (LuongCb * 0.2)
                else:
                    luongnv = (LuongCb * 1) + (LuongCb * 0.5)
                row["Lương"] = str(luongnv)
                rows.append(row)
        with open(dataNhanVien, "w", encoding="utf8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        HienThi()
    def SinhMaNV():
        existing_ids = set()
        with open(dataNhanVien, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(row["Mã Nhân Viên"])

        new_id = 1
        while True:
            new_id_str = f"NV{new_id:03}"
            if new_id_str not in existing_ids:
                return new_id_str
            new_id += 1
    def ThemNhanVien():
        ls.delete(0, END)
        Ma_nv = SinhMaNV()
        stringMaNV.set(Ma_nv)
        ten_nv = stringTenNV.get()
        sdt = stringSDT.get()
        diachi = stringDiaChi.get()
        soluongban=0
        Luong = 0
        if not Ma_nv or not ten_nv or not sdt or not diachi:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        with open(dataNhanVien, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([Ma_nv, ten_nv, sdt,diachi,soluongban,Luong])
        messagebox.showinfo("Thông Báo", f"Sản phẩm '{ten_nv}' đã được thêm.")
        HienThi()
    def Xoa():
        index = ls.curselection()
        if not index or index[0] == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm để xóa!")
            return
        text = ls.get(index)
        tx = text.split(" - ")
        ma_de_xoa = tx[0]
        change = []
        with open(dataNhanVien, 'r', encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Mã Nhân Viên"] != ma_de_xoa:
                    change.append(row)
        with open(dataNhanVien, 'w', newline='', encoding="utf8") as f:
            wr = csv.DictWriter(f, fieldnames=columns)
            wr.writeheader()
            wr.writerows(change)
        HienThi()
        messagebox.showinfo("Thông Báo", f"Sản phẩm có Mã {ma_de_xoa} đã được xoá.")
    def HienThi():
        ls.delete(0, END)
        header = " - ".join(columns)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))
        with open(dataNhanVien, "r", encoding="utf8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = f"{row['Mã Nhân Viên']} - {row['Tên Nhân Viên']} - {row['Số Điện Thoại']} - {row['Địa Chỉ']} - {row['Số Lượng Bán']} - {row['Lương']}"
                ls.insert(END, item)
    def TimKiem():
        ls.delete(0, END)
        tukhoa = simpledialog.askstring("Thông Báo", "Vui lòng nhập nhân viên cần tìm của bạn:")
        if tukhoa:
            tukhoa = tukhoa.lower()
        else:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if not tukhoa:
            messagebox.showinfo("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        with open(dataNhanVien, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if tukhoa in row["Mã Nhân Viên"].lower() or tukhoa in row["Tên Nhân Viên"].lower():
                    item = f"{row['Mã Nhân Viên']} - {row['Tên Nhân Viên']} - {row['Số Điện Thoại']} - {row['Địa Chỉ']} - {row['Số Lượng Bán']} - {row['Lương']}"
                    ls.insert(END, item)
                    found = True
            if not found:
                ls.insert(END, "Không tìm thấy sản phẩm phù hợp.")
    def SapXep():
        with open(dataNhanVien, 'r', encoding='utf8') as f:
            reader = csv.DictReader(f)
            sx = sorted(reader, key=lambda x: x["Tên Nhân Viên"])
        ls.delete(0, END)
        header = " - ".join(columns)
        ls.insert(END, header)
        ls.insert(END, "-" * len(header))
        for row in sx:
            item = f"{row['Mã Nhân Viên']} - {row['Tên Nhân Viên']} - {row['Số Điện Thoại']} - {row['Địa Chỉ']} - {row['Số Lượng Bán']} - {row['Lương']}"
            ls.insert(END, item)
    def SuaNhanVien():
        index = ls.curselection()
        if not index or index[0] == 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn nhân viên để sửa!")
            return
        text = ls.get(index)
        tx = text.split(" - ")
        ma_nv = tx[0]

        with open(dataNhanVien, 'r', encoding='utf8') as file:
            reader = csv.DictReader(file)
            rows = []
            found = False
            for row in reader:
                if row["Mã Nhân Viên"] == ma_nv:
                    stringMaNV.set(row["Mã Nhân Viên"])
                    stringTenNV.set(row["Tên Nhân Viên"])
                    stringSDT.set(row["Số Điện Thoại"])
                    stringDiaChi.set(row["Địa Chỉ"])
                    found = True
                rows.append(row)

            if not found:
                messagebox.showerror("Lỗi", "Không tìm thấy nhân viên để sửa.")
                return
        def LuuSanPham():
            new_ma_nv = stringMaNV.get()
            new_ten_nv = stringTenNV.get()
            new_SDT = stringSDT.get()
            new_luong=TinhLuongNv()
            for row in rows:
                if row["Mã Nhân Viên"] == ma_nv:
                    row["Mã Nhân Viên"] = new_ma_nv
                    row["Tên Nhân Viên"] = new_ten_nv
                    row["Số Điện Thoại"] = new_SDT
                    row["Lương"]=new_luong
            with open(dataNhanVien, 'w', newline='', encoding='utf8') as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Thông Báo", f"Nhân viên '{new_ten_nv}' đã được sửa.")
            HienThi()

        btnLuu = tk.Button(frButtons, text="Lưu", justify=tk.CENTER, bg='lightgreen', command=LuuSanPham)
        btnLuu.grid(row=0, column=7, padx=5, pady=5)

    stringMaNV = StringVar()
    stringTenNV = StringVar()
    stringSDT = StringVar()
    stringDiaChi = StringVar()

    heading = tk.Frame(GDienChinh, bg='#e6f0fa', bd=3, relief="ridge")
    heading.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.05)

    KetQua = tk.Frame(GDienChinh, bd=3, relief="ridge")
    KetQua.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.4)

    frInput = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frInput.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.2)

    frButtons = tk.Frame(GDienChinh, bd=3, relief="ridge")
    frButtons.place(relx=0.05, rely=0.9, relwidth=0.9, relheight=0.08)

    lbtt = tk.Label(heading, text="Thông Tin Nhân Viên", justify=tk.CENTER,font=("Arial", 18, "bold"), bg='#e6f0fa', fg='#004080')
    lbtt.place(relx=0.5, rely=0.5, anchor="center")
    ls = tk.Listbox(KetQua, width=80)
    ls.place(relwidth=1, relheight=1)
    HienThi()

    lbTenNV = tk.Label(frInput, text="Tên Nhân Viên: ", fg='black', justify=tk.CENTER)
    lbTenNV.grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringTenNV).grid(row=0, column=1, padx=5, pady=5)

    lbSoDienThoai = tk.Label(frInput, text="Số điện thoại: ", fg='black', justify=tk.CENTER)
    lbSoDienThoai.grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringSDT).grid(row=1, column=1, padx=5, pady=5)

    lbDiaChi = tk.Label(frInput, text="Địa chỉ: ", fg='black', justify=tk.CENTER)
    lbDiaChi.grid(row=0, column=2, padx=5, pady=5)
    tk.Entry(frInput, width=30, textvariable=stringDiaChi).grid(row=0, column=3, padx=5, pady=5)

    btnAdd = tk.Button(frButtons, text="Thêm", justify=tk.CENTER, bg='lightblue', command=ThemNhanVien)
    btnAdd.grid(row=0, column=0, padx=5, pady=5)
    btnXoa = tk.Button(frButtons, text="Xoá", justify=tk.CENTER, bg='lightblue', command=Xoa)
    btnXoa.grid(row=0, column=1, padx=5, pady=5)
    btnHienThi = tk.Button(frButtons, text="Hien Thi", justify=tk.CENTER, bg='lightblue', command=HienThi)
    btnHienThi.grid(row=0, column=2, padx=5, pady=5)
    btnTimKiem = tk.Button(frButtons, text="Tìm kiếm", justify=tk.CENTER, bg='lightblue', command=TimKiem)
    btnTimKiem.grid(row=0, column=3, padx=5, pady=5)
    btnSapXep = tk.Button(frButtons, text="Sắp xếp", justify=tk.CENTER, bg="lightblue", command=SapXep)
    btnSapXep.grid(row=0, column=4, padx=5, pady=5)
    btnSua = tk.Button(frButtons, text="Sửa", justify=tk.CENTER, bg='lightblue', command=SuaNhanVien)
    btnSua.grid(row=0, column=5, padx=5, pady=5)
    btnTinhLuong = tk.Button(frButtons, text="Tính Lương", justify=tk.CENTER, bg='lightblue', command=TinhLuongNv)
    btnTinhLuong.grid(row=0, column=6, padx=5, pady=5)

GDienChinh = tk.Tk()
GDienChinh.title("Quản lý cửa hàng di động")
GDienChinh.geometry('800x650')
GDienChinh.config(bg='lightblue')
bg_image = Image.open("AnhNen.png")
bg = ImageTk.PhotoImage(bg_image)
canvas1 = Canvas(GDienChinh, width=800, height=700)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=bg, anchor="nw")
canvas1.image = bg

frChaoMung = tk.Frame(GDienChinh, width=700, height=100, bg='#e6f0fa', bd=3, relief="ridge")
frChaoMung.place(relx=0.5, rely=0.3, anchor="center")

lbWelcome = tk.Label(frChaoMung, text="Chào mừng đến với chương trình quản lí cửa hàng",font=("Arial", 18, "bold"), bg='#e6f0fa', fg='#004080')
lbWelcome.pack(expand=True, fill="both")

btnKho = tk.Button(GDienChinh, text="Sản Phẩm", bg='#66a3ff', fg='white', activebackground='#0059b3',font=("Arial", 10, "bold"), width=10, height=3, command=GiaoDien_Kho)
btnKho.place(x=100,y=0)

btnKhHang = tk.Button(GDienChinh, text="Hoá Đơn", bg='#66a3ff', fg='white', activebackground='#0059b3',font=("Arial", 10, "bold"), width=10, height=3, command=GiaoDien_HD)
btnKhHang.place(x=200,y=0)

btnNhanVien = tk.Button(GDienChinh, text="Nhân Viên", bg='#66a3ff', fg='white', activebackground='#0059b3',font=("Arial",10, "bold"), width=10, height=3, command=GiaoDien_NhanVien)
btnNhanVien.place(x=0, y=0)

def center_window(root):
    GDienChinh.update_idletasks()
    width = GDienChinh.winfo_width()
    height = GDienChinh.winfo_height()
    x = (GDienChinh.winfo_screenwidth() // 2) - (width // 2)
    y = (GDienChinh.winfo_screenheight() // 2) - (height // 2)
    GDienChinh.geometry(f'{width}x{height}+{x}+{y}')

center_window(GDienChinh)
GDienChinh.mainloop()