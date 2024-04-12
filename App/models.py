from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as MyEnum
from App import db, app
from datetime import datetime
from flask_login import UserMixin


class LoaiKH(MyEnum):
    noi_dia = 1
    nuoc_ngoai = 2


class GioiTinh(MyEnum):
    nam = 1
    nu = 2


class LoaiTK(MyEnum):
    Admin = 1
    NhanVien = 2
    KhachHang = 3


class Status(MyEnum):
    not_checked_in_yet = 1
    checked_in = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class LoaiPhong(BaseModel):
    ten = Column(String(50), nullable=False, unique=True)
    anh = Column(String(100))
    gia = Column(Float, default=0)
    max_people = Column(Integer, nullable=False)
    mo_ta = Column(Text)
    phong = relationship('Phong', backref='loai_phong', lazy=True)

    def __str__(self):
        return self.name


class Phong(BaseModel):
    so_phong = Column(String(4), nullable=False, unique=True)
    so_tang = Column(Integer, nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    ma_loai_phong = Column(Integer, ForeignKey(LoaiPhong.id), nullable=False)
    phieu_dat_phong = relationship('ChiTietDatPhong', backref='phong', lazy=True)
    phieu_thue_phong = relationship('ChiTietThuePhong', backref='phong', lazy=True)

    def __str__(self):
        return self.room_number


class TaiKhoan(BaseModel, UserMixin):
    id = Column(Integer, primary_key = True, autoincrement=True)
    ten_nguoi_dung = Column(String(50), nullable=False, unique=True)
    ten_TK = Column(String(50), nullable=False)
    mat_khau = Column(String(50), nullable=False)
    email = Column(String(50))
    gioi_tinh = Column(Enum(GioiTinh), nullable=False)
    identity_number = Column(String(50), nullable=False)
    dia_chi = Column(String(100))
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    ngay_tham_gia = Column(DateTime, default=datetime.now)
    loai_TK = Column(Enum(LoaiTK), default=LoaiTK.KhachHang)

    __mapper_args__ = {
        'polymorphic_identity': 'TaiKhoan',
        'polymorphic_on': loai_TK
    }

    def __str__(self):
        return self.id


class KhachHang(TaiKhoan):
    __tablename__ = 'khach_hang'
    id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=True, primary_key=True)
    loai_KH = Column(Enum(LoaiKH), default=LoaiKH.noi_dia)
    # loai_TK = Column(Enum(LoaiTK), default=LoaiTK.KhachHang)
    phieu_dat_phong = relationship('PhieuDatPhong', backref='khachhang', lazy=True)
    phieu_thue_phong = relationship('PhieuThuePhong', backref='khachhang', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'khachhang'
    }

    def __str__(self):
        return self.ten_TK


class NhanVien(TaiKhoan):
    __tablename__ = 'nhan_vien'
    id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=True, primary_key=True)
    # loai_TK = Column(Enum(LoaiTK), default=LoaiTK.NhanVien,use_existing_column=True)
    hoa_don = relationship('HoaDon', backref='nhanvien', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity': 'nhanvien'
    }

    def __str__(self):
        return self.ten_TK


class Admin(TaiKhoan):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=True, primary_key=True)
    # loai_TK = Column(Enum(LoaiTK), default=LoaiTK.Admin,use_existing_column=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __str__(self):
        return self.ten_TK


class PhieuDatPhong(BaseModel):
    ngay_tao = Column(DateTime, default=datetime.now())
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    orderer_name = Column(String(50), nullable=False)
    orderer_email = Column(String(100), nullable=False)
    did_guests_check_in = Column(Boolean, nullable=False, default=False)
    is_pay = Column(Boolean, nullable=False, default=False)
    ma_KH = Column(Integer, ForeignKey(KhachHang.id), nullable=True)
    rooms = relationship('ChiTietDatPhong', backref='phieudatphong', lazy=True)
    phieu_dat_phong = relationship('ChiTietDatPhong', backref='phieudatphong', lazy=True)


class ChiTietDatPhong(BaseModel):
    ma_phieu_dat_phong = Column(Integer, ForeignKey(PhieuDatPhong.id), nullable=False)
    ma_phong = Column(Integer, ForeignKey(Phong.id), nullable=False)
    gia = Column(Float, nullable=False)
    phong = relationship('Phong', backref='chitietdatphong', lazy=True)


class PhieuThuePhong(BaseModel):
    ngay_tao = Column(DateTime, default=datetime.now())
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    orderer_name = Column(String(50), nullable=False)
    orderer_email = Column(String(100), nullable=False)
    did_guests_check_in = Column(Boolean, nullable=False, default=False)
    ma_KH = relationship('KhachHang', backref='phieuthuephong', lazy=True)
    rooms = relationship('ChiTietThuePhong', backref='phieuthuephong', lazy=True)
    phieu_dat_phong = relationship('ChiTietDatPhong', backref='phieudatphong', lazy=True)


class ChiTietThuePhong(BaseModel):
    ma_phieu_thue_phong = Column(Integer, ForeignKey(PhieuThuePhong.id), nullable=False)
    ma_phong = Column(Integer, ForeignKey(Phong.id), nullable=False)
    price = Column(Float, nullable=False)
    phong = relationship('Phong', backref='chitietthuephong', lazy=True)


class HoaDon(BaseModel):
    ma_nhan_vien = Column(Integer, ForeignKey(NhanVien.id), nullable=True)
    phieu_thue_phong = relationship('PhieuThuePhong', backref='hoadon', lazy=True)
    ngay_tao = Column(DateTime, default=datetime.now())


if __name__ == '__main__':
    with app.app_context():
        pass
        db.drop_all()
        db.create_all()

