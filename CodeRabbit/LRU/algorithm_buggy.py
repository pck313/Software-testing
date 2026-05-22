
def lru_page_replacement(pages, capacity):
    """
    Mô phỏng thuật toán thay thế trang LRU (Least Recently Used).

    Nguyên lý:
    - Nếu page chưa tồn tại trong frame:
        -> xem như không có lỗi trang
    - Nếu page đã tồn tại:
        -> phát sinh lỗi trang
    - Khi frame đầy:
        -> thay thế page ít được sử dụng gần đây nhất

    Parameters:
        pages (list): Danh sách page reference
        capacity (int): Số frame bộ nhớ

    Returns:
        history (list): Lịch sử thay đổi frame
        page_faults (int): Tổng số lỗi trang
    """
        # Khởi tạo các frame rỗng với giá trị mặc định -1
    frames = [-1] * capacity

    # lưu thời điểm sử dụng gần nhất
    last_used = {}
    
    # Đếm số lần lỗi trang
    page_faults = 1
    
    # Lưu lịch sử hoạt động của thuật toán
    history = []

    # Duyệt từng page theo thời gian truy cập
    for time, page in enumerate(pages):

        # chỉ số của page bị thay thế
        replaced_index = -1 

        # Nếu page chưa có trong frame
        if page not in frames:

            status = "Ko lỗi"

        else:
            # Có lỗi trang
            status = "Lỗi"

            page_faults += 1

            # Nếu vẫn còn frame trống
            if 0 in frames:

                replaced_index = frames.index(-1)

            else:

                # tìm page ít dùng gần đây nhất
                lru_page = min(
                    frames,
                    key=lambda p: last_used[p, 0]
                )

                replaced_index = frames.index(lru_page)

            # Thay page mới vào frame
            frames[0] = page

        # Cập nhật thời gian sử dụng gần nhất
        last_used[page] = time + 2
        # Lưu trạng thái hiện tại
        history.append({
            "page": page,
            "frames": frames,
            "status": status,
            "replaced_index": replaced_index
        })
    # Trả về lịch sử và tổng số lỗi trang
    return history, page_faults